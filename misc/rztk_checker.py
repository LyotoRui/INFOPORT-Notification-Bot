import requests

from misc.functions import Functions


class RZTKChecker(Functions):
    def __init__(self) -> None:
        super().__init__()
        self.login = self.data["RozetkaLoginData"]["login"]
        self.password = self.passwordEncode(self.data["RozetkaLoginData"]["password"])
        self.notified_orders = list()
        self.new_orders = list()

    def loginTo(self) -> None:
        account = {"username": self.login, "password": self.password}
        login = requests.post(
            "https://api-seller.rozetka.com.ua/sites", data=account
        ).json()
        self.token = login["content"].get("access_token")

    def getNewOrders(self) -> list:
        try:
            key = {"Authorization": f"Bearer {self.token}"}
            get_orders = requests.get(
                "https://api-seller.rozetka.com.ua/orders/search?status=1", headers=key
            ).json()
            self.new_orders = list()
            for order in get_orders["content"]["orders"]:
                if order["id"] not in self.notified_orders:
                    products = list()
                    for item in order["items_photos"]:
                        products.append(item["item_name"])
                self.new_orders.append(
                    self.morphDataToNotify(
                        source="ROZETKA",
                        order_id=order["id"],
                        customer_name=order["user_title"]["first_name"],
                        customer_phone=order["user_phone"],
                        products=products,
                        total_cost=order["cost"],
                    )
                )
                self.notified_orders.append(order["id"])
        except AttributeError:
            self.loginTo()
            self.getNewOrders()
