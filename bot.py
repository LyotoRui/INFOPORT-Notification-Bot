import telebot

from misc_funcs import loadDataFromSettings


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
    for user in dict(loadDataFromSettings()["Users"]).items():
        bot.send_message(user, text=order_text)
