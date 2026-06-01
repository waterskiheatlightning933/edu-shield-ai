"""
Database module for SQLite operations
Handles student record storage and retrieval
"""

import sqlite3
import pandas as pd
from datetime import datetime
import os

DB_PATH = "student_records.db"

def init_database():
    """Initialize SQLite database with student records table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            roll_number TEXT NOT NULL UNIQUE,
            gender TEXT,
            attendance_percent REAL,
            quiz_average REAL,
            assignment_average REAL,
            midterm_marks REAL,
            study_hours_per_day REAL,
            sleep_hours REAL,
            internet_usage_hours REAL,
            previous_gpa REAL,
            class_participation REAL,
            predicted_risk_level TEXT,
            risk_score REAL,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def save_student_record(student_data):
    """
    Save or update a student record in the database
    
    Args:
        student_data: Dictionary with student information
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if record exists
        cursor.execute("SELECT id FROM student_records WHERE roll_number = ?", 
                      (student_data['roll_number'],))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing record
            cursor.execute('''
                UPDATE student_records 
                SET student_name = ?, gender = ?, attendance_percent = ?,
                    quiz_average = ?, assignment_average = ?, midterm_marks = ?,
                    study_hours_per_day = ?, sleep_hours = ?, internet_usage_hours = ?,
                    previous_gpa = ?, class_participation = ?,
                    predicted_risk_level = ?, risk_score = ?, updated_date = CURRENT_TIMESTAMP
                WHERE roll_number = ?
            ''', (
                student_data['student_name'],
                student_data['gender'],
                student_data['attendance_percent'],
                student_data['quiz_average'],
                student_data['assignment_average'],
                student_data['midterm_marks'],
                student_data['study_hours_per_day'],
                student_data['sleep_hours'],
                student_data['internet_usage_hours'],
                student_data['previous_gpa'],
                student_data['class_participation'],
                student_data.get('predicted_risk_level', ''),
                student_data.get('risk_score', 0),
                student_data['roll_number']
            ))
        else:
            # Insert new record
            cursor.execute('''
                INSERT INTO student_records 
                (student_name, roll_number, gender, attendance_percent, quiz_average,
                 assignment_average, midterm_marks, study_hours_per_day, sleep_hours,
                 internet_usage_hours, previous_gpa, class_participation,
                 predicted_risk_level, risk_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                student_data['student_name'],
                student_data['roll_number'],
                student_data['gender'],
                student_data['attendance_percent'],
                student_data['quiz_average'],
                student_data['assignment_average'],
                student_data['midterm_marks'],
                student_data['study_hours_per_day'],
                student_data['sleep_hours'],
                student_data['internet_usage_hours'],
                student_data['previous_gpa'],
                student_data['class_participation'],
                student_data.get('predicted_risk_level', ''),
                student_data.get('risk_score', 0)
            ))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving record: {e}")
        return False

def get_all_records():
    """Retrieve all student records from database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM student_records ORDER BY created_date DESC", conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error retrieving records: {e}")
        return pd.DataFrame()

def get_student_record(roll_number):
    """Get a specific student record by roll number"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student_records WHERE roll_number = ?", (roll_number,))
        record = cursor.fetchone()
        conn.close()
        
        if record:
            columns = [description[0] for description in cursor.description]
            return dict(zip(columns, record))
        return None
    except Exception as e:
        print(f"Error retrieving record: {e}")
        return None

def delete_student_record(roll_number):
    """Delete a student record"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM student_records WHERE roll_number = ?", (roll_number,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting record: {e}")
        return False

def get_risk_distribution():
    """Get count of students by risk level"""
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(
            "SELECT predicted_risk_level, COUNT(*) as count FROM student_records GROUP BY predicted_risk_level",
            conn
        )
        conn.close()
        return df
    except Exception as e:
        print(f"Error getting risk distribution: {e}")
        return pd.DataFrame()

def get_high_risk_students():
    """Get all high risk students"""
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(
            "SELECT student_name, roll_number, risk_score FROM student_records WHERE predicted_risk_level = 'High Risk' ORDER BY risk_score DESC LIMIT 5",
            conn
        )
        conn.close()
        return df
    except Exception as e:
        print(f"Error getting high risk students: {e}")
        return pd.DataFrame()
