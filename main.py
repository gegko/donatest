import telebot
from envparse import Env
from telebot import types

env = Env()
token = env.str('TOKEN')
chat_id = env.int('ADMIN_CHAT_ID')

CONVERSION_RATE = {'RUB': 1, 'USD': 83}  # конвертация в рубли
SUPER_THANK_YOU_THRESHOLD = 500

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет')


@bot.message_handler(commands=['donate'])
def bot_message(message):
    markup = types.InlineKeyboardMarkup()
    rub_button = types.InlineKeyboardButton('RUB', callback_data='RUB')
    usd_button = types.InlineKeyboardButton('USD', callback_data='USD')
    markup.add(rub_button, usd_button)
    bot.send_message(message.chat.id, 'Выберите нужную валюту: ', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    data = call.data

    if call.data in ['RUB', 'USD']:
        currency = call.data
        if currency == 'RUB':
            amounts = ['50', '200', '500', '1000']
        else:  # USD
            amounts = ['1', '5', '10', '20']

        markup = types.InlineKeyboardMarkup()
        for amount in amounts:
            button = types.InlineKeyboardButton(amount, callback_data=f'{amount}_{currency}')
            markup.add(button)
        close_button = types.InlineKeyboardButton('Закрыть', callback_data='close')
        markup.add(close_button)
        bot.send_message(call.message.chat.id, 'Выбери сумму для доната', reply_markup=markup)
    elif data.startswith(('50_', '200_', '500_', '1000_', '1_', '5_', '10_', '20_')):
        amount, currency = data.split('_')
        amount = int(amount)
        amount_rub = CONVERSION_RATE[currency] * amount
        if amount_rub >= SUPER_THANK_YOU_THRESHOLD:
            bot.send_message(call.message.chat.id, 'ВАУ СПАСИБО!')
        else:
            bot.send_message(call.message.chat.id, 'Спасибо')
    elif data == 'Close':
        bot.send_message(call.message.chat.id, 'До свидания')


bot.infinity_polling()
