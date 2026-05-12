import sqlite3
from database import get_connection
from faker import Faker
import random

fake = Faker()

def add_contact(contact_data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO contacts (name, phone, email, address, notes, follow_up_date, category, health_score, is_favorite, profile_image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        contact_data.get('name'),
        contact_data.get('phone'),
        contact_data.get('email'),
        contact_data.get('address'),
        contact_data.get('notes'),
        contact_data.get('follow_up_date'),
        contact_data.get('category'),
        contact_data.get('health_score', 50),
        contact_data.get('is_favorite', False),
        contact_data.get('profile_image')
    ))
    conn.commit()
    conn.close()

def get_all_contacts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts ORDER BY name ASC')
    contacts = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return contacts

def get_contact_by_id(contact_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def update_contact(contact_id, contact_data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE contacts
        SET name = ?, phone = ?, email = ?, address = ?, notes = ?, 
            follow_up_date = ?, category = ?, health_score = ?, 
            is_favorite = ?, profile_image = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (
        contact_data.get('name'),
        contact_data.get('phone'),
        contact_data.get('email'),
        contact_data.get('address'),
        contact_data.get('notes'),
        contact_data.get('follow_up_date'),
        contact_data.get('category'),
        contact_data.get('health_score'),
        contact_data.get('is_favorite'),
        contact_data.get('profile_image'),
        contact_id
    ))
    conn.commit()
    conn.close()

def delete_contact(contact_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
    conn.commit()
    conn.close()

def search_contacts(query):
    conn = get_connection()
    cursor = conn.cursor()
    search_query = f"%{query}%"
    cursor.execute('''
        SELECT * FROM contacts 
        WHERE name LIKE ? OR phone LIKE ? 
        ORDER BY name ASC
    ''', (search_query, search_query))
    contacts = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return contacts

def toggle_favorite(contact_id, is_favorite):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE contacts SET is_favorite = ? WHERE id = ?', (not is_favorite, contact_id))
    conn.commit()
    conn.close()

def generate_sample_contacts(count=10):
    categories = ['Work', 'Family', 'Friends', 'Networking', 'Other']
    for _ in range(count):
        contact_data = {
            'name': fake.name(),
            'phone': fake.phone_number(),
            'email': fake.email(),
            'address': fake.address().replace('\n', ', '),
            'notes': fake.sentence(),
            'follow_up_date': fake.date_between(start_date='today', end_date='+30d').isoformat(),
            'category': random.choice(categories),
            'health_score': random.randint(10, 100),
            'is_favorite': random.choice([True, False, False, False]), # 25% chance of being favorite
            'profile_image': None
        }
        add_contact(contact_data)
