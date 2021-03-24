import telebot
import requests
import json
from extentions import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_handler(message):
    some_txt = 'Чтобы начать роботу введите команду в следующем формате:\n' \
               '   <Имя валюты><в какую валюту перевести><количество переводимой валюты>\n' \
               'Увидеть список всех доступных валют /values'
    bot.send_message(message.chat.id, some_txt)


@bot.message_handler(commands=['values'])
def values_hand(message):
    some_txt = 'Доступные валюты:'
    for key in keys.keys():
        some_txt += '\n' + key
    bot.send_message(message.chat.id, some_txt)


@bot.message_handler(content_types=['text'])
def text_hand(message):
    try:
        values = message.text.lower().split(' ')
        if len(values) != 3:
            raise APIException('Неверное количество параметров')
        quote, base, amount = values
        res = MoneyConverter.get_price(quote, base, amount)
    except APIException as fail:
        bot.send_message(message.chat.id, f'Ошибка пользователя:\n{fail}')
    except Exception:
        bot.send_message(message.chat.id, "Технические неполадки. Не могу ответить")
    else:
        text = f'Цена {amount} {quote} в {base} - {float(res) * float(amount)}'
        bot.send_message(message.chat.id, text)




bot.polling(none_stop=True)
