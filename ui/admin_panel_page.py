from PyQt5 import QtWidgets, QtCore
from learning_platform.user_service import (
    get_all_users,
    update_user_role,
    delete_user
)

FORM_WIDTH = 720


class AdminPanelPage(QtWidgets.QWidget):
    back_to_menu = QtCore.pyqtSignal()

    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user

        # 🔥 храним несохранённые изменения
        self.pending_roles = {}  # user_id -> role

        self._build_ui()
        self._load_users()

    # =================================================
    # UI
    # =================================================
    def _build_ui(self):
        outer = QtWidgets.QVBoxLayout(self)
        outer.setAlignment(QtCore.Qt.AlignCenter)
        outer.addStretch()

        container = QtWidgets.QWidget()
        container.setFixedWidth(FORM_WIDTH)
        container.setObjectName("Card")

        root = QtWidgets.QVBoxLayout(container)
        root.setSpacing(18)
        root.setContentsMargins(28, 26, 28, 26)

        # ----- HEADER -----
        title = QtWidgets.QLabel("Админ-панель")
        title.setObjectName("Title")
        title.setAlignment(QtCore.Qt.AlignCenter)

        subtitle = QtWidgets.QLabel("Управление пользователями")
        subtitle.setObjectName("Subtitle")
        subtitle.setAlignment(QtCore.Qt.AlignCenter)

        header = QtWidgets.QWidget()
        header.setObjectName("HeaderCard")

        header_layout = QtWidgets.QVBoxLayout(header)
        header_layout.setSpacing(6)
        header_layout.setContentsMargins(24, 20, 24, 20)
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)

        root.addWidget(header)

        # ----- USERS LIST -----
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.content = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content)
        self.content_layout.setSpacing(14)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll.setWidget(self.content)
        root.addWidget(self.scroll, 1)

        # ----- FOOTER -----
        footer = QtWidgets.QHBoxLayout()
        footer.setSpacing(12)

        btn_back = self._secondary_button("← В меню")
        btn_back.clicked.connect(self.back_to_menu.emit)

        btn_save = self._primary_button("Сохранить")
        btn_save.clicked.connect(self._save_changes)

        footer.addWidget(btn_back)
        footer.addStretch()
        footer.addWidget(btn_save)

        root.addLayout(footer)

        outer.addWidget(container)
        outer.addStretch()

        self._apply_styles()

    # =================================================
    # USERS
    # =================================================
    def _load_users(self):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for user in get_all_users():
            self.content_layout.addWidget(self._create_user_card(user))

        self.content_layout.addStretch()

    # =================================================
    # SAVE
    # =================================================
    def _save_changes(self):
        if not self.pending_roles:
            return

        for user_id, role in self.pending_roles.items():
            update_user_role(user_id, role)

        self.pending_roles.clear()
        self._load_users()

    # =================================================
    # USER CARD
    # =================================================
    def _create_user_card(self, user):
        card = QtWidgets.QWidget()
        card.setObjectName("UserCard")

        layout = QtWidgets.QHBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(14)

        # ----- INFO -----
        info = QtWidgets.QVBoxLayout()
        info.setSpacing(6)

        username = QtWidgets.QLabel(user.username)
        username.setObjectName("Username")

        fullname = QtWidgets.QLabel(user.full_name or "")
        fullname.setObjectName("Fullname")

        info.addWidget(username)
        info.addWidget(fullname)

        layout.addLayout(info)
        layout.addStretch()

        # ----- CONTROLS -----
        role = QtWidgets.QComboBox()
        role.addItems(["user", "teacher", "admin"])
        role.setCurrentText(user.role)

        # 🔥 сохраняем ТОЛЬКО локально
        role.currentTextChanged.connect(
            lambda r, uid=user.id: self.pending_roles.__setitem__(uid, r)
        )

        btn_delete = QtWidgets.QPushButton("Удалить")
        btn_delete.setObjectName("DangerButton")
        btn_delete.clicked.connect(
            lambda _, uid=user.id: self._delete(uid)
        )

        controls = QtWidgets.QVBoxLayout()
        controls.setSpacing(8)
        controls.addWidget(role)
        controls.addWidget(btn_delete)

        layout.addLayout(controls)

        return card

    def _delete(self, user_id):
        delete_user(user_id)
        self.pending_roles.pop(user_id, None)
        self._load_users()

    # =================================================
    # BUTTONS
    # =================================================
    def _primary_button(self, text):
        btn = QtWidgets.QPushButton(text)
        btn.setFixedHeight(52)
        btn.setObjectName("PrimaryButton")
        btn.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed
        )
        return btn

    def _secondary_button(self, text):
        btn = QtWidgets.QPushButton(text)
        btn.setFixedHeight(52)
        btn.setObjectName("SecondaryButton")
        btn.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed
        )
        return btn

    # =================================================
    # STYLES
    # =================================================
    def _apply_styles(self):
        self.setStyleSheet("""
        QWidget {
            background: #f5f7ff;
            font-family: Inter;
        }

        QWidget#Card {
            background: white;
            border-radius: 28px;
        }

        QLabel#Title {
            font-size: 30px;
            font-weight: 800;
            color: #0f172a;
        }

        QLabel#Subtitle {
            font-size: 14px;
            color: #64748b;
        }

        QWidget#UserCard {
            background: #f8fafc;
            border: 1px solid #e5e7eb;
            border-radius: 22px;
        }

        QLabel#Username {
            font-size: 16px;
            font-weight: 700;
        }

        QLabel#Fullname {
            font-size: 13px;
            color: #64748b;
        }

        QComboBox {
            padding: 10px 12px;
            border-radius: 18px;
            border: 1px solid #e5e7eb;
            background: white;
            min-width: 150px;
        }

        QPushButton {
            border-radius: 26px;
            font-size: 15px;
            font-weight: 600;
            padding: 12px;
        }

        QPushButton#PrimaryButton {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #6366f1,
                stop:1 #22d3ee
            );
            color: white;
        }

        QPushButton#SecondaryButton {
            background: white;
            border: 1px solid #e5e7eb;
            color: #111827;
        }

        QPushButton#DangerButton {
            background: #fee2e2;
            color: #dc2626;
            border-radius: 20px;
        }
        """)
