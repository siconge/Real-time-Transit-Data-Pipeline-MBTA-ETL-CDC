from sqlalchemy import create_engine

from utils.constants import DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_PORT_MYSQL, DATABASE_NAME, TABLE_NAME

# Create the database URI and engine
uri = f'mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT_MYSQL}/{DATABASE_NAME}'
engine = create_engine(uri)

def insert_mbta_record(mbta_dict_list):
    query = f'''
    INSERT INTO {TABLE_NAME} (id, bearing, current_status, current_stop_sequence, direction_id, longitude, latitude, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    with engine.begin() as conn:
        for mbta_dict in mbta_dict_list:
            val = (
                mbta_dict['id'],
                mbta_dict['bearing'],
                mbta_dict['current_status'],
                mbta_dict['current_stop_sequence'],
                mbta_dict['direction_id'],
                mbta_dict['longitude'],
                mbta_dict['latitude'],
                mbta_dict['updated_at']
            )
            conn.execute(query, val)

def read_mbta_record(last_check_stamp):
    query = f'''
    SELECT * FROM {TABLE_NAME}
    WHERE updated_at > %s
    ORDER BY updated_at DESC
    '''
    with engine.connect() as conn:
        result = conn.execute(query, (last_check_stamp,))
        records = [dict(row) for row in result]
    return records