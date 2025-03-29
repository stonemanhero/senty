from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import pyqtSignal

class ItemWidget(QWidget):
    viewClicked = pyqtSignal(int)
    editClicked = pyqtSignal(int)
    deleteClicked = pyqtSignal(int)
    
    def __init__(self, secret_id, subject, tags, updated_at, parent=None):
        super(ItemWidget, self).__init__(parent)
        self.secret_id = secret_id
        self.subject = subject
        self.tags = tags
        self.updated_at = updated_at  # Retained for later use (e.g., in view dialog)
        self.initUI()
        
    def initUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        subject_label = QLabel(self.subject)
        tags_label = QLabel(self.tags)
        
        view_button = QPushButton("View")
        edit_button = QPushButton("Edit")
        delete_button = QPushButton("Delete")
        
        view_button.clicked.connect(lambda: self.viewClicked.emit(self.secret_id))
        edit_button.clicked.connect(lambda: self.editClicked.emit(self.secret_id))
        delete_button.clicked.connect(lambda: self.deleteClicked.emit(self.secret_id))
        
        layout.addWidget(subject_label)
        layout.addWidget(tags_label)
        layout.addStretch()  # Push buttons to the far right
        layout.addWidget(view_button)
        layout.addWidget(edit_button)
        layout.addWidget(delete_button)
        
        self.setLayout(layout)
