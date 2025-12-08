# ui_base.py

from PyQt5 import QtWidgets, QtCore
from ui.ui_style import STYLE_BUTTON, STYLE_FIELD, STYLE_TITLE, STYLE_CARD


class CenterCardPage(QtWidgets.QWidget):
    """Готовый мобильный шаблон 9:16."""

    def __init__(self):
        super().__init__()

        outer = QtWidgets.QVBoxLayout(self)
        outer.addStretch()

        self.card = QtWidgets.QFrame()
        self.card.setStyleSheet(STYLE_CARD)
        self.card_layout = QtWidgets.QVBoxLayout(self.card)
        self.card_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.card_layout.setSpacing(20)

        outer.addWidget(self.card, alignment=QtCore.Qt.AlignCenter)
        outer.addStretch()

    def add_title(self, text):
        label = QtWidgets.QLabel(text)
        label.setStyleSheet(STYLE_TITLE)
        self.card_layout.addWidget(label)
        return label

    def add_field(self, placeholder):
        field = QtWidgets.QLineEdit()
        field.setPlaceholderText(placeholder)
        field.setFixedWidth(330)
        field.setMinimumHeight(45)
        field.setStyleSheet(STYLE_FIELD)
        self.card_layout.addWidget(field)
        return field

    def add_button(self, text):
        btn = QtWidgets.QPushButton(text)
        btn.setFixedWidth(330)
        btn.setMinimumHeight(45)
        btn.setStyleSheet(STYLE_BUTTON)
        self.card_layout.addWidget(btn)
        return btn

    def add_label(self, text, size=18):
        label = QtWidgets.QLabel(text)
        label.setStyleSheet(f"font-size:{size}px; color:#444;")
        self.card_layout.addWidget(label)
        return label
