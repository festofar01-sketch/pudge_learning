APP_STYLE = """
/* =========================================================
   GLOBAL RESET
========================================================= */
* {
    outline: none;
}

QMainWindow, QWidget {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 #f6f8ff,
        stop:1 #eef2ff
    );
    font-family: "Inter", "Segoe UI", sans-serif;
    color: #0f172a;
    font-size: 14px;
}

/* =========================================================
   REMOVE ALL CARDS / FRAMES
========================================================= */
QFrame {
    background: transparent;
    border: none;
}

#card {
    background: transparent;
    border: none;
}

/* =========================================================
   TITLES & TEXT
========================================================= */
QLabel#title, QLabel#Title {
    font-size: 32px;
    font-weight: 800;
    color: #0f172a;
}

QLabel#subtitle, QLabel#Subtitle {
    font-size: 14px;
    color: #64748b;
}

QLabel {
    background: transparent;
}

/* =========================================================
   INPUTS (LOGIN / FORMS)
========================================================= */
QLineEdit {
    background-color: #ffffff;
    border-radius: 22px;
    border: 2px solid #e5e7eb;
    padding: 16px 18px;
    font-size: 15px;
    color: #0f172a;
}

QLineEdit::placeholder {
    color: #94a3b8;
}

QLineEdit:focus {
    border: 2px solid #6366f1;
    background-color: #ffffff;
}

/* =========================================================
   PRIMARY BUTTON (LOGIN / START / CHECK)
========================================================= */
QPushButton#menuButton,
QPushButton#PrimaryButton {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #6366f1,
        stop:1 #22d3ee
    );
    color: white;
    border: none;
    border-radius: 24px;
    font-size: 17px;
    font-weight: 700;
    padding: 18px;
}

QPushButton#menuButton:hover,
QPushButton#PrimaryButton:hover {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #4f46e5,
        stop:1 #06b6d4
    );
}

QPushButton#menuButton:pressed,
QPushButton#PrimaryButton:pressed {
    background-color: #4338ca;
}

/* =========================================================
   SECONDARY BUTTON
========================================================= */
QPushButton#secondaryButton,
QPushButton#SecondaryButton {
    background-color: #ffffff;
    color: #0f172a;
    border-radius: 24px;
    border: 2px solid #e5e7eb;
    font-size: 16px;
    font-weight: 600;
    padding: 18px;
}

QPushButton#secondaryButton:hover,
QPushButton#SecondaryButton:hover {
    border: 2px solid #6366f1;
    color: #6366f1;
    background-color: #f8fafc;
}

/* =========================================================
   DANGER BUTTON
========================================================= */
QPushButton#dangerButton,
QPushButton#DangerButton {
    background-color: #fee2e2;
    color: #b91c1c;
    border-radius: 24px;
    border: none;
    font-size: 16px;
    font-weight: 700;
    padding: 18px;
}

QPushButton#dangerButton:hover,
QPushButton#DangerButton:hover {
    background-color: #fecaca;
}

/* =========================================================
   TEST / ANSWER BUTTONS
========================================================= */
QPushButton#testButton {
    background-color: #ffffff;
    border-radius: 18px;
    border: 2px solid #e5e7eb;
    padding: 14px 18px;
    font-size: 15px;
    font-weight: 600;
}

QPushButton#testButton:hover {
    border: 2px solid #6366f1;
    color: #6366f1;
}

/* =========================================================
   PROGRESS BAR
========================================================= */
QProgressBar {
    background-color: #e5e7eb;
    border-radius: 10px;
    height: 10px;
}

QProgressBar::chunk {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #6366f1,
        stop:1 #22d3ee
    );
    border-radius: 10px;
}

/* =========================================================
   LISTS / SCROLL
========================================================= */
QScrollArea {
    border: none;
    background: transparent;
}

QScrollBar:vertical {
    background: transparent;
    width: 10px;
}

QScrollBar::handle:vertical {
    background: #c7d2fe;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background: #a5b4fc;
}

/* =========================================================
   MESSAGE / STATUS TEXT
========================================================= */
QLabel#status {
    font-size: 14px;
    color: #334155;
}

/* =========================================================
   CHECKBOX / RADIO (на будущее)
========================================================= */
QCheckBox {
    spacing: 10px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
}

QCheckBox::indicator:unchecked {
    border-radius: 6px;
    border: 2px solid #c7d2fe;
    background: white;
}

QCheckBox::indicator:checked {
    border-radius: 6px;
    border: 2px solid #6366f1;
    background: #6366f1;
}

/* =========================================================
   TOOLTIP
========================================================= */
QToolTip {
    background-color: #0f172a;
    color: white;
    border-radius: 8px;
    padding: 6px 10px;
    font-size: 12px;
}

/* =========================================================
   DISABLED STATE
========================================================= */
QPushButton:disabled {
    background: #e5e7eb;
    color: #94a3b8;
    border: none;
}
"""
