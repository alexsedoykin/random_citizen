import telebot
from telebot import types
from RuRandomCitizen import RandomName
from random import randint
from main import api_token

token = api_token
bot = telebot.TeleBot(token, parse_mode=None)

def rnd_name(gen=randint(0, 1)):
    name = RandomName(gen)
    return f'{name.last_name}\n' \
           f'{name.first_name}\n' \
           f'{name.middle_name}\n' \
           f'{name.date}\n' \
           f'{name.address}\n' \
           f'{name.telephone}\n' \
           f'{name.email}\n' \
           f'{name.card_number}\n'


markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(types.KeyboardButton("/male"))
markup.add(types.KeyboardButton("/female"))
markup.add(types.KeyboardButton("/random"))

@bot.message_handler(commands=['male'])
def start_message(message):
    text = rnd_name(1)
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(commands=['female'])
def start_message(message):
    text = rnd_name(0)
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(commands=['random'])
def start_message(message):
    text = rnd_name()
    bot.send_message(message.chat.id, text, reply_markup=markup)

bot.infinity_polling()