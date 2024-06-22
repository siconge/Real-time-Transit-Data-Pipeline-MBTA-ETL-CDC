import configparser
import os

parser = configparser.ConfigParser()
parser.read(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.conf'))

MBTA_CONTAINER_NETWORK = parser.get('mbta', 'mbta_container_network')
MBTA_MYSQL_IMAGE = parser.get('mbta', 'mbta_mysql_image')
MBTA_MYSQL_CONTAINER = parser.get('mbta', 'mbta_mysql_container')
MBTA_MONGO_CONTAINER = parser.get('mbta', 'mbta_mongo_container')
MBTA_API_URL = parser.get('mbta', 'mbta_api_url')


INPUT_PATH = parser.get('file_paths', 'input_path')
OUTPUT_PATH = parser.get('file_paths', 'output_path')

DATABASE_HOST = parser.get('database', 'database_host')
DATABASE_USER = parser.get('database', 'database_username')
DATABASE_PASSWORD = parser.get('database', 'database_password')
DATABASE_PORT_MYSQL = parser.get('database', 'database_port_mysql')
DATABASE_PORT_MONGO = parser.get('database', 'database_port_mongo')
DATABASE_NAME = parser.get('database', 'database_name')
TABLE_NAME = parser.get('database', 'table_name')