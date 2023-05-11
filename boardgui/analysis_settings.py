from PyQt5.QtWidgets import QLabel, QSpinBox, QVBoxLayout, QTextEdit
import os

class AnalysisSettings:
    def __init__(self):
        self.layout = QVBoxLayout()
        self.init_ui()

    def init_ui(self):
        self.num_moves_label, self.num_moves_spinbox = self.create_spinbox(
            "Number of moves:", 1, 50, 5)
        self.time_limit_label, self.time_limit_spinbox = self.create_spinbox(
            "Time limit (s):", 1, 60, 5)
        self.num_cores_label, self.num_cores_spinbox = self.create_spinbox(
            "Number of cores:", 1, os.cpu_count(), 1)
        self.depth_label, self.depth_spinbox = self.create_spinbox(
            "Depth:", 1, 50, 1)

        self.layout.addWidget(self.num_moves_label)
        self.layout.addWidget(self.num_moves_spinbox)
        self.layout.addWidget(self.time_limit_label)
        self.layout.addWidget(self.time_limit_spinbox)
        self.layout.addWidget(self.num_cores_label)
        self.layout.addWidget(self.num_cores_spinbox)
        self.layout.addWidget(self.depth_label)
        self.layout.addWidget(self.depth_spinbox)
        self.layout.addWidget(QLabel("Moves"))

        self.analysis_output = QTextEdit()
        self.analysis_output.setReadOnly(True)
        self.layout.addWidget(self.analysis_output)

        self.layout.addWidget(QLabel("Engine Analysis"))
        self.move_history_text = QTextEdit()
        self.move_history_text.setReadOnly(True)
        self.layout.addWidget(self.move_history_text)

    def create_spinbox(self, label_text, min_value, max_value, default_value):
        label = QLabel(label_text)
        spinbox = QSpinBox()
        spinbox.setRange(min_value, max_value)
        spinbox.setValue(default_value)
        return label, spinbox