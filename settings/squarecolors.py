from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QDialogButtonBox, QColorDialog, QGridLayout
from PyQt5.QtGui import QColor, QTransform
from board.chessboard import ChessBoard

class SquareColorDialog(QDialog):
    def __init__(self, chess_board, parent=None):
        super().__init__(parent)
        self.chess_board = chess_board
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Set Individual Square Colors")

        layout = QGridLayout()

        for i in range(8):
            for j in range(8):
                button = QPushButton()
                key = 'A' if (i + j) % 2 == 0 else 'B'
                color = self.chess_board.get_square_color(i, j)
                button.setStyleSheet(f"background-color: {color.name()}")
                button.clicked.connect(lambda _, x=i, y=j: self.change_square_color(x, y))
                layout.addWidget(button, j, i)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box, 8, 0, 1, 8)

        self.setLayout(layout)

    def change_square_color(self, x, y):
        key = 'A' if (x + y) % 2 == 0 else 'B'
        color = self.chess_board.get_square_color(x, y)
        color_dialog = QColorDialog(color, self)
        ok = color_dialog.exec_()
        if ok:
            color = color_dialog.currentColor()
            self.chess_board.set_square_color(x, y, color)
            sender = self.sender()
            sender.setStyleSheet(f"background-color: {color.name()}")