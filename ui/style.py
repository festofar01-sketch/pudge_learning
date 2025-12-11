APP_STYLE = """
/* === GLOBAL BLACK–GOLD PREMIUM THEME === */

QWidget {
    background-color: #0D0D0D;          /* глубокий чёрный */
    color: #E8C674;                     /* золотой текст */
    font-family: 'Segoe UI';
}

/* Заголовки */
QLabel {
    font-size: 28px;
    font-weight: bold;
    color: #FFD36B;                     /* яркое премиум-золото */
    qproperty-alignment: AlignCenter;
}

/* Кнопки */
QPushButton {
    background-color: #1A1A1A;          /* чёрный графит */
    color: #FFD36B;
    border: 2px solid #BD9D4D;          /* золотая рамка */
    border-radius: 14px;
    padding: 12px;
    min-width: 260px;
    max-width: 260px;
    font-size: 17px;
}

QPushButton:hover {
    background-color: #262626;
    border-color: #E8C674;
}

QPushButton:pressed {
    background-color: #000000;
    border-color: #967728;
}

/* Поля ввода */
QLineEdit {
    background-color: #111111;
    color: #FFD36B;
    border: 2px solid #BD9D4D;
    border-radius: 10px;
    padding: 8px;
    selection-background-color: #FFD36B;
    selection-color: #000000;
    min-width: 260px;
    max-width: 260px;
}

QLineEdit:focus {
    border-color: #FFD36B;
}

/* Прогресс-бар */
QProgressBar {
    background-color: #1A1A1A;
    border-radius: 10px;
    height: 16px;
    border: 2px solid #BD9D4D;
}

QProgressBar::chunk {
    background-color: #FFD36B;
    border-radius: 10px;
}

/* Scrollbars (если появятся) */
QScrollBar:vertical {
    background: #0D0D0D;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #BD9D4D;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #FFD36B;
}

/* Frame (если используешь) */
QFrame {
    border: none;
}
"""
