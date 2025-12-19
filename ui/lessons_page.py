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
        card.setMaximumWidth(420)

        self.layout = QtWidgets.QVBoxLayout(card)
        self.layout.setSpacing(18)

        # ----- ПРОГРЕСС + СЕРДЕЧКИ -----
        top = QtWidgets.QHBoxLayout()
        top.setAlignment(QtCore.Qt.AlignCenter)

        self.progress = QtWidgets.QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(10)
        self.progress.setFixedWidth(260)

        self.hearts = QtWidgets.QLabel("❤️ ❤️ ❤️")
        self.hearts.setAlignment(QtCore.Qt.AlignRight)
        self.hearts.setStyleSheet("font-size:16px;")

        top.addWidget(self.progress)
        top.addSpacing(12)
        top.addWidget(self.hearts)

        self.layout.addLayout(top)

        # ----- TITLE -----
        self.title = QtWidgets.QLabel("Урок")
        self.title.setObjectName("title")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.title)

        self.number = QtWidgets.QLabel("")
        self.number.setObjectName("subtitle")
        self.number.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.number)

        self.question = QtWidgets.QLabel("")
        self.question.setWordWrap(True)
        self.question.setAlignment(QtCore.Qt.AlignCenter)

        self.question.setStyleSheet("""
            QLabel {
                font-size: 20px;        /* 🔥 меньше */
                font-weight: 700;
                color: #0f172a;
                padding: 4px 8px;
            }
        """)

        self.layout.addWidget(self.question)

        # ----- ОТВЕТЫ -----
        self.buttons = []
        for _ in range(4):
            b = QtWidgets.QPushButton("")
            b.setObjectName("testButton")
            b.setFixedSize(340, 64)
            b.clicked.connect(self.check)

            font = b.font()
            font.setPointSize(15)
            font.setBold(True)
            b.setFont(font)

            self.buttons.append(b)
            self.layout.addWidget(b, alignment=QtCore.Qt.AlignCenter)

        # ----- ДОСРОЧНО -----
        self.finish_btn = QtWidgets.QPushButton("Завершить досрочно")
        self.finish_btn.setObjectName("dangerButton")
        self.finish_btn.setFixedSize(340, 56)
        self.finish_btn.clicked.connect(self.finish_early)
        self.layout.addWidget(self.finish_btn, alignment=QtCore.Qt.AlignCenter)

        self.status = QtWidgets.QLabel("")
        self.status.setAlignment(QtCore.Qt.AlignCenter)
        self.status.setWordWrap(True)

        font = self.status.font()
        font.setPointSize(18)  # 🔥 БОЛЬШОЙ ТЕКСТ
        font.setBold(True)
        self.status.setFont(font)

        self.status.setStyleSheet("""
            QLabel {
                color: #ef4444;
                padding: 12px;
            }
        """)

        self.layout.addWidget(self.status)

        self.menu_btn = QtWidgets.QPushButton("В главное меню")
        self.menu_btn.setObjectName("secondaryButton")
        self.menu_btn.setFixedSize(340, 56)
        self.menu_btn.clicked.connect(self.go_main_menu.emit)
        self.menu_btn.hide()
        self.layout.addWidget(self.menu_btn, alignment=QtCore.Qt.AlignCenter)

        main.addWidget(card)
        main.addStretch()

        # ================== АНИМАЦИИ ==================
        self.opacity = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity)

        self.fade_anim = QtCore.QPropertyAnimation(self.opacity, b"opacity")
        self.fade_anim.setDuration(280)

        self.shake_anim = QtCore.QPropertyAnimation(self, b"pos")
        self.shake_anim.setDuration(160)

    # ================== ВСПОМОГАТЕЛЬНО ==================

    def set_question_text(self, text):
        self.question.setText(text)

        length = len(text)

        # 🔥 ОЧЕНЬ КРУПНЫЕ РАЗМЕРЫ
        if length <= 25:
            size = 30
        elif length <= 45:
            size = 27
        elif length <= 70:
            size = 24
        else:
            size = 21

        font = self.question.font()
        font.setPointSize(size)
        font.setBold(True)
        self.question.setFont(font)

    def update_hearts(self):
        left = max(0, self.MAX_ERRORS - self.wrong_count)
        self.hearts.setText("❤️ " * left)

    # ================== ЛОГИКА (НЕ ТРОГАЛ) ==================

    def load_level(self, name, questions, task_level=1):
        self.level_name = name
        self.questions = questions
        self.task_level = task_level
        self.index = 0
        self.correct_count = 0
        self.wrong_count = 0

        self.progress.show()
        self.progress.setValue(0)
        self.update_hearts()

        for b in self.buttons:
            b.show()
            b.setEnabled(True)

        self.finish_btn.show()
        self.menu_btn.hide()

        self.title.setText("Урок")
        self.status.setText("")
        self.show_question()

    def show_question(self):
        q, answers = self.questions[self.index]

        self.number.setText(f"Вопрос {self.index + 1} из {len(self.questions)}")
        self.set_question_text(q)

        answers = list(answers)
        random.shuffle(answers)

        for b, (text, ok) in zip(self.buttons, answers):
            b.setText(text)
            b.correct = ok
            b.setEnabled(True)

        percent = int((self.index / len(self.questions)) * 100)
        self.progress.setValue(percent)

        self.fade()

    def check(self):
        btn = self.sender()
        self.status.setText("")

        if getattr(btn, "correct", False):
            self.correct_count += 1
            self.index += 1
            QtCore.QTimer.singleShot(120, self.next_step)
        else:
            self.wrong_count += 1
            self.update_hearts()
            self.shake()
            if self.wrong_count >= self.MAX_ERRORS:
                QtCore.QTimer.singleShot(400, self.finish)

    def next_step(self):
        if self.index >= len(self.questions):
            self.finish()
        else:
            self.show_question()

    def finish_early(self):
        self.finish(save=True)

    def finish(self, save=True):
        for b in self.buttons:
            b.hide()

        self.finish_btn.hide()
        self.progress.hide()
        self.menu_btn.show()

        if save:
            self.save_progress.emit(
                self.level_name,
                self.correct_count,
                self.wrong_count,
                len(self.questions)
            )

        # ===== ЗАГОЛОВОК =====
        self.title.setText("Результат")

        # ===== ОПРЕДЕЛЯЕМ ИКОНКУ =====
        success = self.wrong_count < self.MAX_ERRORS

        icon = "🎉" if success else "💔"
        icon_color = "#22c55e" if success else "#ef4444"

        # ===== ОГРОМНЫЙ СМАЙЛИК + ТЕКСТ =====
        self.question.setText(f"""
        <div style="text-align:center; margin-top:10px;">
            <div style="
                font-size:120px;
                line-height:1;
                margin-bottom:20px;
            ">
                {icon}
            </div>

            <div style="
                font-size:28px;
                font-weight:800;
                color:#0f172a;
                margin-bottom:12px;
            ">
                Задание завершено
            </div>

            <div style="
                font-size:18px;
                color:#475569;
            ">
                Правильных: <b>{self.correct_count}</b><br>
                Ошибок: <b>{self.wrong_count}</b>
            </div>
        </div>
        """)

        # 🔥 ФИКСИРУЕМ БОЛЬШОЙ ШРИФТ
        font = self.question.font()
        font.setPointSize(26)
        font.setBold(True)
        self.question.setFont(font)

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
