from PyQt5 import QtWidgets, QtCore


class LevelsPage(QtWidgets.QWidget):

    level_selected = QtCore.pyqtSignal(str)
    back_to_menu = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        # ===== ОСНОВНОЙ ЛЕЙАУТ =====
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.setSpacing(20)

        # ===== ЗАГОЛОВОК =====
        title = QtWidgets.QLabel("Выберите уровень языка")
        title.setObjectName("title")
        title.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(title)

        # ===== КОНТЕЙНЕР ДЛЯ КНОПОК =====
        self.buttons_layout = QtWidgets.QVBoxLayout()
        self.buttons_layout.setAlignment(QtCore.Qt.AlignCenter)   # 🔥 ВАЖНО
        self.buttons_layout.setSpacing(14)

        main_layout.addLayout(self.buttons_layout)

        # ===== КНОПКА НАЗАД =====
        back_btn = QtWidgets.QPushButton("← Назад")
        back_btn.setObjectName("secondaryButton")
        back_btn.setFixedWidth(260)
        back_btn.clicked.connect(self.back_to_menu.emit)
        main_layout.addWidget(back_btn, alignment=QtCore.Qt.AlignCenter)

    # ==================================
    #        ЗАГРУЗКА УРОВНЕЙ
    # ==================================
    def load_levels(self, level_list):
        # очистить старые кнопки
        while self.buttons_layout.count():
            item = self.buttons_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # создать новые
        for code, name in level_list:
            btn = QtWidgets.QPushButton(f"{code} — {name}")
            btn.setObjectName("menuButton")
            btn.setFixedWidth(260)                    # 🔥 одинаковая ширина
            btn.clicked.connect(lambda _, c=code: self.level_selected.emit(c))

            # 🔥 добавляем С ВЫРАВНИВАНИЕМ
            self.buttons_layout.addWidget(
                btn,
                alignment=QtCore.Qt.AlignCenter
            )
