from PyQt5 import QtWidgets, QtCore
from learning_platform.services import (
    update_username,
    update_password,
    update_fullname,
    delete_user,
)


class SettingsPage(QtWidgets.QWidget):

    back_to_menu = QtCore.pyqtSignal()
    logout_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.current_user = None

        # ===== ОСНОВНОЙ ЛЕЙАУТ =====
        main = QtWidgets.QVBoxLayout(self)
        main.setAlignment(QtCore.Qt.AlignCenter)

        # ===== КАРТОЧКА =====
        card = QtWidgets.QFrame()
        card.setObjectName("card")
        card.setFixedWidth(340)

        layout = QtWidgets.QVBoxLayout(card)
        layout.setSpacing(16)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        # ===== ЗАГОЛОВОК =====
        title = QtWidgets.QLabel("Настройки")
        title.setObjectName("title")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        # ===== ИЗМЕНИТЬ ИМЯ =====
        btn_name = QtWidgets.QPushButton("Изменить имя")
        btn_name.setObjectName("secondaryButton")
        btn_name.setFixedWidth(260)
        btn_name.clicked.connect(self.change_fullname)
        layout.addWidget(btn_name)

        # ===== ИЗМЕНИТЬ ЛОГИН =====
        btn_login = QtWidgets.QPushButton("Изменить логин")
        btn_login.setObjectName("secondaryButton")
        btn_login.setFixedWidth(260)
        btn_login.clicked.connect(self.change_username)
        layout.addWidget(btn_login)

        # ===== ИЗМЕНИТЬ ПАРОЛЬ =====
        btn_pass = QtWidgets.QPushButton("Изменить пароль")
        btn_pass.setObjectName("secondaryButton")
        btn_pass.setFixedWidth(260)
        btn_pass.clicked.connect(self.change_password)
        layout.addWidget(btn_pass)

        # ===== УДАЛИТЬ АККАУНТ =====
        btn_delete = QtWidgets.QPushButton("Удалить аккаунт")
        btn_delete.setObjectName("dangerButton")
        btn_delete.setFixedWidth(260)
        btn_delete.clicked.connect(self.delete_account)
        layout.addWidget(btn_delete)

        # ===== ВЫЙТИ =====
        btn_logout = QtWidgets.QPushButton("Выйти из аккаунта")
        btn_logout.setObjectName("dangerButton")
        btn_logout.setFixedWidth(260)
        btn_logout.clicked.connect(self.logout)
        layout.addWidget(btn_logout)

        # ===== НАЗАД =====
        btn_back = QtWidgets.QPushButton("← Назад")
        btn_back.setObjectName("secondaryButton")
        btn_back.setFixedWidth(260)
        btn_back.clicked.connect(self.back_to_menu.emit)
        layout.addWidget(btn_back)

        main.addWidget(card)

    # ======================================
    #          ПОЛЬЗОВАТЕЛЬ
    # ======================================
    def set_user(self, user):
        self.current_user = user

    # ======================================
    #          СМЕНА ИМЕНИ
    # ======================================
    def change_fullname(self):
        if not self.current_user:
            return

        name, ok = QtWidgets.QInputDialog.getText(
            self, "Имя", "Введите новое имя:"
        )
        if ok and name:
            update_fullname(self.current_user.id, name)
            QtWidgets.QMessageBox.information(self, "Готово", "Имя изменено")

    # ======================================
    #          СМЕНА ЛОГИНА
    # ======================================
    def change_username(self):
        if not self.current_user:
            return

        login, ok = QtWidgets.QInputDialog.getText(
            self, "Логин", "Введите новый логин:"
        )
        if not ok or not login:
            return

        success = update_username(self.current_user.id, login)
        if success:
            QtWidgets.QMessageBox.information(self, "Готово", "Логин изменён")
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Логин занят")

    # ======================================
    #          СМЕНА ПАРОЛЯ
    # ======================================
    def change_password(self):
        if not self.current_user:
            return

        password, ok = QtWidgets.QInputDialog.getText(
            self, "Пароль", "Введите новый пароль:",
            QtWidgets.QLineEdit.Password
        )
        if ok and password:
            update_password(self.current_user.id, password)
            QtWidgets.QMessageBox.information(self, "Готово", "Пароль изменён")

    # ======================================
    #          УДАЛЕНИЕ
    # ======================================
    def delete_account(self):
        if not self.current_user:
            return

        confirm = QtWidgets.QMessageBox.question(
            self,
            "Удаление аккаунта",
            "Вы уверены? Аккаунт будет удалён навсегда.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )

        if confirm == QtWidgets.QMessageBox.Yes:
            delete_user(self.current_user.id)
            QtWidgets.QMessageBox.information(self, "Удалено", "Аккаунт удалён")
            self.logout_signal.emit()

    # ======================================
    #              ВЫХОД
    # ======================================
    def logout(self):
        self.current_user = None
        self.logout_signal.emit()
