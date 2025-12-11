GLOBAL_STYLE = """
/* Общий фон */
QWidget {
    background-color: #F3F6FB;   /* нежный голубовато-серый */
    font-family: Segoe UI, Arial;
    font-size: 16px;
}

/* Заголовки */
QLabel {
    color: #1D3557;              /* глубокий синий */
}

/* Кнопки */
QPushButton {
    background-color: #4CAF50;   /* зелёный */
    color: white;
    border-radius: 12px;
    padding: 12px;
    font-size: 16px;
    border: none;
}

/* Наведение */
QPushButton:hover {
    background-color: #43A047;
}

/* Нажатие */
QPushButton:pressed {
    background-color: #3D8F41;
}

/* Поля ввода */
QLineEdit {
    background: white;
    border: 2px solid #A8DADC;
    border-radius: 10px;
    padding: 8px;
    font-size: 16px;
}

QLineEdit:focus {
    border: 2px solid #457B9D;
}

/* Прогресс бар */
QProgressBar {
    border: none;
    border-radius: 10px;
    background-color: #DDE6F1;
    height: 16px;
}

QProgressBar::chunk {
    background-color: #4CAF50;
    border-radius: 10px;
}
"""
