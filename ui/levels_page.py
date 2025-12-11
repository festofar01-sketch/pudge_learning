from PyQt5 import QtWidgets, QtCore


class LevelsPage(QtWidgets.QWidget):

    level_selected = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.setSpacing(15)

        title = QtWidgets.QLabel("Выберите уровень языка")
        title.setObjectName("title")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        self.buttons_layout = QtWidgets.QVBoxLayout()
        self.buttons_layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.addLayout(self.buttons_layout)

        back_btn = QtWidgets.QPushButton("← Назад")
        back_btn.setObjectName("secondaryButton")
        back_btn.clicked.connect(lambda: self.parent().setCurrentIndex(2))
        layout.addWidget(back_btn, alignment=QtCore.Qt.AlignCenter)

    def load_levels(self, level_list):
        while self.buttons_layout.count():
            item = self.buttons_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for code, name in level_list:
            btn = QtWidgets.QPushButton(f"{code} — {name}")
            btn.setObjectName("menuButton")
            btn.setFixedWidth(260)
            btn.clicked.connect(lambda _, c=code: self.level_selected.emit(c))
            self.buttons_layout.addWidget(btn, alignment=QtCore.Qt.AlignCenter)
