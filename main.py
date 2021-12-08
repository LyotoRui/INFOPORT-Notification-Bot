import base64
import logging
import re
import secrets
import sqlite3
import sys
import time as t

import requests
from bs4 import BeautifulSoup
from requests.sessions import session

sys.dont_write_bytecode = True


class RZTKChecker():
    def __init__(self) -> None:
        self.login = secrets.RZTK_LOGIN
        self.password = secrets.RZTK_PASSWORD

    def password_encode(self):
        password_encode = str(self.password).encode('UTF-8')
        password = base64.b64encode(password_encode)
        self.password_encoded = password.decode('UTF-8')

    def login_to(self):
        account = {
            'username': self.login,
            'password': self.password_encoded
        }
        login = requests.post(
            'https://api-seller.rozetka.com.ua/sites',
            data=account
        ).json()
        self.token = login['content'].get('access_token')


class WebSiteChecker():
    def __init__(self) -> None:
        self.header = secrets.HEADER
        self.login = secrets.WEB_LOGIN
        self.password = secrets.WEB_PASSWORD
        self.session = requests.Session()
        self.notified_orders = {}
    
    def login_to(self):
        _data = {
            'act': 'users',
            'opt': 'CpLogin',
            'path': '/cp/',
            'login': self.login,
            'password': self.password
            }
        self.session.post(
            'https://infoport.pro/cp/',
            headers=self.header,
            data=_data
            )

    def new_orders(self):
        data = self.session.get(
            'https://infoport.pro/cp/orders/',
            headers=self.header
            ).text
        soup = BeautifulSoup(data, 'lxml')
        order_list = soup.find(class_="ordert").find_all('tr')
        for order in order_list:
            if len(order) > 3:
                order = order.find_all('td')
                clear_order = self.except_html(order)
                if len(clear_order[-1]) == 0:
                    products = {}
                    mid_prod = []
                    for item in clear_order[6:-3]:
                        mid_prod.append(item)
                        if len(mid_prod) == 3:
                            products.update(
                                {mid_prod[0]: {'count': mid_prod[1],
                                'price':mid_prod[2]}}
                                )
                            mid_prod = []
                    order_info = {
                        'customers_name': clear_order[4],
                        'customers_phone': clear_order[-3],
                        'total_cost': clear_order[-2]
                    }
                    order_info.update({'products': products})
                    self.notified_orders.update({clear_order[1]: order_info})

    def except_html(self, order: list) -> list[str]:
        pattern = r'<[^>]*>'
        clear_list = [re.sub(pattern, '', str(item)) for item in order]
        clear_list[5] = ''
        return clear_list
            


class Bot():
    def __init__(self) -> None:
        self.token = secrets.BOT_TOKEN


def work():
    pass

if __name__ == '__main__':
    test = WebSiteChecker()
    test.login_to()
    test.new_orders()
    print(test.notified_orders)
