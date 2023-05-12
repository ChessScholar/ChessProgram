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
from board.mouse import MouseHandler
from config import CONFIG


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.analysis_timer = None

    def init_ui(self):
        """Initialize the main UI components."""
        self.setWindowTitle("Chess Board GUI")
        self.setCentralWidget(ChessBoardView())
        self.create_menus()
        self.load_settings()
        self.create_engine_settings()
        self.engine = None
        self.mouse_handler = MouseHandler(self.centralWidget().scene())

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
        settings = {
            'board_colors': [color.name() for color in self.centralWidget().scene().default_board_colors]
        }
        with open('settings.json', 'w') as settings_file:
            json.dump(settings, settings_file)

    def load_settings(self):
        """Load settings from a JSON file, if it exists."""
        if os.path.exists('settings.json'):
            with open('settings.json', 'r') as settings_file:
                settings = json.load(settings_file)
                board_colors = {key: QColor(color) for key, color in settings['board_colors'].items()}
                chess_board = self.centralWidget().scene()
                chess_board.default_board_colors = board_colors
                chess_board.clear()
                chess_board.init_ui()
        if 'board_colors' in settings:
                board_colors = {key: QColor(color) for key, color in settings['board_colors'].items()}
                chess_board = self.centralWidget().scene()
                chess_board.default_board_colors = board_colors
                chess_board.clear()
                chess_board.init_ui()

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

####################  ENGINE  ##########################

    def create_engine_settings(self):
        engine_settings = QDockWidget("Engine Settings", self)
        engine_settings.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        engine_group = QGroupBox("Engine")
        engine_layout = QVBoxLayout()

        self.start_engine_button = QPushButton("Start Engine")
        self.start_engine_button.clicked.connect(self.start_engine)
        engine_layout.addWidget(self.start_engine_button)

        self.stop_engine_button = QPushButton("Stop Engine")
        self.stop_engine_button.clicked.connect(self.stop_engine)
        engine_layout.addWidget(self.stop_engine_button)

        engine_group.setLayout(engine_layout)

        options_group = QGroupBox("Options")
        options_layout = QFormLayout()

        self.depth_spinbox = QSpinBox()
        self.depth_spinbox.setRange(1, 100)
        self.depth_spinbox.setValue(10)
        options_layout.addRow("Depth:", self.depth_spinbox)

        self.lines_spinbox = QSpinBox()
        self.lines_spinbox.setRange(1, 100)
        self.lines_spinbox.setValue(1)
        options_layout.addRow("Lines:", self.lines_spinbox)

        self.cores_spinbox = QSpinBox()
        self.cores_spinbox.setRange(1, 100)
        self.cores_spinbox.setValue(1)
        options_layout.addRow("Cores:", self.cores_spinbox)

        self.nnue_checkbox = QCheckBox("Use NNUE")
        options_layout.addRow(self.nnue_checkbox)

        options_group.setLayout(options_layout)

        layout = QVBoxLayout()
        layout.addWidget(engine_group)
        layout.addWidget(options_group)

        container = QWidget()
        container.setLayout(layout)
        engine_settings.setWidget(container)

        self.addDockWidget(Qt.RightDockWidgetArea, engine_settings)

        self.engine_output = QTextEdit()
        self.engine_output.setReadOnly(True)
        layout.addWidget(self.engine_output)
    
    def start_engine(self):
        engine_path = CONFIG['engine_path']
        nnue_path = CONFIG['nnue_path']

        try:
            self.engine = ChessEngine(engine_path, nnue_path)
            self.update_engine_analysis()

            # Create a QTimer and connect it to the update_engine_analysis method
            self.analysis_timer = QTimer(self)
            self.analysis_timer.timeout.connect(self.update_engine_analysis)
            self.analysis_timer.start(1000)  # Update every 1000 milliseconds (1 second)

        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "Engine not found. Please check the engine path in the config file.")

    def update_engine_analysis(self):
        if self.engine:
            board = self.centralWidget().scene().board
            depth = self.depth_spinbox.value()
            lines = self.lines_spinbox.value()
            cores = self.cores_spinbox.value()
            use_nnue = self.nnue_checkbox.isChecked()

            options = {
                "Threads": cores,
                "Use NNUE": use_nnue
            }
            if self.engine.nnue_path and use_nnue:  # Access nnue_path from the engine instance
                options["EvalFile"] = self.engine.nnue_path

            self.engine.set_engine_options(options)
            limit = chess.engine.Limit(depth=depth)
            analysis_info = self.engine.engine.analyse(board, limit, multipv=lines, info=chess.engine.INFO_ALL)
            self.engine_output.clear()
            move_pairs = []
            for i, info in enumerate(analysis_info):
                move_san = board.san(info['pv'][0])
                if i % 2 == 0:
                    move_pairs.append(f"{(i // 2) + 1}. {move_san}")
                else:
                    move_pairs[-1] += f" {move_san}"
            self.engine_output.append(" ".join(move_pairs))
            print(analysis_info)

    def engine_output_callback(self, output):
        print(output)

    def stop_engine(self):
        print("Updating engine analysis...")
        if self.engine:
            self.engine.close()
            self.engine = None

            # Stop the QTimer
            if self.analysis_timer:
                self.analysis_timer.stop()
                self.analysis_timer = None