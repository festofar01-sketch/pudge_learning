from PyQt5 import QtWidgets, QtCore
from services.progress_service import get_user_progress


class ProfilePage(QtWidgets.QWidget):

    back_to_menu = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.user = None

        main = QtWidgets.QVBoxLayout(self)
        main.setAlignment(QtCore.Qt.AlignCenter)
        main.setContentsMargins(20, 20, 20, 20)

        card = QtWidgets.QFrame()
        card.setObjectName("card")
        card.setMinimumWidth(360)
        card.setMaximumWidth(400)

        layout = QtWidgets.QVBoxLayout(card)
        layout.setSpacing(14)

        # ===== ЗАГОЛОВОК =====
        title = QtWidgets.QLabel("Профиль")
        title.setObjectName("title")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        self.username_label = QtWidgets.QLabel("")
        self.username_label.setObjectName("subtitle")
        self.username_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.username_label)

        # ===== ТАБЛИЦА =====
        self.table = QtWidgets.QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels([
            "Уровень",
            "Верно",
            "Неверно",
            "Всего",
            "Статус"
        ])

        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        # ===== СТИЛЬ ТАБЛИЦЫ =====
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #0f0f0f;
                gridline-color: #d4af37;
                color: #d4af37;
                border: 1px solid #d4af37;
            }
            QHeaderView::section {
                background-color: #0f0f0f;
                color: #d4af37;
                border: 1px solid #d4af37;
                padding: 4px;
                font-weight: bold;
            }
            QTableWidget::item {
                border: 1px solid #2b2b2b;
                padding: 4px;
            }
        """)

        layout.addWidget(self.table)

        # ===== НАЗАД =====
        back_btn = QtWidgets.QPushButton("Назад")
        back_btn.setObjectName("secondaryButton")
        back_btn.clicked.connect(self.back_to_menu.emit)
        layout.addWidget(back_btn)

        main.addWidget(card)

    # ==========================================
    def set_user(self, user):
        self.user = user
        self.username_label.setText(f"Пользователь: {user.username}")
        self.load_progress()

    # ==========================================
    def load_progress(self):
        rows = get_user_progress(self.user.id)

        # -------- УБИРАЕМ ПОВТОРЫ УРОВНЕЙ --------
        levels = {}

        for level, correct, wrong, total, percent, created_at in rows:
            if level not in levels:
                levels[level] = {
                    "correct": correct,
                    "wrong": wrong,
                    "total": total
                }
            else:
                # берём лучший результат
                levels[level]["correct"] = max(levels[level]["correct"], correct)
                levels[level]["wrong"] = min(levels[level]["wrong"], wrong)

        self.table.setRowCount(len(levels))

        for row_index, (level, data) in enumerate(levels.items()):
            correct = data["correct"]
            wrong = data["wrong"]
            total = data["total"]

            status = "✔ Пройден" if correct == total else "⏳ Не завершён"

            self.table.setItem(row_index, 0, QtWidgets.QTableWidgetItem(level))
            self.table.setItem(row_index, 1, QtWidgets.QTableWidgetItem(str(correct)))
            self.table.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(wrong)))
            self.table.setItem(row_index, 3, QtWidgets.QTableWidgetItem(str(total)))
            self.table.setItem(row_index, 4, QtWidgets.QTableWidgetItem(status))
