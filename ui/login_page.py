from PyQt5 import QtWidgets, QtCore


class LoginPage(QtWidgets.QWidget):
    login_success = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        outer = QtWidgets.QVBoxLayout(self)
        outer.setAlignment(QtCore.Qt.AlignCenter)

        container = QtWidgets.QWidget()
        container.setFixedWidth(520)

        layout = QtWidgets.QVBoxLayout(container)
        layout.setSpacing(22)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        title = QtWidgets.QLabel("Добро пожаловать 👋")
        title.setObjectName("title")
        title.setAlignment(QtCore.Qt.AlignCenter)

        subtitle = QtWidgets.QLabel("Войдите, чтобы продолжить обучение")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(QtCore.Qt.AlignCenter)

        self.login = QtWidgets.QLineEdit()
        self.login.setPlaceholderText("Логин")

        self.password = QtWidgets.QLineEdit()
        self.password.setPlaceholderText("Пароль")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.btn_login = QtWidgets.QPushButton("Войти")
        self.btn_login.setObjectName("primary")
        self.btn_login.clicked.connect(self.handle_login)

        self.btn_register = QtWidgets.QPushButton("Создать аккаунт")
        self.btn_register.setObjectName("secondary")

        self.status = QtWidgets.QLabel("")
        self.status.setStyleSheet("color:#ef4444")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(10)
        layout.addWidget(self.login)
        layout.addWidget(self.password)
        layout.addWidget(self.btn_login)
        layout.addWidget(self.btn_register)
        layout.addWidget(self.status)

        outer.addWidget(container)

    def handle_login(self):
        if not self.login.text():
            self.status.setText("Введите логин")
            return
        self.login_success.emit(self.login.text())
