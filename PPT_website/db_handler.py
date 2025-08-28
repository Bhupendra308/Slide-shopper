import mysql.connector
from datetime import datetime

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Password',
    'database': 'ppt_store'
}

def get_connection():
    """Establish a database connection."""
    return mysql.connector.connect(**db_config)

def store_booking(name, email, ppt_id):
    """Store booking information in the database with timestamp."""
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO bookings (name, email, ppt_id, created_at) VALUES (%s, %s, %s, %s)"
    created_at = datetime.now()  # Get the current timestamp
    cursor.execute(query, (name, email, ppt_id, created_at))
    conn.commit()
    cursor.close()
    conn.close()

def store_contact(name, email, message):
    """Store contact information in the database with timestamp."""
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO contact (name, email, message, created_at) VALUES (%s, %s, %s, %s)"
    created_at = datetime.now()  # Get the current timestamp
    cursor.execute(query, (name, email, message, created_at))
    conn.commit()
    cursor.close()
    conn.close()

