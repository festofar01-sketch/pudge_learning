from ui.ui_base import CenterCardPage
from PyQt5 import QtCore
from data import LEVELS


class TopicsPage(CenterCardPage):
    topic_selected = QtCore.pyqtSignal(str, str)  # уровень, тема

    def __init__(self):
        super().__init__()
        self.level = None

    def set_level(self, level):
        self.level = level
        self.card_layout.setSpacing(20)

        # очищаем старые кнопки
        while self.card_layout.count() > 0:
            item = self.card_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # заголовок уровня
        self.add_title(f"Темы уровня {level}")

        # темы
        for topic_name in LEVELS[level].keys():
            btn = self.add_button(topic_name.capitalize())
            btn.clicked.connect(
                lambda checked, T=topic_name: self.topic_selected.emit(self.level, T)
            )
