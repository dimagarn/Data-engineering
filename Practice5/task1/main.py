from pprint import pprint
import pymongo
import pickle
import json
from bson import json_util


def create_and_update_db():
	objects = []
	with open('task_1_item.pkl', 'rb') as openfile:
		data = pickle.load(openfile)

	for item in data:
		record = {}
		record['id'] = item['id']
		record['age'] = int(item['age'])
		record['city'] = item['city']
		record['job'] = item['job']
		record['salary'] = int(item['salary'])
		record['year'] = int(item['year'])
		objects.append(record)

	client = pymongo.MongoClient()
	db = client['task1_db']
	db.drop_collection('workers')
	collection = db['workers']

	for record in objects:
		collection.insert_one(record)

	result = (collection.find().sort('salary', pymongo.DESCENDING).limit(10))


	with open("salary_sorted.json", "w", encoding="utf-8") as file:
		file.write(json_util.dumps(result, ensure_ascii=False))

	result = list(collection.find({'age': {'$lt': 30}}).sort('salary', pymongo.DESCENDING).limit(15))

	with open("age_filtered.json", "w", encoding="utf-8") as file:
		file.write(json_util.dumps(result, ensure_ascii=False))

	result = list(
		collection.find(
			{'$and': [{'city': 'Тарраса'}, {'job': {'$in': ['Повар', 'Строитель', 'Врач']}}]}).sort(
			'age', pymongo.ASCENDING).limit(10))

	with open("hard_predicate_sorted.json", "w", encoding="utf-8") as file:
		file.write(json_util.dumps(result, ensure_ascii=False))

	result = collection.count_documents({'$and': [{'age': {'$gte': 20, '$lte': 40}},
												  {'year': {'$in': [2019, 2020, 2021, 2022]}}, {
													  '$or': [{'salary': {'$gt': 50000, '$lte': 75000}},
															  {'salary': {'$gt': 125000, '$lt': 150000}}]}]})

	with open("counted.json", "w", encoding="utf-8") as file:
		json.dump({"count": result}, file, ensure_ascii=False, indent=2)


if __name__ == '__main__':
	create_and_update_db()
