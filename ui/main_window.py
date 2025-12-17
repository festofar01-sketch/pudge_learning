from PyQt5 import QtWidgets

from ui.login_page import LoginPage
from ui.main_menu_page import MainMenuPage
from ui.levels_page import LevelsPage
from ui.task_levels_page import TaskLevelsPage
from ui.lessons_page import LessonPage
from ui.syntax_lesson_page import SyntaxLessonPage
from ui.profile_page import ProfilePage
from ui.settings_page import SettingsPage

from learning_platform.services import (
    load_levels,
    load_questions_by_level_and_task,
    save_progress
)

from learning_platform.user_service import load_syntax_questions_by_level
from ui.style import APP_STYLE


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        # ===== ОКНО =====
        self.setWindowTitle("Pudge Learning")
        self.resize(1000, 720)
        self.setMinimumSize(900, 600)
        self.setStyleSheet(APP_STYLE)

        # ===== СОСТОЯНИЕ =====
        self.current_user = None
        self.selected_lang_level = None
        self.selected_task_level = None

        # ===== STACK =====
        self.stack = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stack)

        # ===== СТРАНИЦЫ =====
        self.login = LoginPage()
        self.menu = MainMenuPage()
        self.levels = LevelsPage()
        self.task_levels = TaskLevelsPage()
        self.lesson = LessonPage()
        self.syntax_lesson = SyntaxLessonPage()
        self.profile = ProfilePage()
        self.settings = SettingsPage()

        # ===== STACK ADD =====
        self.stack.addWidget(self.login)         # 0
        self.stack.addWidget(self.menu)          # 1
        self.stack.addWidget(self.levels)        # 2
        self.stack.addWidget(self.task_levels)   # 3
        self.stack.addWidget(self.lesson)        # 4
        self.stack.addWidget(self.syntax_lesson) # 5
        self.stack.addWidget(self.profile)       # 6
        self.stack.addWidget(self.settings)      # 7

        # ===== СИГНАЛЫ =====

        # --- LOGIN ---
        self.login.login_success.connect(self.after_login)

        # --- MAIN MENU ---
        self.menu.start_learning.connect(self.open_levels)
        self.menu.open_profile.connect(self.open_profile)
        self.menu.open_settings.connect(self.open_settings)
        self.menu.exit_app.connect(self.close)

        # --- LEVELS ---
        self.levels.level_selected.connect(self.open_task_levels)
        self.levels.back_to_menu.connect(self.go_menu)

        # --- TASK LEVELS ---
        self.task_levels.task_selected.connect(self.open_lesson)
        self.task_levels.back_signal.connect(self.back_to_levels)

        # --- LESSON ---
        self.lesson.save_progress.connect(self.save)
        self.lesson.go_main_menu.connect(self.go_menu)

        # --- SYNTAX LESSON ---
        self.syntax_lesson.save_progress.connect(self.save)
        self.syntax_lesson.go_main_menu.connect(self.go_menu)

        # --- PROFILE / SETTINGS ---
        self.profile.back_to_menu.connect(self.go_menu)
        self.settings.back_to_menu.connect(self.go_menu)
        self.settings.logout_signal.connect(self.logout)

        # ===== START =====
        self.stack.setCurrentIndex(0)

    # =================================================
    #                    LOGIN
    # =================================================

    def after_login(self, user):
        self.current_user = user
        self.settings.set_user(user)
        self.stack.setCurrentIndex(1)

    # =================================================
    #                 НАВИГАЦИЯ
    # =================================================

    def open_levels(self):
        self.levels.load_levels(load_levels())
        self.stack.setCurrentIndex(2)

    def open_task_levels(self, level_code):
        self.selected_lang_level = level_code
        self.stack.setCurrentIndex(3)

    def back_to_levels(self):
        self.stack.setCurrentIndex(2)

    def open_lesson(self, task_level):
        self.selected_task_level = task_level

        # ===== СИНТАКСИС (task_level = 3) =====
        if task_level == 3:
            questions = load_syntax_questions_by_level(
                self.selected_lang_level
            )

            self.syntax_lesson.load_level(
                self.selected_lang_level,
                questions
            )

            self.stack.setCurrentWidget(self.syntax_lesson)
            return

        # ===== ОБЫЧНЫЕ ТЕСТЫ =====
        questions = load_questions_by_level_and_task(
            self.selected_lang_level,
            task_level
        )

        self.lesson.load_level(
            self.selected_lang_level,
            questions,
            task_level
        )

        self.stack.setCurrentWidget(self.lesson)

    def open_profile(self):
        self.profile.set_user(self.current_user)
        self.stack.setCurrentIndex(6)

    def open_settings(self):
        self.stack.setCurrentIndex(7)

    def go_menu(self):
        self.stack.setCurrentIndex(1)

    # =================================================
    #                 ПРОГРЕСС
    # =================================================

    def save(self, level, correct, wrong, total):
        if self.current_user:
            save_progress(
                self.current_user.id,
                level,
                correct,
                wrong,
                total
            )

    # =================================================
    #                  LOGOUT
    # =================================================

    def logout(self):
        self.current_user = None
        self.stack.setCurrentIndex(0)
