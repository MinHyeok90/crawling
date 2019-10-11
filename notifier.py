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


def send(message):
    bot = get_bot()
    chat_room = get_chat_room()
    bot.sendMessage(chat_room, message)
    # print(message)


def create_link(num):
    url_pre = 'www.encar.com/dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid='
    url_post = '&wtClick_korList=019&advClickPosition=kor_normal_p1_g1'
    return url_pre + num + url_post


def extract_newer(separated_by_status):
    return separated_by_status['newer']


def extract_leave(separated_by_status):
    return separated_by_status['leave']


def extract_deleted(separated_by_status):
    return separated_by_status['deleted']


def new_car_msg(newer):
    contents_list = []
    for car in newer:
        contents = car['Model'] + \
                   "/" + str(car['Price']) + \
                   "\n링크: " + create_link(car['Id']) + \
                   "\n"
        contents_list.append(contents)
    return contents_list


def notify_newer_cars(separated_by_status):
    newer = separated_by_status['newer']
    contents = new_car_msg(newer)
    if len(contents) > 15:
        for i in range(15):
            send("신규 " + str(i + 1) + "번째\n" + contents[i])
    else:
        for i in range(len(contents)):
            send("신규 " + str(i + 1) + "번째\n" + contents[i])


def notify_header(separated_by_status):
    newer = separated_by_status['newer']
    leave = separated_by_status['leave']
    deleted = separated_by_status['deleted']
    title = "신규" + str(len(newer)) + "/" + \
            "유지" + str(len(leave)) + "/" + \
            "팔림" + str(len(deleted))
    send(title)


def notify_validator(separated_by_status):
    if len(extract_newer(separated_by_status)) == 0 and len(extract_deleted(separated_by_status)) == 0:
        return False
    return True


def notify(separated_by_status):
    if notify_validator(separated_by_status):
        notify_header(separated_by_status)
        notify_newer_cars(separated_by_status)


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
