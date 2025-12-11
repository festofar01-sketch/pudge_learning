import sys
from PyQt5 import QtWidgets, QtCore
from ui.main_window import MainWindow


# Перехват всех необработанных исключений, чтобы видеть ошибку в консоли,
# а не просто вылет с кодом 0xC0000409
def excepthook(exc_type, exc_value, exc_traceback):
    print("UNCAUGHT EXCEPTION:", exc_type.__name__, exc_value)
    # стандартное поведение тоже оставим, чтобы был traceback
    sys.__excepthook__(exc_type, exc_value, exc_traceback)


sys.excepthook = excepthook


def main():
    # Рекомендуемые настройки для корректного отображения на Windows / high DPI
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
