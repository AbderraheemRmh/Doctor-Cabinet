# Configurer la connexion à la base de données 
import mysql.connector
import pandas as pd
import bcrypt

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="cabinet"
    )

# dataframe
def query_to_dataframe(query):
    conn = get_db_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Fonctions CRUD pour les patients avec Pandas
# Créer un patient :
def create_patient(name, age, gender, phone=None, email=None, medical_history=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO patients (name, age, gender, phone, email, medical_history)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (name, age, gender, phone, email, medical_history))
    conn.commit()
    cursor.close()
    conn.close()

# Lire les informations des patients :
def read_patients():
    query = "SELECT * FROM patients"
    return query_to_dataframe(query)

def read_patient_id(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM patients WHERE name = %s"
    cursor.execute(query, (name,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

# Mettre à jour un patient :
def update_patient(patient_id, name=None, age=None, gender=None, phone=None, email=None, medical_history=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    fields = []
    values = []
    if name:
        fields.append("name = %s")
        values.append(name)
    if age:
        fields.append("age = %s")
        values.append(age)
    if gender:
        fields.append("gender = %s")
        values.append(gender)
    if phone:
        fields.append("phone = %s")
        values.append(phone)
    if email:
        fields.append("email = %s")
        values.append(email)
    if medical_history:
        fields.append("medical_history = %s")
        values.append(medical_history)
    values.append(patient_id)
    query = f"UPDATE patients SET {', '.join(fields)} WHERE id = %s"
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

# Supprimer un patient 
def delete_patient(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM patients WHERE id = %s"
    cursor.execute(query, (patient_id,))
    conn.commit()
    cursor.close()
    conn.close()

# Fonctions CRUD pour les medecins avec Pandas
# Créer un médecin


def hash_password(password):
    password = str(password)  # Convertir en string si ce n'est pas déjà le cas
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_doctor(username, password, name, specialization=None, phone=None, email=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Hacher le mot de passe avant de l'enregistrer
    password_hash = hash_password(password)

    query = """
    INSERT INTO doctors (username, password_hash, name, specialization, phone, email)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (username, password_hash, name, specialization, phone, email))
    conn.commit()
    cursor.close()
    conn.close()

# Lire les informations des médecins
def read_doctors():
    query = "SELECT id, username, name, specialization, phone, email FROM doctors"
    return query_to_dataframe(query)

def read_doctor_id(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM doctors WHERE name = %s"
    cursor.execute(query, (name,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

# Mettre à jour un médecin
def update_doctor(doctor_id, username=None, password_hash=None, name=None, specialization=None, phone=None, email=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    fields = []
    values = []
    if username:
        fields.append("username = %s")
        values.append(username)
    if password_hash:
        fields.append("password_hash = %s")
        values.append(password_hash)
    if name:
        fields.append("name = %s")
        values.append(name)
    if specialization:
        fields.append("specialization = %s")
        values.append(specialization)
    if phone:
        fields.append("phone = %s")
        values.append(phone)
    if email:
        fields.append("email = %s")
        values.append(email)
    values.append(doctor_id)
    query = f"UPDATE doctors SET {', '.join(fields)} WHERE id = %s"
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

# Supprimer un médecin
def delete_doctor(doctor_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM doctors WHERE id = %s"
    cursor.execute(query, (doctor_id,))
    conn.commit()
    cursor.close()
    conn.close()

# # Fonctions CRUD pour les infirmières avec Pandas
# Créer une infirmière
def create_nurse(username, password, name, phone=None, email=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Hacher le mot de passe avant de l'insérer
    password_hash = hash_password(password)

    query = """
    INSERT INTO nurses (username, password_hash, name, phone, email)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (username, password_hash, name, phone, email))
    conn.commit()
    cursor.close()
    conn.close()


# Lire les informations des infirmières
def read_nurses():
    query = "SELECT id, username, name, phone, email FROM nurses"
    return query_to_dataframe(query)

def read_nurse_id(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM nurses WHERE name = %s"
    cursor.execute(query, (name,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

# Mettre à jour une infirmière
def update_nurse(nurse_id, username=None, password_hash=None, name=None, phone=None, email=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    fields = []
    values = []
    if username:
        fields.append("username = %s")
        values.append(username)
    if password_hash:
        fields.append("password_hash = %s")
        values.append(password_hash)
    if name:
        fields.append("name = %s")
        values.append(name)
    if phone:
        fields.append("phone = %s")
        values.append(phone)
    if email:
        fields.append("email = %s")
        values.append(email)
    values.append(nurse_id)
    query = f"UPDATE nurses SET {', '.join(fields)} WHERE id = %s"
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

# Supprimer une infirmière
def delete_nurse(nurse_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM nurses WHERE id = %s"
    cursor.execute(query, (nurse_id,))
    conn.commit()
    cursor.close()
    conn.close()

# Fonctions CRUD pour les rendez-vous avec Pandas
# Créer un rendez-vous
def create_appointment(patient_id, nurse_id=None, doctor_id=None, appointment_date=None, appointment_time=None, status='pending'):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO appointments (patient_id, nurse_id, doctor_id, appointment_date, appointment_time, status)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (patient_id, nurse_id, doctor_id, appointment_date, appointment_time, status))
    conn.commit()
    cursor.close()
    conn.close()

# Lire les informations des rendez-vous
def read_appointments():
    query = """
    SELECT 
        a.id,
        p.name AS patient_name,
        d.name AS doctor_name,
        n.name AS nurse_name,
        a.appointment_date,
        a.appointment_time, 
        a.status
    FROM appointments a
    JOIN patients p ON a.patient_id = p.id
    JOIN doctors d ON a.doctor_id = d.id
    JOIN nurses n ON a.nurse_id = n.id 
    ORDER BY a.appointment_date, a.appointment_time;
    """
    return query_to_dataframe(query)

def patient_by_doctor():
    query = """
    SELECT d.name AS doctor_name, COUNT(a.patient_id) AS patient_count
    FROM appointments a
    JOIN doctors d ON a.doctor_id = d.id
    GROUP BY d.name;
    """
    return query_to_dataframe(query)

# Mettre à jour un rendez-vous
def update_appointment(appointment_id, patient_id=None, nurse_id=None, doctor_id=None, appointment_date=None, appointment_time=None, status=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    fields = []
    values = []
    if patient_id:
        fields.append("patient_id = %s")
        values.append(patient_id)
    if nurse_id:
        fields.append("nurse_id = %s")
        values.append(nurse_id)
    if doctor_id:
        fields.append("doctor_id = %s")
        values.append(doctor_id)
    if appointment_date:
        fields.append("appointment_date = %s")
        values.append(appointment_date)
    if appointment_time:
        fields.append("appointment_time = %s")
        values.append(appointment_time)
    if status:
        fields.append("status = %s")
        values.append(status)
    values.append(appointment_id)
    query = f"UPDATE appointments SET {', '.join(fields)} WHERE id = %s"
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

# Supprimer un rendez-vous
def delete_appointment(appointment_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM appointments WHERE id = %s"
    cursor.execute(query, (appointment_id,))
    conn.commit()
    cursor.close()
    conn.close()

def update_appointment_status (appointment_id, new_status):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE appointments SET status = %s WHERE id = %s"
    
    try:
        cursor.execute(query, (new_status, appointment_id))
        conn.commit()
    except Exception as e:
        print(f"Error updating status: {e}")
    finally:
        cursor.close()
        conn.close()







# Stocke hashed_password.decode('utf-8') dans la base de données

# fonction pour verifier le nom d'utilisateur de medecin et l'infermier

def verify_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Vérifier si l'utilisateur est un médecin
    cursor.execute("SELECT password_hash FROM doctors WHERE username = %s", (username,))
    doctor = cursor.fetchone()

    if doctor:
        stored_hash = doctor["password_hash"]
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode('utf-8')  # S'assurer que c'est bien en bytes
        
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            return "Doctor"
        else:
            return "Mot de passe incorrect pour le médecin"

    # Vérifier si l'utilisateur est une infirmière
    cursor.execute("SELECT password_hash FROM nurses WHERE username = %s", (username,))
    nurse = cursor.fetchone()

    if nurse:
        stored_hash = nurse["password_hash"]
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode('utf-8')  # S'assurer que c'est bien en bytes
        
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            return "Nurse"
        else:
            return "Mot de passe incorrect pour l'infirmière"

    return "Utilisateur inexistant"


