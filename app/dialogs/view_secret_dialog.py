import datetime
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QPushButton, 
    QHBoxLayout, QMessageBox, QApplication, QLabel
)

class ViewSecretDialog(QDialog):
    def __init__(self, secret, parent=None):
        super(ViewSecretDialog, self).__init__(parent)
        self.secret = secret  # A dict with keys: subject, email, username, password, notes, tags, updated_at, id
        self.setWindowTitle("View Secret")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        # Subject
        self.subject_edit = QLineEdit(self.secret["subject"])
        self.subject_edit.setReadOnly(True)
        btn_copy_subject = QPushButton("Copy")
        btn_copy_subject.clicked.connect(lambda: self.copy_text(self.subject_edit.text()))
        hl_subject = QHBoxLayout()
        hl_subject.addWidget(self.subject_edit)
        hl_subject.addWidget(btn_copy_subject)
        form_layout.addRow("Subject", hl_subject)
        
        # Email
        self.email_edit = QLineEdit(self.secret["email"])
        self.email_edit.setReadOnly(True)
        btn_copy_email = QPushButton("Copy")
        btn_copy_email.clicked.connect(lambda: self.copy_text(self.email_edit.text()))
        hl_email = QHBoxLayout()
        hl_email.addWidget(self.email_edit)
        hl_email.addWidget(btn_copy_email)
        form_layout.addRow("Email", hl_email)
        
        # Username
        self.username_edit = QLineEdit(self.secret["username"])
        self.username_edit.setReadOnly(True)
        btn_copy_username = QPushButton("Copy")
        btn_copy_username.clicked.connect(lambda: self.copy_text(self.username_edit.text()))
        hl_username = QHBoxLayout()
        hl_username.addWidget(self.username_edit)
        hl_username.addWidget(btn_copy_username)
        form_layout.addRow("Username", hl_username)
        
        # Password
        self.password_edit = QLineEdit(self.secret["password"])
        self.password_edit.setReadOnly(True)
        btn_copy_password = QPushButton("Copy")
        btn_copy_password.clicked.connect(lambda: self.copy_text(self.password_edit.text()))
        hl_password = QHBoxLayout()
        hl_password.addWidget(self.password_edit)
        hl_password.addWidget(btn_copy_password)
        form_layout.addRow("Password", hl_password)
        
        # Notes
        self.notes_edit = QTextEdit(self.secret["notes"])
        self.notes_edit.setReadOnly(True)
        btn_copy_notes = QPushButton("Copy")
        btn_copy_notes.clicked.connect(lambda: self.copy_text(self.notes_edit.toPlainText()))
        hl_notes = QHBoxLayout()
        hl_notes.addWidget(self.notes_edit)
        hl_notes.addWidget(btn_copy_notes)
        form_layout.addRow("Notes", hl_notes)
        
        # Tags
        self.tags_edit = QLineEdit(self.secret["tags"])
        self.tags_edit.setReadOnly(True)
        btn_copy_tags = QPushButton("Copy")
        btn_copy_tags.clicked.connect(lambda: self.copy_text(self.tags_edit.text()))
        hl_tags = QHBoxLayout()
        hl_tags.addWidget(self.tags_edit)
        hl_tags.addWidget(btn_copy_tags)
        form_layout.addRow("Tags", hl_tags)
        
        layout.addLayout(form_layout)
        
        # Add extra spacing above last updated info
        layout.addSpacing(10)
        
        # Show last updated as informational text at the bottom (without a copy button)
        last_updated = self.format_date(self.secret["updated_at"])
        info_label = QLabel(f"Last Updated: {last_updated}")
        info_label.setStyleSheet("font-style: italic;")
        layout.addWidget(info_label)
        
        self.setLayout(layout)

    def copy_text(self, text):
        QApplication.clipboard().setText(text)
        QMessageBox.information(self, "Copied", "Text copied to clipboard.")

    def format_date(self, date_str):
        """
        Converts a date string in the format 'Y-m-d H:M:S' to 'd/m/Y H:M:S'.
        """
        try:
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            return dt.strftime("%d/%m/%Y %H:%M:%S")
        except Exception:
            return date_str
