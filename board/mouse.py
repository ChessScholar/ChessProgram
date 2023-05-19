from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtWidgets import QGraphicsRectItem
from board.chessboard import ChessBoard, ChessSquare
from PyQt5.QtGui import QColor, QBrush, QTransform
import chess

class MouseHandler:
    def __init__(self, chessboard: ChessBoard, main_window):  # Add main_window parameter
        self.chessboard = chessboard
        self.main_window = main_window  # Store main_window as an instance attribute
        self.selected_square = None

    def handle_click(self, position: QPointF):
        file, rank = int(position.x() // 100), int(position.y() // 100)
        square = chess.square(file, rank)

        
        if not self.selected_square:
            piece = self.chessboard.board.piece_at(square)
            if piece:
                self.selected_square = square
                
                # Highlight the selected square
                x ,y = (chess.square_file(square),chess.square_rank(square))
                self.chessboard.highlight_square(x,y)

        else:
            dest_item=self.chessboard.itemAt(file*100 ,rank*100,QTransform())
            
            if isinstance(dest_item ,ChessSquare) :
               prev_file ,prev_rank= (chess.square_file(self.selected_square),chess.square_rank( self.selected_square ))
               
               # Remove highlight from the previously selected square               
               previous_item=self.chessboard.itemAt(prev_file * 100 ,prev_rank * 100,QTransform())                
               
               key_prev='A'if (prev_file + prev_rank )%2==0 else 'B'
               color_prev=self.chessboard.default_board_colors[key_prev]
          
          
               previous_item.set_color(QColor(color_prev))
               
           # Move piece and update highlight           
               self.chessboard.move_piece(self.selected_square, square)
               self.selected_square = None