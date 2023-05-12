from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtGui import QBrush, QTransform, QColorTransform
import chess

class ChessSquare(QGraphicsRectItem):
    def __init__(self, x, y, color):
        super().__init__(x * 100, y * 100, 100, 100)
        self.color = color
        self.setBrush(QBrush(color))

    def set_color(self, color):
        self.color = color
        self.setBrush(QBrush(color))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x, y = int(self.x() // 100), int(self.y() // 100)
            square = chess.square(x, y)
            piece = self.scene().board.piece_at(square)
            self.scene().squareClicked.emit(square, piece, x, y)