import app_repository

original_data = []
stay_ids = []
new_ids = []


def converter_list_to_dic_id_as_key(list_data):
    '''
        from : [{}, {}, {}]
        to : {'id':{}, 'id':{}, 'id':{}}
    '''
    return dict((list_data[j]['Id'], list_data[j]) for j in range(len(list_data)))


def converter_dic_to_list(dics):
    '''
        from : {'id':{}, 'id':{}, 'id':{}}
        to : [{}, {}, {}]
    '''
    res = []
    for key, value in dics:
        res.append(value)
    return res


def leave_ids_extractor(original, new):
    return original.keys() & new.keys()


def new_ids_extractor(original, new):
    return new.keys() - original.keys()


def deleted_ids_extractor(original, new):
    return original.keys() - new.keys()


def new_leave_deleted_id_extractor(original, new):
    # ids: set like {'25167131', '25167135', ...}
    newer_ids = new_ids_extractor(original, new)
    leave_ids = leave_ids_extractor(original, new)
    deleted_ids = deleted_ids_extractor(original, new)
    return newer_ids, leave_ids, deleted_ids


def return_as_add_type_in_dic(original, leave_ids, newer_ids, deleted_ids):
    '''
        [ '65456':{'id':65456, ... , 'status':'newer' }, 'id':{}, 'id':{}, ... ]
    '''
    # this converter need to save operation
    print("not impl")


def return_as_separated_list_in_dic(original, newer, leave_ids, newer_ids, deleted_ids):
    '''
        {
            'newer':[{id:1, }, {}, {}, ...],
            'leave':[{id:2, }, {}, {}, ...],
            'remover':[{id:3, }, {}, {}, ...]
        }
    '''
    new_cars = []
    leave_cars = []
    deleted_cars = []
    for id in newer_ids:
        new_cars.append(newer[id])
    for id in leave_ids:
        leave_cars.append(newer[id])
    for id in deleted_ids:
        deleted_cars.append(original[id])
    return {'newer': new_cars, 'leave': leave_cars, 'deleted': deleted_cars}


def convert_for_save_with_status(ori_cars, leave, newer, deleted):
    return return_as_add_type_in_dic(ori_cars, leave, newer, deleted)


def convert_separated_by_status(ori_cars, newer, leave_ids, newer_ids, deleted_ids):
    return return_as_separated_list_in_dic(ori_cars, newer, leave_ids, newer_ids, deleted_ids)


def distinguish(cars):
    original_car_list = app_repository.load_leave_cars()
    origi_cars = converter_list_to_dic_id_as_key(original_car_list)
    newer_cars = converter_list_to_dic_id_as_key(cars)

    newer_ids, leave_ids, deleted_ids = new_leave_deleted_id_extractor(origi_cars, newer_cars)

    return convert_separated_by_status(origi_cars, newer_cars, newer_ids, leave_ids, deleted_ids)


def test():
    import test
    data4 = test.get_test_list_original()
    data2 = test.get_test_list_newer()
    origi_cars = converter_list_to_dic_id_as_key(data4)
    newer_cars = converter_list_to_dic_id_as_key(data2)

    # convert_test
    print("convert_test")
    converted = converter_list_to_dic_id_as_key(data4)
    for car in converted:
        print(converted[car])

    # extractor test
    print("extractor test")
    newer, leave, deleted = new_leave_deleted_id_extractor(origi_cars, newer_cars)
    print(newer, leave, deleted)

    # convert_separated_by_status test
    print("convert_separated_by_status test")
    x = convert_separated_by_status(origi_cars, newer_cars, leave, newer, deleted)
    print(x)

# test()
