#!/usr/bin/env python
# encoding=utf-8
import telegram


def get_bot():
    f = open('my_key', 'r')
    key = f.readline()
    bot = telegram.Bot(token=key)
    return bot


def get_chat_room():
    f = open('my_chat_room', 'r')
    chat_room_number = f.readline()
    return chat_room_number


# 생성한 텔레그램 봇 /start 시작 후 사용자 id 받아 오기
# chat_id = bot.getUpdates()[-1].message.chat.id
# print('user id :', chat_id)
# 사용자 id로 메시지 보내기
# bot.sendMessage(chat_id, u'bot이 보낸 메시지')

def send(bot, chat_room, message):
    bot.sendMessage(chat_room, message)


def create_link(num):
    url_pre = u'www.encar.com/dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid='
    url_post = u'&wtClick_korList=019&advClickPosition=kor_normal_p1_g1'
    return url_pre + num + url_post


def new_car_msg(newer):
    hello = "===신규 매물! " + str(len(newer)) + "건\n"
    contents = ""
    for car in newer:
        id = car['Id']
        contents = contents + \
                   "\n번호: " + id + \
                   "\n차종: " + car['Model'] + \
                   "\n가격: " + str(car['Price']) + \
                   "\n링크: " + create_link(id) + \
                   "\n"
    return hello + contents


def leave_car_msg(leave):
    leave_contents = "===기존 매물 " + str(len(leave)) + "건\n"
    return leave_contents


def deleted_car_msg(deleted):
    deleted_contents = "===삭제 매물 " + str(len(deleted)) + "건\n"
    return deleted_contents


def converter_readability(separated_by_status):
    newer = separated_by_status['newer']
    leave = separated_by_status['leave']
    deleted = separated_by_status['deleted']

    ncm = new_car_msg(newer)
    lcm = leave_car_msg(leave)
    dcm = deleted_car_msg(deleted)

    return ncm + "\n" + lcm + "\n" + dcm


def notify(separated_by_status):
    bot = get_bot()
    chat_room = get_chat_room()
    readable_data = converter_readability(separated_by_status)
    send(bot, chat_room, readable_data)


def test():
    import test
    # print("get bot")
    # get_bot()

    # print("converter_readability test")
    data = test.get_separated_by_status_three_newer()
    x = converter_readability(data)
    # print(x)

    print("send long message test")
    notify(data)

# test()
