import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def debug_database():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'vitalink')
        )
        
        cursor = connection.cursor(dictionary=True)
        
        print("🔍 DEBUGGING DATABASE CONTENT:")
        print("=" * 50)
        
        # Check users table
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        print(f"📋 Users table: {len(users)} records")
        for user in users:
            print(f"   - ID: {user['id']}, Email: {user['email']}, Type: {user['user_type']}")
        
        # Check doctors table
        cursor.execute("SELECT * FROM doctors")
        doctors = cursor.fetchall()
        print(f"👨‍⚕️ Doctors table: {len(doctors)} records")
        for doctor in doctors:
            print(f"   - ID: {doctor['id']}, User ID: {doctor['user_id']}, Specialization: {doctor['specialization']}")
        
        # Check patients table
        cursor.execute("SELECT * FROM patients")
        patients = cursor.fetchall()
        print(f"👤 Patients table: {len(patients)} records")
        for patient in patients:
            print(f"   - ID: {patient['id']}, User ID: {patient['user_id']}")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_database()