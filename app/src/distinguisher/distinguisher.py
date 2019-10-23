import requests
from bs4 import BeautifulSoup
from repository import app_repository
from model.division_state_cars import DivisionStateCars
from model.car import Car
from crawler.validator import Validator
original_data = []
stay_ids = []
new_ids = []


def converter_list_to_dic_id_as_key(list_data):
    '''
        from : [{}, {}, {}]
        to : {'id':{}, 'id':{}, 'id':{}}
    '''
    # res = {}
    # for j in range(len(list_data)):
    #     if list_data[j]['Id'] in res:
    #         print("중복 발생!")
    #         raise "UnreliableData"
    #     res[list_data[j]['Id']] = list_data[j]
    # return res
    return dict((list_data[j]['Id'], list_data[j]) for j in range(len(list_data)))


def new_ids_extractor(saved_list, latest_list):
    return latest_list.keys() - saved_list.keys()


def leave_ids_extractor(saved_list, latest_list):
    return saved_list.keys() & latest_list.keys()


def deleted_ids_extractor(saved_list, latest_list):
    return saved_list.keys() - latest_list.keys()


def validate_removed(deleted_id):
    rm_url = "http://www.encar.com/dc/dc_cardetailview.do?carid="
    rm_url += deleted_id
    req = requests.get(rm_url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find('div', {'class': 'cardetail_none'})
    if data == None:
        return False
    return True


def extract_not_removed(deleted_ids):
    not_removed = set()
    for id in deleted_ids:
        if validate_removed(id) == False:
            not_removed.add(id)
            print("not removed : " + id)
    return not_removed


def extract_updated_item(new_car, deleted_list):
    for de in deleted_list:
        if (round(new_car["Mileage"]) == de["Mileage"] and
            round(new_car["Year"]) == de["Year"] and
            new_car["Badge"] == de["Badge"] and
            new_car["Model"] == de["Model"] and
            new_car["Manufacturer"] == de["Manufacturer"] and
                round(new_car["Price"]) == de["Price"]):
            de["Id"] = new_car["Id"]
            deleted_list.remove(de)
            return de
    return None


def distinguish(latest_list):
    original_car_list = app_repository.load_leave_cars()
    dsc = DivisionStateCars()
    try:
        # Validator().check_duplicate_item(cars)
        latest_dic = converter_list_to_dic_id_as_key(latest_list)
        saved_dic = converter_list_to_dic_id_as_key(original_car_list)
        
        newer_ids_preset = new_ids_extractor(saved_dic, latest_dic)
        leave_ids_preset = leave_ids_extractor(saved_dic, latest_dic)
        deleted_ids_preset = deleted_ids_extractor(saved_dic, latest_dic)
        
        new_car_list = []
        for id in newer_ids_preset:
            new_car_list.append(latest_dic[id])
        new_car_dic = converter_list_to_dic_id_as_key(new_car_list)
        
        # validate removed is real?
        need_move_ids = extract_not_removed(deleted_ids_preset) 
        leave_ids_preset = (leave_ids_preset | need_move_ids)
        deleted_ids_preset = (deleted_ids_preset - need_move_ids)
        
        #get_updated_from_deleted
        removed_car_list = app_repository.find_candidate_as_updated_from_deleted()
        updated_list = []
        for new_item in new_car_dic.values():
            res = extract_updated_item(new_item, removed_car_list)
            if res:
                newer_ids_preset.remove(res.get("Id"))
                updated_list.append(res)
        app_repository.update_deleted_all(removed_car_list)
        '''
        return to
        {
            'new_cars':[{id:1, }, {}, {}, ...],
            'leave_cars':[{id:2, }, {}, {}, ...],
            'deleted_cars':[{id:3, }, {}, {}, ...]
        }
        '''
        new_cars = list(latest_dic.get(id) for id in newer_ids_preset)
        leave_cars = list(saved_dic.get(id) for id in leave_ids_preset)
        updated_cars = updated_list
        deleted_cars = list(saved_dic.get(id) for id in deleted_ids_preset)
        
        # return {'newer': new_cars, 'leave': leave_cars, 'deleted': deleted_cars}
        total = {}
        total['newer'] = new_cars
        total['leave'] = leave_cars
        total['updated'] = updated_cars
        total['deleted'] = deleted_cars
        
        dsc = DivisionStateCars()
        dsc.by_separated_status(total)
    except:
        raise "신뢰할 수 없는 데이터 발생."

    return dsc


def test():
    from app import test
    data4 = test.get_test_list_original()
    data2 = test.get_test_list_newer()
    origi_cars = converter_list_to_dic_id_as_key(data4)
    newer_cars = converter_list_to_dic_id_as_key(data2)

    # convert_test
    print("convert_test")
    converted = converter_list_to_dic_id_as_key(data4)
    for car in converted:
        print(converted[car])

# test()
