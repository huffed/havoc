import json

with open('config/config.json') as f:
    connection = json.load(f)

databases = connection['databases']

"""
MYSQL Database
"""
mysql_info = databases['mysql']
mysql_uri = f"mysql+mysqlconnector://{mysql_info['username']}:{mysql_info['password']}@{mysql_info['hostname']}:{mysql_info['port']}/{mysql_info['schema']}"
