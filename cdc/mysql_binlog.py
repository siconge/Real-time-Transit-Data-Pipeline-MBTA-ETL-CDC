# pip3 install pymysql==0.10.1
# pip3 install mysql-replication==0.22

from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import WriteRowsEvent, UpdateRowsEvent, DeleteRowsEvent

from utils.constants import DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_PORT_MYSQL, DATABASE_NAME, TABLE_NAME

MYSQL_SETTINGS = {
    'host':DATABASE_HOST,
    'port':DATABASE_PORT_MYSQL,
    'user':DATABASE_USER,
    'passwd':DATABASE_PASSWORD
}

def capture_mysql_binlog():
    stream = BinLogStreamReader(
        connection_settings=MYSQL_SETTINGS,
        server_id=3,
        blocking=True,
        only_events=[WriteRowsEvent, UpdateRowsEvent, DeleteRowsEvent]
    )

    for binlogevent in stream:
        binlogevent.dump()
    
    stream.close()