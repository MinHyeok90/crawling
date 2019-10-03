import requests
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_title = 'result.json'

search_url = 'http://api.encar.com/search/car/list/premium?count=true&q=(And.Hidden.N._.(C.CarType.Y._.Manufacturer.%ED%98%84%EB%8C%80.)_.OfficeCityState.%EA%B2%BD%EA%B8%B0._.Trust.ExtendWarranty._.Options.%EB%B8%8C%EB%A0%88%EC%9D%B4%ED%81%AC+%EC%9E%A0%EA%B9%80+%EB%B0%A9%EC%A7%80(ABS_)._.Options.%ED%9B%84%EB%B0%A9+%EC%B9%B4%EB%A9%94%EB%9D%BC._.Options.%EC%A3%BC%EC%B0%A8%EA%B0%90%EC%A7%80%EC%84%BC%EC%84%9C(%EC%A0%84%EB%B0%A9_)._.Category.SUV.)&sr=%7CModifiedDate%7C0%7C100'
item_url_pre = 'http://www.encar.com/dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid='
item_url_post = '&wtClick_korList=019&advClickPosition=kor_normal_p1_g1'


def save(data):
    with open(os.path.join(BASE_DIR, file_title), 'w+', encoding='UTF-8-sig') as json_file:
        json_file.write(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4))


def crawling():
    req = requests.get(search_url)
    return req.json()


def crawling_and_save():
    json_data = crawling()
    save(json_data)
    return json_data


def from_file():
    with open(os.path.join(BASE_DIR, file_title), encoding='UTF-8-sig') as json_file:
        json_data = json.load(json_file)
    return json_data


def my_interest_order():
    order = []
    order.append('Id')
    order.append('Manufacturer')
    order.append('Price')
    order.append('ModifiedDate')
    order.append('Badge')
    return order


# {
#             "Badge": "디젤 2.0 4WD",
#             "BadgeDetail": "프레스티지",
#             "FormYear": "2019",
#             "FuelType": "디젤",
#             "Id": "25049206",
#             "Manufacturer": "현대",
#             "Mileage": 11923.0,
#             "Model": "싼타페 TM",
#             "ModifiedDate": "2019-10-03 19:31:00.000 +09",
#             "OfficeCityState": "경기",
#             "Photo": "/carpicture04/pic2504/25049206_",
#             "Photos": [
#                 {
#                     "location": "/carpicture04/pic2504/25049206_001.jpg",
#                     "ordering": 1.0,
#                     "type": "001",
#                     "updatedDate": "2019-07-08T03:31:11Z"
#                 }
#             ],
#             "Price": 3290.0,
#             "Separation": [
#                 "B"
#             ],
#             "Transmission": "오토",
#             "Trust": [
#                 "Warranty",
#                 "ExtendWarranty",
#                 "Inspection"
#             ],
#             "Year": 201806.0
#         },

def extract_my_interest(total_data):
    my_order = my_interest_order()
    print(my_order)
    for item in total_data['SearchResults']:
        del item['Photos']
        record = []
        for i in my_order:
            record.append(item[i])
        print(record)

def get_additional_info(id):
    url = item_url_pre + id + item_url_post;
    req = requests.get(url)

def main():
    # json_data = crawling_and_save()
    json_data = from_file()
    extract_my_interest(json_data)


main()
