from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import bcrypt
import jwt

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'vitalink-secret-key-2024')

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'vitalink')
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Helper function to hash passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Helper function to verify passwords
def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# JWT token generation
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

# Authentication middleware
def token_required(f):
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
        except:
            return jsonify({'error': 'Token is invalid'}), 401
        
        return f(current_user_id, *args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

@app.route('/')
def home():
    return jsonify({
        "message": "Vitalink API is running",
        "status": "success",
        "version": "1.0.0"
    })

@app.route('/api/health')
def health_check():
    conn = get_db_connection()
    if conn:
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"})
    else:
        return jsonify({"status": "unhealthy", "database": "disconnected"}), 500

# Authentication routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        user_type = data.get('user_type', 'patient')
        
        if not all([email, password, first_name, last_name]):
            return jsonify({'error': 'All fields are required'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
            
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({'error': 'User already exists'}), 400
        
        # Create user
        hashed_password = hash_password(password)
        cursor.execute(
            "INSERT INTO users (email, password_hash, first_name, last_name, user_type) VALUES (%s, %s, %s, %s, %s)",
            (email, hashed_password, first_name, last_name, user_type)
        )
        user_id = cursor.lastrowid
        
        # Create patient or doctor record
        if user_type == 'patient':
            cursor.execute(
                "INSERT INTO patients (user_id) VALUES (%s)",
                (user_id,)
            )
        elif user_type == 'doctor':
            license_number = data.get('license_number')
            specialization = data.get('specialization')
            if not license_number or not specialization:
                return jsonify({'error': 'License number and specialization are required for doctors'}), 400
            cursor.execute(
                "INSERT INTO doctors (user_id, license_number, specialization) VALUES (%s, %s, %s)",
                (user_id, license_number, specialization)
            )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        token = generate_token(user_id)
        return jsonify({
            'message': 'User created successfully',
            'token': token,
            'user_id': user_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
            
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT u.*, 
                   p.id as patient_id, 
                   d.id as doctor_id, 
                   d.specialization,
                   d.available
            FROM users u 
            LEFT JOIN patients p ON u.id = p.user_id 
            LEFT JOIN doctors d ON u.id = d.user_id 
            WHERE u.email = %s
        """, (email,))
        
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not user or not verify_password(password, user['password_hash']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        token = generate_token(user['id'])
        
        user_data = {
            'id': user['id'],
            'email': user['email'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'user_type': user['user_type'],
            'is_verified': user['is_verified']
        }
        
        if user['user_type'] == 'patient':
            user_data['patient_id'] = user['patient_id']
        elif user['user_type'] == 'doctor':
            user_data['doctor_id'] = user['doctor_id']
            user_data['specialization'] = user['specialization']
            user_data['available'] = user['available']
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': user_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Doctors routes
@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    try:
        specialization = request.args.get('specialization')
        available = request.args.get('available')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT u.id, u.first_name, u.last_name, u.profile_picture_url,
                   d.specialization, d.years_of_experience, d.consultation_fee,
                   d.available, d.is_online, d.avg_rating, d.total_reviews
            FROM users u
            JOIN doctors d ON u.id = d.user_id
            WHERE u.user_type = 'doctor'
        """
        
        params = []
        if specialization:
            query += " AND d.specialization = %s"
            params.append(specialization)
        if available:
            query += " AND d.available = %s"
            params.append(available == 'true')
        
        cursor.execute(query, params)
        doctors = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(doctors)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT u.*, d.*
            FROM users u
            JOIN doctors d ON u.id = d.user_id
            WHERE d.id = %s
        """, (doctor_id,))
        
        doctor = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not doctor:
            return jsonify({'error': 'Doctor not found'}), 404
        
        return jsonify(doctor)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Appointments routes
@app.route('/api/appointments', methods=['POST'])
@token_required
def create_appointment(current_user_id):
    try:
        data = request.get_json()
        doctor_id = data.get('doctor_id')
        appointment_date = data.get('appointment_date')
        appointment_time = data.get('appointment_time')
        appointment_type = data.get('appointment_type', 'video')
        symptoms = data.get('symptoms', '')
        
        if not all([doctor_id, appointment_date, appointment_time]):
            return jsonify({'error': 'Doctor ID, date, and time are required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get patient ID
        cursor.execute("SELECT id FROM patients WHERE user_id = %s", (current_user_id,))
        patient = cursor.fetchone()
        if not patient:
            return jsonify({'error': 'Patient profile not found'}), 404
        
        # Create appointment
        cursor.execute("""
            INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, appointment_type, symptoms)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (patient['id'], doctor_id, appointment_date, appointment_time, appointment_type, symptoms))
        
        appointment_id = cursor.lastrowid
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'message': 'Appointment created successfully',
            'appointment_id': appointment_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/appointments', methods=['GET'])
@token_required
def get_user_appointments(current_user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if user is patient or doctor
        cursor.execute("SELECT user_type FROM users WHERE id = %s", (current_user_id,))
        user = cursor.fetchone()
        
        if user['user_type'] == 'patient':
            cursor.execute("SELECT id FROM patients WHERE user_id = %s", (current_user_id,))
            patient = cursor.fetchone()
            if not patient:
                return jsonify({'error': 'Patient profile not found'}), 404
            
            cursor.execute("""
                SELECT a.*, 
                       u.first_name as doctor_first_name, u.last_name as doctor_last_name,
                       d.specialization
                FROM appointments a
                JOIN doctors d ON a.doctor_id = d.id
                JOIN users u ON d.user_id = u.id
                WHERE a.patient_id = %s
                ORDER BY a.appointment_date DESC, a.appointment_time DESC
            """, (patient['id'],))
            
        else:  # doctor
            cursor.execute("SELECT id FROM doctors WHERE user_id = %s", (current_user_id,))
            doctor = cursor.fetchone()
            if not doctor:
                return jsonify({'error': 'Doctor profile not found'}), 404
            
            cursor.execute("""
                SELECT a.*, 
                       u.first_name as patient_first_name, u.last_name as patient_last_name
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
                JOIN users u ON p.user_id = u.id
                WHERE a.doctor_id = %s
                ORDER BY a.appointment_date DESC, a.appointment_time DESC
            """, (doctor['id'],))
        
        appointments = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify(appointments)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Messages routes
@app.route('/api/messages', methods=['POST'])
@token_required
def send_message(current_user_id):
    try:
        data = request.get_json()
        receiver_id = data.get('receiver_id')
        message_text = data.get('message_text')
        appointment_id = data.get('appointment_id')
        
        if not receiver_id or not message_text:
            return jsonify({'error': 'Receiver ID and message text are required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO messages (sender_id, receiver_id, appointment_id, message_text)
            VALUES (%s, %s, %s, %s)
        """, (current_user_id, receiver_id, appointment_id, message_text))
        
        conn.commit()
        message_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'message': 'Message sent successfully',
            'message_id': message_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/messages/<int:receiver_id>', methods=['GET'])
@token_required
def get_messages(current_user_id, receiver_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT m.*, 
                   u1.first_name as sender_first_name, u1.last_name as sender_last_name,
                   u2.first_name as receiver_first_name, u2.last_name as receiver_last_name
            FROM messages m
            JOIN users u1 ON m.sender_id = u1.id
            JOIN users u2 ON m.receiver_id = u2.id
            WHERE (m.sender_id = %s AND m.receiver_id = %s) 
               OR (m.sender_id = %s AND m.receiver_id = %s)
            ORDER BY m.created_at ASC
        """, (current_user_id, receiver_id, receiver_id, current_user_id))
        
        messages = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify(messages)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)