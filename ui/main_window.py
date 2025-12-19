from PyQt5 import QtWidgets, QtCore

from ui.login_page import LoginPage
from ui.register_page import RegisterPage
from ui.main_menu_page import MainMenuPage
from ui.profile_page import ProfilePage
from ui.settings_page import SettingsPage
from ui.admin_panel_page import AdminPanelPage
from ui.teacher_panel_page import TeacherPanelPage
from ui.result_page import ResultPage
from ui.levels_page import LevelsPage
from ui.task_levels_page import TaskLevelsPage
from ui.lessons_page import LessonPage
from ui.syntax_lesson_page import SyntaxLessonPage

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

        # ===== STATE =====
        self.current_user = None
        self.selected_lang_level = None
        self.selected_task_level = None

        self.admin_panel = None
        self.teacher_panel = None

        self._build_ui()

    # =================================================
    # UI
    # =================================================
    def _build_ui(self):
        self.setWindowTitle("Pudge Learning")
        self.resize(1000, 720)
        self.setMinimumSize(900, 600)
        self.setStyleSheet(APP_STYLE)

        self.stack = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stack)

        # ----- PAGES -----
        self.login = LoginPage()
        self.register = RegisterPage()

        self.menu = MainMenuPage()
        self.profile = ProfilePage()
        self.settings = SettingsPage()

        self.levels = LevelsPage()
        self.task_levels = TaskLevelsPage()
        self.lesson = LessonPage()
        self.syntax_lesson = SyntaxLessonPage()
        self.result_page = ResultPage()

        # ----- STACK ADD -----
        self.stack.addWidget(self.login)
        self.stack.addWidget(self.register)

        self.stack.addWidget(self.menu)
        self.stack.addWidget(self.levels)
        self.stack.addWidget(self.task_levels)
        self.stack.addWidget(self.lesson)
        self.stack.addWidget(self.syntax_lesson)
        self.stack.addWidget(self.result_page)
        self.stack.addWidget(self.profile)
        self.stack.addWidget(self.settings)

        # ----- SIGNALS -----

        # LOGIN / REGISTER
        self.login.login_success.connect(self.after_login)
        self.login.open_register.connect(self.open_register)

        self.register.back_to_login.connect(self.open_login)
        self.register.register_success.connect(self.after_register)

        # MENU
        self.menu.start_learning.connect(self.open_levels)
        self.menu.open_profile.connect(self.open_profile)
        self.menu.open_settings.connect(self.open_settings)
        self.menu.open_admin_panel.connect(self.open_role_panel)
        self.menu.exit_app.connect(self.close)

        # LEVELS
        self.levels.level_selected.connect(self.open_task_levels)
        self.levels.back_to_menu.connect(self.go_menu)

        # TASK LEVELS
        self.task_levels.task_selected.connect(self.open_lesson)
        self.task_levels.back_signal.connect(self.back_to_levels)

        # LESSONS
        self.lesson.save_progress.connect(self.save)
        self.lesson.go_main_menu.connect(self.go_menu)

        self.syntax_lesson.save_progress.connect(self.save)
        self.syntax_lesson.go_main_menu.connect(self.go_menu)

        # RESULT
        self.result_page.go_main_menu.connect(self.go_menu)

        # PROFILE / SETTINGS
        self.profile.back_to_menu.connect(self.go_menu)
        self.settings.back_to_menu.connect(self.go_menu)
        self.settings.logout_signal.connect(self.logout)

        self.stack.setCurrentWidget(self.login)

    # =================================================
    # LOGIN / REGISTER
    # =================================================
    def open_register(self):
        self.stack.setCurrentWidget(self.register)

    def open_login(self):
        self.stack.setCurrentWidget(self.login)

    def after_register(self):
        self.stack.setCurrentWidget(self.login)

    def after_login(self, user):
        self.current_user = user

        self.menu.set_user(user)
        self.profile.set_user(user)
        self.settings.set_user(user)

        self.stack.setCurrentWidget(self.menu)

    # =================================================
    # NAVIGATION
    # =================================================
    def go_menu(self):
        self.stack.setCurrentWidget(self.menu)

    def open_levels(self):
        self.levels.load_levels(load_levels())
        self.stack.setCurrentWidget(self.levels)

    def back_to_levels(self):
        self.stack.setCurrentWidget(self.levels)

    def open_task_levels(self, level_code):
        self.selected_lang_level = level_code
        self.stack.setCurrentWidget(self.task_levels)

    def open_lesson(self, task_level):
        self.selected_task_level = task_level

        if task_level == 3:
            questions = load_syntax_questions_by_level(self.selected_lang_level)
            self.syntax_lesson.load_level(self.selected_lang_level, questions)
            self.stack.setCurrentWidget(self.syntax_lesson)
            return

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
        self.stack.setCurrentWidget(self.profile)

    def open_settings(self):
        self.stack.setCurrentWidget(self.settings)

    # =================================================
    # ADMIN / TEACHER
    # =================================================
    def open_role_panel(self):
        if not self.current_user:
            return

        if self.current_user.role == "admin":
            if not self.admin_panel:
                self.admin_panel = AdminPanelPage(self.current_user)
                self.admin_panel.back_to_menu.connect(self.go_menu)
                self.stack.addWidget(self.admin_panel)
            self.stack.setCurrentWidget(self.admin_panel)

        elif self.current_user.role == "teacher":
            if not self.teacher_panel:
                self.teacher_panel = TeacherPanelPage(self.current_user)
                self.teacher_panel.back_to_menu.connect(self.go_menu)
                self.stack.addWidget(self.teacher_panel)
            self.stack.setCurrentWidget(self.teacher_panel)

    # =================================================
    # PROGRESS
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
    # LOGOUT
    # =================================================
    def logout(self):
        self.current_user = None
        self.stack.setCurrentWidget(self.login)
