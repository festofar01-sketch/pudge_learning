from PyQt5 import QtWidgets
from learning_platform.user_service import add_syntax_question


class AddSyntaxQuestionDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, level="A1"):
        super().__init__(parent)
        self.setWindowTitle("Добавить синтаксис")
        self.setFixedSize(460, 340)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(12)

        self.level = QtWidgets.QComboBox()
        self.level.addItems(["A1", "A2", "B1", "B2", "C1"])
        self.level.setCurrentText(level)

        self.words = QtWidgets.QLineEdit()
        self.words.setPlaceholderText("Слова через запятую: I,am,a,student")

        self.order = QtWidgets.QLineEdit()
        self.order.setPlaceholderText("Правильный порядок: I,am,a,student")

        self.status = QtWidgets.QLabel("")
        self.status.setStyleSheet("color:#dc2626; font-size:13px;")

        btn = QtWidgets.QPushButton("Сохранить")
        btn.clicked.connect(self.save)

        layout.addWidget(QtWidgets.QLabel("Уровень"))
        layout.addWidget(self.level)

        layout.addWidget(QtWidgets.QLabel("Слова"))
        layout.addWidget(self.words)

        layout.addWidget(QtWidgets.QLabel("Правильный порядок"))
        layout.addWidget(self.order)

        layout.addWidget(self.status)
        layout.addWidget(btn)

    def save(self):
        level = self.level.currentText()

        words_list = [w.strip() for w in self.words.text().split(",") if w.strip()]
        order_list = [w.strip() for w in self.order.text().split(",") if w.strip()]

        if not words_list or not order_list:
            self.status.setText("Заполни слова и порядок")
            return

        if len(words_list) != len(order_list):
            self.status.setText("Количество слов и порядок не совпадают")
            return

        # 🔥 sentence формируем автоматически
        sentence = " ".join(order_list)

        add_syntax_question(
            level,
            sentence,
            "{" + ",".join(words_list) + "}",
            "{" + ",".join(order_list) + "}"
        )

        self.accept()
