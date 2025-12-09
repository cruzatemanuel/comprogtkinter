import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'faretracker_db'
}

def get_connection():
    """Create and return MySQL database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        print(f"Please ensure MySQL is running and database '{DB_CONFIG['database']}' exists")
        return None
    except Exception as e:
        print(f"Unexpected error connecting to database: {e}")
        return None

def initialize_database():
    """Database and tables must be created manually"""
    # No automatic creation - users must create database and tables manually
    pass

# CRUD Operations for Users

def create_user(srcode, name, password, college):
    """Insert a new user into the database"""
    connection = get_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO users (srcode, name, password, college)
            VALUES (%s, %s, %s, %s)
        """, (srcode, name, password, college))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"Error creating user: {e}")
        if connection:
            connection.close()
        return False

def get_user(srcode):
    """Get user by SRCODE"""
    connection = get_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE srcode = %s", (srcode,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        return user
    except Error as e:
        print(f"Error getting user: {e}")
        if connection:
            connection.close()
        return None

def update_college(srcode, new_college):
    """Update user's college"""
    connection = get_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE users SET college = %s WHERE srcode = %s
        """, (new_college, srcode))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"Error updating college: {e}")
        if connection:
            connection.close()
        return False

# CRUD Operations for Fare History

def save_fare_record(srcode, district, start_location, destination, include_trike, total_fare):
    """Save a fare calculation record"""
    connection = get_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO fare_history (srcode, district, start_location, destination, include_trike, total_fare)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (srcode, district, start_location, destination, include_trike, total_fare))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"Error saving fare record: {e}")
        if connection:
            connection.close()
        return False

def get_user_fares(srcode):
    """Get all fare records for a user"""
    connection = get_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM fare_history 
            WHERE srcode = %s 
            ORDER BY created_date DESC
        """, (srcode,))
        fares = cursor.fetchall()
        cursor.close()
        connection.close()
        return fares
    except Error as e:
        print(f"Error getting user fares: {e}")
        if connection:
            connection.close()
        return []

def delete_fare_record(record_id):
    """Delete a fare record by ID"""
    connection = get_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM fare_history WHERE id = %s", (record_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"Error deleting fare record: {e}")
        if connection:
            connection.close()
        return False

def get_weekly_average(srcode):
    """Calculate average fare for the last 7 days"""
    connection = get_connection()
    if not connection:
        return 0.0
    
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT AVG(total_fare) as avg_fare
            FROM fare_history
            WHERE srcode = %s AND created_date >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        """, (srcode,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return float(result[0]) if result[0] else 0.0
    except Error as e:
        print(f"Error calculating weekly average: {e}")
        if connection:
            connection.close()
        return 0.0

