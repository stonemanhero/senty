import os
import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_filename="scm_data.sqlite"):
        # Define the folder and SQLite file path (e.g., ~/.senty/scm_data.sqlite)
        self.app_dir = os.path.join(os.path.expanduser("~"), ".senty")
        if not os.path.exists(self.app_dir):
            os.makedirs(self.app_dir)
        self.db_path = os.path.join(self.app_dir, db_filename)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS secrets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            email TEXT,
            username TEXT,
            password TEXT,
            notes TEXT,
            tags TEXT,
            updated_at TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_secret(self, subject, email, username, password, notes, tags):
        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = """
        INSERT INTO secrets (subject, email, username, password, notes, tags, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cur = self.conn.cursor()
        cur.execute(query, (subject, email, username, password, notes, tags, updated_at))
        self.conn.commit()
        return cur.lastrowid

    def get_all_secrets(self):
        query = "SELECT * FROM secrets ORDER BY updated_at DESC"
        cur = self.conn.execute(query)
        return cur.fetchall()

    def search_secrets(self, keyword):
        keyword = f'%{keyword}%'
        query = """
        SELECT * FROM secrets
        WHERE subject LIKE ? OR tags LIKE ?
        ORDER BY updated_at DESC
        """
        cur = self.conn.execute(query, (keyword, keyword))
        return cur.fetchall()

    def get_secret_by_id(self, secret_id):
        query = "SELECT * FROM secrets WHERE id = ?"
        cur = self.conn.execute(query, (secret_id,))
        return cur.fetchone()

    def update_secret(self, secret_id, subject, email, username, password, notes, tags):
        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = """
        UPDATE secrets
        SET subject = ?, email = ?, username = ?, password = ?, notes = ?, tags = ?, updated_at = ?
        WHERE id = ?
        """
        self.conn.execute(query, (subject, email, username, password, notes, tags, updated_at, secret_id))
        self.conn.commit()

    def delete_secret(self, secret_id):
        query = "DELETE FROM secrets WHERE id = ?"
        self.conn.execute(query, (secret_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
