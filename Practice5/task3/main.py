import msgpack
import json
import csv
from pymongo import MongoClient
from bson.json_util import dumps, loads

def connect():
    client = MongoClient()
    db = client['task3_db']
    return db.person

def get_from_csv(filename):
    with open(filename, 'rb') as mp_file:
        items = msgpack.load(mp_file)
    return items
def insert_many(collection, data):
    result = collection.insert_many(data)
    print(result)


def first_query(collection):
    result = collection.delete_many({
        '$or' : [
            {'salary': {'$lt':25_000}},
            {'salary':{'$gt':175_000}}
        ]
    })
    print(result)

def second_query(collection):
    result = collection.update_many({},{
        '$inc': {
            'age': 1
        }
    })
    print(result)

def third_query(collection):
    filter = {
        "job" : {"$in": ["Архитектор", "Косметолог", "Строитель"]}
    }
    update = {
            "$mul" : {
                'salary': 1.05
        }
    }
    result = collection.update_many(filter, update)
    print(result)

def fourth_query(collection):
    filter = {
        "city" : {"$in": ["Луго", "Москва", "Сан-Себастьян"]}
    }
    update = {
            "$mul" : {
                'salary': 1.07
        }
    }
    result = collection.update_many(filter, update)
    print(result)

def fifth_query(collection):
    filter = {
        "city" : {"$in": ["Картахена", "Вальядолид", "Москва"]},
        "job" : {"$in": ["Продавец", "Менеджер", "Косметолог"]},
        "$or": [
                {'age': {"$gt":18, '$lt':25}},
                {'age': {"$gt":50, '$lt':65}}
            ]
    }
    update = {
            "$mul" : {
                'salary': 1.1
        }
    }
    result = collection.update_many(filter, update)
    print(result)

def sixth_query(collection):
    result = collection.delete_many({
        '$or' : [
            {'age': {'$lt':25}},
            {'age':{'$gt':80}}
        ]
    })
    print(result)
data = get_from_csv('task_3_item.msgpack')
insert_many(connect(), data)
first_query(connect())
second_query(connect())
third_query(connect())
fourth_query(connect())
fifth_query(connect())
sixth_query(connect())