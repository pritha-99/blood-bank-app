import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="pritha",   # replace with your actual password
        database="blood_bank"
        autocommit=True 
    )

