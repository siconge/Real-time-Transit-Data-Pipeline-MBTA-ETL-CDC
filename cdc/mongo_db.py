import pymongo

from utils.constants import DATABASE_HOST, DATABASE_PORT_MONGO, DATABASE_NAME, TABLE_NAME

# Create MongoDB client and connect to the database and collection
uri = f'mongodb://{DATABASE_HOST}:{DATABASE_PORT_MONGO}/{DATABASE_NAME}'
client = pymongo.MongoClient(uri)
db = client[DATABASE_NAME]
collection = db[TABLE_NAME]

def write_mbta_record(records):
    for record in records:
        filter_criteria = {'record_num': record['record_num']}
        update_operation = {'$set': record}
        collection.update_one(filter_criteria, update_operation, upsert=True)

def read_mbta_record(last_check_stamp):
    query = {'updated_at': {'$gt': last_check_stamp}}
    projection = {'_id': 0}
    records = list(collection.find(query, projection).sort('updated_at', -1))
    return records