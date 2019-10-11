#!/usr/bin/env python
# encoding=utf-8
import telegram
import os
from app.model.division_state_cars import DivisionStateCars


def get_dic():
    return os.path.dirname(os.path.abspath(__file__))


def get_bot():
    f = open(get_dic() + '/my_key', 'r')
    key = f.readline()
    bot = telegram.Bot(token=key)
    return bot


def get_chat_room():
    f = open(get_dic() + '/my_chat_room', 'r')
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


def car_msg(cars):
    contents_list = []
    for car in cars:
        contents = car['Model'] + \
                   "/" + str(car['Price']) + \
                   "\n링크: " + create_link(car['Id']) + \
                   "\n"
        contents_list.append(contents)
    return contents_list


def notify_newer_cars(dsc: DivisionStateCars):
    newer = dsc.get_newer()
    contents = car_msg(newer)
    if len(contents) > 15:
        for i in range(15):
            send("신규 " + str(i + 1) + "번째\n" + contents[i])
    else:
        for i in range(len(contents)):
            send("신규 " + str(i + 1) + "번째\n" + contents[i])


def notify_deleted_cars(dsc: DivisionStateCars):
    deleted = dsc.get_deleted()
    contents = car_msg(deleted)
    for i in range(len(contents)):
        send("삭제 " + str(i + 1) + "\n" + contents[i])


def notify_header(dsc: DivisionStateCars):
    title = "신규" + str(dsc.get_len_newer()) + "/" + \
            "유지" + str(dsc.get_len_leave()) + "/" + \
            "삭제" + str(dsc.get_len_deleted())
    send(title)


def notify_validator(dsc: DivisionStateCars):
    if dsc.get_len_newer() == 0 and dsc.get_len_deleted() == 0:
        return False
    return True


def notify(dsc: DivisionStateCars):
    if notify_validator(dsc):
        notify_header(dsc)
        notify_newer_cars(dsc)


def force_header_notify(dsc: DivisionStateCars):
    notify_header(dsc)


def force_header_notify_as_leave_by_list(leave):
    dsc = DivisionStateCars()
    dsc.set_leave(leave)
    notify_header(dsc)


def test():
    from app import test
    # print("get bot")
    # get_bot()

    # print("converter_readability test")
    data = test.get_separated_by_status_three_newer()
    # print(x)

    print("send long message test")
    notify(data)


def test_path():
    import os
    stri = os.path.dirname(os.path.abspath(__file__))
    print(stri)

# if __name__ == "__main__":
    # test()
test_path()
pass
