import pymongo
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
myclient = pymongo.MongoClient("mongodb://192.168.99.100:27017/")


def save_leave_cars(leave_cars):
    if len(leave_cars) > 0:
        mydb = myclient.jungo_car_app
        mycol = mydb.leave_cars
        mycol.insert_many(leave_cars)


def load_leave_cars():
    mydb = myclient.jungo_car_app
    mycol = mydb.leave_cars
    res = []
    for x in mycol.find():
        res.append(x)
    return res


def drop_leave_cars():
    mydb = myclient.jungo_car_app
    mycol = mydb.leave_cars
    mycol.drop()


def save_deleted_cars(deleted_cars):
    if len(deleted_cars) > 0:
        mydb = myclient.jungo_car_app
        mycol = mydb.deleted_cars
        mycol.insert_many(deleted_cars)


def load_deleted_cars():
    mydb = myclient.jungo_car_app
    mycol = mydb.deleted_cars
    res = []
    for x in mycol.find():
        res.append(x)
    return res


def drop_deleted_cars():
    mydb = myclient.jungo_car_app
    mycol = mydb.deleted_cars
    mycol.drop()


def drop_all():
    drop_leave_cars()
    drop_deleted_cars()


def update_leave_and_deleted(separated_by_status):
    newer = separated_by_status['newer']
    leave = separated_by_status['leave']
    deleted = separated_by_status['deleted']
    drop_leave_cars()
    save_leave_cars(newer)
    save_leave_cars(leave)
    save_deleted_cars(deleted)


def test():
    from app import test
    print("update_leave_and_deleted test")
    d = test.get_separated_by_status()
    update_leave_and_deleted(d)
