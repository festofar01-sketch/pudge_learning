# style.py
# Готовые стили для всех элементов приложения

STYLE_BUTTON = """
QPushButton {
    background-color: #4CAF50;
    color: white;
    padding: 12px;
    font-size: 16px;
    border-radius: 12px;
    border: none;
}
QPushButton:hover {
    background-color: #43A047;
}
QPushButton:pressed {
    background-color: #2E7D32;
}
"""

STYLE_FIELD = """
QLineEdit {
    padding: 12px;
    font-size: 16px;
    border-radius: 10px;
    border: 2px solid #4CAF50;
    background: white;
}
QLineEdit:focus {
    border: 2px solid #2E7D32;
}
"""

STYLE_TITLE = """
QLabel {
    font-size: 28px;
    font-weight: bold;
    color: #2E7D32;
}
"""

STYLE_SUBTITLE = """
QLabel {
    font-size: 18px;
    color: #444;
}
"""

STYLE_CARD = """
QFrame {
    background: rgba(255, 255, 255, 0.92);
    border-radius: 20px;
    padding: 25px;
}
"""

APP_STYLE = """
QWidget {
    background: qlineargradient(
        x1: 0, y1: 0,
        x2: 0, y2: 1,
        stop: 0 #dbffe3,
        stop: 1 #ffffff
    );
    font-family: 'Segoe UI';
}
"""
