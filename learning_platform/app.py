from PyQt5 import QtWidgets
from ui.main_window import MainWindow
from learning_platform.global_style import APP_STYLE


import sys

def main():
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
