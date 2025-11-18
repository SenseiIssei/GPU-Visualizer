"""
GPU Component Visibility Panel

Author: 𝙅𝙖𝙠𝙤𝙗 / 𝙎𝙚𝙣𝙨𝙚𝙞 𝙄𝙨𝙨𝙚𝙞

Overview:
- Show/Hide GPU components and toggle performance modes
- Emits UI-driven state changes to the 3D view
"""

from PySide6 import QtCore, QtGui, QtWidgets
from typing import Dict, Callable

class ComponentVisibilityPanel(QtWidgets.QGroupBox):
    
    def __init__(self, view3d_instance=None):
        super().__init__("Component Visibility")
        self.view3d = view3d_instance
        
        self.component_checkboxes = {}
        self.performance_radio = {}
        self.init_ui()
        self.setup_connections()
        
    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        components_group = QtWidgets.QGroupBox("Show/Hide Components")
        components_layout = QtWidgets.QGridLayout(components_group)
        components = [
            ("chassis", "Chassis", True),
            ("cooling", "Cooling System", True),
            ("pcb", "PCB Board", True),
            ("gpu_die", "GPU Die", True),
            ("vram", "VRAM Chips", True),
            ("power_delivery", "Power Delivery", True),
            ("backplate", "Backplate", True),
            ("io_bracket", "I/O Bracket", True),
            ("microscopic", "Microscopic Details", True),
            ("traces", "PCB Traces", True)
        ]
        
        for i, (key, label, default) in enumerate(components):
            checkbox = QtWidgets.QCheckBox(label)
            checkbox.setChecked(default)
            self.component_checkboxes[key] = checkbox
            components_layout.addWidget(checkbox, i // 2, i % 2)
        
        layout.addWidget(components_group)
        performance_group = QtWidgets.QGroupBox("Performance Mode")
        performance_layout = QtWidgets.QVBoxLayout(performance_group)
        performance_modes = [
            ("low", "Low Performance (30 FPS, basic details)"),
            ("balanced", "Balanced (60 FPS, good details)"),
            ("ultra", "Ultra Quality (60 FPS, maximum details)")
        ]
        
        for key, label in performance_modes:
            radio = QtWidgets.QRadioButton(label)
            self.performance_radio[key] = radio
            performance_layout.addWidget(radio)
        
        self.performance_radio["balanced"].setChecked(True)
        
        layout.addWidget(performance_group)
        buttons_layout = QtWidgets.QHBoxLayout()
        self.show_all_btn = QtWidgets.QPushButton("Show All")
        self.hide_all_btn = QtWidgets.QPushButton("Hide All")
        self.reset_btn = QtWidgets.QPushButton("Reset View")
        buttons_layout.addWidget(self.show_all_btn)
        buttons_layout.addWidget(self.hide_all_btn)
        buttons_layout.addWidget(self.reset_btn)
        layout.addLayout(buttons_layout)
        layout.addStretch()
        
    def setup_connections(self):
        for key, checkbox in self.component_checkboxes.items():
            checkbox.toggled.connect(lambda checked, k=key: self.on_component_toggled(k, checked))
        for key, radio in self.performance_radio.items():
            radio.toggled.connect(lambda checked, k=key: self.on_performance_changed(k, checked))
        self.show_all_btn.clicked.connect(self.show_all_components)
        self.hide_all_btn.clicked.connect(self.hide_all_components)
        self.reset_btn.clicked.connect(self.reset_view)
        
    def on_component_toggled(self, component: str, visible: bool):
        if self.view3d:
            self.view3d.set_component_visibility(component, visible)
            
    def on_performance_changed(self, mode: str, checked: bool):
        if checked and self.view3d:
            self.view3d.set_performance_mode(mode)
            self.update_component_checkboxes_for_mode(mode)
            
    def update_component_checkboxes_for_mode(self, mode: str):
        if mode == "low":
            self.component_checkboxes["microscopic"].setChecked(False)
            self.component_checkboxes["traces"].setChecked(False)
            self.component_checkboxes["microscopic"].setEnabled(False)
            self.component_checkboxes["traces"].setEnabled(False)
        else:
            self.component_checkboxes["microscopic"].setEnabled(True)
            self.component_checkboxes["traces"].setEnabled(True)
            
    def show_all_components(self):
        for checkbox in self.component_checkboxes.values():
            checkbox.setChecked(True)
            
    def hide_all_components(self):
        for checkbox in self.component_checkboxes.values():
            checkbox.setChecked(False)
            
    def reset_view(self):
        essential_components = ["chassis", "cooling", "pcb", "gpu_die", "vram", "io_bracket"]
        for key, checkbox in self.component_checkboxes.items():
            checkbox.setChecked(key in essential_components)
        
        self.performance_radio["balanced"].setChecked(True)
        
        if self.view3d:
            self.view3d.reset_camera()
            
    def set_view3d(self, view3d_instance):
        self.view3d = view3d_instance
        if self.view3d:
            current_state = self.view3d.get_component_visibility_state()
            for key, visible in current_state.items():
                if key in self.component_checkboxes:
                    self.component_checkboxes[key].setChecked(visible)