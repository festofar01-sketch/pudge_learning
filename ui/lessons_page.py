# lessons_page.py

from PyQt5 import QtWidgets, QtCore
from ui.ui_base import CenterCardPage


class LessonsPage(CenterCardPage):
    lesson_selected = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.add_title("Уроки A1")

        btn = self.add_button("Урок 1: Животные 🐱🐶")
        btn.clicked.connect(self.lesson_selected.emit)
