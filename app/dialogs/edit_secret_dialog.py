from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QPushButton, QMessageBox, QHBoxLayout

class EditSecretDialog(QDialog):
    def __init__(self, db_manager, secret, parent=None):
        super(EditSecretDialog, self).__init__(parent)
        self.db_manager = db_manager
        self.secret = secret  # A dict containing the secret details (including id)
        self.setWindowTitle("Edit Secret")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.subject_edit = QLineEdit(self.secret["subject"])
        self.email_edit = QLineEdit(self.secret["email"])
        self.username_edit = QLineEdit(self.secret["username"])
        self.password_edit = QLineEdit(self.secret["password"])
        self.notes_edit = QTextEdit(self.secret["notes"])
        self.tags_edit = QLineEdit(self.secret["tags"])

        form_layout.addRow("Subject*", self.subject_edit)
        form_layout.addRow("Email", self.email_edit)
        form_layout.addRow("Username", self.username_edit)
        form_layout.addRow("Password", self.password_edit)
        form_layout.addRow("Notes", self.notes_edit)
        form_layout.addRow("Tags", self.tags_edit)
        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        btn_save = QPushButton("Save")
        btn_cancel = QPushButton("Cancel")
        btn_save.clicked.connect(self.handle_save)
        btn_cancel.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(btn_save)
        button_layout.addWidget(btn_cancel)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def handle_save(self):
        subject = self.subject_edit.text().strip()
        if not subject:
            QMessageBox.warning(self, "Input Error", "Subject is required.")
            return
        email = self.email_edit.text().strip()
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        notes = self.notes_edit.toPlainText().strip()
        raw_tags = self.tags_edit.text().strip()
        if raw_tags:
            tag_list = [tag.strip() for tag in raw_tags.split(',') if tag.strip()]
            tags = ','.join(tag_list)
        else:
            tags = ""
        try:
            self.db_manager.update_secret(
                self.secret["id"], subject, email, username, password, notes, tags
            )
            QMessageBox.information(self, "Success", "Secret updated successfully.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update secret: {str(e)}")
