from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QTransform
import chess

class MouseHandler:
    def __init__(self, chess_board):
        self.chess_board = chess_board
        self.chess_board.squareClicked.connect(self.on_square_clicked)
        self.selected_piece = None

    def on_square_clicked(self, square, piece, x, y):
        if self.selected_piece:
            self.move_piece(square, piece, x, y)
        else:
            self.select_piece(square, piece, x, y)

    def select_piece(self, square, piece, x, y):
        if piece:
            self.selected_piece = self.chess_board.itemAt(x * 100, y * 100, QTransform())  # Update this line
            self.selected_piece.setFlag(QGraphicsItem.ItemIsMovable, True)

    def move_piece(self, target_square, target_piece, x, y):
        source_square = chess.square(self.selected_piece.x() // 100, self.selected_piece.y() // 100)
        move = chess.Move(source_square, target_square)
        san_move = self.chess_board.board.san(move)

        try:
            self.chess_board.board.push_san(san_move)
            self.selected_piece.setPos(x * 100, y * 100)
            self.selected_piece.setFlag(QGraphicsItem.ItemIsMovable, False)
            self.selected_piece = None
            self.chess_board.clear()
            self.chess_board.init_ui()
        except ValueError:
            self.selected_piece.setFlag(QGraphicsItem.ItemIsMovable, False)
            self.selected_piece = None