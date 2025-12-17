from PyQt5 import QtWidgets, QtCore, QtGui
import random
from math import floor


# =========================
#   CONSTANTS / SIZES
# =========================
CARD_WIDTH = 640
BANK_INNER_WIDTH = 560

WORD_W = 130
WORD_H = 52
SLOT_W = 130
SLOT_H = 52

H_SPACING = 14
V_SPACING = 14

MAX_ERRORS = 3


# =========================
#   HELPERS
# =========================
def _parse_words(data):
    """
    Поддерживает:
    - list/tuple: ["I","am","a","student"]
    - str: "{I,am,a,student}" или "I,am,a,student"
    """
    if data is None:
        return []

    if isinstance(data, (list, tuple)):
        return [str(x) for x in data]

    if isinstance(data, str):
        s = data.strip()
        if s.startswith("{") and s.endswith("}"):
            s = s[1:-1]
        parts = [p.strip() for p in s.split(",")]
        return [p for p in parts if p]

    return [str(data)]


def _make_drag_pixmap(widget: QtWidgets.QWidget):
    return widget.grab()


# =========================
#   DROP TARGET: WORD BANK
# =========================
class WordBankArea(QtWidgets.QFrame):
    dropped_from_slot = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setObjectName("wordBankFrame")
        self.setFixedWidth(BANK_INNER_WIDTH)

        outer = QtWidgets.QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        self.grid_host = QtWidgets.QWidget()
        self.grid = QtWidgets.QGridLayout(self.grid_host)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setHorizontalSpacing(H_SPACING)
        self.grid.setVerticalSpacing(V_SPACING)
        self.grid.setAlignment(QtCore.Qt.AlignCenter)

        outer.addWidget(self.grid_host, alignment=QtCore.Qt.AlignCenter)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            self.dropped_from_slot.emit(event.mimeData().text())
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()

    def clear(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _cols(self):
        usable = BANK_INNER_WIDTH
        cell = WORD_W + H_SPACING
        return max(1, floor((usable + H_SPACING) / cell))

    def add_words(self, widgets):
        cols = self._cols()
        r, c = 0, 0
        for w in widgets:
            self.grid.addWidget(w, r, c, alignment=QtCore.Qt.AlignCenter)
            c += 1
            if c >= cols:
                c = 0
                r += 1


# =========================
#   DRAG SOURCE: WORD
# =========================
class DraggableWord(QtWidgets.QLabel):
    """
    Слово в банке:
    - перетаскивается в слот
    - если перенос успешный -> сообщаем странице, что слово "взяли" из банка
    """
    def __init__(self, text: str, page):
        super().__init__(text)
        self.page = page

        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setFixedSize(WORD_W, WORD_H)

        f = self.font()
        f.setPointSize(14)
        f.setBold(True)
        self.setFont(f)

        self.setStyleSheet("""
            QLabel {
                border: 2px solid #f5c542;
                border-radius: 12px;
                background: #1e1e1e;
                color: #f5c542;
                padding-left: 6px;
                padding-right: 6px;
            }
        """)

    def mousePressEvent(self, event):
        if event.button() != QtCore.Qt.LeftButton:
            return

        drag = QtGui.QDrag(self)
        mime = QtCore.QMimeData()
        mime.setText(self.text())
        mime.setProperty("source_type", "bank")
        drag.setMimeData(mime)

        drag.setPixmap(_make_drag_pixmap(self))
        drag.setHotSpot(event.pos())

        result = drag.exec_(QtCore.Qt.MoveAction)

        # ВАЖНО: если drop успешный, слово должно исчезнуть ИЗ МОДЕЛИ банка
        if result == QtCore.Qt.MoveAction:
            self.page.on_word_taken_from_bank(self.text())


# =========================
#   DROP SLOT (drag back)
# =========================
class DropSlot(QtWidgets.QLabel):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.word = None

        self.setAcceptDrops(True)
        self.setFixedSize(SLOT_W, SLOT_H)
        self.setAlignment(QtCore.Qt.AlignCenter)

        f = self.font()
        f.setPointSize(14)
        f.setBold(True)
        self.setFont(f)

        self.empty_style = """
            QLabel {
                border: 2px dashed #f5c542;
                border-radius: 12px;
                background: #111;
            }
        """
        self.filled_style = """
            QLabel {
                border: 2px solid #f5c542;
                border-radius: 12px;
                background: #1e1e1e;
                color: #f5c542;
                padding-left: 6px;
                padding-right: 6px;
            }
        """
        self.setStyleSheet(self.empty_style)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if self.word is not None:
            return
        if not event.mimeData().hasText():
            return

        self.word = event.mimeData().text()
        self.setText(self.word)
        self.setStyleSheet(self.filled_style)

        event.setDropAction(QtCore.Qt.MoveAction)
        event.accept()

    def mousePressEvent(self, event):
        # Перетаскиваем слово из слота обратно в банк
        if event.button() != QtCore.Qt.LeftButton or not self.word:
            return

        drag = QtGui.QDrag(self)
        mime = QtCore.QMimeData()
        mime.setText(self.word)
        mime.setProperty("source_type", "slot")
        drag.setMimeData(mime)

        drag.setPixmap(_make_drag_pixmap(self))
        drag.setHotSpot(event.pos())

        result = drag.exec_(QtCore.Qt.MoveAction)

        # Если реально утащили (drop принят банком)
        if result == QtCore.Qt.MoveAction:
            # слот очищаем
            self.word = None
            self.setText("")
            self.setStyleSheet(self.empty_style)
            # добавление в банк сделает bank.dropEvent -> page.on_drop_back_to_bank


# =========================
#   MAIN PAGE
# =========================
class SyntaxLessonPage(QtWidgets.QWidget):
    save_progress = QtCore.pyqtSignal(str, int, int, int)
    go_main_menu = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.level_name = ""
        self.questions = []
        self.index = 0
        self.correct = 0
        self.wrong = 0
        self.correct_order = []

        # банк хранит ТОЛЬКО доступные слова (не спрятанные виджеты)
        self._bank_words = []

        # ========== OUTER ==========
        outer = QtWidgets.QVBoxLayout(self)
        outer.setAlignment(QtCore.Qt.AlignCenter)
        outer.addStretch()

        # ========== CARD ==========
        self.card = QtWidgets.QFrame()
        self.card.setObjectName("card")
        self.card.setFixedWidth(CARD_WIDTH)

        self.card_layout = QtWidgets.QVBoxLayout(self.card)
        self.card_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.card_layout.setSpacing(16)
        self.card_layout.setContentsMargins(30, 24, 30, 24)

        # чтобы не прыгало
        self.card_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        # progress
        self.progress = QtWidgets.QProgressBar()
        self.progress.setObjectName("goldProgress")
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(False)
        self.progress.setFixedWidth(BANK_INNER_WIDTH)
        self.card_layout.addWidget(self.progress, alignment=QtCore.Qt.AlignCenter)

        self.title = QtWidgets.QLabel("Собери предложение")
        self.title.setObjectName("title")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.card_layout.addWidget(self.title)

        self.counter = QtWidgets.QLabel("")
        self.counter.setObjectName("subtitle")
        self.counter.setAlignment(QtCore.Qt.AlignCenter)
        self.card_layout.addWidget(self.counter)

        # slots
        self.slots_host = QtWidgets.QWidget()
        self.slots_host.setFixedWidth(BANK_INNER_WIDTH)
        self.slots_layout = QtWidgets.QHBoxLayout(self.slots_host)
        self.slots_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.slots_layout.setSpacing(H_SPACING)
        self.slots_layout.setContentsMargins(0, 0, 0, 0)
        self.card_layout.addWidget(self.slots_host, alignment=QtCore.Qt.AlignCenter)

        # bank
        self.bank = WordBankArea()
        self.bank.dropped_from_slot.connect(self.on_drop_back_to_bank)
        self.card_layout.addWidget(self.bank, alignment=QtCore.Qt.AlignCenter)

        # buttons
        self.check_btn = QtWidgets.QPushButton("Проверить")
        self.check_btn.setObjectName("menuButton")
        self.check_btn.setFixedSize(320, 54)
        self.check_btn.clicked.connect(self.check)
        self.card_layout.addWidget(self.check_btn, alignment=QtCore.Qt.AlignCenter)

        self.finish_btn = QtWidgets.QPushButton("Завершить досрочно")
        self.finish_btn.setObjectName("dangerButton")
        self.finish_btn.setFixedSize(320, 54)
        self.finish_btn.clicked.connect(self.finish_early)
        self.card_layout.addWidget(self.finish_btn, alignment=QtCore.Qt.AlignCenter)

        self.status = QtWidgets.QLabel("")
        self.status.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop
        )

        self.status.setWordWrap(True)
        self.status.setFixedHeight(56)  # фикс дёрганья
        self.card_layout.addWidget(self.status)

        self.menu_btn = QtWidgets.QPushButton("В главное меню")
        self.menu_btn.setObjectName("secondaryButton")
        self.menu_btn.setFixedSize(320, 54)
        self.menu_btn.clicked.connect(self.go_main_menu.emit)
        self.menu_btn.hide()
        self.card_layout.addWidget(self.menu_btn, alignment=QtCore.Qt.AlignCenter)

        outer.addWidget(self.card, alignment=QtCore.Qt.AlignCenter)
        outer.addStretch()

        # ========== ANIM ==========
        self.opacity = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity)

        self.fade_anim = QtCore.QPropertyAnimation(self.opacity, b"opacity")
        self.fade_anim.setDuration(260)

        self.shake_anim = QtCore.QPropertyAnimation(self, b"pos")
        self.shake_anim.setDuration(180)

    # =========================
    #   LOADING
    # =========================
    def load_level(self, level_name, questions):
        self.level_name = level_name
        self.questions = questions or []
        self.index = 0
        self.correct = 0
        self.wrong = 0

        self.menu_btn.hide()
        self.check_btn.show()
        self.finish_btn.show()
        self.progress.show()
        self.progress.setValue(0)

        self.status.setText("")
        self._show_question()

    def _question_to_words(self, q):
        # q ожидается dict: {"words":..., "correct_order":...}
        words = _parse_words(q.get("words"))
        correct = _parse_words(q.get("correct_order"))
        return words, correct

    # =========================
    #   UI BUILDERS
    # =========================
    def _clear_layout_widgets(self, layout: QtWidgets.QLayout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _rebuild_bank(self):
        self.bank.clear()
        widgets = [DraggableWord(w, self) for w in self._bank_words]
        self.bank.add_words(widgets)

    def _show_question(self):
        if not self.questions:
            self.status.setText("<span style='color:#ff4d6d;'>Нет заданий.</span>")
            self.finish(save=False)
            return

        q = self.questions[self.index]
        words, correct = self._question_to_words(q)

        if not words or not correct:
            self.status.setText("<span style='color:#ff4d6d;'>Ошибка данных вопроса.</span>")
            self.finish(save=False)
            return

        self.correct_order = correct[:]

        # банк = ВСЕ слова этого вопроса (дубликаты допускаются!)
        self._bank_words = words[:]
        random.shuffle(self._bank_words)

        self.counter.setText(f"Задание {self.index + 1} из {len(self.questions)}")

        percent = int((self.index / max(1, len(self.questions))) * 100)
        self.progress.setValue(percent)

        left = max(0, MAX_ERRORS - self.wrong)
        self.status.setText(f"Осталось попыток: <b>{left}</b>")

        # slots
        self._clear_layout_widgets(self.slots_layout)
        for _ in range(len(self.correct_order)):
            self.slots_layout.addWidget(DropSlot(self), alignment=QtCore.Qt.AlignCenter)

        # bank
        self._rebuild_bank()
        self.fade()

    # =========================
    #   BANK MODEL SYNC
    # =========================
    def on_word_taken_from_bank(self, text: str):
        """
        Слово успешно ушло из банка в слот -> убираем его из списка доступных.
        (убираем одну штуку, даже если есть дубликаты)
        """
        try:
            self._bank_words.remove(text)
        except ValueError:
            pass
        self._rebuild_bank()

    def on_drop_back_to_bank(self, text: str):
        """
        Слово успешно вернули в банк (drag из слота в область банка)
        """
        self._bank_words.append(text)
        self._rebuild_bank()

    # =========================
    #   CHECK / FINISH
    # =========================
    def _current_answer(self):
        ans = []
        for i in range(self.slots_layout.count()):
            slot = self.slots_layout.itemAt(i).widget()
            if not slot.word:
                return None
            ans.append(slot.word)
        return ans

    def check(self):
        answer = self._current_answer()
        if answer is None:
            self.status.setText("⚠️ Заполни все поля")
            return

        if answer == self.correct_order:
            self.correct += 1
            self.index += 1

            if self.index >= len(self.questions):
                self.finish(save=True)
            else:
                self._show_question()
        else:
            self.wrong += 1
            left = max(0, MAX_ERRORS - self.wrong)
            self.status.setText(
                f"<span style='color:#ff4d6d;'><b>❌ Неправильно</b></span> | "
                f"Осталось попыток: <b>{left}</b>"
            )
            self.shake()

            if self.wrong >= MAX_ERRORS:
                QtCore.QTimer.singleShot(250, lambda: self.finish(save=True))

    def finish_early(self):
        self.finish(save=True)

    def finish(self, save=True):
        self._clear_layout_widgets(self.slots_layout)
        self.bank.clear()
        self.check_btn.hide()
        self.finish_btn.hide()
        self.progress.hide()

        self.menu_btn.show()

        if save:
            self.save_progress.emit(
                self.level_name,
                self.correct,
                self.wrong,
                len(self.questions)
            )

        icon = "❌" if self.wrong >= MAX_ERRORS else "✅"
        color = "#ff4d6d" if icon == "❌" else "#6bff95"

        self.status.setText(f"""
        <div style="margin-top:-150px; font-size:72px; color:{color}; text-align:center;">
            {icon}
        </div>

        <div style="margin-top:12px; font-size:14px; text-align:center;">
            Правильных: <b>{self.correct}</b> &nbsp;|&nbsp;
            Ошибок: <b>{self.wrong}</b>
        </div>
        """)

        self.fade()

    # =========================
    #   ANIMATIONS
    # =========================
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
