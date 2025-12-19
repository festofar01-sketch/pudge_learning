from PyQt5 import QtWidgets, QtCore


class ResultPage(QtWidgets.QWidget):
    go_main_menu = QtCore.pyqtSignal()

    MAX_ERRORS = 3

    def __init__(self):
        super().__init__()

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
        self.progress.hide()  # на результате не нужен

        self.hearts = QtWidgets.QLabel()
        self.hearts.setAlignment(QtCore.Qt.AlignRight)
        self.hearts.setStyleSheet("font-size:16px;")

        top.addWidget(self.progress)
        top.addSpacing(12)
        top.addWidget(self.hearts)

        self.layout.addLayout(top)

        # ----- TITLE -----
        self.title = QtWidgets.QLabel("Результат")
        self.title.setObjectName("title")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.title)

        self.number = QtWidgets.QLabel("")
        self.number.setObjectName("subtitle")
        self.number.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.number)

        # ----- CONTENT -----
        self.content = QtWidgets.QLabel("")
        self.content.setWordWrap(True)
        self.content.setAlignment(QtCore.Qt.AlignCenter)

        self.content.setStyleSheet("""
            QLabel {
                font-size: 26px;
                font-weight: 700;
                color: #0f172a;
                padding: 4px 8px;
            }
        """)

        self.layout.addWidget(self.content)

        # ----- BUTTON -----
        self.menu_btn = QtWidgets.QPushButton("В главное меню")
        self.menu_btn.setObjectName("secondaryButton")
        self.menu_btn.setFixedSize(340, 56)
        self.menu_btn.clicked.connect(self.go_main_menu.emit)
        self.layout.addWidget(self.menu_btn, alignment=QtCore.Qt.AlignCenter)

        main.addWidget(card)
        main.addStretch()

        # ================== АНИМАЦИЯ ==================
        self.opacity = QtWidgets.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity)

        self.fade_anim = QtCore.QPropertyAnimation(self.opacity, b"opacity")
        self.fade_anim.setDuration(280)

    # ================== API ==================
    def set_result(self, *, correct, wrong, total, lives):
        # ----- HEARTS -----
        self.hearts.setText("❤️ " * lives)

        # ----- SUBTITLE -----
        self.number.setText(f"Вопрос {total} из {total}")

        # ----- SUCCESS / FAIL -----
        success = wrong < self.MAX_ERRORS
        icon = "🎉" if success else "💔"

        # ----- CONTENT -----
        self.content.setText(f"""
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
                Правильных: <b>{correct}</b><br>
                Ошибок: <b>{wrong}</b>
            </div>
        </div>
        """)

        self.fade()

    # ================== ANIMATION ==================
    def fade(self):
        self.fade_anim.stop()
        self.fade_anim.setStartValue(0)
        self.fade_anim.setEndValue(1)
        self.fade_anim.start()
