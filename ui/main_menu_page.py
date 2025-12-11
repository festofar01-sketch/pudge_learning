from PyQt5 import QtWidgets, QtCore


class MainMenuPage(QtWidgets.QWidget):
    start_learning = QtCore.pyqtSignal()
    open_settings = QtCore.pyqtSignal()
    exit_app = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setAlignment(QtCore.Qt.AlignCenter)

        # ——— КАРТОЧКА ———
        card = QtWidgets.QFrame()
        card.setObjectName("card")
        card.setMinimumWidth(330)

        card_layout = QtWidgets.QVBoxLayout(card)
        card_layout.setAlignment(QtCore.Qt.AlignCenter)
        card_layout.setSpacing(20)

        # ——— ЗАГОЛОВОК ———
        title = QtWidgets.QLabel("Главное меню")
        title.setObjectName("title")
        card_layout.addWidget(title)

        # ——— КНОПКА НАЧАТЬ ОБУЧЕНИЕ ———
        btn_learn = QtWidgets.QPushButton("Начать обучение")
        btn_learn.setObjectName("menuButton")
        btn_learn.clicked.connect(self.start_learning.emit)
        card_layout.addWidget(btn_learn)

        # ——— КНОПКА НАСТРОЙКИ ———
        btn_settings = QtWidgets.QPushButton("Настройки")
        btn_settings.setObjectName("menuButton")
        btn_settings.clicked.connect(self.open_settings.emit)
        card_layout.addWidget(btn_settings)

        # ——— КНОПКА ВЫХОД ———
        btn_exit = QtWidgets.QPushButton("Выход")
        btn_exit.setObjectName("menuButton")
        btn_exit.clicked.connect(self.exit_app.emit)
        card_layout.addWidget(btn_exit)

        # добавляем карточку
        main_layout.addWidget(card)
