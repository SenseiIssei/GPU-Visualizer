"""
GPU Visualizer Controls Panel

Author: 𝙅𝙖𝙠𝙤𝙗 / 𝙎𝙚𝙣𝙨𝙚𝙞 𝙄𝙨𝙨𝙚𝙞

Overview:
- Central UI for GPU selection, view modes, colormaps, and simulation knobs
- Emits signals to synchronize views and simulation in real time
- Includes JSON import/export and logging utilities
"""
from PySide6 import QtCore, QtWidgets
from .layouts import PRESETS
from .resources import COLORMAPS
from .logWindow import LogWindow, LogWindowButton

class Controls(QtWidgets.QWidget):
    changed_layout = QtCore.Signal(str)
    changed_colormap = QtCore.Signal(str)
    changed_coloring_mode = QtCore.Signal(str)
    changed_view_mode2d = QtCore.Signal(str)
    changed_speed = QtCore.Signal(int)
    changed_util = QtCore.Signal(int)
    changed_power_mv = QtCore.Signal(int)
    start_clicked = QtCore.Signal()
    stop_clicked = QtCore.Signal()
    import_json_clicked = QtCore.Signal()
    export_json_clicked = QtCore.Signal()
    log_window_clicked = QtCore.Signal()

    def __init__(self):
        super().__init__()
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(10)

        title = QtWidgets.QLabel("GPU Visualizer")
        title.setStyleSheet("font-size:20px;font-weight:600;")
        root.addWidget(title)

        self.log_window = LogWindow()
        
        self.log_button = LogWindowButton(self.log_window)
        root.addWidget(self.log_button)
        self.log_button.clicked.connect(self.log_window_clicked)

        preset_group = QtWidgets.QGroupBox("GPU Layout Preset")
        preset_lay = QtWidgets.QFormLayout(preset_group)
        self.preset = QtWidgets.QComboBox()
        self.preset.addItems(list(PRESETS.keys()))
        self.view_combo = QtWidgets.QComboBox()
        self.view_combo.addItems(["Logical", "SM Focus", "Die View"])
        preset_lay.addRow(QtWidgets.QLabel("Choose GPU family (illustrative):"), self.preset)
        preset_lay.addRow(QtWidgets.QLabel("2D arrangement style:"), self.view_combo)
        root.addWidget(preset_group)
        self.preset.currentTextChanged.connect(self.changed_layout)
        self.view_combo.currentTextChanged.connect(self.changed_view_mode2d)

        color_group = QtWidgets.QGroupBox("Color & Metric")
        color_lay = QtWidgets.QFormLayout(color_group)
        self.color_mode = QtWidgets.QComboBox()
        self.color_mode.addItems(["Utilization", "Temperature", "Memory pressure"])
        self.colormap = QtWidgets.QComboBox()
        self.colormap.addItems(list(COLORMAPS.keys()))
        color_lay.addRow(QtWidgets.QLabel("Metric colored on tiles/cores:"), self.color_mode)
        color_lay.addRow(QtWidgets.QLabel("Colormap palette:"), self.colormap)
        root.addWidget(color_group)
        self.color_mode.currentTextChanged.connect(self.changed_coloring_mode)
        self.colormap.currentTextChanged.connect(self.changed_colormap)

        sim_group = QtWidgets.QGroupBox("Simulation Controls")
        sim_lay = QtWidgets.QFormLayout(sim_group)
        self.speed = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.speed.setRange(16, 600)
        self.speed.setValue(100)
        self.util  = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.util.setRange(0, 100)
        self.util.setValue(70)
        self.power = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.power.setRange(600, 1300)
        self.power.setValue(1050)
        sim_lay.addRow(QtWidgets.QLabel("Animation speed (ms per step):"), self.speed)
        sim_lay.addRow(QtWidgets.QLabel("Global utilization (%):"), self.util)
        sim_lay.addRow(QtWidgets.QLabel("Core voltage (mV, illustrative):"), self.power)
        root.addWidget(sim_group)
        self.speed.valueChanged.connect(self.changed_speed)
        self.util.valueChanged.connect(self.changed_util)
        self.power.valueChanged.connect(self.changed_power_mv)

        io_group = QtWidgets.QGroupBox("Layouts – Import/Export")
        io_lay = QtWidgets.QHBoxLayout(io_group)
        imp = QtWidgets.QPushButton("Import JSON layout…")
        exp = QtWidgets.QPushButton("Export JSON layout…")
        io_lay.addWidget(imp)
        io_lay.addWidget(exp)
        root.addWidget(io_group)
        imp.clicked.connect(self.import_json_clicked)
        exp.clicked.connect(self.export_json_clicked)

        run_group = QtWidgets.QGroupBox("Run Simulation")
        run_lay = QtWidgets.QHBoxLayout(run_group)
        start = QtWidgets.QPushButton("Start")
        stop = QtWidgets.QPushButton("Stop")
        run_lay.addWidget(start)
        run_lay.addWidget(stop)
        root.addWidget(run_group)
        start.clicked.connect(self.start_clicked)
        stop.clicked.connect(self.stop_clicked)

        help_box = QtWidgets.QGroupBox("Hints")
        help_lay = QtWidgets.QVBoxLayout(help_box)
        help_lay.addWidget(QtWidgets.QLabel(
            "• 2D: drag to pan, wheel to zoom.\n"
            "• 3D: Left-drag orbit, Right-drag pan, wheel to zoom.\n"
            "• Utilization & Voltage affect activity and derived metrics.\n"
            "• Use JSON import to load more precise per-SKU floorplans."
        ))
        root.addWidget(help_box)
        root.addStretch(1)

    def get_log_window(self):
        return self.log_window