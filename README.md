# Senty - Secret Manager

Senty is a secure desktop application for managing your secrets (passwords, emails, usernames, notes, etc.). Built with Python and PyQt5, Senty stores your secrets in an encrypted SQLite database and uses your master password to decrypt data only in memory.

## Features

**Master Password Protection:**  
Set and verify a master password on first run. The master password hash and a salt are stored securely in `~/.senty/config.json`.

**Encrypted Storage:**  
All secret data is encrypted using the `cryptography` package before being stored in SQLite (`~/.senty/scm_data.sqlite`).

**Search Functionality:**  
Search through your decrypted secrets in memory by subject or tags.

**CRUD Operations:**  
Add, view (with copy buttons for each field), edit, and delete your secrets.

**Cross-Platform UI:**  
A modern, non-resizable PyQt5 interface that is centered on startup.

## Requirements

- Python 3.10+
- [PyQt5](https://pypi.org/project/PyQt5/)
- [cryptography](https://pypi.org/project/cryptography/)

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd senty
   ```

2. **Create and activate a virtual environment:**

	```bash
	python3 -m venv venv
	source venv/bin/activate   # On Windows, use: venv\Scripts\activate
	```

3. **Install dependencies:**

	```bash
	pip install -r requirements.txt
	```
## Project Structure

	senty/
	├── app/
	│   ├── __init__.py
	│   ├── config_manager.py         # Manages master password and config file in ~/.senty
	│   ├── database.py               # Handles SQLite operations and encryption/decryption
	│   ├── dialogs/
	│   │   ├── __init__.py
	│   │   ├── master_password_dialog.py  # Master password prompt
	│   │   ├── add_secret_dialog.py       # Add Secret modal dialog
	│   │   ├── view_secret_dialog.py      # View Secret modal dialog
	│   │   └── edit_secret_dialog.py      # Edit Secret modal dialog
	│   ├── utils/
	│   │   ├── __init__.py
	│   │   └── encryption.py         # Encryption utilities using cryptography package
	│   └── views/
	│       ├── __init__.py
	│       ├── main_window.py        # Main application window
	│       └── item_widget.py        # Custom widget for displaying secret items
	├── resources/                    # Icons, stylesheets, etc.
	│   └── icons/
	│       └── add.png               # Icon for Add button
	├── requirements.txt              # Python dependencies
	├── README.md                     # Project documentation
	└── main.py                       # Application entry point

## Usage

### Set/Enter Master Password
- **First Run:**  
  Senty will prompt you to set a master password.
- **Subsequent Launches:**  
  You will be required to enter your master password to decrypt your secrets.

### Manage Secrets
- **Add:**  
  Use the **Add** button (with icon) to create new secrets.
- **Search:**  
  Use the **Search** field to filter secrets by subject or tags.
- **List:**  
  Each secret is listed with options to **View**, **Edit**, or **Delete**.
- **View Dialog:**  
  In the View dialog, sensitive fields include a copy button. The "Last Updated" information is shown in italic at the bottom.

### Sync & About
- **Sync:**  
  The **Sync** button is a placeholder for future remote syncing features.
- **About:**  
  The **About** button displays application and author info.
- **Exit:**  
  The **Exit** button confirms before closing the app.


## Packaging

For production, you can package Senty into a single executable (e.g., using [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/)).  
**Note:** The SQLite database and configuration files will be stored in the `~/.senty` directory to ensure they remain writable and isolated.


## Security Considerations

### Encryption
Senty encrypts all secret data on disk using a key derived from your master password and a stored salt. Decryption occurs only in memory after successful authentication.

### Master Password Storage
The master password hash and salt are stored in `~/.senty/config.json`. It is recommended to use a strong, unique master password.


## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.


## License

This project is licensed under the **MIT License**.



