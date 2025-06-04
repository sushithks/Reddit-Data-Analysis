import configparser
import os

parser = configparser.ConfigParser()
parser.read(os.path.join(os.path.dirname(__file__), '../config/config.conf'))


SECRET = parser.get('api_keys', 'secret_key')
CLIENT_ID = parser.get('api_keys', 'client_id')
