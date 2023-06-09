import sys
from PyQt5.QtWidgets import QApplication
from settings.mainwindow import MainWindow
from board.chessboardview import ChessBoardView

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    exit_code = app.exec_()
    main_window.save_settings()
    sys.exit(exit_code)

def create_window():
    app = QApplication([])
    app.setApplicationName("Chess")
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    window = ChessBoardView()
    window.resize(QSize(800, 800))
    window.show()
    return app.exec_()

if __name__ == "__main__":
    main()