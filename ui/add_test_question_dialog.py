from PyQt5 import QtWidgets
from learning_platform.user_service import teacher_add_question


class AddTestQuestionDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, level="A1", task_level=1):
        super().__init__(parent)

        # текущее состояние
        self.level = level
        self.task_level = task_level

        self.setWindowTitle("Добавить вопрос")
        self.setFixedSize(540, 680)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(10)

        # ===== STATUS =====
        self.status = QtWidgets.QLabel("")
        self.status.setStyleSheet("color:#dc2626; font-size:13px;")

        # =================================================
        # TOP CONTROLS
        # =================================================
        top = QtWidgets.QHBoxLayout()
        top.setSpacing(12)

        # ----- LEVEL -----
        self.level_box = QtWidgets.QComboBox()
        self.level_box.addItems(["A1", "A2", "B1", "B2", "C1"])
        self.level_box.setCurrentText(self.level)
        self.level_box.currentTextChanged.connect(self._on_level_change)

        # ----- TASK TYPE -----
        self.task_box = QtWidgets.QComboBox()
        self.task_box.addItems([
            "Перевод слов",
            "Вставить слово"
        ])
        self.task_box.setCurrentIndex(self.task_level - 1)
        self.task_box.currentIndexChanged.connect(self._on_task_change)

        top.addWidget(QtWidgets.QLabel("Уровень"))
        top.addWidget(self.level_box)
        top.addSpacing(10)
        top.addWidget(QtWidgets.QLabel("Тип задания"))
        top.addWidget(self.task_box)

        layout.addLayout(top)

        # =================================================
        # QUESTION
        # =================================================
        layout.addWidget(QtWidgets.QLabel("Вопрос"))

        self.question = QtWidgets.QTextEdit()
        self._update_question_placeholder()
        layout.addWidget(self.question)

        # =================================================
        # ANSWERS
        # =================================================
        self.answers = [QtWidgets.QLineEdit() for _ in range(4)]
        for i, a in enumerate(self.answers, start=1):
            a.setPlaceholderText(f"Ответ {i}")
            layout.addWidget(a)

        # =================================================
        # CORRECT
        # =================================================
        layout.addWidget(QtWidgets.QLabel("Правильный ответ (1–4)"))

        self.correct = QtWidgets.QSpinBox()
        self.correct.setRange(1, 4)
        self.correct.setValue(1)
        layout.addWidget(self.correct)

        layout.addWidget(self.status)

        # =================================================
        # SAVE
        # =================================================
        btn = QtWidgets.QPushButton("Сохранить")
        btn.clicked.connect(self.save)
        layout.addWidget(btn)

    # =================================================
    # EVENTS
    # =================================================
    def _on_level_change(self, level):
        self.level = level

    def _on_task_change(self, index):
        self.task_level = index + 1
        self._update_question_placeholder()

    def _update_question_placeholder(self):
        if self.task_level == 1:
            self.question.setPlaceholderText(
                "Введите текст вопроса\nПример: How is 'student' translated?"
            )
        else:
            self.question.setPlaceholderText(
                "Введите предложение с пропуском\nПример: I ___ a student"
            )

    # =================================================
    # SAVE
    # =================================================
    def save(self):
        question_text = self.question.toPlainText().strip()
        answers = [a.text().strip() for a in self.answers]
        correct_answer = self.correct.value()

        self.status.clear()

        if not question_text:
            self.status.setText("Введите текст вопроса")
            return

        if any(not a for a in answers):
            self.status.setText("Все варианты ответов должны быть заполнены")
            return

        try:
            teacher_add_question(
                self.level,
                self.task_level,
                question_text,
                answers[0],
                answers[1],
                answers[2],
                answers[3],
                correct_answer
            )
        except Exception as e:
            self.status.setText("Ошибка сохранения вопроса")
            return

        self.accept()
