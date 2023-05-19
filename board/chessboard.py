from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QColor, QBrush, QTransform
import chess
from board.chesssquare import ChessSquare

class ChessBoard(QGraphicsScene):
    squareClicked = pyqtSignal(chess.Square, str ,int ,int)

    def __init__(self):
        super().__init__()
        self.default_board_colors = {'A': QColor(240, 217, 181), 'B': QColor(181, 136, 99)}
        self.board = chess.Board()
        self.init_ui()
        self.selected_square = None
        
    def init_ui(self):
        for i in range(8):
            for j in range(8):
                key = 'A' if (i + j) % 2 == 0 else 'B'
                color = self.default_board_colors[key]
                square = ChessSquare(i, j, color)
                self.addItem(square)
        self.place_pieces()

    def set_square_color(self, x, y, color):
        key = 'A' if (x + y) % 2 == 0 else 'B'
        square = self.itemAt(x * 100, y * 100, QTransform())
        if square:
            square.set_color(color)
            self.default_board_colors[key] = color

    def board_colors(self):
        self.clear()
        self.init_ui()
        return self.default_board_colors

    def get_board_color(self, index):
        key = 'A' if index == 0 else 'B'
        return self.default_board_colors[key]

    def get_square_color(self, x, y):
        key = 'A' if (x + y) % 2 == 0 else 'B'
        square = self.itemAt(x * 100, y * 100, QTransform())
        if square:
            return square.color
        return self.default_board_colors[key]

    def set_board_color(self, index, color):
        key = 'A' if index == 0 else 'B'
        self.default_board_colors[key] = color
        self.clear()
        self.init_ui()
        
    def place_pieces(self):
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                x, y = chess.square_file(square), chess.square_rank(square)
                pixmap = self.get_piece_image(piece)
                piece_item = QGraphicsPixmapItem(pixmap)
                piece_item.setPos(x * 100, y * 100)
                self.addItem(piece_item)
                
    def get_piece_image(self, piece):
        piece_name = piece.symbol().lower()
        piece_color = "w" if piece.color == chess.WHITE else "b"
        file_name = f"img/chesspieces/{piece_color}{piece_name.upper()}.png"
        return QtGui.QPixmap(file_name)

    def find_piece(self, x, y):
        target_x, target_y = x * 100, y * 100
        for item in self.items():
            if isinstance(item, QGraphicsPixmapItem) and item.x() == target_x and item.y() == target_y:
                return item
        return None

    def move_piece(self, from_square, to_square):
        piece = self.board.piece_at(from_square)
        if piece:
            self.board.set_piece_at(to_square, piece)
            self.board.remove_piece_at(from_square)
            self.clear()
            self.init_ui()

    def highlight_square(self, x, y):
        key = 'A' if (x + y) % 2 == 0 else 'B'
        color = QColor(self.default_board_colors[key])
        alpha = 100 if self.itemAt(x * 100, y * 100, QTransform()).isSelected() else 255
        color.setAlpha(alpha)
        
        square = self.itemAt(x * 100, y * 100, QTransform())
        if square:
            square.set_color(color)
