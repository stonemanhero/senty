import sys
from PyQt5.QtWidgets import QApplication, QDialog
from app.config_manager import ConfigManager
from app.dialogs.master_password_dialog import MasterPasswordDialog
from app.views.main_window import MainWindow
from app.utils.encryption import derive_key

def main():
    app = QApplication(sys.argv)
    config_manager = ConfigManager()

    # Decide whether to set a new master password or verify an existing one.
    if config_manager.has_master_password():
        dialog = MasterPasswordDialog(config_manager, is_setting=False)
    else:
        dialog = MasterPasswordDialog(config_manager, is_setting=True)

    if dialog.exec_() == QDialog.Accepted:
        master_password = dialog.password_edit.text()
        salt = config_manager.get_salt()
        encryption_key = derive_key(master_password, salt)
        window = MainWindow(config_manager, encryption_key)
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
