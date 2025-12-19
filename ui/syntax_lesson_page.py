from PyQt5 import QtWidgets, QtCore, QtGui
import random

# ================== CONSTANTS ==================
CARD_WIDTH = 720
INNER_WIDTH = 560
WORD_HEIGHT = 52
SLOT_HEIGHT = 52
SPACING = 16
MAX_ERRORS = 3


# ================== HELPERS ==================
def parse_words(data):
    if isinstance(data, (list, tuple)):
        return [str(x) for x in data]
    if isinstance(data, str):
        return [w.strip() for w in data.strip("{}").split(",") if w.strip()]
    return []


def calc_cell_width(count):
    spacing = SPACING * (count - 1)
    width = (INNER_WIDTH - spacing) // max(1, count)
    return max(110, min(width, 160))


def grab(widget):
    return widget.grab()


# ================== WORD BANK ==================
class WordBank(QtWidgets.QFrame):
    dropped_from_slot = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setFixedWidth(INNER_WIDTH)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setSpacing(SPACING)
        self.layout.setAlignment(QtCore.Qt.AlignCenter)

    def clear(self):
        while self.layout.count():
            w = self.layout.takeAt(0).widget()
            if w:
                w.deleteLater()

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.acceptProposedAction()

    def dropEvent(self, e):
        self.dropped_from_slot.emit(e.mimeData().text())
        e.acceptProposedAction()


# ================== DRAG WORD ==================
class DraggableWord(QtWidgets.QLabel):
    def __init__(self, text, page, width):
        super().__init__(text)
        self.page = page

        self.setFixedSize(width, WORD_HEIGHT)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setCursor(QtCore.Qt.PointingHandCursor)

        f = self.font()
        f.setBold(True)
        f.setPointSize(14)
        self.setFont(f)

        self.setStyleSheet("""
        QLabel {
            background: #ffffff;
            border-radius: 18px;
            border: 2px solid #e5e7eb;
        }
        QLabel:hover {
            border-color: #6366f1;
            background: #eef2ff;
        }
        """)

    def mousePressEvent(self, e):
        drag = QtGui.QDrag(self)
        mime = QtCore.QMimeData()
        mime.setText(self.text())
        drag.setMimeData(mime)
        drag.setPixmap(grab(self))
        drag.setHotSpot(e.pos())

        if drag.exec_(QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            self.page.on_take_from_bank(self.text())


# ================== SLOT ==================
class DropSlot(QtWidgets.QLabel):
    def __init__(self, page, width):
        super().__init__()
        self.page = page
        self.word = None

        self.setAcceptDrops(True)
        self.setFixedSize(width, SLOT_HEIGHT)
        self.setAlignment(QtCore.Qt.AlignCenter)

        f = self.font()
        f.setBold(True)
        f.setPointSize(14)
        self.setFont(f)

        self.empty_style = """
        QLabel {
            background: #f8fafc;
            border: 2px dashed #c7d2fe;
            border-radius: 18px;
        }
        """
        self.filled_style = """
        QLabel {
            background: #ffffff;
            border: 2px solid #6366f1;
            border-radius: 18px;
        }
        """
        self.setStyleSheet(self.empty_style)

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.acceptProposedAction()

    def dropEvent(self, e):
        if self.word is not None:
            return
        self.word = e.mimeData().text()
        self.setText(self.word)
        self.setStyleSheet(self.filled_style)
        e.acceptProposedAction()

    def mousePressEvent(self, e):
        if not self.word:
            return

        drag = QtGui.QDrag(self)
        mime = QtCore.QMimeData()
        mime.setText(self.word)
        drag.setMimeData(mime)
        drag.setPixmap(grab(self))
        drag.setHotSpot(e.pos())

        if drag.exec_(QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            self.word = None
            self.setText("")
            self.setStyleSheet(self.empty_style)


# ================== MAIN PAGE ==================
class SyntaxLessonPage(QtWidgets.QWidget):
    save_progress = QtCore.pyqtSignal(str, int, int, int)
    go_main_menu = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        # ===== STATE =====
        self.level = ""
        self.questions = []
        self.index = 0
        self.correct = 0
        self.wrong = 0
        self.lives = MAX_ERRORS
        self.is_finished = False
        self.correct_order = []
        self.bank_words = []

        # ===== ROOT =====
        root = QtWidgets.QVBoxLayout(self)
        root.setAlignment(QtCore.Qt.AlignCenter)

        # ===== CARD =====
        self.card = QtWidgets.QFrame()
        self.card.setFixedWidth(CARD_WIDTH)

        self.card_layout = QtWidgets.QVBoxLayout(self.card)
        self.card_layout.setSpacing(18)
        self.card_layout.setContentsMargins(48, 36, 48, 36)

        root.addWidget(self.card)

        # ===== TOP =====
        top = QtWidgets.QHBoxLayout()

        self.progress = QtWidgets.QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(18)

        self.lives_label = QtWidgets.QLabel()
        self.lives_label.setAlignment(QtCore.Qt.AlignRight)
        self.lives_label.setFixedWidth(80)

        top.addWidget(self.progress)
        top.addWidget(self.lives_label)
        self.card_layout.addLayout(top)

        # ===== TITLE =====
        self.title = QtWidgets.QLabel("Собери предложение")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.card_layout.addWidget(self.title)

        self.counter = QtWidgets.QLabel("")
        self.counter.setAlignment(QtCore.Qt.AlignCenter)
        self.card_layout.addWidget(self.counter)

        # ===== SLOTS =====
        self.slots_layout = QtWidgets.QHBoxLayout()
        self.slots_layout.setSpacing(SPACING)
        self.slots_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.card_layout.addLayout(self.slots_layout)

        # ===== BANK =====
        self.bank = WordBank()
        self.bank.dropped_from_slot.connect(self.on_return_to_bank)
        self.card_layout.addWidget(self.bank, alignment=QtCore.Qt.AlignCenter)

        # ===== BUTTONS =====
        self.check_btn = QtWidgets.QPushButton("Проверить")
        self.check_btn.setFixedSize(360, 56)
        self.check_btn.clicked.connect(self.check)
        self.card_layout.addWidget(self.check_btn, alignment=QtCore.Qt.AlignCenter)

        self.finish_btn = QtWidgets.QPushButton("Завершить досрочно")
        self.finish_btn.setFixedSize(360, 56)
        self.finish_btn.clicked.connect(self.finish_early)
        self.card_layout.addWidget(self.finish_btn, alignment=QtCore.Qt.AlignCenter)

        self.status = QtWidgets.QLabel("")
        self.status.setAlignment(QtCore.Qt.AlignCenter)
        self.card_layout.addWidget(self.status)

    # ================== LIVES ==================
    def update_lives_ui(self):
        self.lives_label.setText("❤️" * self.lives + "🤍" * (MAX_ERRORS - self.lives))

    # ================== LOAD ==================
    def load_level(self, level, questions):
        self.level = level

        # 🔥 ЖЁСТКО ПРИВОДИМ К dict
        self.questions = []
        for q in questions:
            if isinstance(q, dict):
                self.questions.append(q)
            else:
                # защита на случай старого формата
                self.questions.append({
                    "sentence": q[1] if len(q) > 1 else "",
                    "words": q[2],
                    "correct_order": q[3]
                })

        self.index = 0
        self.correct = 0
        self.wrong = 0
        self.lives = MAX_ERRORS
        self.is_finished = False

        self.update_lives_ui()
        self.show_question()

    def show_question(self):
        q = self.questions[self.index]

        # ✅ ВОТ ТУТ ТЕПЕРЬ 100% БУДЕТ ТЕКСТ
        self.title.setText(q["sentence"])
        self.status.clear()

        self.correct_order = parse_words(q["correct_order"])
        self.bank_words = parse_words(q["words"])
        random.shuffle(self.bank_words)

        self.counter.setText(f"Вопрос {self.index + 1} из {len(self.questions)}")
        self.progress.setValue(int(self.index / len(self.questions) * 100))

        while self.slots_layout.count():
            w = self.slots_layout.takeAt(0).widget()
            if w:
                w.deleteLater()

        width = calc_cell_width(len(self.correct_order))
        for _ in self.correct_order:
            self.slots_layout.addWidget(DropSlot(self, width))

        self.rebuild_bank(width)

    def rebuild_bank(self, width):
        self.bank.clear()
        for w in self.bank_words:
            self.bank.layout.addWidget(DraggableWord(w, self, width))

    def on_take_from_bank(self, word):
        if word in self.bank_words:
            self.bank_words.remove(word)
        self.rebuild_bank(calc_cell_width(len(self.correct_order)))

    def on_return_to_bank(self, word):
        self.bank_words.append(word)
        self.rebuild_bank(calc_cell_width(len(self.correct_order)))

    def current_answer(self):
        ans = []
        for i in range(self.slots_layout.count()):
            slot = self.slots_layout.itemAt(i).widget()
            if not slot.word:
                return None
            ans.append(slot.word)
        return ans

    # ================== CHECK ==================
    def check(self):
        ans = self.current_answer()
        if ans is None:
            self.status.setText("Заполни все слова")
            return

        if ans == self.correct_order:
            self.correct += 1
            self.index += 1
            if self.index >= len(self.questions):
                self.finish()
            else:
                self.show_question()
        else:
            self.wrong += 1
            self.lives -= 1
            self.update_lives_ui()
            self.status.setText("❌ Неправильно")
            if self.lives <= 0:
                self.finish()

    # ================== FINISH ==================
    def finish_early(self):
        self.finish()

    def finish(self):
        # защита от повторного вызова
        if self.is_finished:
            return
        self.is_finished = True

        # сохраняем прогресс
        self.save_progress.emit(
            self.level,
            self.correct,
            self.wrong,
            len(self.questions)
        )

        # получаем главное окно (НЕ parent!)
        main_window = self.window()

        # передаём данные на страницу результата
        main_window.result_page.set_result(
            correct=self.correct,
            wrong=self.wrong,
            total=len(self.questions),
            lives=self.lives
        )

        # переключаем экран
        main_window.stack.setCurrentWidget(main_window.result_page)