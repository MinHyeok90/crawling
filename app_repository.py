import pymongo
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# myclient = pymongo.MongoClient("127.0.0.1", 27017)
myclient = pymongo.MongoClient("mongodb://192.168.99.100:27017/")

def save(data):
    # save_data_title_as_file(data, file_title)
    mydb = myclient["jungo_car_app"]
    mycol = mydb["customers"]
    mydic = {"name": "John"}
    x = mycol.insert_one(mydic)


def create_database():
    print(x.inserted_id)




# def save_to_csv(json_data):
#     df = pandas.read_json(json_data)
#     df.to_csv("test.csv", encoding='utf-8')
