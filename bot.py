import telebot

from misc_funcs import loadDataFromSettings

try:
    notify_ids = loadDataFromSettings()["Users"]
except TypeError:
    loadDataFromSettings()
    notify_ids = loadDataFromSettings()["Users"]

try:
    bot = telebot.TeleBot(
        token=loadDataFromSettings()["BotToken"],
        parse_mode=None
        )
except TypeError:
    loadDataFromSettings()
    bot = telebot.TeleBot(
        token=loadDataFromSettings()["BotToken"],
        parse_mode=None
        )


@bot.message_handler(commands=["login"])
def login(message) -> None:
    bot.send_message(message.chat.id, str(message.chat.id))


@bot.message_handler(content_types=["text"])
def notify(order_text: str) -> None:
    for user in notify_ids.keys():
        bot.send_message(notify_ids[user], text=order_text)
