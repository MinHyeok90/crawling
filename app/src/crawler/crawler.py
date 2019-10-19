from bs4 import BeautifulSoup
from urllib import parse
import requests
from crawler.page_url_generator import PageUrlGenerator
from crawler.exceptions.changed_total_count import ChangedTotalCount
from crawler.exceptions.fail_crawl import FailCrawl
from crawler.exceptions.duplicate_item import DuplicateItem

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


def send_request(search_url):
    req = requests.get(search_url)
    return req.json()


def list_crawler(cur_url):
    return send_request(cur_url)


def validate_list_duplicate_item(cars):
    res = {}
    duplicated = set()
    for car in cars:
        if car['Id'] in res:
            res[car['Id']] += 1
            duplicated.add(car['Id'])
        else:
            res[car['Id']] = 1

    if len(duplicated) > 0:
        duplicaters = []
        for x in duplicated:
            duplicaters.append((x, res[x]))
        raise DuplicateItem(str(list(duplicaters)))


def init_pageurlgenerator():
    global parsed_url
    pug = PageUrlGenerator()
    pug.source_url(parsed_url.geturl())
    pug.initialize()
    return pug


def crawl(pug: PageUrlGenerator):
    cur_url = pug.first_url()
    simple_json_list_data = list_crawler(cur_url)
    result_records = convert_to_my_interest(simple_json_list_data)
    creteria_count = int(simple_json_list_data['Count'])
    cur_total_count = simple_json_list_data['Count']
    print("매물", creteria_count, "개 확인! 로딩 중...")
    while cur_total_count > len(result_records):
        url = pug.next()
        simple_json_list_data = list_crawler(url)
        cur_total_count = simple_json_list_data['Count']
        result_records.extend(convert_to_my_interest(simple_json_list_data))
        if creteria_count != cur_total_count:
            raise ChangedTotalCount(str(
                "ChangedTotalCount from " + str(creteria_count) + " to " + str(cur_total_count)))
    return result_records


def crawler():
    try:
        pug: PageUrlGenerator = init_pageurlgenerator()
        result_records = crawl(pug)
        validate_list_duplicate_item(result_records)
    except ChangedTotalCount as e:
        print("총 수 변경 발생", e)
        print("재시도")
        try:
            pug: PageUrlGenerator = init_pageurlgenerator()
            result_records = crawl(pug)
            pass
        except:
            print("재시도실패")
            raise FailCrawl("Fail retry ChangedTotalCount")

    except DuplicateItem as e:
        print("종복 발생", e)
        raise FailCrawl("DuplicateItem")
    except Exception as e:
        print("알 수 없는 이유로 실패했네? 괜찮아! 좀 이따 알아서 하겠지!")
        raise FailCrawl(e)

    return result_records
