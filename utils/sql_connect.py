import json

with open('config/config.json') as f:
    connection = json.load(f)

databases = connection['databases']

mysql = databases['mysql']