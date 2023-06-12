import logging
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# Включение логирования для получения информации об ошибках
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Определение состояний (states) для выбора валюты
STATE_DEFAULT = 0
STATE_RUB = 1
STATE_USD = 2

# Обработка команды /start
def start(update, context):
    # Создание клавиатуры для выбора валюты
    keyboard = [[KeyboardButton('RUB'), KeyboardButton('USD')]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    # Отправка сообщения с приветствием и клавиатурой
    update.message.reply_text('Привет! Какую валюту хочешь использовать?', reply_markup=reply_markup)

# Обработка команды /donate
def donate(update, context):
    # Создание клавиатуры с кнопками сумм донатов
    currency = context.user_data.get('currency', 'RUB')
    if currency == 'USD':
        amounts = [10, 20, 50, 100]
    else:
        amounts = [500, 1000, 2000, 5000]
    
    buttons = [InlineKeyboardButton(str(amount), callback_data=str(amount)) for amount in amounts]
    keyboard = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Отправка сообщения с меню донатов
    update.message.reply_text('Выбери сумму доната:', reply_markup=reply_markup)

# Обработка выбора суммы доната
def donate_amount(update, context):
    # Получение выбранной суммы из обратного вызова
    amount = int(update.callback_query.data)
    
    # Отправка благодарности в зависимости от выбранной суммы
    if amount < 500:
        update.callback_query.answer('Спасибо!')
    else:
        update.callback_query.answer('Суперспасибо!')
    
    # Закрытие меню донатов
    update.callback_query.message.edit_reply_markup()

# Обработка выбора валюты
def select_currency(update, context):
    # Получение выбранной валюты
    currency = update.message.text
    
    if currency == 'RUB':
        context.user_data['currency'] = 'RUB'
    elif currency == 'USD':
        context.user_data['currency'] = 'USD'
    else:
        
