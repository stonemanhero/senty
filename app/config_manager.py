import os
import json
import hashlib
import base64

class ConfigManager:
    """
    Manages configuration including storing and verifying the master password.
    The configuration is saved in a JSON file in the ~/.senty folder.
    """
    def __init__(self):
        self.app_dir = os.path.join(os.path.expanduser("~"), ".senty")
        if not os.path.exists(self.app_dir):
            os.makedirs(self.app_dir)
        self.config_file = os.path.join(self.app_dir, "config.json")
        self.config = {}
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    self.config = json.load(f)
            except Exception as e:
                print("Error loading config:", e)
                self.config = {}
        else:
            self.config = {}

    def save_config(self):
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.config, f)
        except Exception as e:
            print("Error saving config:", e)

    def has_master_password(self):
        return "master_password_hash" in self.config

    def set_master_password(self, password):
        # Store a SHA-256 hash of the password (for demonstration purposes)
        hashed = hashlib.sha256(password.encode()).hexdigest()
        self.config["master_password_hash"] = hashed
        # Also generate and store a salt if not already present
        if "salt" not in self.config:
            salt = base64.urlsafe_b64encode(os.urandom(16)).decode()
            self.config["salt"] = salt
        self.save_config()

    def verify_master_password(self, password):
        if not self.has_master_password():
            return False
        hashed = hashlib.sha256(password.encode()).hexdigest()
        return hashed == self.config.get("master_password_hash")

    def get_salt(self):
        if "salt" not in self.config:
            salt = base64.urlsafe_b64encode(os.urandom(16)).decode()
            self.config["salt"] = salt
            self.save_config()
        return base64.urlsafe_b64decode(self.config["salt"])
