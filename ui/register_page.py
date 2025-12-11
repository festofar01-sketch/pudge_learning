from PyQt5 import QtWidgets, QtCore
from learning_platform.services import register_user


class RegisterPage(QtWidgets.QWidget):
    switch_to_login = QtCore.pyqtSignal()

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

        # --- ЗАГОЛОВОК ---
        title = QtWidgets.QLabel("Регистрация")
        title.setObjectName("title")
        card_layout.addWidget(title)

        # --- ПОЛЕ ЛОГИНА ---
        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Имя пользователя")
        self.username_input.setObjectName("inputField")
        card_layout.addWidget(self.username_input)

        # --- ПОЛЕ ПОЛНОГО ИМЕНИ ---
        self.fullname_input = QtWidgets.QLineEdit()
        self.fullname_input.setPlaceholderText("Полное имя")
        self.fullname_input.setObjectName("inputField")
        card_layout.addWidget(self.fullname_input)

        # --- ПАРОЛЬ ---
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setObjectName("inputField")
        card_layout.addWidget(self.password_input)

        # --- КНОПКА РЕГИСТРАЦИИ ---
        reg_btn = QtWidgets.QPushButton("Создать аккаунт")
        reg_btn.setObjectName("primaryButton")
        reg_btn.clicked.connect(self.try_register)
        card_layout.addWidget(reg_btn)

        # --- НАЗАД ---  (ИСПРАВЛЕНО!)
        back_btn = QtWidgets.QPushButton("Назад")
        back_btn.setObjectName("secondaryButton")
        back_btn.clicked.connect(lambda: self.switch_to_login.emit())   # ← FIX
        card_layout.addWidget(back_btn)

        main_layout.addWidget(card)

    # --------------------- РЕГИСТРАЦИЯ ---------------------
    def try_register(self):
        username = self.username_input.text().strip()
        fullname = self.fullname_input.text().strip() or None
        password = self.password_input.text().strip()

        if not username or not password:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите логин и пароль!")
            return

        try:
            register_user(username, password, fullname)
            QtWidgets.QMessageBox.information(self, "Успех", "Аккаунт создан!")
            self.switch_to_login.emit()
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Такой логин уже существует!")
