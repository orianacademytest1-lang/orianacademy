import sqlite3
import hashlib
import os
from pydantic import BaseModel
from typing import Optional
from fastapi import HTTPException, status

# Database setup
DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with users table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit() # Commit the table creation

    # Create admin user if doesn't exist
    try:
        admin_password = hash_password("Oriana@2026")
        cursor.execute('''
            INSERT INTO users (email, password, full_name, is_admin)
            VALUES (?, ?, ?, 1)
        ''', ("orianaservicces2026@gmail.com", admin_password, "Admin User"))
        conn.commit()
        print("Admin user created successfully")
    except sqlite3.IntegrityError:
        print("Admin user already exists")
    
    conn.close()

# Pydantic models
class UserSignup(BaseModel):
    email: str
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: str
    password: str

# Helper functions for password hashing
def hash_password(password: str) -> str:
    # In a real app, use a salt and a better algorithm like bcrypt
    # But to avoid dependencies, we'll use SHA-256 with a simple fixed salt
    salt = "oriana_academy_salt_2026"
    return hashlib.sha256((password + salt).encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

# Auth logic
def create_user(user: UserSignup):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_pwd = hash_password(user.password)
    try:
        cursor.execute(
            "INSERT INTO users (email, password, full_name) VALUES (?, ?, ?)",
            (user.email, hashed_pwd, user.full_name)
        )
        conn.commit()
        user_id = cursor.lastrowid
        return {"id": user_id, "email": user.email, "full_name": user.full_name}
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    finally:
        conn.close()

def authenticate_user(login_data: UserLogin):
    """Authenticate a user and return their details"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE email = ?', (login_data.email,))
    user = cursor.execute('SELECT * FROM users WHERE email = ?', (login_data.email,)).fetchone()
    conn.close()
    
    if user and verify_password(login_data.password, user['password']):
        return {
            "id": user['id'],
            "email": user['email'],
            "full_name": user['full_name'],
            "is_admin": bool(user['is_admin'])
        }
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password"
    )

def get_all_users():
    """Retrieve all registered users from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, email, full_name, is_admin, created_at 
        FROM users 
        ORDER BY created_at DESC
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

# Initialize DB on load
init_db()
