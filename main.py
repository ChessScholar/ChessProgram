import sys
from PyQt5.QtWidgets import QApplication
from boardgui.mainwindow import MainWindow

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    exit_code = app.exec_()
    main_window.save_settings()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()