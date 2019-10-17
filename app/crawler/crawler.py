from bs4 import BeautifulSoup
from urllib import parse
import requests

from app.crawler.page_url_generator import PageUrlGenerator

parsed_url = parse.urlparse("http://api.encar.com/search/car/list/premium?count=true&q=(And.Hidden.N._.CarType.Y._.(Or.OfficeCityState.%EC%84%9C%EC%9A%B8._.OfficeCityState.%EA%B2%BD%EA%B8%B0.)_.Transmission.%EC%98%A4%ED%86%A0._.Category.SUV._.Trust.Inspection.)&sr=%7CModifiedDate%7C0%7C50")
# search_url = 'http://api.encar.com/search/car/list/premium?count=true&q=(And.Hidden.N._.(C.CarType.Y._.Manufacturer.%ED%98%84%EB%8C%80.)_.OfficeCityState.%EA%B2%BD%EA%B8%B0._.Trust.ExtendWarranty._.Options.%EB%B8%8C%EB%A0%88%EC%9D%B4%ED%81%AC+%EC%9E%A0%EA%B9%80+%EB%B0%A9%EC%A7%80(ABS_)._.Options.%ED%9B%84%EB%B0%A9+%EC%B9%B4%EB%A9%94%EB%9D%BC._.Options.%EC%A3%BC%EC%B0%A8%EA%B0%90%EC%A7%80%EC%84%BC%EC%84%9C(%EC%A0%84%EB%B0%A9_)._.Category.SUV.)&sr=%7CModifiedDate%7C0%7C100'
item_url_pre = 'http://www.encar.com/dc/dc_cardetailview.do?pageid=dc_carsearch&listAdvType=normal&carid='
item_url_post = '&wtClick_korList=019&advClickPosition=kor_normal_p1_g1'

test_mode = True
test_limit_cnt = 3


def is_test_mode():
    return test_mode


def limiter_is_nedded_limit_for_test():
    if is_test_mode:
        return True
    else:
        return False


def print_my_interests(title, results):
    print("Result!")
    print(title)
    print(results)


def my_interest_order():
    order = []
    order.append('Id')
    order.append('ModifiedDate')
    order.append('Manufacturer')
    order.append('Price')
    order.append('Year')
    order.append('Mileage')
    order.append('Model')
    order.append('Badge')
    return order


def my_interest_order_and_photodate_view():
    order = my_interest_order()
    order.append('Photos_updatedDate')
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

def convert_to_my_interest(total_data):
    my_order = my_interest_order()
    records = []
    for item in total_data['SearchResults']:
        record = {}
        for key in my_order:
            record[key] = item[key]
        # record.append(item['Photos'][0]['updatedDate'])
        del item['Photos']
        records.append(record)
    return records


def add_photo_date(records):
    records_with_photodate = []
    # TODO: implement add photodate to records
    # for item in records:
    #
    return records_with_photodate


def crawl_detail(id):
    print("parsing: " + str(id) + "...")
    url = item_url_pre + str(id) + item_url_post
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find('ul', {'class': 'list_carinfo carinfo_etc'})
    more_specific_data = data.find_all('em')
    tmp = []
    i = 0
    for tag in more_specific_data:
        if i == 2 or i == 4:  # 조회수, 찜
            tmp.append(tag.text)
        i = i + 1
    return tmp


def crawl_detail_by_records_ids(table):
    for item in table:
        cnt_and_zzim = crawl_detail(item['Id'])
        item['조회수'] = cnt_and_zzim[0]
        item['찜수'] = cnt_and_zzim[1]
    print(table)
    return table


def send(search_url):
    req = requests.get(search_url)
    return req.json()
    '''
    {
        Count: 5391,
        SearchResults: [
            {}
            {}
        ]
    }
    '''


def list_crawler(cur_url):
    return send(cur_url)


def crawler():
    global parsed_url
    pug = PageUrlGenerator()
    pug.source_url(parsed_url.geturl())
    pug.initialize()
    cur_url = pug.first_url()
    simple_json_list_data = list_crawler(cur_url)
    result_records = convert_to_my_interest(simple_json_list_data)
    
    while pug.has_next(): #TODO
        url = pug.next()
        simple_json_list_data = list_crawler(url)
        result_records.extend(convert_to_my_interest(simple_json_list_data))
    # result_table = crawl_detail_by_records_ids(result_records)
    return result_records


def test():
    data = crawler()
    for x in data:
        print(x)
# test()
