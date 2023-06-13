import telebot
from envparse import Env

env = Env()
TOKEN = env.str('TOKEN')
bot_link = env.str('bot_link')
bot_search_name = env.str('bot_search_name')

print(TOKEN)
