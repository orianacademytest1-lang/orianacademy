import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional

# Database setup
DB_PATH = os.path.join(os.path.dirname(__file__), "oriana_data.db")

def get_db_connection():
    """Get a database connection with row factory"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_data_db():
    """Initialize database tables for contact submissions and enrollments"""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=20.0) # Higher timeout for concurrent init
        cursor = conn.cursor()
        
        # Contact submissions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contact_submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                subject TEXT,
                message TEXT NOT NULL,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Enrollments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS enrollments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                course TEXT NOT NULL,
                message TEXT,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Settings table for SMTP configuration
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE,
                value TEXT NOT NULL
            )
        ''')

        # Workshops table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workshops (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                location TEXT NOT NULL,
                status TEXT DEFAULT 'Upcoming',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Workshop registrations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workshop_registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workshop_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                status TEXT NOT NULL, -- Career Break, Working, Student
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (workshop_id) REFERENCES workshops (id)
            )
        ''')

        # Seed initial workshop if not exists
        cursor.execute("SELECT COUNT(*) FROM workshops WHERE title = ?", ("Women's Day Special Workshop",))
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO workshops (title, date, time, location)
                VALUES (?, ?, ?, ?)
            ''', ("Women's Day Special Workshop", "March 8, 2026", "10:30 AM – 1:30 PM (IST)", "Oriana Academy / Online"))
        
        conn.commit()
        conn.close()
        print("✅ Data tables initialized successfully")
    except sqlite3.OperationalError as e:
        if "locked" in str(e).lower():
            print("ℹ️ Database locked during initialization, skipping as it's likely being handled by another worker.")
        else:
            print(f"❌ Database initialization error: {e}")
    except Exception as e:
        print(f"❌ Unexpected database error: {e}")

# Contact submission functions
def save_contact_submission(name: str, email: str, phone: str, subject: str, message: str) -> int:
    """Save a contact form submission"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO contact_submissions (name, email, phone, subject, message)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, email, phone, subject, message))
    
    conn.commit()
    submission_id = cursor.lastrowid
    conn.close()
    
    return submission_id

def get_all_contact_submissions() -> List[Dict]:
    """Get all contact submissions"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM contact_submissions 
        ORDER BY submitted_at DESC
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def delete_contact_submission(submission_id: int) -> bool:
    """Delete a contact submission"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contact_submissions WHERE id = ?', (submission_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

def update_contact_submission(submission_id: int, name: str, email: str, phone: str, subject: str, message: str) -> bool:
    """Update a contact submission"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE contact_submissions 
        SET name = ?, email = ?, phone = ?, subject = ?, message = ?
        WHERE id = ?
    ''', (name, email, phone, subject, message, submission_id))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated


# Enrollment functions
def save_enrollment(name: str, email: str, phone: str, course: str, message: str = None) -> int:
    """Save an enrollment submission"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO enrollments (name, email, phone, course, message)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, email, phone, course, message))
    
    conn.commit()
    enrollment_id = cursor.lastrowid
    conn.close()
    
    return enrollment_id

def get_all_enrollments() -> List[Dict]:
    """Get all enrollments"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM enrollments 
        ORDER BY submitted_at DESC
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def delete_enrollment(enrollment_id: int) -> bool:
    """Delete an enrollment"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM enrollments WHERE id = ?', (enrollment_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

def update_enrollment(enrollment_id: int, name: str, email: str, phone: str, course: str, message: str) -> bool:
    """Update an enrollment"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE enrollments 
        SET name = ?, email = ?, phone = ?, course = ?, message = ?
        WHERE id = ?
    ''', (name, email, phone, course, message, enrollment_id))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated


# Get statistics
def get_stats() -> Dict:
    """Get dashboard statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as count FROM contact_submissions')
    total_contacts = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM enrollments')
    total_enrollments = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM workshop_registrations')
    total_workshop_registrations = cursor.fetchone()['count']
    
    conn.close()
    
    return {
        "total_contacts": total_contacts,
        "total_enrollments": total_enrollments,
        "total_workshop_registrations": total_workshop_registrations
    }

# Workshop functions
def save_workshop_registration(workshop_id: int, name: str, email: str, phone: str, status: str) -> int:
    """Save a workshop registration"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO workshop_registrations (workshop_id, name, email, phone, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (workshop_id, name, email, phone, status))
    
    conn.commit()
    registration_id = cursor.lastrowid
    conn.close()
    
    return registration_id

def get_all_workshop_registrations() -> List[Dict]:
    """Get all workshop registrations with workshop titles"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT wr.*, w.title as workshop_title, w.date as workshop_date 
        FROM workshop_registrations wr
        JOIN workshops w ON wr.workshop_id = w.id
        ORDER BY wr.registered_at DESC
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def get_all_workshops() -> List[Dict]:
    """Get all workshops"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM workshops ORDER BY created_at DESC')
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def delete_workshop_registration(reg_id: int) -> bool:
    """Delete a workshop registration"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM workshop_registrations WHERE id = ?', (reg_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

def get_workshop_stats() -> Dict:
    """Get workshop statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as count FROM workshops')
    total_workshops = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM workshop_registrations')
    total_registrations = cursor.fetchone()['count']
    
    conn.close()
    
    return {
        "total_workshops": total_workshops,
        "total_registrations": total_registrations
    }

# Settings functions
def save_smtp_settings(email: str, password: str, receiver: str, **kwargs):
    """Save SMTP settings to the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    settings = [
        ('smtp_email', email),
        ('smtp_password', password),
        ('receiver_email', receiver),
        ('resend_api_key', kwargs.get('resend_api_key', ''))
    ]
    
    for key, value in settings:
        cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value)
            VALUES (?, ?)
        ''', (key, value))
    
    conn.commit()
    conn.close()

def get_smtp_settings() -> Dict:
    """Retrieve SMTP settings from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM settings')
    rows = cursor.fetchall()
    conn.close()
    
    settings = {row['key']: row['value'] for row in rows}
    # Return defaults if not set
    return {
        "smtp_email": settings.get('smtp_email', ''),
        "smtp_password": settings.get('smtp_password', ''),
        "receiver_email": settings.get('receiver_email', ''),
        "resend_api_key": settings.get('resend_api_key', '')
    }
