from PyQt5 import QtWidgets, QtCore


class CoursesPage(QtWidgets.QWidget):
    start_test = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        title = QtWidgets.QLabel("Обучение")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size:26px; font-weight:bold;")
        layout.addWidget(title)

        btn = QtWidgets.QPushButton("Начать тест")
        btn.setFixedWidth(300)
        btn.clicked.connect(self.start_test.emit)
        layout.addWidget(btn)
