import pymongo
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# myclient = pymongo.MongoClient("127.0.0.1", 27017)
myclient = pymongo.MongoClient("mongodb://192.168.99.100:27017/")


def save_all(list_data):
    mydb = myclient.jungo_car_app
    mycol = mydb.jungo_cars
    x = mycol.insert_many(list_data)


def find_all():
    print("not tested")
    mydb = myclient.jungo_car_app
    mycol = mydb.jungo_cars
    res = []
    for x in mycol.find():
        res.append(x)
    return res

# def test():
#     mylist = [
#         {"name": "Amy", "address": "Apple st 652"},
#         {"name": "Hannah", "address": "Mountain 21"},
#         {"name": "Michael", "address": "Valley 345"},
#         {"name": "Sandy", "address": "Ocean blvd 2"},
#         {"name": "Betty", "address": "Green Grass 1"},
#         {"name": "Richard", "address": "Sky st 331"},
#         {"name": "Susan", "address": "One way 98"},
#         {"name": "Vicky", "address": "Yellow Garden 2"},
#         {"name": "Ben", "address": "Park Lane 38"},
#         {"name": "William", "address": "Central st 954"},
#         {"name": "Chuck", "address": "Main Road 989"},
#         {"name": "Viola", "address": "Sideway 1633"}
#     ]
#     save_all(mylist)
# test()

# x = find_all()
# for i in x:
#     print(x)
