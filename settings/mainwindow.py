from PyQt5.QtWidgets import (QMainWindow, QAction, QDockWidget, QLabel, QVBoxLayout, QWidget,
                             QMessageBox, QPushButton, QColorDialog, QSpinBox, QDialog, QDialogButtonBox,
                             QGroupBox, QFormLayout, QCheckBox, QTextEdit)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor
import chess.engine
import os
import json
from board.chessboardview import ChessBoardView
from settings.squarecolors import SquareColorDialog
from Engine.engine import ChessEngine
from config import CONFIG
from Engine.enginemanager import EngineManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.analysis_timer = None
        self.engine_manager = EngineManager(self)

    def init_ui(self):
        """Initialize the main UI components."""
        self.setWindowTitle("Chess Board GUI")
        
        chess_board_view = ChessBoardView(self)  # Pass self (main_window) as an argument
        self.setCentralWidget(chess_board_view)
        
        self.create_menus()
        self.load_settings()
        
    def create_menus(self):
        """Create the main menu bar items."""
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        board_menu = menubar.addMenu("Board")
        analysis_menu = menubar.addMenu("Analysis")
        view_menu = menubar.addMenu("View")

        board_colors_action = QAction("Board Colors", self)
        board_colors_action.triggered.connect(self.open_board_colors_dialog)
        board_menu.addAction(board_colors_action)

####################  GRAPHICS  ##########################

    def prompt_save_changes(self, apply_changes, discard_changes):
        """Prompt the user to save or discard changes."""
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Save Changes")
        message_box.setText("Save changes before exiting?")
        message_box.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        message_box.setDefaultButton(QMessageBox.Save)

        result = message_box.exec_()

        if result == QMessageBox.Save:
            apply_changes()
        elif result == QMessageBox.Discard:
            discard_changes()
        else:
            return False

        return True

    def save_settings(self):
        """Save the current settings to a JSON file."""
        chess_board = self.centralWidget().scene()
        board_colors = {
            'A': chess_board.default_board_colors['A'].name(),
            'B': chess_board.default_board_colors['B'].name(),
            'individual': {}
        }
        for i in range(8):
            for j in range(8):
                key = f"{i}-{j}"
                color = chess_board.get_square_color(i, j)
                board_colors['individual'][key] = color.name()

        settings = {
            'board_colors': board_colors
        }
        with open('settings.json', 'w') as settings_file:
            json.dump(settings, settings_file)

    def load_settings(self):
        """Load settings from a JSON file, if it exists."""
        if os.path.exists('settings.json'):
            with open('settings.json', 'r') as settings_file:
                settings = json.load(settings_file)
                chess_board = self.centralWidget().scene()
                if 'A' in settings['board_colors']:
                    chess_board.default_board_colors['A'] = QColor(settings['board_colors']['A'])
                if 'B' in settings['board_colors']:
                    chess_board.default_board_colors['B'] = QColor(settings['board_colors']['B'])
                if 'individual' in settings['board_colors']:
                    for i in range(8):
                        for j in range(8):
                            key = f"{i}-{j}"
                            if key in settings['board_colors']['individual']:
                                color = QColor(settings['board_colors']['individual'][key])
                                chess_board.set_square_color(i, j, color)


    def open_board_colors_dialog(self):
        """Open the board colors dialog."""
        chess_board = self.centralWidget().scene()
        original_board_colors = chess_board.default_board_colors.copy()

        color_dialog = QDialog(self)
        color_dialog.setWindowTitle("Board Colors")
        layout = QVBoxLayout()

        set_a_color = QPushButton("Set A Color", self)
        set_a_color.clicked.connect(lambda: self.set_board_color(chess_board, 0))
        layout.addWidget(set_a_color)

        set_b_color = QPushButton("Set B Color", self)
        set_b_color.clicked.connect(lambda: self.set_board_color(chess_board, 1))
        layout.addWidget(set_b_color)

        set_individual_colors = QPushButton("Set Individual Colors", self)
        set_individual_colors.clicked.connect(lambda: self.set_individual_board_colors(chess_board))
        layout.addWidget(set_individual_colors)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(color_dialog.accept)
        layout.addWidget(button_box)

        restore_defaults = QPushButton("Restore Defaults", self)
        restore_defaults.clicked.connect(lambda: self.restore_default_board_colors(chess_board))
        layout.addWidget(restore_defaults)

        color_dialog.setLayout(layout)
        result = color_dialog.exec_()

        if result == QDialog.Accepted:
            save_changes = lambda: None
            discard_changes = lambda: (setattr(chess_board, 'default_board_colors', original_board_colors),
                                       chess_board.clear(),
                                       chess_board.init_ui())

            if not self.prompt_save_changes(save_changes, discard_changes):
                return

    def restore_default_board_colors(self, chess_board):
        """Restore the default board colors."""
        default_colors = [QColor(240, 217, 181), QColor(181, 136, 99)]
        chess_board.default_board_colors = default_colors
        chess_board.clear()
        chess_board.init_ui()

    def set_board_color(self, chess_board, index):
        """Update the board color at the given index."""
        color_dialog = QColorDialog(chess_board.get_board_color(index), self)
        if color_dialog.exec_():
            color = color_dialog.currentColor()
            chess_board.set_board_color(index, color)
            chess_board.clear()
            chess_board.init_ui()

    def set_individual_board_colors(self, chess_board):
        """Open the dialog to set individual board colors."""
        square_color_dialog = SquareColorDialog(chess_board, self)
        square_color_dialog.exec_()