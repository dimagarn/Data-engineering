import os
import csv
import sqlite3
import json
import pickle

my_file_part_1 = os.path.join(os.path.dirname(__file__), os.path.normpath('data'), os.path.normpath('task_3_var_04_part_1.csv'))
my_file_part_2 = os.path.join(os.path.dirname(__file__), os.path.normpath('data'), os.path.normpath('task_3_var_04_part_2.pkl'))
res_file = os.path.join(os.path.dirname(__file__), os.path.normpath('result'))

def read_second(file_name):
    with open(file_name, 'rb') as file:
        data = pickle.load(file)
    for item in data:
        item.pop('acousticness')
        item.pop('popularity')
    return data


def read_first(file_name):
    items = []
    with open(file_name, 'r', encoding='utf-8') as file:
        data = csv.reader(file, delimiter=';')
        data.__next__()

        for row in data:
            if len(row) == 0: continue
            item = dict()
            item['artist'] = row[0]
            item['song'] = row[1]
            item['duration_ms'] = int(row[2])
            item['year'] = int(row[3])
            item['tempo'] = float(row[4])
            item['genre'] = row[5]
            item['energy'] = float(row[6])
            items.append(item)
    return items


def connect_to_db(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection


def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO music (artist, song, duration_ms, year, tempo, genre, energy) 
        VALUES(:artist, :song, :duration_ms, :year, :tempo, :genre, :energy)""", data)
    db.commit()


# Сортируем по годам 
def top_year(db, limit):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM music ORDER BY year DESC LIMIT ?", [limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


# смотрим числовые характеристики для продолжительности песен
def charact_duration_ms(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            SUM(duration_ms) as sum,
            AVG(duration_ms) as avg,
            MIN(duration_ms) as min, 
            MAX(duration_ms) as max
        FROM music
                        """)
    print(dict(res.fetchone()))
    cursor.close()
    return []


def popul_artist(db):
    cursor = db.cursor()
    items = []
    res = cursor.execute("""
        SELECT 
            CAST(COUNT(*) as REAL) / (SELECT COUNT(*) FROM music) as count,
            artist
        FROM music
        GROUP BY artist
                        """)
    for row in res.fetchall():
        items.append(dict(row))
    return items


def filter_year(db, min_year, limit):
    items = []
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM music
        WHERE year >= ?
        ORDER BY tempo DESC
        LIMIT ?
        """, [min_year, limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


data_1 = read_first(my_file_part_1)
data_2 = read_second(my_file_part_2)
data12 = data_1 + data_2
print(data_1[0].keys())
print(data_2[0].keys())

db = connect_to_db(os.path.join(os.path.dirname(__file__), os.path.normpath('third_db')))
insert_data(db, data12)

sort_views = top_year(db, 14)
with open(os.path.join(res_file, os.path.normpath("res_3_sorted.json")), 'w', encoding='utf-8') as f:
    f.write(json.dumps(sort_views, ensure_ascii=False))

charact_duration_ms(db)

pop_art = popul_artist(db)
with open(os.path.join(res_file, os.path.normpath("res_3_popular.json")), 'w', encoding='utf-8') as f:
    f.write(json.dumps(pop_art, ensure_ascii=False))

fil_year = filter_year(db, 2013, 19)
with open(os.path.join(res_file, os.path.normpath("res_3_filtered.json")), 'w', encoding='utf-8') as f:
    f.write(json.dumps(fil_year, ensure_ascii=False))