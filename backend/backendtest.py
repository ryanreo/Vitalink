import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'vitalink')
        )
        
        if connection.is_connected():
            print("✅ Successfully connected to MySQL database!")
            
            # Test query
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()
            print(f"✅ Connected to database: {db_name[0]}")
            
            # Check if tables exist
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print("✅ Tables in database:")
            for table in tables:
                print(f"   - {table[0]}")
            
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure MySQL is running")
        print("2. Check your .env file credentials")
        print("3. Verify the database exists")
        print("4. Check if MySQL service is started")

if __name__ == "__main__":
    test_connection()