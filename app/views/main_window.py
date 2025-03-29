from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QListWidget, QListWidgetItem, QMessageBox, QDialog, QDesktopWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from app.database import DatabaseManager
from app.dialogs.add_secret_dialog import AddSecretDialog
from app.views.item_widget import ItemWidget

class MainWindow(QMainWindow):
    def __init__(self, config_manager, encryption_key, parent=None):
        super(MainWindow, self).__init__(parent)
        self.config_manager = config_manager
        self.encryption_key = encryption_key
        self.db_manager = DatabaseManager(self.encryption_key)  # Pass encryption key here
        self.setWindowTitle("Senty - Secret Manager")
        self.resize(800, 600)
        self.center_window()
        self.setFixedSize(self.size())
        self.initUI()
        self.load_secrets()

    def center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Horizontal menu layout
        menu_layout = QHBoxLayout()
        btn_add = QPushButton("Add")
        add_icon = QIcon("resources/icons/add.png")  # Ensure this path is correct
        btn_add.setIcon(add_icon)
        btn_add.clicked.connect(self.handle_add)
        btn_sync = QPushButton("Sync")
        btn_sync.clicked.connect(self.handle_sync)
        menu_layout.addWidget(btn_add)
        menu_layout.addWidget(btn_sync)
        menu_layout.addStretch()
        btn_about = QPushButton("About")
        btn_about.clicked.connect(self.handle_about)
        btn_exit = QPushButton("Exit")
        btn_exit.clicked.connect(self.handle_exit)
        menu_layout.addWidget(btn_about)
        menu_layout.addWidget(btn_exit)
        main_layout.addLayout(menu_layout)

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search secrets...")
        self.search_edit.setFocus()
        self.search_edit.textChanged.connect(self.handle_search)
        main_layout.addWidget(self.search_edit)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("QListWidget::item:selected { background: transparent; }")
        main_layout.addWidget(self.list_widget)

    def load_secrets(self):
        self.list_widget.clear()
        secrets = self.db_manager.get_all_secrets()
        for secret in secrets:
            secret_id = secret["id"]
            subject = secret["subject"]
            tags = secret["tags"]
            updated_at = secret["updated_at"]
            item_widget = ItemWidget(secret_id, subject, tags, updated_at)
            item_widget.viewClicked.connect(self.handle_view_secret)
            item_widget.editClicked.connect(self.handle_edit_secret)
            item_widget.deleteClicked.connect(self.handle_delete_secret)
            list_item = QListWidgetItem(self.list_widget)
            list_item.setSizeHint(item_widget.sizeHint())
            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, item_widget)

    def handle_search(self):
        keyword = self.search_edit.text().strip().lower()
        self.list_widget.clear()
        all_secrets = self.db_manager.get_all_secrets()
        # Filter in memory on decrypted data
        filtered = [
            secret for secret in all_secrets
            if keyword in secret["subject"].lower() or keyword in secret["tags"].lower()
        ]
        for secret in filtered:
            secret_id = secret["id"]
            subject = secret["subject"]
            tags = secret["tags"]
            updated_at = secret["updated_at"]
            item_widget = ItemWidget(secret_id, subject, tags, updated_at)
            item_widget.viewClicked.connect(self.handle_view_secret)
            item_widget.editClicked.connect(self.handle_edit_secret)
            item_widget.deleteClicked.connect(self.handle_delete_secret)
            list_item = QListWidgetItem(self.list_widget)
            list_item.setSizeHint(item_widget.sizeHint())
            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, item_widget)

    def handle_add(self):
        dialog = AddSecretDialog(self.db_manager, self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_secrets()

    def handle_sync(self):
        QMessageBox.information(self, "Sync", "Sync action triggered.")

    def handle_about(self):
        about_text = (
            "Senty - Secret Manager\n\n"
            "A secure application to manage your secrets.\n\n"
            "Author: stonemanhero@gmail.com"
        )
        QMessageBox.information(self, "About Senty", about_text)

    def handle_exit(self):
        reply = QMessageBox.question(
            self, "Exit Confirmation",
            "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.close()

    def handle_view_secret(self, secret_id):
        secret = self.db_manager.get_secret_by_id(secret_id)
        if secret:
            from app.dialogs.view_secret_dialog import ViewSecretDialog
            dialog = ViewSecretDialog(secret, self)
            dialog.exec_()

    def handle_edit_secret(self, secret_id):
        secret = self.db_manager.get_secret_by_id(secret_id)
        if secret:
            from app.dialogs.edit_secret_dialog import EditSecretDialog
            dialog = EditSecretDialog(self.db_manager, secret, self)
            if dialog.exec_() == QDialog.Accepted:
                self.load_secrets()

    def handle_delete_secret(self, secret_id):
        reply = QMessageBox.question(
            self, "Delete Confirmation",
            "Are you sure you want to delete this secret?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.db_manager.delete_secret(secret_id)
            self.load_secrets()
