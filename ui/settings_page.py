from PyQt5 import QtWidgets, QtCore
from learning_platform.services import (
    update_username,
    update_password,
    update_fullname,
    delete_user,
)


class SettingsPage(QtWidgets.QWidget):

    # специальный сигнал для выхода из аккаунта → MainWindow
    logout_signal = QtCore.pyqtSignal()
    back_to_menu = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.current_user = None  # сюда MainWindow передает user

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setAlignment(QtCore.Qt.AlignCenter)

        # ===== КАРТОЧКА =====
        card = QtWidgets.QFrame()
        card.setObjectName("card")
        card.setMinimumWidth(330)
        card.setMaximumWidth(360)

        card_layout = QtWidgets.QVBoxLayout(card)
        card_layout.setAlignment(QtCore.Qt.AlignCenter)
        card_layout.setSpacing(20)

        # ===== ЗАГОЛОВОК =====
        title = QtWidgets.QLabel("Настройки")
        title.setObjectName("title")
        card_layout.addWidget(title)

        # ============================
        #        СМЕНА ИМЕНИ
        # ============================
        name_btn = QtWidgets.QPushButton("Изменить имя")
        name_btn.setObjectName("secondaryButton")
        name_btn.clicked.connect(self.change_fullname)
        card_layout.addWidget(name_btn)

        # ============================
        #      СМЕНА ПАРОЛЯ
        # ============================
        pass_btn = QtWidgets.QPushButton("Изменить пароль")
        pass_btn.setObjectName("secondaryButton")
        pass_btn.clicked.connect(self.change_password)
        card_layout.addWidget(pass_btn)

        # ============================
        #      СМЕНА ЛОГИНА
        # ============================
        login_btn = QtWidgets.QPushButton("Изменить логин")
        login_btn.setObjectName("secondaryButton")
        login_btn.clicked.connect(self.change_username)
        card_layout.addWidget(login_btn)

        # ============================
        #      СМЕНА ЯЗЫКА
        # ============================
        lang_btn = QtWidgets.QPushButton("Язык: Русский / English")
        lang_btn.setObjectName("secondaryButton")
        lang_btn.clicked.connect(self.switch_language)
        card_layout.addWidget(lang_btn)

        # ============================
        #     УДАЛЕНИЕ АККАУНТА
        # ============================
        del_btn = QtWidgets.QPushButton("Удалить аккаунт")
        del_btn.setObjectName("dangerButton")
        del_btn.clicked.connect(self.delete_account)
        card_layout.addWidget(del_btn)

        # ============================
        #     ВЫХОД ИЗ АККАУНТА
        # ============================
        logout_btn = QtWidgets.QPushButton("Выйти из аккаунта")
        logout_btn.setObjectName("dangerButton")
        logout_btn.clicked.connect(self.logout)
        card_layout.addWidget(logout_btn)

        # ====== НАЗАД ======
        back_btn = QtWidgets.QPushButton("Назад")
        back_btn.setObjectName("secondaryButton")
        back_btn.clicked.connect(lambda: self.back_to_menu.emit())
        card_layout.addWidget(back_btn)

        main_layout.addWidget(card)

    # ==========================================
    #        ПОЛУЧАЕМ ТЕКУЩЕГО ПОЛЬЗОВАТЕЛЯ
    # ==========================================
    def set_user(self, user):
        self.current_user = user

    # ==========================================
    #          СМЕНА ИМЕНИ
    # ==========================================
    def change_fullname(self):
        if self.current_user is None:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пользователь не найден")
            return

        new = QtWidgets.QInputDialog.getText(self, "Новое имя", "Введите новое имя:")[0]
        if new:
            update_fullname(self.current_user.id, new)
            QtWidgets.QMessageBox.information(self, "Успех", "Имя изменено!")

    # ==========================================
    #          СМЕНА ПАРОЛЯ
    # ==========================================
    def change_password(self):
        if self.current_user is None:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пользователь не найден")
            return

        new = QtWidgets.QInputDialog.getText(self, "Новый пароль", "Введите новый пароль:")[0]
        if new:
            update_password(self.current_user.id, new)
            QtWidgets.QMessageBox.information(self, "Успех", "Пароль изменён!")

    # ==========================================
    #          СМЕНА ЛОГИНА
    # ==========================================
    def change_username(self):
        if self.current_user is None:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пользователь не найден")
            return

        new = QtWidgets.QInputDialog.getText(self, "Новый логин", "Введите новый логин:")[0]
        if not new:
            return

        ok = update_username(self.current_user.id, new)
        if ok:
            QtWidgets.QMessageBox.information(self, "Успех", "Логин изменён!")
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Логин уже занят!")

    # ==========================================
    #          СМЕНА ЯЗЫКА
    # ==========================================
    def switch_language(self):
        QtWidgets.QMessageBox.information(self, "Язык", "Переключатель языка скоро будет добавлен!")

    # ==========================================
    #          УДАЛЕНИЕ АККАУНТА
    # ==========================================
    def delete_account(self):
        if self.current_user is None:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пользователь не найден")
            return

        confirm = QtWidgets.QMessageBox.question(
            self,
            "Удаление",
            "Ты точно хочешь удалить аккаунт? Это действие необратимо.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )

        if confirm == QtWidgets.QMessageBox.Yes:
            delete_user(self.current_user.id)
            QtWidgets.QMessageBox.information(self, "Удалён", "Аккаунт удалён!")
            self.logout_signal.emit()

    # ==========================================
    #          ВЫХОД ИЗ АККАУНТА
    # ==========================================
    def logout(self):
        QtWidgets.QMessageBox.information(self, "Выход", "Вы вышли из аккаунта!")
        self.current_user = None
        self.logout_signal.emit()
