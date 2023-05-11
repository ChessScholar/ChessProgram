from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from boardgui.chessboard import ChessBoard

class ChessBoardView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(ChessBoard())
        self.setRenderHint(QPainter.Antialiasing)
        self.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing, True)
        self.setOptimizationFlag(QGraphicsView.DontSavePainterState, True)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

    def resizeEvent(self, event):
        size = min(self.width(), self.height())
        self.setFixedSize(size, size)
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)