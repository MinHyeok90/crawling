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


def drop_all():
    mydb = myclient.jungo_car_app
    mycol = mydb.jungo_cars
    mycol.drop()


def save_all_test():
    mylist = [
        {'Id': '25167131', 'ModifiedDate': '2019-10-09 23:57:38.000 +09', 'Manufacturer': '현대', 'Price': 1950.0,
         'Year': 201402.0, 'Mileage': 79786.0, 'Model': '맥스크루즈', 'Badge': '디젤(e-VGT) 2.2 4WD 익스클루시브', '조회수': '200',
         '찜수': '2'},
        {'Id': '25479305', 'ModifiedDate': '2019-10-09 23:56:59.000 +09', 'Manufacturer': '현대', 'Price': 2270.0,
         'Year': 201708.0, 'Mileage': 8098.0, 'Model': '코나', 'Badge': '1.6 터보 4WD', '조회수': '720', '찜수': '6'},
        {'Id': '25109309', 'ModifiedDate': '2019-10-09 23:53:59.000 +09', 'Manufacturer': '현대', 'Price': 1750.0,
         'Year': 201302.0, 'Mileage': 33488.0, 'Model': '싼타페 DM', 'Badge': '디젤(e-VGT) 2.0 2WD 프리미엄', '조회수': '933',
         '찜수': '9'},
        {'Id': '25377212', 'ModifiedDate': '2019-10-01 20:18:39.000 +09', 'Manufacturer': '현대', 'Price': 2590.0,
         'Year': 201705.0, 'Mileage': 67541.0, 'Model': '더 뉴 맥스크루즈', 'Badge': '디젤 2.2 4WD', '조회수': '1042', '찜수': '3'},
    ]
    save_all(mylist)
# save_all_test()


def find_all_test():
    x = find_all()
    for i in x:
        print(x)
# find_all_test()
