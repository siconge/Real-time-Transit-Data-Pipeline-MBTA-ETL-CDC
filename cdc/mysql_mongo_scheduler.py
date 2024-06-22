# Build a CDC system to automate change propagation from a container-based MySQL to MongoDB using Python

from threading import Timer
from datetime import datetime, timedelta
import time
import mysql_db
import mongo_db

def initial_timestamp():
    return (datetime.now() - timedelta(seconds=10)).strftime('%Y-%m-%d %H:%M:%S')

def status(records, db):
    print(f'--- {db} updated with {len(records)} records ---')
    for record in records:
        print(record)

def cdc_timeloop(last_check_stamp):
    print(f'--- ' + time.ctime() + ' ---')
    records = mysql_db.read_mbta_record(last_check_stamp)
    status(records, 'mysql')
    mongo_db.write_mbta_record(records)
    if records:
        last_check_stamp = max(record['updated_at'] for record in records)
    status(mongo_db.read_mbta_record(), 'mongo')
    Timer(10, cdc_timeloop, args=[last_check_stamp]).start()