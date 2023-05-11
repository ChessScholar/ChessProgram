from PyQt5.QtWidgets import (QMainWindow, QAction, QDockWidget, QLabel, QVBoxLayout, QWidget,
                             QMessageBox, QPushButton, QColorDialog)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor
import chess.engine
from boardgui.chessboardview import ChessBoardView
from settings.analysis_settings import AnalysisSettings
from settings.engine.engine import UCIEngine

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.engine = None
        self.init_ui()
        self.analysis_timer = QTimer()
        self.analysis_timer.timeout.connect(self.update_analysis)

    def init_ui(self):
        self.setWindowTitle("Chess Board GUI")
        self.setCentralWidget(ChessBoardView())

        self.create_menus()
        self.create_analysis_dock()

        self.load_settings()

    def create_menus(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        board_menu = menubar.addMenu("Board")
        analysis_menu = menubar.addMenu("Analysis")
        view_menu = menubar.addMenu("View")

        board_colors_action = QAction("Board Colors", self)
        board_colors_action.triggered.connect(self.board_colors)
        board_menu.addAction(board_colors_action)

        start_analysis_action = QAction("Start Analysis", self)
        start_analysis_action.triggered.connect(self.start_analysis)
        analysis_menu.addAction(start_analysis_action)

        stop_analysis_action = QAction("Stop Analysis", self)
        stop_analysis_action.triggered.connect(self.stop_analysis)
        analysis_menu.addAction(stop_analysis_action)

    def create_analysis_dock(self):
        self.analysis_settings = AnalysisSettings()

        analysis_dock = QDockWidget("Analysis", self)
        analysis_dock.setWidget(QWidget())
        self.addDockWidget(Qt.RightDockWidgetArea, analysis_dock)
        analysis_dock.widget().setLayout(self.analysis_settings.layout)

        self.num_moves_label, self.num_moves_spinbox = self.create_spinbox(
            "Number of moves:", 1, 50, 5)
        self.time_limit_label, self.time_limit_spinbox = self.create_spinbox(
            "Time limit (s):", 1, 60, 5)
        self.num_cores_label, self.num_cores_spinbox = self.create_spinbox(
            "Number of cores:", 1, os.cpu_count(), 1)
        self.depth_label, self.depth_spinbox = self.create_spinbox(
            "Depth:", 1, 50, 1)

        vbox = QVBoxLayout()
        vbox.addWidget(self.num_moves_label)
        vbox.addWidget(self.num_moves_spinbox)
        vbox.addWidget(self.time_limit_label)
        vbox.addWidget(self.time_limit_spinbox)
        vbox.addWidget(self.num_cores_label)
        vbox.addWidget(self.num_cores_spinbox)
        vbox.addWidget(self.depth_label)
        vbox.addWidget(self.depth_spinbox)
        vbox.addWidget(QLabel("Moves"))
        vbox.addWidget(self.analysis_output)
        vbox.addWidget(QLabel("Engine Analysis"))
        vbox.addWidget(self.move_history_text)

        analysis_dock.widget().setLayout(vbox)

    def display_analysis_output(self, info):
        analysis_output = "Custom Analysis Result:\n"
        
        if 'pv' in info:
            pv_moves = " > ".join(move.uci() for move in info['pv'])
            analysis_output += f"Principal Variation: {pv_moves}\n"
        else:
            analysis_output += "Principal Variation not available\n"
        
        if 'score' in info:
            analysis_output += f"Evaluation Score: {info['score']}\n"
        
        if 'wdl' in info:
            analysis_output += f"Win/Draw/Loss Probabilities: {info['wdl']}\n"
        
        if 'nodes' in info:
            analysis_output += f"Nodes Searched: {info['nodes']}\n"
        
        if 'nps' in info:
            analysis_output += f"Nodes per Second: {info['nps']}\n"
        
        if 'depth' in info:
            analysis_output += f"Search Depth: {info['depth']}\n"
        
        self.analysis_output.setPlainText(analysis_output)

    def create_move_history_list(self):
        move_history_list = QListWidget()
        move_history_list.setAlternatingRowColors(True)
        return move_history_list

    def create_spinbox(self, label_text, min_value, max_value, default_value):
        label = QLabel(label_text)
        spinbox = QSpinBox()
        spinbox.setRange(min_value, max_value)
        spinbox.setValue(default_value)
        return label, spinbox

        self.load_settings()

    def prompt_save_changes(self, apply_changes, discard_changes):
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Save Changes")
        message_box.setText("Do you want to save the changes before exiting?")
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
        settings = {
            'board_colors': [color.name() for color in self.centralWidget().scene().default_board_colors]
        }
        with open('settings.json', 'w') as settings_file:
            json.dump(settings, settings_file)

    def load_settings(self):
        if os.path.exists('settings.json'):
            with open('settings.json', 'r') as settings_file:
                settings = json.load(settings_file)
                board_colors = [QColor(color) for color in settings['board_colors']]
                chess_board = self.centralWidget().scene()
                chess_board.default_board_colors = board_colors
                chess_board.clear()
                chess_board.init_ui()

    def board_colors(self):
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
        default_colors = [QColor(240, 217, 181), QColor(181, 136, 99)]
        chess_board.default_board_colors = default_colors
        chess_board.clear()
        chess_board.init_ui()

    def set_board_color(self, chess_board, index):
        color_dialog = QColorDialog(chess_board.get_board_color(index), self)
        if color_dialog.exec_():
            color = color_dialog.currentColor()
            chess_board.set_board_color(index, color)
            chess_board.clear()
            chess_board.init_ui()

    def set_individual_board_colors(self, chess_board):
        square_color_dialog = SquareColorDialog(chess_board, self)
        square_color_dialog.exec_()

    def start_analysis(self):
        if self.engine is None:
            engine_path = "C:/Users/Matt PC/Downloads/stockfish_15.1_win_x64_avx2/stockfish_15.1_win_x64_avx2/stockfish-windows-2022-x86-64-avx2.exe"  # Replace with the path to your UCI engine
            self.engine = UCIEngine(engine_path)

        num_cores = self.num_cores_spinbox.value()  # Get the number of cores from the spin box
        self.engine.set_num_cores(num_cores)  # Set the number of cores for the engine

        self.board = self.centralWidget().scene().board
        self.analysis_timer.start(1000)  # Update the analysis every second (1000 ms)

    def stop_analysis(self):
        if self.engine is not None:
            self.engine.stop_analysis()
            self.analysis_timer.stop()
            
    def update_analysis(self):
        if self.engine is None:
            return

        depth = self.depth_spinbox.value()
        time_limit = self.time_limit_spinbox.value()
        limit = chess.engine.Limit(depth=depth, time=time_limit)
        info = self.engine.analyze(self.board, limit)
        self.display_analysis(info)
        if 'pv' in info:
            num_moves = self.num_moves_spinbox.value()
            variation = info['pv'][:num_moves]
            pv_moves = self.board.variation_san(variation)
            self.display_move_history(pv_moves.split())
        else:
            self.display_analysis_output(info)
        print(info)  # Print the analysis result, you can modify this to display the result in the GUI

    def display_analysis(self, info):
        # Convert the info dictionary to a string and display it in the GUI
        analysis_text = ""
        for key, value in info.items():
            analysis_text += f"{key}: {value}\n"
        self.analysis_output.setPlainText(analysis_text)

    def display_move_history(self, moves):
        move_pairs = [moves[i:i + 2] for i in range(0, len(moves), 2)]

        history_text = ""
        for i, move_pair in enumerate(move_pairs):
            history_text += f"{i + 1}. {' '.join(move_pair)}\n"

        self.move_history_text.setPlainText(history_text)
        
    def closeEvent(self, event):
        if self.engine is not None:
            self.engine.close()
        event.accept()