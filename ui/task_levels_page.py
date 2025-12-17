from PyQt5 import QtWidgets, QtCore
class TaskLevelsPage(QtWidgets.QWidget):

    task_selected = QtCore.pyqtSignal(int)
    back_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        main = QtWidgets.QVBoxLayout(self)
        main.setAlignment(QtCore.Qt.AlignCenter)
        main.setSpacing(20)

        title = QtWidgets.QLabel("Уровень заданий")
        title.setObjectName("title")
        main.addWidget(title)

        self.btn1 = self.make_btn("🟢 Перевод слов", 1)
        self.btn2 = self.make_btn("🔵 Вставить слово", 2)
        self.btn3 = self.make_btn("🟣 Синтаксис (скоро)", 3)

        main.addWidget(self.btn1)
        main.addWidget(self.btn2)
        main.addWidget(self.btn3)

        back = QtWidgets.QPushButton("← Назад")
        back.setObjectName("secondaryButton")
        back.setFixedWidth(260)
        back.clicked.connect(self.back_signal.emit)
        main.addWidget(back)

    def make_btn(self, text, level, enabled=True):
        btn = QtWidgets.QPushButton(text)
        btn.setObjectName("menuButton")
        btn.setFixedWidth(260)
        btn.setEnabled(enabled)
        btn.clicked.connect(lambda _, lv=level: self.task_selected.emit(lv))
        return btn
