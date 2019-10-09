import pymongo
import json


def find_stay(data):
    print("not implement")


def find_new(data):
    print("not implement")


def find_removed(data):
    print("not implement")


def find_interest(data):
    print("not implement")


# def converter(data):
#     return data


def distinguish(data):
    # data = converter(naive_data)
    data_checked_new = find_new(data)
    data_checked_remove = find_removed(data_checked_new)
    data_checked_interest = find_interest(data_checked_remove)
    return data_checked_interest
