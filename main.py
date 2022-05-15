import secrets
import time as t

import telebot

from rztk_checker import RZTKChecker
from web_checker import WebChecker

bot = telebot.TeleBot(token=secrets.BOT_TOKEN, parse_mode=None)


@bot.message_handler(commands=['login'])
def login(message):
    print(message.chat.id)


@bot.message_handler(content_types=["text"])
def notify(notif: str):
    for user in secrets.USER_IDS:
        bot.send_message(user, text=notif)


def work():
    web.getNewOrders()
    if len(web.new_orders):
        for order in web.new_orders:
            notify(order)
    rztk.getNewOrders()
    if len(rztk.new_orders):
        for order in rztk.new_orders:
            notify(order)


if __name__ == '__main__':
    web = WebChecker()
    rztk = RZTKChecker()
    while True:
        work()
        t.sleep(15)
