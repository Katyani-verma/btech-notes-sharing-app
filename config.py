import mysql.connector

def get_db_connection():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="krajput@2005",  # Apna MySQL root password daalein
        database="online_notes_db"
    )
    return db