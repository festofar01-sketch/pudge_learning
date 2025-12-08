from PyQt5 import QtWidgets
from ui.login_page import LoginPage
from ui.register_page import RegisterPage
from ui.courses_page import CoursesPage
from ui.test_page import TestPage


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pudge Learning")
        self.setFixedSize(420, 760)

        self.stack = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stack)

        self.login_page = LoginPage()
        self.register_page = RegisterPage()
        self.courses_page = CoursesPage()
        self.test_page = TestPage()

        # Добавляем в стек
        self.stack.addWidget(self.login_page)     # 0
        self.stack.addWidget(self.register_page)  # 1
        self.stack.addWidget(self.courses_page)   # 2
        self.stack.addWidget(self.test_page)      # 3

        # Навигация
        self.login_page.switch_to_register.connect(
            lambda: self.stack.setCurrentIndex(1)
        )
        self.register_page.switch_to_login.connect(
            lambda: self.stack.setCurrentIndex(0)
        )

        self.login_page.login_success.connect(self.open_courses)

        self.courses_page.start_test.connect(self.open_test)

    def open_courses(self, user):
        self.courses_page.set_user(user)
        self.stack.setCurrentIndex(2)

    def open_test(self):
        self.test_page.start_test()
        self.stack.setCurrentIndex(3)
