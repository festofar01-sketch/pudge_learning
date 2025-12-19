from PyQt5 import QtWidgets, QtCore
from learning_platform.user_service import check_login

FORM_WIDTH = 420


class LoginPage(QtWidgets.QWidget):
    login_success = QtCore.pyqtSignal(object)
    open_register = QtCore.pyqtSignal()

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

        title = QtWidgets.QLabel("Добро пожаловать 👋")
        title.setObjectName("Title")
        title.setAlignment(QtCore.Qt.AlignCenter)

        subtitle = QtWidgets.QLabel("Войдите, чтобы продолжить обучение")
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

        self.btn_login = self._primary_button("Войти")
        self.btn_login.clicked.connect(self.handle_login)

        self.btn_register = self._secondary_button("Создать аккаунт")
        self.btn_register.clicked.connect(self.open_register.emit)

        self.status = QtWidgets.QLabel("")
        self.status.setObjectName("Status")
        self.status.setAlignment(QtCore.Qt.AlignCenter)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(10)
        layout.addWidget(self.login)
        layout.addWidget(self.password)
        layout.addWidget(self.btn_login)
        layout.addWidget(self.btn_register)
        layout.addWidget(self.status)

        outer.addWidget(container)
        outer.addStretch()

    # ================= LOGIC =================
    def handle_login(self):
        username = self.login.text().strip()
        password = self.password.text()

        self.status.clear()

        if not username:
            self.status.setText("Введите логин")
            return

        if not password:
            self.status.setText("Введите пароль")
            return

        user = check_login(username, password)

        if not user:
            self.status.setText("Неверный логин или пароль")
            return

        self.login_success.emit(user)

    # ================= BUTTONS =================
    def _primary_button(self, text):
        btn = QtWidgets.QPushButton(text)
        btn.setFixedHeight(52)
        btn.setCursor(QtCore.Qt.PointingHandCursor)
        btn.setObjectName("PrimaryButton")
        btn.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed
        )
        return btn

    def _secondary_button(self, text):
        btn = QtWidgets.QPushButton(text)
        btn.setFixedHeight(52)
        btn.setCursor(QtCore.Qt.PointingHandCursor)
        btn.setObjectName("SecondaryButton")
        btn.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed
        )
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
