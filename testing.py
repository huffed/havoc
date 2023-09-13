import mysql.connector

# Replace these with your database credentials
host = "192.168.1.208"
user = "jack"
password = "Cr1m1n4ls"
database = "admin"

try:
    # Attempt to connect to the MySQL server
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    if connection.is_connected():
        print("Connected to MySQL database")
        connection.close()
    else:
        print("Connection failed")
except Exception as e:
    print(f"Error: {str(e)}")
