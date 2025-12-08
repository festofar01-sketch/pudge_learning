from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5.QtCore import QPropertyAnimation
import random


class TestPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # 15 вопросов по теме "Животные"
        self.questions = [
            ("Как переводится 'cat'?", [
                ("Кошка", True), ("Собака", False), ("Птица", False), ("Корова", False),
            ]),
            ("Как переводится 'dog'?", [
                ("Собака", True), ("Кошка", False), ("Лошадь", False), ("Утка", False),
            ]),
            ("Как переводится 'bird'?", [
                ("Птица", True), ("Медведь", False), ("Рыба", False), ("Лиса", False),
            ]),
            ("Как переводится 'fish'?", [
                ("Рыба", True), ("Змея", False), ("Птица", False), ("Корова", False),
            ]),
            ("Как переводится 'cow'?", [
                ("Корова", True), ("Свинья", False), ("Коза", False), ("Овца", False),
            ]),
            ("Как переводится 'horse'?", [
                ("Лошадь", True), ("Осел", False), ("Тигр", False), ("Кот", False),
            ]),
            ("Как переводится 'duck'?", [
                ("Утка", True), ("Курица", False), ("Гусь", False), ("Петух", False),
            ]),
            ("Как переводится 'chicken'?", [
                ("Курица", True), ("Утка", False), ("Гусь", False), ("Петух", False),
            ]),
            ("Как переводится 'sheep'?", [
                ("Овца", True), ("Коза", False), ("Свинья", False), ("Кошка", False),
            ]),
            ("Как переводится 'goat'?", [
                ("Коза", True), ("Овца", False), ("Лошадь", False), ("Корова", False),
            ]),
            ("Как переводится 'pig'?", [
                ("Свинья", True), ("Корова", False), ("Кот", False), ("Собака", False),
            ]),
            ("Как переводится 'fox'?", [
                ("Лиса", True), ("Волк", False), ("Тигр", False), ("Кот", False),
            ]),
            ("Как переводится 'wolf'?", [
                ("Волк", True), ("Лиса", False), ("Слон", False), ("Кролик", False),
            ]),
            ("Как переводится 'rabbit'?", [
                ("Кролик", True), ("Змея", False), ("Крокодил", False), ("Мышь", False),
            ]),
            ("Как переводится 'mouse'?", [
                ("Мышь", True), ("Крыса", False), ("Крот", False), ("Бобр", False),
            ]),
        ]

        self.index = 0

        layout = QtWidgets.QVBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.setSpacing(15)

        title = QtWidgets.QLabel("Тест: Животные 🐶🐱")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size:26px; font-weight:bold; color:#2E7D32;")
        layout.addWidget(title)

        self.number_label = QtWidgets.QLabel("")
        self.number_label.setAlignment(QtCore.Qt.AlignCenter)
        self.number_label.setStyleSheet("font-size:16px; color:#555;")
        layout.addWidget(self.number_label)

        # Прогресс-бар
        self.progress = QtWidgets.QProgressBar()
        self.progress.setFixedWidth(300)
        self.progress.setRange(0, len(self.questions))
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet("""
            QProgressBar { background:#eee; border-radius:8px; height:14px; }
            QProgressBar::chunk { background:#4CAF50; border-radius:8px; }
        """)
        layout.addWidget(self.progress)

        self.label_question = QtWidgets.QLabel("")
        self.label_question.setAlignment(QtCore.Qt.AlignCenter)
        self.label_question.setStyleSheet("font-size:20px;")
        layout.addWidget(self.label_question)

        # Кнопки ответа
        self.buttons = []
        for _ in range(4):
            btn = QtWidgets.QPushButton("")
            btn.setFixedWidth(300)
            btn.setMinimumHeight(42)
            btn.setStyleSheet("""
                QPushButton {
                    background:#4CAF50;
                    color:white;
                    font-size:16px;
                    border-radius:10px;
                }
                QPushButton:hover { background:#43A047; }
            """)
            btn.clicked.connect(self.handle_answer)
            self.buttons.append(btn)
            layout.addWidget(btn)

        self.status_label = QtWidgets.QLabel("")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size:18px;")
        layout.addWidget(self.status_label)

    # --------------------- АНИМАЦИИ ----------------------

    def fade_in(self, widget, duration=350):
        """Плавное появление."""
        effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(effect)

        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(duration)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.start()

        widget.animation = anim

    def shake(self, widget):
        """Тряска при неправильном ответе."""
        anim = QPropertyAnimation(widget, b"pos")
        anim.setDuration(250)
        anim.setKeyValueAt(0, widget.pos())
        anim.setKeyValueAt(0.25, widget.pos() + QtCore.QPoint(-6, 0))
        anim.setKeyValueAt(0.50, widget.pos() + QtCore.QPoint(6, 0))
        anim.setKeyValueAt(0.75, widget.pos() + QtCore.QPoint(-6, 0))
        anim.setKeyValueAt(1, widget.pos())
        anim.start()
        widget.animation = anim

    # ----------------------- ЛОГИКА ----------------------

    def start_test(self):
        self.index = 0
        self.progress.setValue(0)
        self.show_question()

    def show_question(self):
        question, answers = self.questions[self.index]

        total = len(self.questions)
        self.number_label.setText(f"Вопрос {self.index + 1} из {total}")
        self.label_question.setText(question)
        self.progress.setValue(self.index)
        self.status_label.setText("")

        # Анимация появления
        self.fade_in(self.label_question)
        self.fade_in(self.number_label)
        self.fade_in(self.progress)

        # Перемешиваем варианты
        answers = list(answers)
        random.shuffle(answers)

        for btn, (text, correct) in zip(self.buttons, answers):
            btn.setText(text)
            btn.is_correct = correct
            btn.show()
            self.fade_in(btn, duration=250)

    def handle_answer(self):
        btn = self.sender()

        if btn.is_correct:
            self.status_label.setText("Правильно! 😊")
            QtCore.QTimer.singleShot(250, self.next_question)
        else:
            self.status_label.setText("Неправильно 😢 Попробуй ещё раз")
            self.shake(self.label_question)

    def next_question(self):
        self.index += 1

        if self.index >= len(self.questions):
            self.finish_test()
        else:
            self.show_question()

    def finish_test(self):
        self.progress.setValue(len(self.questions))
        self.number_label.setText("")
        self.label_question.setText("Тест завершён! 🎉")
        self.status_label.setText("Ты молодец! Продолжай учиться ✨")

        for btn in self.buttons:
            btn.hide()
