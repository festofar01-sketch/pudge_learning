from PyQt5 import QtWidgets, QtCore, QtGui


FORM_WIDTH = 420


class MainMenuPage(QtWidgets.QWidget):
    start_learning = QtCore.pyqtSignal()
    open_profile = QtCore.pyqtSignal()
    open_settings = QtCore.pyqtSignal()
    open_admin_panel = QtCore.pyqtSignal()   # 🔥 НОВОЕ
    exit_app = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.current_user = None
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
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        # ---------- TITLE ----------
        title = QtWidgets.QLabel("Pudge Learning")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setObjectName("Title")
        layout.addWidget(title)

        subtitle = QtWidgets.QLabel("Главное меню")
        subtitle.setAlignment(QtCore.Qt.AlignCenter)
        subtitle.setObjectName("Subtitle")
        layout.addWidget(subtitle)

        layout.addSpacing(20)

        # ---------- BUTTONS ----------
        self.btn_start = self._primary_button("Начать обучение")
        self.btn_profile = self._secondary_button("Профиль")
        self.btn_settings = self._secondary_button("Настройки")

        # 🔥 АДМИН-КНОПКА
        self.btn_admin = self._secondary_button("Админ-панель")
        self.btn_admin.hide()  # ❗ по умолчанию скрыта

        self.btn_exit = self._danger_button("Выход")

        self.btn_start.clicked.connect(self.start_learning.emit)
        self.btn_profile.clicked.connect(self.open_profile.emit)
        self.btn_settings.clicked.connect(self.open_settings.emit)
        self.btn_admin.clicked.connect(self.open_admin_panel.emit)
        self.btn_exit.clicked.connect(self.exit_app.emit)

        layout.addWidget(self.btn_start)
        layout.addWidget(self.btn_profile)
        layout.addWidget(self.btn_settings)
        layout.addWidget(self.btn_admin)   # 🔥 добавили в меню
        layout.addSpacing(6)
        layout.addWidget(self.btn_exit)

        outer.addWidget(container)
        outer.addStretch()

    # ================= PUBLIC =================
    def set_user(self, user):
        self.current_user = user

        if user.role in ("admin", "teacher"):
            self.btn_admin.setText(
                "Админ-панель" if user.role == "admin" else "Панель преподавателя"
            )
            self.btn_admin.show()
        else:
            self.btn_admin.hide()

    # ================= BUTTONS =================
    def _primary_button(self, text):
        btn = QtWidgets.QPushButton(text)
        btn.setFixedSize(FORM_WIDTH, 64)
        btn.setCursor(QtCore.Qt.PointingHandCursor)
        btn.setObjectName("PrimaryButton")
        return btn

    def _secondary_button(self, text):
        btn = QtWidgets.QPushButton(text)
        btn.setFixedSize(FORM_WIDTH, 60)
        btn.setCursor(QtCore.Qt.PointingHandCursor)
        btn.setObjectName("SecondaryButton")
        return btn

    def _danger_button(self, text):
        btn = QtWidgets.QPushButton(text)
        btn.setFixedSize(FORM_WIDTH, 60)
        btn.setCursor(QtCore.Qt.PointingHandCursor)
        btn.setObjectName("DangerButton")
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

        QPushButton#PrimaryButton:hover {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #4f46e5,
                stop:1 #0ea5e9
            );
        }

        QPushButton#SecondaryButton {
            background: white;
            border: 1px solid #e5e7eb;
            color: #111827;
        }

        QPushButton#SecondaryButton:hover {
            background: #f1f5f9;
        }

        QPushButton#DangerButton {
            background: #fee2e2;
            color: #dc2626;
            border: none;
        }

        QPushButton#DangerButton:hover {
            background: #fecaca;
        }
        """)
