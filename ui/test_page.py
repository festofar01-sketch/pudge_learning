from PyQt5 import QtWidgets, QtCore, QtGui
import random


class TestPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.questions = [...]  # сокращено для примера

        self.index = 0

        # ОСНОВНОЙ ЛЕЙАУТ
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setAlignment(QtCore.Qt.AlignCenter)

        # КАРТОЧКА
        self.card = QtWidgets.QFrame()
        self.card.setObjectName("card")
        self.card.setMinimumWidth(330)

        layout = QtWidgets.QVBoxLayout(self.card)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.setSpacing(18)

        self.title = QtWidgets.QLabel("Тест: Животные")
        self.title.setObjectName("title")
        layout.addWidget(self.title)

        self.number_label = QtWidgets.QLabel("")
        self.number_label.setObjectName("subtitle")
        layout.addWidget(self.number_label)

        self.progress = QtWidgets.QProgressBar()
        self.progress.setRange(0, len(self.questions))
        self.progress.setTextVisible(False)
        self.progress.setObjectName("goldProgress")
        layout.addWidget(self.progress)

        self.question_label = QtWidgets.QLabel("")
        self.question_label.setObjectName("subtitle")
        layout.addWidget(self.question_label)

        self.buttons = []
        for _ in range(4):
            btn = QtWidgets.QPushButton("")
            btn.setObjectName("testButton")
            btn.setFixedWidth(260)
            btn.setMinimumHeight(36)
            btn.clicked.connect(self.handle_answer)
            self.buttons.append(btn)
            layout.addWidget(btn, alignment=QtCore.Qt.AlignCenter)

        self.status_label = QtWidgets.QLabel("")
        self.status_label.setObjectName("subtitle")
        layout.addWidget(self.status_label)

        main_layout.addWidget(self.card)

        # АНИМАЦИИ
        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        self.fade_anim = QtCore.QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_anim.setDuration(250)

        # shake — теперь на card
        self.shake_anim = QtCore.QPropertyAnimation(self.card, b"pos")
        self.shake_anim.setDuration(150)

    def fade_in(self):
        self.fade_anim.stop()
        self.fade_anim.setStartValue(0)
        self.fade_anim.setEndValue(1)
        self.fade_anim.start()

    def shake(self):
        start = self.card.pos()
        self.shake_anim.stop()
        self.shake_anim.setKeyValueAt(0, start)
        self.shake_anim.setKeyValueAt(0.25, start + QtCore.QPoint(10, 0))
        self.shake_anim.setKeyValueAt(0.5, start - QtCore.QPoint(10, 0))
        self.shake_anim.setKeyValueAt(0.75, start + QtCore.QPoint(10, 0))
        self.shake_anim.setKeyValueAt(1, start)
        self.shake_anim.start()

    def start_test(self):
        self.fade_anim.stop()
        self.shake_anim.stop()

        for btn in self.buttons:
            btn.show()
            btn.setEnabled(True)

        self.index = 0
        self.progress.setValue(0)
        self.fade_in()
        self.show_question()

    def show_question(self):
        q, answers = self.questions[self.index]

        self.number_label.setText(f"Вопрос {self.index + 1} из {len(self.questions)}")
        self.question_label.setText(q)
        self.status_label.setText("")

        answers = list(answers)
        random.shuffle(answers)

        for btn, (text, correct) in zip(self.buttons, answers):
            btn.setText(text)
            btn.correct = correct

        self.fade_in()

    def handle_answer(self):
        btn = self.sender()

        if btn.correct:
            self.status_label.setText("Правильно! ✨")
            self.index += 1

            if self.index >= len(self.questions):
                self.finish_test()
            else:
                self.progress.setValue(self.index)
                self.show_question()
        else:
            self.status_label.setText("Неправильно 😢")
            self.shake()

    def finish_test(self):
        self.progress.setValue(len(self.questions))
        self.question_label.setText("Тест завершён! 🎉")
        self.status_label.setText("Отличная работа!")

        for btn in self.buttons:
            btn.hide()

        self.fade_in()
