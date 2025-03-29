from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class MasterPasswordDialog(QDialog):
    """
    A dialog to either set or verify the master password.
    If setting, the user must enter and confirm the new password.
    If verifying, the user simply enters the master password.
    """
    def __init__(self, config_manager, is_setting=False, parent=None):
        super(MasterPasswordDialog, self).__init__(parent)
        self.config_manager = config_manager
        self.is_setting = is_setting
        self.setWindowTitle("Set Master Password" if is_setting else "Enter Master Password")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Instruction label
        label_text = "Set a new master password:" if self.is_setting else "Enter your master password:"
        self.label = QLabel(label_text)
        layout.addWidget(self.label)

        # Password entry field
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_edit)

        # Confirm field if setting a new password
        if self.is_setting:
            self.confirm_label = QLabel("Confirm master password:")
            layout.addWidget(self.confirm_label)
            self.confirm_edit = QLineEdit()
            self.confirm_edit.setEchoMode(QLineEdit.Password)
            layout.addWidget(self.confirm_edit)

        # Submit button
        self.button = QPushButton("Submit")
        self.button.clicked.connect(self.on_submit)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def on_submit(self):
        password = self.password_edit.text().strip()
        if not password:
            QMessageBox.warning(self, "Input Error", "Password cannot be empty.")
            return

        if self.is_setting:
            confirm = self.confirm_edit.text().strip()
            if password != confirm:
                QMessageBox.warning(self, "Input Error", "Passwords do not match.")
                return
            self.config_manager.set_master_password(password)
            self.accept()
        else:
            if self.config_manager.verify_master_password(password):
                self.accept()
            else:
                QMessageBox.warning(self, "Authentication Failed", "Incorrect master password.")
                self.password_edit.clear()
