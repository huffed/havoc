import json
from sqlalchemy import create_engine

with open('config/config.json') as f:
    connection = json.load(f)

databases = connection['databases']

"""
MYSQL Database
"""
mysql_info = databases['mysql']
mysql_url = f"mysql+mysqlconnector://{mysql_info['username']}:{mysql_info['password']}@{mysql_info['hostname']}:{mysql_info['port']}/{mysql_info['schema']}"
mysql_engine = create_engine(mysql_url)
mysql_connection = mysql_engine.connect()
