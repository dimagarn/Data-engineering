import csv
import sqlite3
import json


def parse_data(filename):
    items = []
    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)

        for row in reader:
            if len(row) == 0:
                continue
            item = {
                'title': row[0],
                'author': row[1],
                'genre': row[2],
                'pages': int(row[3]),
                'published_year': int(row[4]),
                'isbn': row[5],
                'rating': float(row[6]),
                'views': int(row[7])
            }
            items.append(item)
    return items


def insert_data(db, data):
    cursor = db.cursor()

    cursor.executemany("""
        INSERT INTO books (title, author, genre, pages, published_year, isbn, rating, views)
        VALUES(
            :title, :author, :genre, :pages, 
            :published_year, :isbn, :rating, :views
        )
    """, data)

    db.commit()


def get_stat_by_pages(db):
    cursor = db.cursor()
    res = cursor.execute("""
    SELECT
        SUM(pages) as sum,
        AVG(pages) as avg,                
        MIN(pages) as min,
        MAX(pages) as max
    FROM books
    """)

    print(dict(res.fetchone()))

    cursor.close()
    return []


def get_freq_by_century(db):
    cursor = db.cursor()
    res = cursor.execute("""
    SELECT
        CAST(count(*) as REAL) / (SELECT COUNT(*) FROM books) as count,
        (published_year/100)+1 as published_century
    FROM books
    GROUP BY (published_year/100)+1
    """)
    for row in res.fetchall():
        print(dict(row))


def filter_by_year(db, min_year, limit=10):
    cursor = db.cursor()
    items = []
    res = cursor.execute("""
            SELECT title, published_year, views FROM books
            WHERE published_year > ?
            ORDER BY views DESC
            LIMIT ?
            """, [min_year, limit])
    for row in res.fetchall():
        item = dict(row)
        items.append(item)

    cursor.close()
    return items


def get_top_by_views(db, limit):
    cursor = db.cursor()

    res = cursor.execute("SELECT title, author, views FROM books ORDER BY views DESC LIMIT ?", [limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)

    cursor.close()
    return items

def connect_to_db(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection


items = parse_data('task_1_var_04_item.csv')
db = connect_to_db('db')

sorted_items = get_top_by_views(db, 10)
get_stat_by_pages(db)
get_freq_by_century(db)
sorted_items_with_year = filter_by_year(db, 1955)

insert_data(db, items)

with open("top_10_views.json", "w", encoding="utf-8") as r_json:
    r_json.write(json.dumps(sorted_items, ensure_ascii=False))

with open("top_10_views_with_year.json", "w", encoding="utf-8") as r_json:
    r_json.write(json.dumps(sorted_items_with_year, ensure_ascii=False))  