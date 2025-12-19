APP_STYLE = """
/* =========================================================
   GLOBAL RESET & BASE
========================================================= */
* {
    outline: none;
}

QMainWindow, QWidget {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 #f6f8ff,
        stop:1 #eef2ff
    );
    font-family: "Inter", "Segoe UI", sans-serif;
    color: #0f172a;
}

/* =========================================================
   BASE LABEL (ВАЖНО: БЕЗ font-size)
========================================================= */
QLabel {
    background: transparent;
}

/* =========================================================
   TYPOGRAPHY
========================================================= */
QLabel#title, QLabel#Title {
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -0.5px;
}

QLabel#subtitle, QLabel#Subtitle {
    font-size: 16px;
    color: #64748b;
}

QLabel#status {
    font-size: 16px;
    color: #334155;
}

/* =========================================================
   RESULT SCREEN (ВОТ ГЛАВНОЕ)
========================================================= */
QLabel#ResultTitle {
    font-size: 40px;
    font-weight: 900;
    qproperty-alignment: AlignCenter;
}

QLabel#ResultSubtitle {
    font-size: 18px;
    color: #64748b;
    qproperty-alignment: AlignCenter;
}

QLabel#ResultIcon {
    font-size: 96px;
    qproperty-alignment: AlignCenter;
}

QLabel#ResultStats {
    font-size: 22px;
    font-weight: 700;
    qproperty-alignment: AlignCenter;
}

/* =========================================================
   CARDS
========================================================= */
QFrame#card {
    background: #ffffff;
    border-radius: 28px;
    border: 1px solid #e5e7eb;
}

/* =========================================================
   BUTTONS (без изменений)
========================================================= */
QPushButton {
    border: none;
    border-radius: 26px;
    font-size: 16px;
    font-weight: 600;
    padding: 18px;
}

QPushButton#PrimaryButton,
QPushButton#menuButton {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #6366f1,
        stop:1 #22d3ee
    );
    color: white;
    font-size: 17px;
    font-weight: 700;
}

QPushButton#secondaryButton {
    background: #ffffff;
    border: 2px solid #e5e7eb;
}

QPushButton#dangerButton {
    background: #fee2e2;
    color: #b91c1c;
}

/* =========================================================
   PROGRESS
========================================================= */
QProgressBar {
    background: #e5e7eb;
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

/* ================= ADMIN TABLE ================= */

QTableWidget#AdminTable {
    background: white;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    gridline-color: #e5e7eb;
    font-size: 14px;
}

QTableWidget#AdminTable::item {
    padding: 12px;
}

QTableWidget#AdminTable::item:selected {
    background: #eef2ff;
}

QHeaderView::section {
    background: #f8fafc;
    border: none;
    font-weight: 700;
    color: #0f172a;
    padding: 10px;
}

/* === ROLE SELECT === */
QComboBox#RoleBox {
    border-radius: 12px;
    padding: 6px 10px;
    border: 1px solid #e5e7eb;
    background: white;
}

QComboBox#RoleBox:hover {
    border: 1px solid #6366f1;
}

/* === SMALL BUTTONS === */
QPushButton#PrimaryButtonSmall {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #6366f1,
        stop:1 #22d3ee
    );
    color: white;
    border-radius: 14px;
    padding: 8px 12px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton#DangerButtonSmall {
    background: #fee2e2;
    color: #dc2626;
    border-radius: 14px;
    padding: 8px 12px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton#DangerButtonSmall:hover {
    background: #fecaca;
}

"""
