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


def send(bot, chat_room, message):
    bot.sendMessage(chat_room, message)
    # print(message)


def create_link(num):
    url_pre = 'www.encar.com/dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid='
    url_post = '&wtClick_korList=019&advClickPosition=kor_normal_p1_g1'
    return url_pre + num + url_post


def new_car_msg(newer):
    hello = "===신규 매물! " + str(len(newer)) + "건\n"
    contents_list = []
    for car in newer:
        id = car['Id']
        contents = "번호: " + id + \
                   "\n차종: " + car['Model'] + \
                   "\n가격: " + str(car['Price']) + \
                   "\n링크: " + create_link(id) + \
                   "\n"
        contents_list.append(contents)
    return hello, contents_list


def leave_car_msg(leave):
    leave_contents = "===기존 매물 " + str(len(leave)) + "건\n"
    return leave_contents


def deleted_car_msg(deleted):
    deleted_contents = "===삭제 매물 " + str(len(deleted)) + "건\n"
    return deleted_contents


def notify_newer_cars(separated_by_status):
    bot = get_bot()
    chat_room = get_chat_room()
    newer = separated_by_status['newer']
    hello, contents = new_car_msg(newer)
    send(bot, chat_room, hello)
    if len(contents) > 15:
        for i in range(15):
            send(bot, chat_room, str(i) + "번째 매물\n" + contents[i])
    else:
        for c in contents:
            send(bot, chat_room, c)


def notify_leave_cars(separated_by_status):
    bot = get_bot()
    chat_room = get_chat_room()
    leave = separated_by_status['leave']
    readable_data = leave_car_msg(leave)
    send(bot, chat_room, readable_data)


def notify_deleted_cars(separated_by_status):
    bot = get_bot()
    chat_room = get_chat_room()
    deleted = separated_by_status['deleted']
    readable_data = deleted_car_msg(deleted)
    send(bot, chat_room, readable_data)


def notify(separated_by_status):
    notify_newer_cars(separated_by_status)
    notify_leave_cars(separated_by_status)
    notify_deleted_cars(separated_by_status)


def test():
    import test
    # print("get bot")
    # get_bot()

    # print("converter_readability test")
    data = test.get_separated_by_status_three_newer()
    # print(x)

    print("send long message test")
    notify(data)

# test()
