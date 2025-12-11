from PyQt5 import QtWidgets
from ui.login_page import LoginPage
from ui.register_page import RegisterPage
from ui.main_menu_page import MainMenuPage
from ui.levels_page import LevelsPage
from ui.lessons_page import LessonPage
from ui.settings_page import SettingsPage
from learning_platform.services import load_levels, load_questions_by_level
from ui.style import APP_STYLE


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pudge Learning")
        self.setFixedSize(420, 760)
        self.setStyleSheet(APP_STYLE)

        self.stack = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stack)

        # === СТРАНИЦЫ ===
        self.login_page = LoginPage()        # 0
        self.register_page = RegisterPage()  # 1
        self.main_menu = MainMenuPage()      # 2
        self.levels_page = LevelsPage()      # 3
        self.lesson_page = LessonPage()      # 4
        self.settings_page = SettingsPage()  # 5

        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.register_page)
        self.stack.addWidget(self.main_menu)
        self.stack.addWidget(self.levels_page)
        self.stack.addWidget(self.lesson_page)
        self.stack.addWidget(self.settings_page)

        # === ЛОГИКА ПЕРЕКЛЮЧЕНИЯ ===
        self.login_page.switch_to_register.connect(lambda: self.stack.setCurrentIndex(1))
        self.register_page.switch_to_login.connect(lambda: self.stack.setCurrentIndex(0))

        self.login_page.login_success.connect(self.after_login)

        self.main_menu.start_learning.connect(self.open_levels)
        self.main_menu.open_settings.connect(lambda: self.stack.setCurrentIndex(5))
        self.main_menu.exit_app.connect(self.close)

        self.levels_page.level_selected.connect(self.open_lesson)

        self.settings_page.back_to_menu.connect(lambda: self.stack.setCurrentIndex(2))

        # === ВАЖНО: подключаем сигналы из LessonPage ===
        self.lesson_page.go_main_menu.connect(lambda: self.stack.setCurrentIndex(2))
        self.lesson_page.back_to_levels.connect(lambda: self.stack.setCurrentIndex(3))

    # ==========================
    def after_login(self, user):
        self.current_user = user
        self.stack.setCurrentIndex(2)

    # ==========================
    def open_levels(self):
        levels = load_levels()
        self.levels_page.load_levels(levels)
        self.stack.setCurrentIndex(3)

    # ==========================
    def open_lesson(self, level_code):
        questions = load_questions_by_level(level_code)
        self.lesson_page.load_level(level_code, questions)
        self.stack.setCurrentIndex(4)
