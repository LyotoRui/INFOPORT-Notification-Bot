import telebot
from misc.functions import Functions

bot = telebot.TeleBot(token=Functions().data['BotToken'])
users = Functions().data['Users']

@bot.message_handler(commands=["login"])
def login(message) -> None:
    bot.send_message(message.chat.id, str(message.chat.id))


@bot.message_handler(content_types=["text"])
def notify(order_text: str) -> None:
    for user in users.keys():
        bot.send_message(users[user], text=order_text)
