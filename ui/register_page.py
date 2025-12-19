from PyQt5 import QtWidgets, QtCore
from learning_platform.user_service import register_user

FORM_WIDTH = 420


class RegisterPage(QtWidgets.QWidget):
    register_success = QtCore.pyqtSignal()
    back_to_login = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self._build_ui()
        self._apply_styles()

    # ================= UI =================
    def _build_ui(self):
        outer = QtWidgets.QVBoxLayout(self)
        outer.setAlignment(QtCore.Qt.AlignCenter)
        outer.addStretch()

        container = QtWidgets.QWidget()
        container.setFixedWidth(FORM_WIDTH)

        layout = QtWidgets.QVBoxLayout(container)
        layout.setSpacing(22)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        title = QtWidgets.QLabel("Создание аккаунта")
        title.setObjectName("Title")
        title.setAlignment(QtCore.Qt.AlignCenter)

        subtitle = QtWidgets.QLabel("Заполните данные для регистрации")
        subtitle.setObjectName("Subtitle")
        subtitle.setAlignment(QtCore.Qt.AlignCenter)

        self.login = QtWidgets.QLineEdit()
        self.login.setPlaceholderText("Логин")
        self.login.setObjectName("Input")
        self.login.setFixedHeight(52)

        self.password = QtWidgets.QLineEdit()
        self.password.setPlaceholderText("Пароль")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("Input")
        self.password.setFixedHeight(52)

        self.password_repeat = QtWidgets.QLineEdit()
        self.password_repeat.setPlaceholderText("Повторите пароль")
        self.password_repeat.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_repeat.setObjectName("Input")
        self.password_repeat.setFixedHeight(52)

        self.btn_register = self._primary_button("Создать аккаунт")
        self.btn_register.clicked.connect(self.handle_register)

        self.btn_back = self._secondary_button("Назад ко входу")
        self.btn_back.clicked.connect(self.back_to_login.emit)

        self.status = QtWidgets.QLabel("")
        self.status.setObjectName("Status")
        self.status.setAlignment(QtCore.Qt.AlignCenter)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(8)
        layout.addWidget(self.login)
        layout.addWidget(self.password)
        layout.addWidget(self.password_repeat)
        layout.addWidget(self.btn_register)
        layout.addWidget(self.btn_back)
        layout.addWidget(self.status)

        outer.addWidget(container)
        outer.addStretch()

    # ================= LOGIC =================
    def handle_register(self):
        username = self.login.text().strip()
        password = self.password.text()
        repeat = self.password_repeat.text()

        self.status.clear()

        if not username:
            self.status.setText("Введите логин")
            return

        if len(password) < 4:
            self.status.setText("Пароль должен быть не короче 4 символов")
            return

        if password != repeat:
            self.status.setText("Пароли не совпадают")
            return

        try:
            register_user(username, password)
        except ValueError:
            self.status.setText("Такой пользователь уже существует")
            return

        self.register_success.emit()

    # ================= BUTTONS =================
    def _primary_button(self, text):
        btn = QtWidgets.QPushButton(text)
        btn.setFixedSize(FORM_WIDTH, 60)
        btn.setCursor(QtCore.Qt.PointingHandCursor)
        btn.setObjectName("PrimaryButton")
        return btn

    def _secondary_button(self, text):
        btn = QtWidgets.QPushButton(text)
        btn.setFixedSize(FORM_WIDTH, 56)
        btn.setCursor(QtCore.Qt.PointingHandCursor)
        btn.setObjectName("SecondaryButton")
        return btn

    # ================= STYLES =================
    def _apply_styles(self):
        self.setStyleSheet("""
        QWidget {
            background: #f5f7ff;
            font-family: Inter;
        }

        QLabel#Title {
            font-size: 32px;
            font-weight: 800;
            color: #0f172a;
        }

        QLabel#Subtitle {
            font-size: 14px;
            color: #64748b;
        }

        QLabel#Status {
            font-size: 13px;
            color: #dc2626;
            min-height: 18px;
        }

        QLineEdit#Input {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 14px;
            padding: 0 14px;
            font-size: 15px;
            color: #0f172a;
        }

        QLineEdit#Input:focus {
            border: 1px solid #6366f1;
        }

        QPushButton {
            border-radius: 22px;
            font-size: 16px;
            font-weight: 600;
        }

        QPushButton#PrimaryButton {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #6366f1,
                stop:1 #22d3ee
            );
            color: white;
        }

        QPushButton#SecondaryButton {
            background: white;
            border: 1px solid #e5e7eb;
            color: #111827;
        }
        """)
