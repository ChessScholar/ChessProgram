from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QColor, QBrush, QTransform
import chess
from boardgui.chesssquare import ChessSquare

class ChessBoard(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.default_board_colors = [QColor(240, 217, 181), QColor(181, 136, 99)]
        self.board = chess.Board()
        self.init_ui()

    def init_ui(self):
        for i in range(8):
            for j in range(8):
                color = self.default_board_colors[(i + j) % 2]
                square = ChessSquare(i, j, color)
                self.addItem(square)

    def set_square_color(self, x, y, color):
        square = self.itemAt(x * 100, y * 100, QTransform())
        if square:
            square.set_color(color)
            self.default_board_colors[(x + y) % 2] = color

    def board_colors(self):
        chess_board = self.scene()
        chess_board.clear()
        chess_board.init_ui()
        return self.default_board_colors

    def get_board_color(self, index):
        return self.default_board_colors[index]

    def set_board_color(self, index, color):
        self.default_board_colors[index] = color