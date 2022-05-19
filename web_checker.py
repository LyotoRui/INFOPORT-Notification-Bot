import requests
from bs4 import BeautifulSoup
from misc_funcs import morphDataToNotify, exceptHtml


class WebChecker:
    def __init__(self, login_data: dict) -> None:
        self.login = login_data["login"]
        self.password = login_data["password"]
        self.session = requests.Session()
        self.notified_orders = list()
        self.new_orders = list()
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.79'
        }

    def loginTo(self):
        _data = {
            "act": "users",
            "opt": "CpLogin",
            "path": "/cp/",
            "login": self.login,
            "password": self.password,
        }
        self.session.post(
            "https://infoport.pro/cp/",headers=self.headers, data=_data
        )

    def getNewOrders(self) -> list:
        try:
            data = self.session.get("https://infoport.pro/cp/orders/", headers=self.headers).text
            soup = BeautifulSoup(data, "lxml")
            order_list = soup.find(class_="ordert").find_all("tr")
            self.new_orders = list()
            for order in order_list:
                if len(order) > 3:
                    order = order.find_all("td")
                    clear_order = exceptHtml(order=order)
                    if clear_order[1] not in self.notified_orders:
                        items = clear_order[4:-3:3]
                        self.new_orders.append(
                            morphDataToNotify(
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
