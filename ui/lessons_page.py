from PyQt5 import QtWidgets, QtCore
import random


class LessonPage(QtWidgets.QWidget):

    save_progress = QtCore.pyqtSignal(str, int, int, int)
    go_main_menu = QtCore.pyqtSignal()

    MAX_ERRORS = 3

    def __init__(self):
        super().__init__()

        self.level_name = ""
        self.questions = []
        self.index = 0
        self.correct_count = 0
        self.wrong_count = 0
        self.task_level = 1

        # ================== UI ==================
        main = QtWidgets.QVBoxLayout(self)
        main.setAlignment(QtCore.Qt.AlignCenter)
        main.addStretch()

        card = QtWidgets.QFrame()
        card.setObjectName("card")
        card.setMinimumWidth(360)
        card.setMaximumWidth(380)

        self.layout = QtWidgets.QVBoxLayout(card)
        self.layout.setSpacing(16)

        # ----- НАЗАД -----
        self.back_btn = QtWidgets.QPushButton("← Назад")
        self.back_btn.setObjectName("secondaryButton")
        self.back_btn.setFixedSize(220, 46)   # 🔥 УВЕЛИЧЕНО
        self.back_btn.clicked.connect(self.go_prev)
        self.layout.addWidget(self.back_btn, alignment=QtCore.Qt.AlignCenter)

        # ----- ПРОГРЕСС -----
        self.progress = QtWidgets.QProgressBar()
        self.progress.setObjectName("goldProgress")
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(False)
        self.layout.addWidget(self.progress)

        # ----- ТЕКСТ -----
        self.title = QtWidgets.QLabel("Урок")
        self.title.setObjectName("title")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.title)

        self.number = QtWidgets.QLabel("")
        self.number.setObjectName("subtitle")
        self.number.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.number)

        self.question = QtWidgets.QLabel("")
        self.question.setObjectName("subtitle")
        self.question.setWordWrap(True)
        self.question.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.question)

        # ----- КНОПКИ ОТВЕТОВ -----
        self.buttons = []
        for _ in range(4):
            b = QtWidgets.QPushButton("")
            b.setObjectName("testButton")
            b.setFixedSize(320, 60)        # 🔥 УВЕЛИЧЕНО
            b.clicked.connect(self.check)

            font = b.font()
            font.setPointSize(14)
            font.setBold(True)
            b.setFont(font)

            self.buttons.append(b)
            self.layout.addWidget(b, alignment=QtCore.Qt.AlignCenter)

        # ----- ДОСРОЧНО -----
        self.finish_btn = QtWidgets.QPushButton("Завершить досрочно")
        self.finish_btn.setObjectName("dangerButton")
        self.finish_btn.setFixedSize(320, 54)   # 🔥 УВЕЛИЧЕНО
        self.finish_btn.clicked.connect(self.finish_early)
        self.layout.addWidget(self.finish_btn, alignment=QtCore.Qt.AlignCenter)

        self.status = QtWidgets.QLabel("")
        self.status.setAlignment(QtCore.Qt.AlignCenter)
        self.status.setWordWrap(True)
        font = self.status.font()
        font.setPointSize(10)
        self.status.setFont(font)
        self.layout.addWidget(self.status)

        self.menu_btn = QtWidgets.QPushButton("В главное меню")
        self.menu_btn.setObjectName("secondaryButton")
        self.menu_btn.setFixedSize(320, 54)   # 🔥 УВЕЛИЧЕНО
        self.menu_btn.clicked.connect(self.go_main_menu.emit)
        self.menu_btn.hide()
        self.layout.addWidget(self.menu_btn, alignment=QtCore.Qt.AlignCenter)

        main.addWidget(card)
        main.addStretch()

        # ================== АНИМАЦИИ ==================
        self.opacity = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity)

        self.fade_anim = QtCore.QPropertyAnimation(self.opacity, b"opacity")
        self.fade_anim.setDuration(300)

        self.shake_anim = QtCore.QPropertyAnimation(self, b"pos")
        self.shake_anim.setDuration(180)

    # ================== ЛОГИКА (БЕЗ ИЗМЕНЕНИЙ) ==================

    def load_level(self, name, questions, task_level=1):
        self.level_name = name
        self.questions = questions
        self.task_level = task_level
        self.index = 0
        self.correct_count = 0
        self.wrong_count = 0

        self.progress.show()
        self.progress.setValue(0)

        for b in self.buttons:
            b.show()
            b.setEnabled(True)

        self.finish_btn.show()
        self.menu_btn.hide()
        self.back_btn.hide()

        self.title.setText("Урок")
        self.status.setText("")
        self.question.setText("")

        self.show_question()

    def show_question(self):
        item = self.questions[self.index]

        q, answers = item
        self.number.setText(f"Вопрос {self.index + 1} из {len(self.questions)}")
        self.question.setText(q)

        answers = list(answers)
        random.shuffle(answers)

        for b, (text, ok) in zip(self.buttons, answers):
            b.setText(text)
            b.correct = ok
            b.show()
            b.setEnabled(True)

        percent = int((self.index / len(self.questions)) * 100)
        self.progress.setValue(percent)

        self.fade()

    def check(self):
        btn = self.sender()
        self.status.setText("")

        attempts_left = max(0, self.MAX_ERRORS - self.wrong_count)

        if getattr(btn, "correct", False):
            self.correct_count += 1
            self.status.setText(
                f"<span style='color:#6bff95;'>Правильно ✅</span> | "
                f"Осталось попыток: <b>{attempts_left}</b>"
            )
            self.index += 1
            QtCore.QTimer.singleShot(50, self.next_step)
        else:
            self.wrong_count += 1
            attempts_left = max(0, self.MAX_ERRORS - self.wrong_count)
            self.status.setText(
                f"<span style='color:#ff4d6d;'>Неправильно ❌</span> | "
                f"Осталось попыток: <b>{attempts_left}</b>"
            )
            self.shake()
            if self.wrong_count >= self.MAX_ERRORS:
                QtCore.QTimer.singleShot(600, self.finish)

    def next_step(self):
        if self.index >= len(self.questions):
            self.finish()
        else:
            self.show_question()

    def go_prev(self):
        if self.index <= 0:
            return
        self.index -= 1
        self.status.setText("")
        self.show_question()

    def finish_early(self):
        self.finish(save=True)

    def finish(self, save=True):
        for b in self.buttons:
            b.hide()

        self.finish_btn.hide()
        self.back_btn.hide()
        self.progress.hide()
        self.menu_btn.show()

        if save:
            self.save_progress.emit(
                self.level_name,
                self.correct_count,
                self.wrong_count,
                len(self.questions)
            )

        self.title.setText("Результат")
        icon = "❌" if self.wrong_count >= self.MAX_ERRORS else "✅"
        color = "#ff4d6d" if icon == "❌" else "#6bff95"

        self.question.setText(f"""
        <div style="text-align:center; margin-top:40px;">
            <div style="font-size:72px; color:{color};">
                {icon}
            </div>
        </div>
        """)

        self.fade()

    # ================== АНИМАЦИИ ==================

    def fade(self):
        self.fade_anim.stop()
        self.fade_anim.setStartValue(0)
        self.fade_anim.setEndValue(1)
        self.fade_anim.start()

    def shake(self):
        p = self.pos()
        self.shake_anim.stop()
        self.shake_anim.setKeyValueAt(0, p)
        self.shake_anim.setKeyValueAt(0.25, p + QtCore.QPoint(-8, 0))
        self.shake_anim.setKeyValueAt(0.5, p + QtCore.QPoint(8, 0))
        self.shake_anim.setKeyValueAt(1, p)
        self.shake_anim.start()
