from PyQt5 import QtWidgets, QtCore, QtGui
import random


class LessonPage(QtWidgets.QWidget):

    back_to_levels = QtCore.pyqtSignal()
    go_main_menu = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.level_name = ""
        self.questions = []
        self.index = 0

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 24, 0, 24)
        main_layout.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addStretch()

        # ======= CARD =======
        card = QtWidgets.QFrame()
        card.setObjectName("card")
        card.setMinimumWidth(330)
        card.setMaximumWidth(360)

        layout = QtWidgets.QVBoxLayout(card)
        layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        layout.setSpacing(16)

        # ======= КНОПКА НАЗАД (Только для вопросов) =======
        self.back_btn = QtWidgets.QPushButton("← Назад")
        self.back_btn.setObjectName("secondaryButton")
        self.back_btn.setFixedWidth(130)
        self.back_btn.clicked.connect(self.go_prev_question)

        back_row = QtWidgets.QHBoxLayout()
        back_row.addWidget(self.back_btn, alignment=QtCore.Qt.AlignLeft)
        back_row.addStretch()
        layout.addLayout(back_row)

        # ======= ПРОГРЕСС =======
        self.progress = QtWidgets.QProgressBar()
        self.progress.setFixedWidth(260)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setObjectName("goldProgress")
        layout.addWidget(self.progress, alignment=QtCore.Qt.AlignCenter)

        # ======= ТЕКСТЫ =======
        self.title_label = QtWidgets.QLabel("Урок английского")
        self.title_label.setObjectName("title")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.title_label)

        self.level_label = QtWidgets.QLabel("")
        self.level_label.setObjectName("subtitle")
        self.level_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.level_label)

        self.number_label = QtWidgets.QLabel("")
        self.number_label.setObjectName("subtitle")
        self.number_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.number_label)

        self.question_label = QtWidgets.QLabel("")
        self.question_label.setObjectName("subtitle")
        self.question_label.setAlignment(QtCore.Qt.AlignCenter)
        self.question_label.setWordWrap(True)
        layout.addWidget(self.question_label)

        # ======= КНОПКИ ОТВЕТОВ =======
        self.buttons = []
        for _ in range(4):
            btn = QtWidgets.QPushButton("")
            btn.setObjectName("testButton")
            btn.setFixedWidth(260)
            btn.setMinimumHeight(38)
            btn.clicked.connect(self.check_answer)
            self.buttons.append(btn)
            layout.addWidget(btn, alignment=QtCore.Qt.AlignCenter)

        # ======= ДОСРОЧНО =======
        self.finish_btn = QtWidgets.QPushButton("Завершить тест досрочно")
        self.finish_btn.setObjectName("dangerButton")
        self.finish_btn.setFixedWidth(260)
        self.finish_btn.setMinimumHeight(34)
        self.finish_btn.clicked.connect(self.finish_early)
        layout.addWidget(self.finish_btn, alignment=QtCore.Qt.AlignCenter)

        # ======= СТАТУС =======
        self.status_label = QtWidgets.QLabel("")
        self.status_label.setObjectName("subtitle")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # ======= КНОПКА «ВЕРНУТЬСЯ В ГЛАВНОЕ МЕНЮ» =======
        self.to_main_btn = QtWidgets.QPushButton("Вернуться в главное меню")
        self.to_main_btn.setObjectName("secondaryButton")
        self.to_main_btn.setFixedWidth(260)
        self.to_main_btn.setMinimumHeight(34)
        self.to_main_btn.clicked.connect(self.go_main_menu.emit)
        self.to_main_btn.hide()
        layout.addWidget(self.to_main_btn, alignment=QtCore.Qt.AlignCenter)

        main_layout.addWidget(card)
        main_layout.addStretch()

        # ======= АНИМАЦИИ =======
        self.opacity = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity)

        self.fade_anim = QtCore.QPropertyAnimation(self.opacity, b"opacity")
        self.fade_anim.setDuration(300)
        self.fade_anim.setEasingCurve(QtCore.QEasingCurve.InOutQuad)

        self.shake_anim = QtCore.QPropertyAnimation(self, b"pos")
        self.shake_anim.setDuration(180)
        self.shake_anim.setEasingCurve(QtCore.QEasingCurve.OutBounce)

        self.progress_anim = QtCore.QPropertyAnimation(self.progress, b"value")
        self.progress_anim.setDuration(350)
        self.progress_anim.setEasingCurve(QtCore.QEasingCurve.InOutQuad)

    # ======================================================
    #                      ЛОГИКА
    # ======================================================

    def fade_in(self):
        self.fade_anim.stop()
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.start()

    def shake(self):
        start = self.pos()
        self.shake_anim.stop()
        self.shake_anim.setKeyValueAt(0.0, start)
        self.shake_anim.setKeyValueAt(0.25, start + QtCore.QPoint(-8, 0))
        self.shake_anim.setKeyValueAt(0.50, start + QtCore.QPoint(+8, 0))
        self.shake_anim.setKeyValueAt(0.75, start + QtCore.QPoint(-8, 0))
        self.shake_anim.setKeyValueAt(1.0, start)
        self.shake_anim.start()

    # ======================================================
    def load_level(self, level_name, questions):
        self.level_name = level_name
        self.questions = questions or []
        self.index = 0

        self.to_main_btn.hide()
        self.back_btn.hide()
        self.progress.setValue(0)

        self.level_label.setText(level_name)
        self.number_label.setText("")
        self.question_label.setText("")
        self.status_label.setText("")

        for btn in self.buttons:
            btn.show()
            btn.setEnabled(True)

        self.finish_btn.show()

        if not questions:
            self.status_label.setStyleSheet("color: red;")
            self.status_label.setText("Для этого уровня нет вопросов")
            return

        self.show_question()
        self.fade_in()

    # ======================================================
    def show_question(self):
        if self.index == 0:
            self.back_btn.hide()
        else:
            self.back_btn.show()

        q, answers = self.questions[self.index]

        self.number_label.setText(f"Вопрос {self.index + 1} из {len(self.questions)}")
        self.question_label.setText(q)
        self.status_label.setText("")

        ans = list(answers)
        random.shuffle(ans)

        for btn, (text, correct) in zip(self.buttons, ans):
            btn.setText(text)
            btn.correct = correct

        percent = int((self.index / len(self.questions)) * 100)
        self.progress_anim.stop()
        self.progress_anim.setStartValue(self.progress.value())
        self.progress_anim.setEndValue(percent)
        self.progress_anim.start()

        self.fade_in()

    # ======================================================
    def check_answer(self):
        btn = self.sender()

        if getattr(btn, "correct", False):
            self.status_label.setStyleSheet("color: gold;")
            self.status_label.setText("Правильно!")

            self.index += 1
            if self.index >= len(self.questions):
                self.finish_level()
            else:
                self.show_question()
        else:
            self.status_label.setStyleSheet("color: red;")
            self.status_label.setText("Неправильно 😢")
            self.shake()

    # ======================================================
    def go_prev_question(self):
        if self.index > 0:
            self.index -= 1
            self.show_question()

    # ======================================================
    def finish_early(self):
        self.hide_buttons()

        self.back_btn.hide()  # УБРАЛИ КНОПКУ НАЗАД
        self.status_label.setStyleSheet("color: gold;")
        self.status_label.setText("Тест завершён досрочно.")

        self.to_main_btn.show()

        self.progress_anim.stop()
        self.progress_anim.setStartValue(self.progress.value())
        self.progress_anim.setEndValue(100)
        self.progress_anim.start()

        self.fade_in()

    # ======================================================
    def finish_level(self):
        self.hide_buttons()

        self.back_btn.hide()  # УБРАЛИ КНОПКУ НАЗАД
        self.status_label.setStyleSheet("color: gold;")
        self.status_label.setText("Уровень пройден! 🎉")

        self.question_label.setText("")

        self.to_main_btn.show()

        self.progress_anim.stop()
        self.progress_anim.setStartValue(self.progress.value())
        self.progress_anim.setEndValue(100)
        self.progress_anim.start()

        self.fade_in()

    # ======================================================
    def hide_buttons(self):
        for btn in self.buttons:
            btn.hide()
        self.finish_btn.hide()
