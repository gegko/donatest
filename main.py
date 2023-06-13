# https://core.telegram.org
# http://t.me/khach_donatest_bot

import telebot
from telebot.types import Message
from envparse import Env
from telebot.types import Message
import json

env = Env()
TOKEN = env.str('TOKEN')
bot_link = env.str('bot_link')
bot_search_name = env.str('bot_search_name')

bot_client = telebot.TeleBot(token=TOKEN)


@bot_client.message_handler(commands=['start', 'donate'])
def echo(message: Message):
    with open('users.json', 'r') as f_o:
        data_from_json = json.load(f_o)

    user_id = message.from_user.id
    username = message.from_user.username

    if str(user_id) not in data_from_json:
        data_from_json[user_id] = {'username': username}
    with open('users.json', 'w') as f_o:
        json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
    bot_client.reply_to(message=message, text=str(f'Приветсвую {user_name}! Ваш userid: {user_id}'))


bot_client.polling()