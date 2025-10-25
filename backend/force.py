import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import bcrypt

load_dotenv()

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def insert_sample_data():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'vitalink')
        )
        
        cursor = connection.cursor(dictionary=True)
        
        print("🗃️ Inserting sample data...")
        
        # Clear existing data (optional - remove this if you want to keep existing data)
        cursor.execute("DELETE FROM prescriptions")
        cursor.execute("DELETE FROM medical_records")
        cursor.execute("DELETE FROM appointments")
        cursor.execute("DELETE FROM messages")
        cursor.execute("DELETE FROM reviews")
        cursor.execute("DELETE FROM payments")
        cursor.execute("DELETE FROM patients")
        cursor.execute("DELETE FROM doctors")
        cursor.execute("DELETE FROM users")
        
        # Insert sample doctors
        doctor_password = hash_password('doctor123')
        
        # Doctor 1
        cursor.execute("""
            INSERT INTO users (email, password_hash, first_name, last_name, user_type, is_verified, phone, date_of_birth, gender) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, ('dr.smith@vitalink.com', doctor_password, 'Sarah', 'Smith', 'doctor', True, '+1234567890', '1980-05-15', 'Female'))
        doctor1_user_id = cursor.lastrowid
        
        cursor.execute("""
            INSERT INTO doctors (user_id, license_number, specialization, consultation_fee, available, years_of_experience, qualifications) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (doctor1_user_id, 'MED123456', 'Cardiology', 50.00, True, 10, 'MD, Board Certified Cardiologist'))
        
        # Doctor 2
        cursor.execute("""
            INSERT INTO users (email, password_hash, first_name, last_name, user_type, is_verified, phone, date_of_birth, gender) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, ('dr.john@vitalink.com', doctor_password, 'John', 'Davis', 'doctor', True, '+1234567891', '1978-08-22', 'Male'))
        doctor2_user_id = cursor.lastrowid
        
        cursor.execute("""
            INSERT INTO doctors (user_id, license_number, specialization, consultation_fee, available, years_of_experience, qualifications) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (doctor2_user_id, 'MED123457', 'Pediatrics', 45.00, True, 8, 'MD, Pediatric Specialist'))
        
        # Doctor 3
        cursor.execute("""
            INSERT INTO users (email, password_hash, first_name, last_name, user_type, is_verified, phone, date_of_birth, gender) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, ('dr.garcia@vitalink.com', doctor_password, 'Maria', 'Garcia', 'doctor', True, '+1234567893', '1982-03-10', 'Female'))
        doctor3_user_id = cursor.lastrowid
        
        cursor.execute("""
            INSERT INTO doctors (user_id, license_number, specialization, consultation_fee, available, years_of_experience, qualifications) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (doctor3_user_id, 'MED123458', 'Dermatology', 55.00, True, 7, 'MD, Dermatology Specialist'))
        
        # Insert sample patients
        patient_password = hash_password('patient123')
        
        # Patient 1
        cursor.execute("""
            INSERT INTO users (email, password_hash, first_name, last_name, user_type, is_verified, phone, date_of_birth, gender) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, ('alice.johnson@vitalink.com', patient_password, 'Alice', 'Johnson', 'patient', True, '+1234567892', '1990-12-05', 'Female'))
        patient1_user_id = cursor.lastrowid
        
        cursor.execute("""
            INSERT INTO patients (user_id, blood_type, height_cm, weight_kg, emergency_contact_name, emergency_contact_phone) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (patient1_user_id, 'O+', 165.0, 65.0, 'Bob Johnson', '+1234567894'))
        
        # Patient 2
        cursor.execute("""
            INSERT INTO users (email, password_hash, first_name, last_name, user_type, is_verified, phone, date_of_birth, gender) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, ('mike.wilson@vitalink.com', patient_password, 'Mike', 'Wilson', 'patient', True, '+1234567895', '1985-07-20', 'Male'))
        patient2_user_id = cursor.lastrowid
        
        cursor.execute("""
            INSERT INTO patients (user_id, blood_type, height_cm, weight_kg, emergency_contact_name, emergency_contact_phone) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (patient2_user_id, 'A+', 180.0, 80.0, 'Sarah Wilson', '+1234567896'))
        
        # Insert sample appointments
        cursor.execute("""
            INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status, appointment_type, symptoms) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (1, 1, '2024-01-20', '10:00:00', 'completed', 'video', 'Chest pain and shortness of breath'))
        
        cursor.execute("""
            INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status, appointment_type, symptoms) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (2, 2, '2024-01-21', '14:30:00', 'scheduled', 'video', 'Regular checkup'))
        
        connection.commit()
        
        print("✅ Sample data inserted successfully!")
        print("👨‍⚕️ Doctors created: 3")
        print("👤 Patients created: 2") 
        print("📅 Appointments created: 2")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    insert_sample_data()