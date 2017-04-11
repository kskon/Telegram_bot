# -*- python3 -*-
# -*- coding: utf-8-*-
# author: kskonovalov100@gmail.com
# date: 2017/04/08
# copyright
# time not wighting

import config
import telebot
from library_num_to_string import numbers_to_text_converter

bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=['text'])
def number_converter(message):
    sn = numbers_to_text_converter(message.text)
    bot.send_message(message.chat.id, sn)

if __name__ == '__main__':
    bot.polling(none_stop=True)
