#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modern GPU Visualizer — Application Entry

Author: 𝙅𝙖𝙠𝙤𝙗 / 𝙎𝙚𝙣𝙨𝙚𝙞 𝙄𝙨𝙨𝙚𝙞

Overview:
- Main window coordinating 2D/3D views, controls, and component panels
- Robust state management for smooth GPU switching and live simulation
- Modern dark UI with responsive layouts and status feedback

Key Modules:
- Views: GPU2DView, GPU3DView
- Controls: selection, parameters, import/export
- Simulation: real-time activity and DVFS-driven dynamics
"""

from gpuviz.controls import Controls
from gpuviz.layouts import PRESETS, load_layout_from_json, dump_layout_to_json
from gpuviz.sim import Simulation
from gpuviz.view2d import GPU2DView
from gpuviz.view3d import GPU3DView, HAVE_GL
from gpuviz.componentHighlighter import ComponentHighlighter, ComponentType
from gpuviz.componentVisibilityPanel import ComponentVisibilityPanel
from PySide6 import QtCore, QtWidgets, QtGui

class DetailedComponentPanel(QtWidgets.QWidget):
    component_selected = QtCore.Signal(str)
    
    def __init__(self):
        super().__init__()
        self.component_highlighter = ComponentHighlighter()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        
        title = QtWidgets.QLabel("🔧 Advanced GPU Component Explorer")
        title.setStyleSheet("""
            QLabel {
                color: #4fc3f7;
                font-size: 18px;
                font-weight: 700;
                padding: 12px;
                background-color: transparent;
                border-bottom: 2px solid #404040;
                margin-bottom: 8px;
            }
        """)
        layout.addWidget(title)
        
        selection_group = QtWidgets.QGroupBox("🎯 Component Selection")
        selection_layout = QtWidgets.QVBoxLayout(selection_group)
        
        self.component_list = QtWidgets.QListWidget()
        self.component_list.setStyleSheet("""
            QListWidget {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 8px;
                padding: 8px;
                color: #e0e0e0;
                font-size: 12px;
            }
            QListWidget::item {
                padding: 8px;
                margin: 2px;
                border-radius: 4px;
                background-color: transparent;
            }
            QListWidget::item:selected {
                background-color: #4fc3f7;
                color: #1a1a1a;
                font-weight: bold;
            }
            QListWidget::item:hover {
                background-color: #404040;
            }
        """)
        
        self.populate_component_list()
        selection_layout.addWidget(self.component_list)
        
        button_layout = QtWidgets.QHBoxLayout()
        
        self.highlight_btn = QtWidgets.QPushButton("🔦 Highlight")
        self.highlight_btn.setStyleSheet("""
            QPushButton {
                background-color: #4fc3f7;
                color: #1a1a1a;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #29b6f6;
            }
            QPushButton:pressed {
                background-color: #0288d1;
            }
        """)
        
        self.clear_btn = QtWidgets.QPushButton("🧹 Clear")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
            QPushButton:pressed {
                background-color: #424242;
            }
        """)
        
        button_layout.addWidget(self.highlight_btn)
        button_layout.addWidget(self.clear_btn)
        selection_layout.addLayout(button_layout)
        
        layout.addWidget(selection_group)
        
        details_group = QtWidgets.QGroupBox("📊 Component Details")
        details_layout = QtWidgets.QVBoxLayout(details_group)
        
        self.component_details = QtWidgets.QTextBrowser()
        self.component_details.setStyleSheet("""
            QTextBrowser {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 8px;
                padding: 12px;
                color: #e0e0e0;
                font-size: 11px;
                line-height: 1.5;
            }
            QTextBrowser h3 {
                color: #4fc3f7;
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 8px;
            }
            QTextBrowser strong {
                color: #81c784;
                font-weight: bold;
            }
            QTextBrowser table {
                border-collapse: collapse;
                margin: 5px 0;
            }
        """)
        self.component_details.setHtml("""
            <div style="color: #b0bec5; text-align: center; padding: 20px;">
                Select a component from the list above to view detailed technical information,
                specifications, manufacturing details, and maintenance guidelines.
            </div>
        """)
        
        details_layout.addWidget(self.component_details)
        layout.addWidget(details_group)
        
        self.performance_indicator = QtWidgets.QLabel("⚡ Performance Impact: None")
        self.performance_indicator.setStyleSheet("""
            QLabel {
                background-color: #404040;
                border-radius: 6px;
                padding: 8px 12px;
                color: #e0e0e0;
                font-size: 11px;
                font-weight: 600;
            }
        """)
        layout.addWidget(self.performance_indicator)
        
        self.component_list.itemSelectionChanged.connect(self._on_component_selected)
        self.highlight_btn.clicked.connect(self._on_highlight_clicked)
        self.clear_btn.clicked.connect(self._on_clear_clicked)
        
    def populate_component_list(self):
        components = [
            ("chassis", "🏗️ GPU Chassis/Enclosure", "Structural housing and thermal management"),
            ("cooling", "❄️ Cooling System", "Fans, heatsink, and heat pipes"),
            ("pcb", "🔌 PCB Board", "Printed circuit board and traces"),
            ("gpu_die", "🎯 GPU Silicon Die", "Core processor and compute units"),
            ("vram", "💾 Video RAM", "High-bandwidth memory chips"),
            ("power_delivery", "⚡ Power Delivery", "VRM and voltage regulation"),
            ("backplate", "🔩 Backplate", "Rear mounting and cooling plate"),
            ("io_bracket", "🖥️ I/O Bracket", "Display ports and power connectors"),
            ("microscopic", "🔬 Microscopic Components", "Resistors, capacitors, ICs"),
            ("traces", "📡 PCB Traces", "Copper pathways and signal routing")
        ]
        
        for component_id, name, description in components:
            item = QtWidgets.QListWidgetItem(f"{name}\n  {description}")
            item.setData(QtCore.Qt.UserRole, component_id)
            item.setToolTip(f"Click to explore {name}")
            self.component_list.addItem(item)
            
    def _on_component_selected(self):
        current_item = self.component_list.currentItem()
        if current_item:
            component_id = current_item.data(QtCore.Qt.UserRole)
            try:
                component_type = ComponentType(component_id)
                component_info = self.component_highlighter.get_component_info(component_type)
                
                if component_info:
                    self.component_details.setHtml(
                        self.component_highlighter.format_component_details(component_info)
                    )
                    
                    impact_color = "#f44336" if "CRITICAL" in component_info.importance else \
                                  "#ff9800" if "HIGH" in component_info.importance else \
                                  "#4caf50" if "MEDIUM" in component_info.importance else "#9e9e9e"
                    
                    self.performance_indicator.setStyleSheet(f"""
                        QLabel {{
                            background-color: {impact_color};
                            border-radius: 6px;
                            padding: 8px 12px;
                            color: #ffffff;
                            font-size: 11px;
                            font-weight: 600;
                        }}
                    """)
                    self.performance_indicator.setText(f"⚡ {component_info.importance}")
                    
            except ValueError:
                self.component_details.setHtml("""
                    <div style="color: #f44336; text-align: center; padding: 20px;">
                        Invalid component selected. Please choose a valid component from the list.
                    </div>
                """)
                self.performance_indicator.setText("⚡ Performance Impact: Unknown")
                
    def _on_highlight_clicked(self):
        current_item = self.component_list.currentItem()
        if current_item:
            component_id = current_item.data(QtCore.Qt.UserRole)
            try:
                component_type = ComponentType(component_id)
                self.component_selected.emit(component_id)
                
                self.highlight_btn.setText("🔦 Active")
                self.highlight_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #4caf50;
                        color: #ffffff;
                        border: none;
                        border-radius: 6px;
                        padding: 8px 16px;
                        font-weight: 600;
                        font-size: 12px;
                    }
                """)
                
            except ValueError:
                pass
                
    def _on_clear_clicked(self):
        self.component_selected.emit("clear")
        
        self.highlight_btn.setText("🔦 Highlight")
        self.highlight_btn.setStyleSheet("""
            QPushButton {
                background-color: #4fc3f7;
                color: #1a1a1a;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #29b6f6;
            }
            QPushButton:pressed {
                background-color: #0288d1;
            }
        """)
        
        self.component_details.setHtml("""
            <div style="color: #b0bec5; text-align: center; padding: 20px;">
                Component highlighting cleared. Select a component to view details.
            </div>
        """)
        self.performance_indicator.setText("⚡ Performance Impact: None")
        self.performance_indicator.setStyleSheet("""
            QLabel {
                background-color: #404040;
                border-radius: 6px;
                padding: 8px 12px;
                color: #e0e0e0;
                font-size: 11px;
                font-weight: 600;
            }
        """)
        
    def set_gpu_model(self, gpu_model):
        if gpu_model:
            self.components = {
                "backplate": {"name": "🔩 Backplate & I/O Bracket", "description": "The structural backbone providing video outputs, mounting support, and EMI shielding."},
                "pcb": {"name": "🔌 Printed Circuit Board (PCB)", "description": "Multi-layer fiberglass foundation with gold-plated PCIe connector and power distribution network."},
                "power_delivery": {"name": "⚡ Power Delivery System", "description": "Multi-phase VRM design with digital controllers for stable power delivery."},
                "gpu_package": {"name": "🎯 GPU Package & Silicon Die", "description": "Advanced silicon die with billions of transistors and streaming multiprocessors."},
                "vram": {"name": "💾 Video Memory (VRAM)", "description": "GDDR6 memory modules with ultra-high bandwidth for gaming performance."},
                "heatsink": {"name": "🌡️ Cooling Heatsink", "description": "Massive aluminum fin array with direct contact technology for optimal heat dissipation."},
                "heatpipes": {"name": "🔥 Heat Pipe Network", "description": "Copper pipes with phase-change cooling technology for efficient heat transfer."},
                "fans": {"name": "💨 Cooling Fans", "description": "Triple fan configuration with optimized blade design and intelligent temperature control."},
                "shroud": {"name": "🛡️ External Shroud", "description": "Engineered housing with optimized airflow channels and LED lighting."},
                "screws": {"name": "🔧 Assembly Hardware", "description": "Precision mounting components for secure assembly and longevity."}
            }
            self.component_list.clear()
            for component_id, component_info in self.components.items():
                item = QtWidgets.QListWidgetItem(component_info["name"])
                item.setData(QtCore.Qt.UserRole, component_id)
                item.setToolTip(f"Click to highlight {component_info['name']}")
                self.component_list.addItem(item)
        else:
            self.component_list.clear()
            
    def _on_component_selected(self):
        current_item = self.component_list.currentItem()
        if current_item:
            component_id = current_item.data(QtCore.Qt.UserRole)
            if component_id in self.components:
                component_info = self.components[component_id]
                self.component_details.setHtml(f"""
                <h3 style="color: #4fc3f7; margin-bottom: 10px;">{component_info['name']}</h3>
                <div style="color: #e0e0e0; line-height: 1.6;">
                {component_info['description']}
                </div>
                """)
                
    def _on_highlight_clicked(self):
        current_item = self.component_list.currentItem()
        if current_item:
            component_id = current_item.data(QtCore.Qt.UserRole)
            self.component_selected.emit(component_id)
            
    def _on_clear_clicked(self):
        self.component_selected.emit("clear")

import json
import sys
import time
from typing import Optional


class ModernGPUVisualizer(QtWidgets.QMainWindow):
    
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern GPU Visualizer")
        self.setGeometry(100, 100, 1920, 1080)
        
        self.setStyleSheet(self._get_modern_stylesheet())
        
        self.current_gpu_name = None
        self.sim = None
        self.is_loading = False
        
        self.setup_ui()
        self._setup_connections()
        self._load_initial_gpu()
        
    def _get_modern_stylesheet(self):
        """Get modern dark theme stylesheet with excellent readability"""
        return """
        QMainWindow {
            background-color: #1a1a1a;
            color: #ffffff;
        }
        
        QWidget {
            background-color: #1a1a1a;
            color: #e0e0e0;
            font-family: 'Segoe UI', 'Arial', sans-serif;
            font-size: 12px;
        }
        
        QLabel {
            color: #ffffff;
            font-weight: 500;
            background-color: transparent;
        }
        
        QLabel#title {
            color: #4fc3f7;
            font-size: 18px;
            font-weight: 700;
            padding: 8px;
        }
        
        QLabel#subtitle {
            color: #81c784;
            font-size: 14px;
            font-weight: 600;
            padding: 4px;
        }
        
        QLabel#description {
            color: #b0bec5;
            font-size: 11px;
            font-weight: 400;
            padding: 4px;
            line-height: 1.4;
        }
        
        QPushButton {
            background-color: #2d2d2d;
            color: #ffffff;
            border: 2px solid #404040;
            border-radius: 8px;
            padding: 10px 16px;
            font-weight: 600;
            font-size: 13px;
            min-height: 20px;
        }
        
        QPushButton:hover {
            background-color: #404040;
            border-color: #4fc3f7;
            color: #4fc3f7;
        }
        
        QPushButton:pressed {
            background-color: #4fc3f7;
            color: #1a1a1a;
        }
        
        QPushButton:disabled {
            background-color: #1f1f1f;
            color: #666666;
            border-color: #333333;
        }
        
        QComboBox {
            background-color: #2d2d2d;
            color: #ffffff;
            border: 2px solid #404040;
            border-radius: 8px;
            padding: 8px 12px;
            font-weight: 600;
            font-size: 13px;
            min-height: 20px;
        }
        
        QComboBox:hover {
            border-color: #4fc3f7;
            background-color: #353535;
        }
        
        QComboBox::drop-down {
            border: none;
            width: 30px;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #ffffff;
            width: 0;
            height: 0;
        }
        
        QComboBox QAbstractItemView {
            background-color: #2d2d2d;
            color: #ffffff;
            border: 2px solid #404040;
            border-radius: 8px;
            selection-background-color: #4fc3f7;
            selection-color: #1a1a1a;
            padding: 4px;
        }
        
        QComboBox QAbstractItemView::item {
            padding: 8px 12px;
            font-weight: 500;
            border-radius: 4px;
            margin: 2px;
        }
        
        QComboBox QAbstractItemView::item:hover {
            background-color: #404040;
            color: #4fc3f7;
        }
        
        QComboBox QAbstractItemView::item:selected {
            background-color: #4fc3f7;
            color: #1a1a1a;
        }
        
        QRadioButton {
            color: #ffffff;
            font-weight: 600;
            font-size: 13px;
            spacing: 8px;
        }
        
        QRadioButton::indicator {
            width: 18px;
            height: 18px;
            border: 2px solid #404040;
            border-radius: 10px;
            background-color: #2d2d2d;
        }
        
        QRadioButton::indicator:hover {
            border-color: #4fc3f7;
            background-color: #353535;
        }
        
        QRadioButton::indicator:checked {
            border-color: #4fc3f7;
            background-color: #4fc3f7;
            width: 8px;
            height: 8px;
            margin: 5px;
        }
        
        QSlider::groove:horizontal {
            border: 1px solid #404040;
            height: 8px;
            background: #2d2d2d;
            border-radius: 4px;
        }
        
        QSlider::handle:horizontal {
            background: #4fc3f7;
            border: 2px solid #ffffff;
            width: 18px;
            margin: -5px 0;
            border-radius: 10px;
        }
        
        QSlider::handle:horizontal:hover {
            background: #29b6f6;
            border-color: #e0e0e0;
        }
        
        QListWidget {
            background-color: #1f1f1f;
            color: #ffffff;
            border: 2px solid #404040;
            border-radius: 10px;
            padding: 8px;
            font-size: 12px;
        }
        
        QListWidget::item {
            padding: 12px 16px;
            margin: 4px;
            border: 1px solid #333333;
            border-radius: 8px;
            background-color: #2d2d2d;
            color: #ffffff;
            font-weight: 500;
        }
        
        QListWidget::item:hover {
            background-color: #404040;
            border-color: #4fc3f7;
            color: #4fc3f7;
        }
        
        QListWidget::item:selected {
            background-color: #4fc3f7;
            color: #1a1a1a;
            border-color: #29b6f6;
            font-weight: 700;
        }
        
        QScrollBar:vertical {
            background-color: #1f1f1f;
            width: 12px;
            border-radius: 6px;
            border: 1px solid #333333;
        }
        
        QScrollBar::handle:vertical {
            background-color: #404040;
            border-radius: 6px;
            min-height: 20px;
            border: 1px solid #333333;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #4fc3f7;
            border-color: #29b6f6;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            border: none;
            background: none;
        }
        
        QStatusBar {
            background-color: #1f1f1f;
            color: #b0bec5;
            border-top: 2px solid #404040;
            font-size: 11px;
            font-weight: 500;
        }
        
        QStatusBar QLabel {
            color: #b0bec5;
            padding: 4px 8px;
        }
        
        QGroupBox {
            color: #ffffff;
            font-weight: 600;
            font-size: 14px;
            border: 2px solid #404040;
            border-radius: 10px;
            margin-top: 8px;
            padding-top: 16px;
            background-color: #1f1f1f;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 8px 0 8px;
            color: #4fc3f7;
        }
        
        QCheckBox {
            color: #ffffff;
            font-weight: 600;
            font-size: 12px;
            spacing: 8px;
        }
        
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border: 2px solid #404040;
            border-radius: 4px;
            background-color: #2d2d2d;
        }
        
        QCheckBox::indicator:hover {
            border-color: #4fc3f7;
            background-color: #353535;
        }
        
        QCheckBox::indicator:checked {
            background-color: #4fc3f7;
            border-color: #29b6f6;
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEwIDNMNC41IDguNUwyIDYiIHN0cm9rZT0iIzFhMWExYSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
        }
        
        QProgressBar {
            border: 2px solid #404040;
            border-radius: 8px;
            text-align: center;
            color: #ffffff;
            font-weight: 600;
            background-color: #1f1f1f;
        }
        
        QProgressBar::chunk {
            background-color: #4fc3f7;
            border-radius: 6px;
            margin: 2px;
        }
        
        QTabWidget::pane {
            border: 2px solid #404040;
            background-color: #1f1f1f;
            border-radius: 10px;
        }
        
        QTabBar::tab {
            background-color: #2d2d2d;
            color: #ffffff;
            border: 2px solid #404040;
            border-bottom: none;
            border-radius: 8px 8px 0 0;
            padding: 8px 16px;
            margin-right: 2px;
            font-weight: 600;
        }
        
        QTabBar::tab:hover {
            background-color: #404040;
            color: #4fc3f7;
        }
        
        QTabBar::tab:selected {
            background-color: #4fc3f7;
            color: #1a1a1a;
        }
        
        QToolTip {
            background-color: #2d2d2d;
            color: #ffffff;
            border: 2px solid #4fc3f7;
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 11px;
            font-weight: 500;
        }
        """
        
    def setup_ui(self):
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QtWidgets.QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        self.controls = Controls()
        self.controls.setMinimumWidth(350)
        self.controls.setMaximumWidth(400)
        
        self.view_container = QtWidgets.QWidget()
        view_layout = QtWidgets.QVBoxLayout(self.view_container)
        view_layout.setContentsMargins(0, 0, 0, 0)
        
        view_mode_group = QtWidgets.QGroupBox("View Mode")
        view_mode_layout = QtWidgets.QHBoxLayout(view_mode_group)
        self.radio_2d = QtWidgets.QRadioButton("2D View")
        self.radio_3d = QtWidgets.QRadioButton("3D View")
        self.radio_3d.setChecked(True)
        
        self.view_mode_group = QtWidgets.QButtonGroup()
        self.view_mode_group.addButton(self.radio_2d, 0)
        self.view_mode_group.addButton(self.radio_3d, 1)
        self.view_mode_group.setExclusive(True)
        
        view_mode_layout.addWidget(self.radio_2d)
        view_mode_layout.addWidget(self.radio_3d)
        view_layout.addWidget(view_mode_group)
        
        self.view_stack = QtWidgets.QStackedWidget()
        self.view2d = GPU2DView()
        self.view3d = GPU3DView()
        self.view_stack.addWidget(self.view2d)
        self.view_stack.addWidget(self.view3d)
        self.view_stack.setCurrentIndex(1)
        view_layout.addWidget(self.view_stack, 1)
        
        self.loading_overlay = QtWidgets.QWidget(self.view_container)
        self.loading_overlay.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 200);
                border-radius: 8px;
            }
        """)
        self.loading_overlay.hide()
        
        loading_layout = QtWidgets.QVBoxLayout(self.loading_overlay)
        loading_layout.setAlignment(QtCore.Qt.AlignCenter)
        
        self.loading_label = QtWidgets.QLabel("Loading GPU Model...")
        self.loading_label.setStyleSheet("""
            QLabel {
                color: #4fc3f7;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        self.loading_label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.loading_spinner = QtWidgets.QLabel()
        self.loading_spinner.setFixedSize(32, 32)
        self.loading_spinner.setStyleSheet("""
            QLabel {
                border: 3px solid #404040;
                border-top: 3px solid #4fc3f7;
                border-radius: 16px;
                background-color: transparent;
            }
        """)
        
        loading_layout.addWidget(self.loading_spinner)
        loading_layout.addWidget(self.loading_label)
        
        right_panel = QtWidgets.QWidget()
        right_panel_layout = QtWidgets.QVBoxLayout(right_panel)
        right_panel_layout.setContentsMargins(0, 0, 0, 0)
        right_panel_layout.setSpacing(10)
        
        self.visibility_panel = ComponentVisibilityPanel(self.view3d)
        self.visibility_panel.setMinimumWidth(400)
        self.visibility_panel.setMaximumWidth(450)
        right_panel_layout.addWidget(self.visibility_panel, 1)
        
        self.component_panel = DetailedComponentPanel()
        self.component_panel.setMinimumWidth(400)
        self.component_panel.setMaximumWidth(450)
        right_panel_layout.addWidget(self.component_panel, 2)
        
        main_layout.addWidget(self.controls)
        main_layout.addWidget(self.view_container, 1)
        main_layout.addWidget(right_panel)
        
        self.status_bar = self.statusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #252525;
                color: #ffffff;
                border-top: 1px solid #404040;
            }
        """)
        self.status_label = QtWidgets.QLabel("Ready")
        self.status_bar.addWidget(self.status_label)
        
    def _on_component_highlighted(self, component_id: str):
        if component_id == "clear":
            self.view3d.clear_highlight()
            self.status_label.setText("Component highlighting cleared")
        else:
            if not self.radio_3d.isChecked():
                self.radio_3d.setChecked(True)
            
            self.view3d.highlight_component(component_id)
            self.status_label.setText(f"Highlighted: {component_id}")
    
    def _on_component_visibility_changed(self, component_type: str, visible: bool):
        self.view3d.set_component_visibility(component_type, visible)
        status = "Shown" if visible else "Hidden"
        self.status_label.setText(f"{component_type}: {status}")
    
    def _on_performance_mode_changed(self, mode: str, checked: bool):
        if checked:
            self.view3d.set_performance_mode(mode)
            self.status_label.setText(f"Performance mode: {mode}")

    def _setup_connections(self):
        self.controls.preset.currentTextChanged.connect(self._on_gpu_selection_changed)
        
        self.controls.start_clicked.connect(self._on_simulation_started)
        self.controls.stop_clicked.connect(self._on_simulation_stopped)
        self.controls.changed_speed.connect(self._on_speed_changed)
        self.controls.changed_util.connect(self._on_utilization_changed)
        self.controls.changed_power_mv.connect(self._on_power_changed)
        
        self.view_mode_group.buttonClicked.connect(self._on_view_mode_changed)
        
        self.component_panel.component_selected.connect(self._on_component_highlighted)
        
        self.controls.changed_colormap.connect(self._on_colormap_changed)
        self.controls.import_json_clicked.connect(self._on_import_json)
        self.controls.export_json_clicked.connect(self._on_export_json)
        
        if hasattr(self.visibility_panel, 'component_checkboxes'):
            for key, checkbox in self.visibility_panel.component_checkboxes.items():
                checkbox.toggled.connect(lambda checked, k=key: self._on_component_visibility_changed(k, checked))
        
    def _load_initial_gpu(self):
        try:
            selected_gpu = self.controls.preset.currentText()
            if not selected_gpu or selected_gpu not in PRESETS:
                selected_gpu = list(PRESETS.keys())[0]
                self.controls.preset.setCurrentText(selected_gpu)
            
            self._load_gpu_model(selected_gpu)
            
        except Exception as e:
            self._show_error(f"Failed to load initial GPU: {e}")
            
    def _on_gpu_selection_changed(self, gpu_name: str):
        if self.is_loading or gpu_name == self.current_gpu_name:
            return
            
        if gpu_name not in PRESETS:
            self._show_error(f"Unknown GPU model: {gpu_name}")
            return
            
        self._load_gpu_model(gpu_name)
        
    def _load_gpu_model(self, gpu_name: str):
        self.is_loading = True
        self._show_loading(True)
        self.status_label.setText(f"Loading {gpu_name}...")
        
        try:
            if self.sim and self.sim.running:
                self.sim.stop()
                
            self.current_layout = PRESETS[gpu_name]
            self.current_gpu_name = gpu_name
            
            self.sim = Simulation(self.current_layout)
            
            self.view2d.set_layout(self.current_layout)
            self.view3d.set_layout(self.current_layout)
            
            QtCore.QTimer.singleShot(100, self._on_gpu_model_loaded)
            
            current_view = "3d" if self.radio_3d.isChecked() else "2d"
            self._connect_simulation_to_view(current_view)
            
            self.sim.start()
            
            self.status_label.setText(f"Loaded: {gpu_name}")
            self._log_message(f"Successfully loaded GPU model: {gpu_name}")
            
        except Exception as e:
            self._show_error(f"Failed to load GPU model {gpu_name}: {e}")
            if self.current_gpu_name:
                self.controls.preset.setCurrentText(self.current_gpu_name)
        finally:
            self.is_loading = False
            self._show_loading(False)
            
    def _on_gpu_model_loaded(self):
        if hasattr(self.view3d, 'gpu_model') and self.view3d.gpu_model:
            self.component_panel.set_gpu_model(self.view3d.gpu_model)
        else:
            self._show_error("GPU model failed to initialize properly")
            
        if not self.sim:
            return
            
        try:
            self.sim.updated.disconnect()
        except:
            pass
            
        current_view = "3d" if self.radio_3d.isChecked() else "2d"
        self._connect_simulation_to_view(current_view)
        
    def _on_view_mode_changed(self, button):
        view_index = self.view_mode_group.id(button)
        
        if view_index == 1:  
            self.view_stack.setCurrentIndex(1)
            self.status_label.setText("3D View Mode")
            self._connect_simulation_to_view("3d")
        else:  
            self.view_stack.setCurrentIndex(0)
            self.status_label.setText("2D View Mode")
            self._connect_simulation_to_view("2d")
    
    def _connect_simulation_to_view(self, view_mode: str):
        if not self.sim:
            return
            
        try:
            self.sim.updated.disconnect()
        except:
            pass
            
        if view_mode == "3d":
            self.sim.updated.connect(self.view3d.update)
        else:
            self.sim.updated.connect(self.view2d.update_colors)
            self.sim.updated.connect(self._throttled_3d_update)
            self.sim.updated.connect(self._throttled_2d_update)
    
    def _throttled_3d_update(self):
        self.view3d.update()
    
    def _throttled_2d_update(self):
        self.view2d.update_colors()
            
    def _on_component_selected(self, component_name: str):
        if component_name == "clear" or component_name == "__CLEAR__":
            self.view3d.clear_highlight()
            self.status_label.setText("Highlight cleared")
        else:
            if not self.radio_3d.isChecked():
                self.radio_3d.setChecked(True)
            self.view3d.highlight_component(component_name)
            self.status_label.setText(f"Selected: {component_name}")
            
    def _on_colormap_changed(self, colormap_name: str):
        self.view2d.set_colormap(colormap_name)
        self.view3d.set_colormap(colormap_name)
        self.status_label.setText(f"Colormap: {colormap_name}")
        
    def _on_speed_changed(self, speed: int):
        if self.sim:
            self.sim.set_speed_ms(speed)
            self.status_label.setText(f"Speed: {speed}ms")
            
    def _on_utilization_changed(self, utilization: int):
        if self.sim:
            self.sim.set_global_util(utilization)
            self.status_label.setText(f"Utilization: {utilization}%")
            
    def _on_power_changed(self, power_mv: int):
        if self.sim:
            self.sim.set_power_mv(power_mv)
            self.status_label.setText(f"Power: {power_mv}mV")
            
    def _on_simulation_started(self):
        if self.sim:
            self.sim.start()
            self.status_label.setText("Simulation started")
            
    def _on_simulation_stopped(self):
        if self.sim:
            self.sim.stop()
            self.status_label.setText("Simulation stopped")
            
    def _on_import_json(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Import GPU Layout", "", "JSON Files (*.json)")
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                layout = load_layout_from_json(data)
                PRESETS[layout.name] = layout
                self.controls.preset.addItem(layout.name)
                self.controls.preset.setCurrentText(layout.name)
                self.status_label.setText(f"Imported: {layout.name}")
            except Exception as e:
                self._show_error(f"Import failed: {e}")
                
    def _on_export_json(self):
        if not self.current_layout:
            return
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Export GPU Layout", f"{self.current_layout.name}.json", 
            "JSON Files (*.json)")
        if path:
            try:
                data = dump_layout_to_json(self.current_layout)
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                self.status_label.setText(f"Exported to: {path}")
            except Exception as e:
                self._show_error(f"Export failed: {e}")
                
    def _show_loading(self, show: bool):
        if show:
            self.loading_overlay.setGeometry(self.view_container.rect())
            self.loading_overlay.show()
            self.loading_overlay.raise_()
        else:
            self.loading_overlay.hide()
            
    def _show_error(self, message: str):
        QtWidgets.QMessageBox.critical(self, "Error", message)
        self.status_label.setText(f"Error: {message}")
        
    def _log_message(self, message: str):
        if hasattr(self.controls, 'log_window'):
            self.controls.log_window.log(message, "INFO")
            
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.loading_overlay.isVisible():
            self.loading_overlay.setGeometry(self.view_container.rect())


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    
    app.setApplicationName("Modern GPU Visualizer")
    app.setApplicationVersion("2.0")
    
    window = ModernGPUVisualizer()
    window.show()
    
    if not HAVE_GL:
        QtWidgets.QMessageBox.information(
            window, "3D Rendering", 
            "3D rendering requires PyOpenGL. Install with:\n\npip install PyOpenGL"
        )
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()