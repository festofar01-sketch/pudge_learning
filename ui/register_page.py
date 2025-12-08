# register_page.py

from PyQt5 import QtWidgets, QtCore
from ui.ui_base import CenterCardPage
from learning_platform.services import register_user


class RegisterPage(CenterCardPage):
    switch_to_login = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.add_title("Регистрация")

        self.username = self.add_field("Логин")
        self.fullname = self.add_field("Полное имя")
        self.password = self.add_field("Пароль")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        btn = self.add_button("Создать аккаунт")
        btn.clicked.connect(self.do_register)

        back = self.add_button("Назад")
        back.clicked.connect(self.switch_to_login.emit)

    def do_register(self):
        try:
            register_user(self.username.text(), self.password.text(), self.fullname.text())
            QtWidgets.QMessageBox.information(self, "Успех", "Аккаунт создан")
            self.switch_to_login.emit()
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Логин занят")
