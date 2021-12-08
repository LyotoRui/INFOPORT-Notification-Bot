from bs4 import BeautifulSoup
import logging
import secrets
import base64
import sqlite3
import requests
import time as t


class RZTKChecker():
    def __init__(self) -> None:
        self.login = secrets.RZTK_LOGIN
        self.password = secrets.RZTK_PASSWORD
        

    def password_encode(self):
        password_encode = str(self.password).encode('UTF-8')
        password = base64.b64encode(password_encode)
        self.password_encoded = password.decode('UTF-8')
        

    def login_to(self):
        account = {'username': self.login, 'password': self.password_encoded}
        login = requests.post('https://api-seller.rozetka.com.ua/sites', data=account).json()
        if not login['success']:
            print(login['errors']['description'])
        else:
            print('LOGIN')


class WebSiteChecker():
    def __init__(self) -> None:
        self.header = secrets.HEADER
        self.login = secrets.WEB_LOGIN
        self.password = secrets.WEB_PASSWORD


class Bot():
    def __init__(self) -> None:
        self.token = secrets.BOT_TOKEN


def work():
    pass

if __name__ == '__main__':
    work()
    test = RZTKChecker()
    test.password_encode()
    test.login_to()
