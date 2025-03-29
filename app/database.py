import os
import sqlite3
from datetime import datetime
from app.utils.encryption import encrypt_text, decrypt_text

class DatabaseManager:
    def __init__(self, encryption_key, db_filename="scm_data.sqlite"):
        self.encryption_key = encryption_key
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
        # Encrypt fields before storing
        enc_subject = encrypt_text(subject, self.encryption_key)
        enc_email = encrypt_text(email, self.encryption_key)
        enc_username = encrypt_text(username, self.encryption_key)
        enc_password = encrypt_text(password, self.encryption_key)
        enc_notes = encrypt_text(notes, self.encryption_key)
        enc_tags = encrypt_text(tags, self.encryption_key)
        query = """
        INSERT INTO secrets (subject, email, username, password, notes, tags, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cur = self.conn.cursor()
        cur.execute(query, (enc_subject, enc_email, enc_username, enc_password, enc_notes, enc_tags, updated_at))
        self.conn.commit()
        return cur.lastrowid

    def get_all_secrets(self):
        query = "SELECT * FROM secrets ORDER BY updated_at DESC"
        cur = self.conn.execute(query)
        rows = cur.fetchall()
        decrypted_rows = []
        for row in rows:
            decrypted_row = {
                "id": row["id"],
                "subject": decrypt_text(row["subject"], self.encryption_key),
                "email": decrypt_text(row["email"], self.encryption_key),
                "username": decrypt_text(row["username"], self.encryption_key),
                "password": decrypt_text(row["password"], self.encryption_key),
                "notes": decrypt_text(row["notes"], self.encryption_key),
                "tags": decrypt_text(row["tags"], self.encryption_key),
                "updated_at": row["updated_at"]
            }
            decrypted_rows.append(decrypted_row)
        return decrypted_rows

    def get_secret_by_id(self, secret_id):
        query = "SELECT * FROM secrets WHERE id = ?"
        cur = self.conn.execute(query, (secret_id,))
        row = cur.fetchone()
        if row:
            return {
                "id": row["id"],
                "subject": decrypt_text(row["subject"], self.encryption_key),
                "email": decrypt_text(row["email"], self.encryption_key),
                "username": decrypt_text(row["username"], self.encryption_key),
                "password": decrypt_text(row["password"], self.encryption_key),
                "notes": decrypt_text(row["notes"], self.encryption_key),
                "tags": decrypt_text(row["tags"], self.encryption_key),
                "updated_at": row["updated_at"]
            }
        return None

    def update_secret(self, secret_id, subject, email, username, password, notes, tags):
        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        enc_subject = encrypt_text(subject, self.encryption_key)
        enc_email = encrypt_text(email, self.encryption_key)
        enc_username = encrypt_text(username, self.encryption_key)
        enc_password = encrypt_text(password, self.encryption_key)
        enc_notes = encrypt_text(notes, self.encryption_key)
        enc_tags = encrypt_text(tags, self.encryption_key)
        query = """
        UPDATE secrets
        SET subject = ?, email = ?, username = ?, password = ?, notes = ?, tags = ?, updated_at = ?
        WHERE id = ?
        """
        self.conn.execute(query, (enc_subject, enc_email, enc_username, enc_password, enc_notes, enc_tags, updated_at, secret_id))
        self.conn.commit()

    def delete_secret(self, secret_id):
        query = "DELETE FROM secrets WHERE id = ?"
        self.conn.execute(query, (secret_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
