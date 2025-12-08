from PyQt5 import QtWidgets, QtCore


class CoursesPage(QtWidgets.QWidget):
    start_test = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.setSpacing(25)

        self.title = QtWidgets.QLabel("Добро пожаловать!")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 26px; font-weight: bold; color: #2E7D32;")
        layout.addWidget(self.title)

        btn = QtWidgets.QPushButton("Тест по теме: Животные 🐶🐱")
        btn.setFixedWidth(320)
        btn.setMinimumHeight(48)
        btn.setStyleSheet("""
            QPushButton {
                background:#4CAF50;
                color:white;
                font-size:18px;
                border-radius:12px;
            }
            QPushButton:hover { background:#43A047; }
        """)
        btn.clicked.connect(self.start_test.emit)
        layout.addWidget(btn)

    def set_user(self, user):
        self.title.setText(f"Привет, {user.username}!")
