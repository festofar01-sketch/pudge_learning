from PyQt5 import QtWidgets, QtCore
from learning_platform.user_service import (
    load_syntax_questions_by_level,
    teacher_load_questions_by_level_and_task,
    teacher_delete_question
)

from ui.add_test_question_dialog import AddTestQuestionDialog
from ui.add_syntax_question_dialog import AddSyntaxQuestionDialog


FORM_WIDTH = 760


def words_to_text(words):
    if isinstance(words, str):
        return " ".join(w.strip() for w in words.strip("{}").split(","))
    return " ".join(words)


class TeacherPanelPage(QtWidgets.QWidget):
    back_to_menu = QtCore.pyqtSignal()

    def __init__(self, user):
        super().__init__()
        self.user = user

        self.current_level = "A1"
        self.current_task = 3  # сразу синтаксис

        self._build_ui()
        self._load_questions()

    # ================= UI =================
    def _build_ui(self):
        outer = QtWidgets.QVBoxLayout(self)
        outer.setAlignment(QtCore.Qt.AlignCenter)

        card = QtWidgets.QWidget()
        card.setFixedWidth(FORM_WIDTH)
        card.setObjectName("Card")

        root = QtWidgets.QVBoxLayout(card)
        root.setSpacing(18)
        root.setContentsMargins(28, 26, 28, 26)

        title = QtWidgets.QLabel("Панель преподавателя")
        title.setObjectName("Title")
        title.setAlignment(QtCore.Qt.AlignCenter)

        subtitle = QtWidgets.QLabel("Управление вопросами")
        subtitle.setAlignment(QtCore.Qt.AlignCenter)

        root.addWidget(title)
        root.addWidget(subtitle)

        self.level_box = QtWidgets.QComboBox()
        self.level_box.addItems(["A1", "A2", "B1", "B2", "C1"])
        self.level_box.currentTextChanged.connect(self._on_level_change)
        root.addWidget(self.level_box)

        self.task_box = QtWidgets.QComboBox()
        self.task_box.addItems([
            "Перевод слов",
            "Вставить слово",
            "Синтаксис"
        ])
        self.task_box.setCurrentIndex(2)
        self.task_box.currentIndexChanged.connect(self._on_task_change)
        root.addWidget(self.task_box)

        self.list = QtWidgets.QListWidget()
        self.list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.list.setFocusPolicy(QtCore.Qt.NoFocus)
        root.addWidget(self.list)

        btns = QtWidgets.QHBoxLayout()

        add_btn = QtWidgets.QPushButton("+ Добавить")
        del_btn = QtWidgets.QPushButton("🗑 Удалить")
        back_btn = QtWidgets.QPushButton("← В меню")

        add_btn.clicked.connect(self._add_question)
        del_btn.clicked.connect(self._delete_question)
        back_btn.clicked.connect(self.back_to_menu.emit)

        btns.addWidget(add_btn)
        btns.addWidget(del_btn)
        btns.addStretch()
        btns.addWidget(back_btn)

        root.addLayout(btns)

        outer.addWidget(card)

    # ================= LOGIC =================
    def _on_level_change(self, level):
        self.current_level = level
        self._load_questions()

    def _on_task_change(self, index):
        self.current_task = index + 1
        self._load_questions()

    def _load_questions(self):
        self.list.clear()

        # --- ТЕСТЫ ---
        if self.current_task in (1, 2):
            data = teacher_load_questions_by_level_and_task(
                self.current_level,
                self.current_task
            )
            for qid, question in data:
                item = QtWidgets.QListWidgetItem(question)
                item.setData(QtCore.Qt.UserRole, qid)
                self.list.addItem(item)

        # --- СИНТАКСИС ---
        else:
            data = load_syntax_questions_by_level(self.current_level)
            for q in data:
                text = words_to_text(q["words"])   # 🔥 ВАЖНО
                item = QtWidgets.QListWidgetItem(text)
                item.setData(QtCore.Qt.UserRole, q["id"])
                self.list.addItem(item)

    def _add_question(self):
        if self.current_task in (1, 2):
            dlg = AddTestQuestionDialog(
                self,
                level=self.current_level,
                task_level=self.current_task
            )
        else:
            dlg = AddSyntaxQuestionDialog(
                self,
                level=self.current_level
            )

        if dlg.exec_():
            self._load_questions()

    def _delete_question(self):
        item = self.list.currentItem()
        if not item:
            return

        qid = item.data(QtCore.Qt.UserRole)
        if self.current_task in (1, 2):
            teacher_delete_question(qid)
        else:
            from learning_platform.user_service import teacher_delete_syntax_question
            teacher_delete_syntax_question(qid)

        self._load_questions()


    # =================================================
    # BUTTONS
    # =================================================
    def _primary_button(self, text):
        btn = QtWidgets.QPushButton(text)
        btn.setFixedHeight(56)
        btn.setObjectName("PrimaryButton")
        btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        return btn

    def _secondary_button(self, text):
        btn = QtWidgets.QPushButton(text)
        btn.setFixedHeight(56)
        btn.setObjectName("SecondaryButton")
        btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        return btn

    def _danger_button(self, text):
        btn = QtWidgets.QPushButton(text)
        btn.setFixedHeight(56)
        btn.setObjectName("DangerButton")
        btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        return btn

    # =================================================
    # STYLES
    # =================================================
    def _apply_styles(self):
        self.setStyleSheet("""
        QWidget {
            background: #f5f7ff;
            font-family: Inter;
        }

        QWidget#Card {
            background: white;
            border-radius: 28px;
        }

        QLabel#Title {
            font-size: 32px;
            font-weight: 800;
            color: #0f172a;
        }

        QLabel#Subtitle {
            font-size: 14px;
            color: #64748b;
        }

        QComboBox {
            padding: 12px 14px;
            border-radius: 22px;
            border: 1px solid #e5e7eb;
            background: white;
            font-size: 15px;
        }

        QListWidget#QuestionList {
            background: #f8fafc;
            border-radius: 22px;
            padding: 10px;
        }

        QListWidget::item {
            background: white;
            border-radius: 16px;
            padding: 12px;
            margin: 6px 0;
        }

        QListWidget::item:selected {
            background: #eef2ff;
        }

        QPushButton {
            border-radius: 28px;
            font-size: 16px;
            font-weight: 600;
        }

        QPushButton#PrimaryButton {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #6366f1,
                stop:1 #22d3ee
            );
            color: white;
        }

        QPushButton#SecondaryButton {
            background: white;
            color: #111827;
        }

        QPushButton#DangerButton {
            background: #fee2e2;
            color: #dc2626;
        }

        QPushButton#DangerButton:hover {
            background: #fecaca;
        }
        """)
