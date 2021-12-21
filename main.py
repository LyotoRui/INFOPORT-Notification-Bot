import base64
import re
import secrets
import sqlite3
from sqlite3.dbapi2 import connect
import sys
import time as t

import requests
import telebot
from bs4 import BeautifulSoup
from requests.sessions import session
from telebot import types


sys.dont_write_bytecode = True

users = sqlite3.connect('users.db', check_same_thread=False)
curs = users.cursor()

notified_orders = {}

class RZTKChecker():
    def __init__(self) -> None:
        self.login = secrets.RZTK_LOGIN
        self.password = secrets.RZTK_PASSWORD

    def password_encode(self):
        password_encode = str(self.password).encode('UTF-8')
        password = base64.b64encode(password_encode)
        self.password_encoded = password.decode('UTF-8')

    def login_to(self):
        self.password_encode()
        account = {
            'username': self.login,
            'password': self.password_encoded
        }
        login = requests.post(
            'https://api-seller.rozetka.com.ua/sites',
            data=account
        ).json()
        self.token = login['content'].get('access_token')
    
    def new_orders(self):
        try:
            key = {'Authorization': f'Bearer {self.token}'}
            orders = requests.get('https://api-seller.rozetka.com.ua/orders/search?status=1', headers=key).json()
            for order in orders['content']['orders']:
                if order['id'] not in notified_orders.keys():
                    order_id = order['id']
                    products = {}
                    order_info = {
                        'customets_name': order['user_title']['first_name'],
                        'customers_phone': order['user_phone'],
                        'total_cost': order['cost']
                    }
                    for item in order['items_photos']:
                        products.update({
                            item['item_name']: {'count': 1,
                            'price': item['item_price']}
                        })
                    order_info.update({'products': products})
                    if order_id not in notified_orders.keys():
                        notify([
                            'ROZETKA',
                            '=============',
                            f'Поступил заказ #{order_id}',
                            '=============',
                            'Покупатель: {}'.format(order_info['customets_name']),
                            'Телефон: {}'.format(order_info['customers_phone']),
                            '=============',
                            f'\n---------------------------\n'.join(products.keys()),
                            '=============',
                            'Итоговая сумма: {} грн'.format(order_info['total_cost'])
                            ])
                        notified_orders.update({order['id']: order_info})
        except AttributeError:
            self.login_to()
            self.new_orders()


class WebSiteChecker():
    def __init__(self) -> None:
        self.header = secrets.HEADER
        self.login = secrets.WEB_LOGIN
        self.password = secrets.WEB_PASSWORD
        self.session = requests.Session()

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
        try:
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
                        if clear_order[1] not in notified_orders.keys():
                            notify([
                                'INFOPORT',
                                '=============',
                                f'Поступил заказ #{clear_order[1]}',
                                '=============',
                                'Покупатель: {}'.format(order_info['customers_name']),
                                'Телефон: {}'.format(order_info['customers_phone']),
                                '=============',
                                f'\n---------------------------\n'.join(products.keys()),
                                '=============',
                                'Итоговая сумма: {} грн'.format(order_info['total_cost'])
                            ])
                            notified_orders.update({clear_order[1]: order_info})
        except AttributeError:
            self.login_to()
            self.new_orders()

    def except_html(self, order: list) -> list:
        pattern = r'<[^>]*>'
        clear_list = [re.sub(pattern, '', str(item)) for item in order]
        clear_list[5] = ''
        return clear_list


bot = telebot.TeleBot(token=secrets.BOT_TOKEN, parse_mode=None)

@bot.message_handler(commands=['login'])
def login(message):
    print(message.chat.id)

@bot.message_handler(content_types=["text"])
def notify(notif: list):
    notif = '\n'.join(notif)
    for user in secrets.USER_IDS:
        bot.send_message(user, text=notif)

def work():
    rozetka = RZTKChecker()
    web = WebSiteChecker()
    web.new_orders()
    rozetka.new_orders()

if __name__ == '__main__':
    while True:
        work()
        t.sleep(15)
