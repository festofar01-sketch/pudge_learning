from PyQt5 import QtWidgets, QtCore
from services.progress_service import get_user_progress

FORM_WIDTH = 420


class ProfilePage(QtWidgets.QWidget):
    back_to_menu = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.user = None
        self._build_ui()
        self._apply_styles()

    # ================= UI =================
    def _build_ui(self):
        self.main = QtWidgets.QVBoxLayout(self)
        self.main.setAlignment(QtCore.Qt.AlignCenter)
        self.main.setContentsMargins(40, 40, 40, 40)
        self.main.setSpacing(26)

        container = QtWidgets.QWidget()
        container.setFixedWidth(FORM_WIDTH)

        layout = QtWidgets.QVBoxLayout(container)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.setSpacing(24)

        # ===== HEADER =====
        title = QtWidgets.QLabel("Профиль")
        title.setObjectName("Title")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        self.username_label = QtWidgets.QLabel("")
        self.username_label.setObjectName("Subtitle")
        self.username_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.username_label)

        # ===== STATS CARD =====
        stats_card = QtWidgets.QFrame()
        stats_card.setObjectName("StatsCard")

        stats_layout = QtWidgets.QGridLayout(stats_card)
        stats_layout.setContentsMargins(24, 24, 24, 24)
        stats_layout.setSpacing(18)

        total_w, self.total_levels_value = self._stat_block("Всего уровней", "0")
        done_w, self.completed_levels_value = self._stat_block("Завершено", "0")
        ok_w, self.correct_answers_value = self._stat_block("Правильных", "0")
        bad_w, self.wrong_answers_value = self._stat_block("Ошибок", "0")

        stats_layout.addWidget(total_w, 0, 0)
        stats_layout.addWidget(done_w, 0, 1)
        stats_layout.addWidget(ok_w, 1, 0)
        stats_layout.addWidget(bad_w, 1, 1)

        layout.addWidget(stats_card)

        # ===== BACK =====
        back_btn = QtWidgets.QPushButton("Назад в меню")
        back_btn.setObjectName("BackButton")
        back_btn.setFixedHeight(58)
        back_btn.clicked.connect(self.back_to_menu.emit)
        layout.addWidget(back_btn)

        self.main.addWidget(container)

    # ================= LOGIC =================
    def set_user(self, user):
        self.user = user
        self.username_label.setText(f"Пользователь: {user.username}")
        self.load_progress()

    def load_progress(self):
        rows = get_user_progress(self.user.id)

        levels = {}
        for level, correct, wrong, total, percent, created_at in rows:
            if level not in levels:
                levels[level] = {
                    "correct": correct,
                    "wrong": wrong,
                    "total": total
                }
            else:
                levels[level]["correct"] = max(levels[level]["correct"], correct)
                levels[level]["wrong"] = min(levels[level]["wrong"], wrong)

        total_correct = sum(d["correct"] for d in levels.values())
        total_wrong = sum(d["wrong"] for d in levels.values())
        completed = sum(1 for d in levels.values() if d["correct"] == d["total"])

        self.total_levels_value.setText(str(len(levels)))
        self.completed_levels_value.setText(str(completed))
        self.correct_answers_value.setText(str(total_correct))
        self.wrong_answers_value.setText(str(total_wrong))

    # ================= UI PARTS =================
    def _stat_block(self, title, value):
        card = QtWidgets.QFrame()
        card.setObjectName("MiniCard")

        layout = QtWidgets.QVBoxLayout(card)
        layout.setSpacing(8)
        layout.setContentsMargins(16, 14, 16, 14)

        lbl = QtWidgets.QLabel(title)
        lbl.setObjectName("StatLabel")

        val = QtWidgets.QLabel(value)
        val.setObjectName("StatValue")

        layout.addWidget(lbl)
        layout.addWidget(val)

        return card, val

    # ================= STYLES =================
    def _apply_styles(self):
        self.setStyleSheet("""
        QWidget {
            background: #f5f7ff;
            font-family: Inter;
        }

        QLabel#Title {
            font-size: 32px;
            font-weight: 900;
            color: #0f172a;
        }

        QLabel#Subtitle {
            font-size: 14px;
            color: #64748b;
            margin-bottom: 8px;
        }

        /* ===== MAIN CARD ===== */
        QFrame#StatsCard {
            background: white;
            border-radius: 28px;
            border: 1px solid #e5e7eb;
        }

        /* ===== MINI CARDS ===== */
        QFrame#MiniCard {
            background: #f8fafc;
            border-radius: 20px;
            border: 1px solid #e5e7eb;
        }

        QLabel#StatLabel {
            font-size: 12px;
            color: #94a3b8;
        }

        QLabel#StatValue {
            font-size: 28px;
            font-weight: 900;
            color: #0f172a;
        }

        /* ===== BUTTON ===== */
        QPushButton#BackButton {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #6366f1,
                stop:1 #22d3ee
            );
            color: white;
            border-radius: 26px;
            font-size: 16px;
            font-weight: 700;
        }

        QPushButton#BackButton:hover {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #4f46e5,
                stop:1 #0ea5e9
            );
        }
        """)
