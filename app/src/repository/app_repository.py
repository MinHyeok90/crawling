import pymongo
import os
import datetime
import pytz
# from model.division_state_cars import DivisionStateCars
import setting_reader

env = setting_reader.get_env()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
myclient = pymongo.MongoClient(env['database']['host'])

def save_leave_cars(leave_cars):
    if leave_cars and len(leave_cars) > 0:
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


def find_candidate_as_updated_from_deleted():
    mydb = myclient.jungo_car_app
    deleted_cars = mydb.deleted_cars
    # for candidate in deleted_cars.find({""}):
    res = []
    for x in deleted_cars.find():
        res.append(x)
    return res


def drop_deleted_cars():
    mydb = myclient.jungo_car_app
    mycol = mydb.deleted_cars
    mycol.drop()


def drop_all():
    drop_leave_cars()
    drop_deleted_cars()


def pre_process(dsc):
    drop_all()
    dsc.add_updated_mark()
    dsc.add_removed_date()


def update_leave_and_deleted(dsc):
    pre_process(dsc)
    save_leave_cars(dsc.get_updated())
    save_leave_cars(dsc.get_leave())
    save_leave_cars(dsc.get_newer())
    save_deleted_cars(dsc.get_deleted())


def update_deleted_all(still_deleted):
    if len(still_deleted) > 0:
        mydb = myclient.jungo_car_app
        deleted = mydb.deleted_cars
        deleted.drop()
        deleted.insert_many(still_deleted)
    


def test():
    from app import test
    print("update_leave_and_deleted test")
    d = test.get_separated_by_status()
    update_leave_and_deleted(d)


def repo_test():
    from app import test
    dsc = DivisionStateCars()
    td = test.get_separated_by_status()
    dsc.of(td)
    update_leave_and_deleted(dsc)


# def connection_test():

# repo_test()

# add_deleted_date()
