# https://core.telegram.org
# http://t.me/khach_donatest_bot

import telebot
from telebot.types import Message
from envparse import Env
from telebot.types import Message
import json
import requests
from datetime import datetime

env = Env()
TOKEN = env.str('TOKEN')
ADMIN_CHAT_ID = env.int('ADMIN_CHAT_ID')
bot_link = env.str('bot_link')
bot_search_name = env.str('bot_search_name')


bot_client = telebot.TeleBot(token=TOKEN)


@bot_client.message_handler(commands=['start'])
def start(message: Message):
    with open('users.json', 'r') as f_o:
        data_from_json = json.load(f_o)

    user_id = message.from_user.id
    username = message.from_user.username

    if str(user_id) not in data_from_json:
        data_from_json[user_id] = {'username': username}
    with open('users.json', 'w') as f_o:
        json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
    bot_client.reply_to(message=message, text=f'Приветсвую {username}! Ваш userid: {user_id}')



def answer_handle(message: Message):
    bot_client.reply_to(message, text='Спасибо за инвестиции')


@bot_client.message_handler(commands=['donate'])
def donate(message: Message):
    bot_client.reply_to(message, text='Какой бюджет вы рассматриваете для своего проекта инвестиций?')
    bot_client.register_next_step_handler(message, answer_handle)


while True:
    try:
        bot_client.polling()
    except JSONDecodeError as err:
        print('Ошибка', err)
        requests.post(f'https://core.telegram.org/bot{TOKEN}'
                      f'/sendMessage?chat_id=42791670&text={datetime.now()} ::: {err.__class__} ::: {err}')