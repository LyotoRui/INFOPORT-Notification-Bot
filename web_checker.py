from itertools import product
import secrets
import requests
from bs4 import BeautifulSoup
from misc_funcs import morphDataToNotify, exceptHtml


class WebChecker:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.notified_orders = list()

    def loginTo(self):
        _data = {
            'act': 'users',
            'opt': 'CpLogin',
            'path': '/cp/',
            'login': secrets.WEB_LOGIN,
            'password': secrets.WEB_PASSWORD
        }
        self.session.post(
            'https://infoport.pro/cp/',
            headers=secrets.HEADER,
            data=_data
        )
    
    def getNewOrders(self) -> list:
        try:
            data = self.session.get(
                'https://infoport.pro/cp/orders/',
                headers=secrets.HEADER
            ).text
            soup = BeautifulSoup(data, 'lxml')
            order_list = soup.find(class_='ordert').find_all('tr')
            new_orders = []
            for order in order_list:
                if len(order) > 3:
                    order = order.find_all('td')
                    clear_order = exceptHtml(order=order)
                    if clear_order[1] not in self.notified_orders:
                        items = clear_order[4:-3:3]
                        new_orders.append(
                            morphDataToNotify(
                                source='INFOPORT',
                                order_id=clear_order[1],
                                customer_name=clear_order[3],
                                customer_phone=clear_order[-2],
                                products=items,
                                total_cost=clear_order[-1]
                            )
                        )
                        self.notified_orders.append(clear_order[1])
            return new_orders
        except AttributeError:
            self.loginTo()
            self.getNewOrders()
