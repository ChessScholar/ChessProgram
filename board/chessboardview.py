from PyQt5.QtWidgets import QGraphicsView, QApplication
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from board.chessboard import ChessBoard
from board.mouse import MouseHandler

class ChessBoardView(QGraphicsView):
    def __init__(self, main_window):  # Add main_window parameter
        super().__init__()
        chess_board = ChessBoard()
        self.setScene(chess_board)
        self.setRenderHint(QPainter.Antialiasing)
        self.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing, True)
        self.setOptimizationFlag(QGraphicsView.DontSavePainterState, True)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.mouse_handler = MouseHandler(chess_board, main_window)  # Pass main_window to MouseHandler

    # Add the following mousePressEvent method to the ChessBoardView class
    def mousePressEvent(self, event):
        position = self.mapToScene(event.x(), event.y())
        self.mouse_handler.handle_click(position)