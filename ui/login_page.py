from PyQt5 import QtWidgets, QtCore
from learning_platform.services import check_login


class LoginPage(QtWidgets.QWidget):
    login_success = QtCore.pyqtSignal(object)
    switch_to_register = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        # --- ОСНОВНОЙ ЛЕЙАУТ ---
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setAlignment(QtCore.Qt.AlignCenter)

        # --- КАРТОЧКА ---
        card = QtWidgets.QFrame()
        card.setObjectName("card")
        card.setMinimumWidth(330)

        card_layout = QtWidgets.QVBoxLayout(card)
        card_layout.setAlignment(QtCore.Qt.AlignCenter)
        card_layout.setSpacing(18)

        # --- ТЕКСТ ---
        title = QtWidgets.QLabel("Добро пожаловать!")
        title.setObjectName("title")
        card_layout.addWidget(title)

        # --- ПОЛЕ ЛОГИНА ---
        self.username = QtWidgets.QLineEdit()
        self.username.setPlaceholderText("Логин")
        self.username.setObjectName("inputField")
        card_layout.addWidget(self.username)

        # --- ПОЛЕ ПАРОЛЯ ---
        self.password = QtWidgets.QLineEdit()
        self.password.setPlaceholderText("Пароль")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("inputField")
        card_layout.addWidget(self.password)

        # --- КНОПКА ВХОДА ---
        btn_login = QtWidgets.QPushButton("Войти")
        btn_login.setObjectName("primaryButton")
        btn_login.clicked.connect(self.try_login)
        card_layout.addWidget(btn_login)

        # --- КНОПКА РЕГИСТРАЦИИ ---
        btn_register = QtWidgets.QPushButton("Создать аккаунт")
        btn_register.setObjectName("secondaryButton")
        btn_register.clicked.connect(lambda: self.switch_to_register.emit())   # ← ИСПРАВЛЕНО
        card_layout.addWidget(btn_register)

        main_layout.addWidget(card)

    # ------------------ ЛОГИКА ------------------
    def try_login(self):
        username = self.username.text().strip()
        password = self.password.text().strip()

        user = check_login(username, password)

        if user:
            self.login_success.emit(user)
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
