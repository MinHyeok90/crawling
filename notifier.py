#!/usr/bin/env python
# encoding=utf-8

import telegram

f = open('mykey', 'r')
key = f.readline()
chat_room = f.readline()

bot = telegram.Bot(token=key)


# 생성한 텔레그램 봇 /start 시작 후 사용자 id 받아 오기
# chat_id = bot.getUpdates()[-1].message.chat.id
# print('user id :', chat_id)
# 사용자 id로 메시지 보내기
# bot.sendMessage(chat_id, u'bot이 보낸 메시지')

def converter(data):
    # TODO: dic to readable string list
    readable = "string"
    return readable


bot.sendMessage(chat_room, u'message')
