import requests
from bs4 import BeautifulSoup

from misc.functions import Functions
from misc.text_templates import HEADERS


class WebChecker(Functions):
    def __init__(self) -> None:
        super().__init__()
        self.login = self.data["WebLoginData"]["login"]
        self.password = self.data["WebLoginData"]["password"]
        self.session = requests.Session()
        self.notified_orders = list()
        self.new_orders = list()

    def loginTo(self):
        data = {
            "act": "users",
            "opt": "CpLogin",
            "path": "/cp/",
            "login": self.login,
            "password": self.password,
        }
        self.session.post("https://infoport.pro/cp/", headers=HEADERS, data=data)

    def getNewOrders(self) -> list:
        try:
            data = self.session.get(
                "https://infoport.pro/cp/orders/", headers=HEADERS
            ).text
            soup = BeautifulSoup(data, "lxml")
            order_list = soup.find(class_="ordert").find_all("tr")
            self.new_orders = list()
            for order in order_list:
                if len(order) > 3:
                    order = order.find_all("td")
                    clear_order = self.exceptHtml(order=order)
                    if clear_order[1] not in self.notified_orders:
                        items = clear_order[4:-3:3]
                        self.new_orders.append(
                            self.morphDataToNotify(
                                source="INFOPORT",
                                order_id=clear_order[1],
                                customer_name=clear_order[3],
                                customer_phone=clear_order[-2],
                                products=items,
                                total_cost=clear_order[-1],
                            )
                        )
                        self.notified_orders.append(clear_order[1])
        except AttributeError:
            self.loginTo()
            self.getNewOrders()
