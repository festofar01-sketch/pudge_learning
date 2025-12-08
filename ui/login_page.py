# login_page.py

from PyQt5 import QtWidgets, QtCore
from ui.ui_base import CenterCardPage
from learning_platform.services import login_user


class LoginPage(CenterCardPage):
    switch_to_register = QtCore.pyqtSignal()
    login_success = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()

        self.add_title("Добро пожаловать!")

        self.username = self.add_field("Логин")
        self.password = self.add_field("Пароль")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        btn = self.add_button("Войти")
        btn.clicked.connect(self.do_login)

        reg_btn = self.add_button("Создать аккаунт")
        reg_btn.clicked.connect(self.switch_to_register.emit)

    def do_login(self):
        u = self.username.text()
        p = self.password.text()

        user = login_user(u, p)
        if user:
            self.login_success.emit(user)
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
