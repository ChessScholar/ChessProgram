from PyQt5.QtWidgets import (QDockWidget, QLabel, QVBoxLayout, QWidget,
                             QMessageBox, QPushButton, QColorDialog, QSpinBox, QDialog, QDialogButtonBox,
                             QGroupBox, QFormLayout, QCheckBox, QTextEdit)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor
import chess.engine
import os
import json
from config import CONFIG
from .engine import ChessEngine

class EngineManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.analysis_timer = None
        self.engine = None
        self.create_engine_settings()   
    
    def create_engine_settings(self):
        engine_settings = QDockWidget("Engine Settings", self.main_window)
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

        self.main_window.addDockWidget(Qt.RightDockWidgetArea, engine_settings)


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
            self.analysis_timer = QTimer()
            self.analysis_timer.timeout.connect(self.update_engine_analysis)
            self.analysis_timer.start(1000)  # Update every 1000 milliseconds (1 second)

        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "Engine not found. Please check the engine path in the config file.")

    def update_engine_analysis(self):
        if self.engine:
            board = self.main_window.centralWidget().scene().board
            depth = self.depth_spinbox.value()
            lines = self.lines_spinbox.value()
            cores = self.cores_spinbox.value()
            use_nnue = self.nnue_checkbox.isChecked()
            memory = 128  # You can set the memory limit here in MB, adjust as needed

            options = {
                "Threads": cores,
                "Use NNUE": use_nnue
            }
            if self.engine.nnue_path and use_nnue:  # Access nnue_path from the engine instance
                options["EvalFile"] = self.engine.nnue_path

            self.engine.set_engine_options(options)
            limit = chess.engine.Limit(depth=depth)
            analysis_info = self.engine.analyze(board, depth=depth, lines=lines, cores=cores, memory=memory)  # Pass the memory limit here
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