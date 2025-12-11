from PyQt5 import QtWidgets, QtCore
from learning_platform.db import fetch_all, execute


class AdminPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.setSpacing(15)

        title = QtWidgets.QLabel("Админ-панель")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; color:#2E7D32;")
        layout.addWidget(title)

        # таблица пользователей
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Логин", "Имя", "Статус"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        layout.addWidget(self.table)

        # кнопки
        btn_refresh = QtWidgets.QPushButton("Обновить список")
        btn_refresh.clicked.connect(self.load_users)

        btn_block = QtWidgets.QPushButton("Заблокировать")
        btn_block.clicked.connect(self.block_user)

        btn_unblock = QtWidgets.QPushButton("Разблокировать")
        btn_unblock.clicked.connect(self.unblock_user)

        btn_delete = QtWidgets.QPushButton("Удалить пользователя")
        btn_delete.clicked.connect(self.delete_user)

        btn_add = QtWidgets.QPushButton("Добавить пользователя")
        btn_add.clicked.connect(self.add_user_dialog)

        # кнопки в линию
        h = QtWidgets.QHBoxLayout()
        for b in (btn_refresh, btn_block, btn_unblock, btn_delete, btn_add):
            h.addWidget(b)
        layout.addLayout(h)

        self.load_users()

    # ------------------ ЛОГИКА ---------------------

    def load_users(self):
        rows = fetch_all("SELECT id, username, full_name, blocked FROM users ORDER BY id")
        self.table.setRowCount(len(rows))

        for i, row in enumerate(rows):
            id_, username, full_name, blocked = row

            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(id_)))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(username))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(full_name or ""))

            status = "Заблокирован" if blocked else "Активен"
            item = QtWidgets.QTableWidgetItem(status)
            item.setForeground(QtCore.Qt.red if blocked else QtCore.Qt.darkGreen)
            self.table.setItem(i, 3, item)

    def get_selected_user_id(self):
        selected = self.table.currentRow()
        if selected < 0:
            return None
        return int(self.table.item(selected, 0).text())

    def block_user(self):
        user_id = self.get_selected_user_id()
        if not user_id:
            return
        execute("UPDATE users SET blocked = TRUE WHERE id = %s", (user_id,))
        self.load_users()

    def unblock_user(self):
        user_id = self.get_selected_user_id()
        if not user_id:
            return
        execute("UPDATE users SET blocked = FALSE WHERE id = %s", (user_id,))
        self.load_users()

    def delete_user(self):
        user_id = self.get_selected_user_id()
        if not user_id:
            return
        execute("DELETE FROM users WHERE id = %s", (user_id,))
        self.load_users()

    def add_user_dialog(self):
        dialog = QtWidgets.QInputDialog()
        dialog.setWindowTitle("Добавить пользователя")
        dialog.setLabelText("Введите логин:")

        if dialog.exec_():
            username = dialog.textValue()
            if username:
                execute(
                    "INSERT INTO users (username, password_hash) VALUES (%s, 'empty')",
                    (username,)
                )
                self.load_users()
