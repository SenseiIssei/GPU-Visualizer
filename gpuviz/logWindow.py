#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide6 import QtCore, QtGui, QtWidgets
from typing import List
import datetime


class LogWindow(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GPU Visualizer Log")
        self.resize(600, 400)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        toolbar = QtWidgets.QHBoxLayout()
        
        self.clear_btn = QtWidgets.QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_log)
        toolbar.addWidget(self.clear_btn)
        
        self.save_btn = QtWidgets.QPushButton("Save")
        self.save_btn.clicked.connect(self.save_log)
        toolbar.addWidget(self.save_btn)
        
        toolbar.addWidget(QtWidgets.QLabel("Filter:"))
        self.filter_combo = QtWidgets.QComboBox()
        self.filter_combo.addItems(["All", "Info", "Warning", "Error", "Performance"])
        self.filter_combo.currentTextChanged.connect(self.filter_logs)
        toolbar.addWidget(self.filter_combo)
        
        self.autoscroll_cb = QtWidgets.QCheckBox("Auto-scroll")
        self.autoscroll_cb.setChecked(True)
        toolbar.addWidget(self.autoscroll_cb)
        
        self.perf_mode_cb = QtWidgets.QCheckBox("Performance Mode")
        self.perf_mode_cb.toggled.connect(self.toggle_performance_mode)
        toolbar.addWidget(self.perf_mode_cb)
        
        toolbar.addStretch()
        
        toolbar_widget = QtWidgets.QWidget()
        toolbar_widget.setLayout(toolbar)
        layout.addWidget(toolbar_widget)
        
        self.log_display = QtWidgets.QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setFont(QtGui.QFont("Consolas", 9))
        self.log_display.setStyleSheet("""
            QTextEdit {
                background-color:
                color:
                border: 1px solid
            }
        """)
        layout.addWidget(self.log_display)
        
        self.log_entries: List[dict] = []
        self.max_entries = 1000
        self.performance_mode = False
        
        self.setup_highlighting()
    
    def setup_highlighting(self):
        self.colors = {
            'INFO': '#d4d4d4',
            'WARNING': '#ffcc02',
            'ERROR': '#ff6b6b',
            'PERFORMANCE': '#4ec9b0',
            'TIMESTAMP': '#858585'
        }
    
    def log(self, message: str, level: str = "INFO"):
        if self.performance_mode and level not in ["ERROR", "WARNING"]:
            return
        
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        entry = {
            'timestamp': timestamp,
            'level': level,
            'message': message
        }
        
        self.log_entries.append(entry)
        
        if len(self.log_entries) > self.max_entries:
            self.log_entries = self.log_entries[-self.max_entries:]
        
        self.update_display()
        
        if self.autoscroll_cb.isChecked():
            self.log_display.moveCursor(QtGui.QTextCursor.End)
    
    def update_display(self):
        self.log_display.clear()
        
        filter_level = self.filter_combo.currentText()
        
        for entry in self.log_entries:
            if filter_level != "All" and entry['level'] != filter_level:
                continue
            
            timestamp_color = self.colors['TIMESTAMP']
            level_color = self.colors.get(entry['level'], self.colors['INFO'])
            
            formatted_entry = f'<span style="color: {timestamp_color}">[{entry["timestamp"]}]</span> '
            formatted_entry += f'<span style="color: {level_color}; font-weight: bold;">{entry["level"]}</span> '
            formatted_entry += f'<span style="color: {self.colors["INFO"]}">{entry["message"]}</span>'
            
            self.log_display.append(formatted_entry)
    
    def clear_log(self):
        self.log_entries.clear()
        self.log_display.clear()
        self.log("Log cleared", "INFO")
    
    def save_log(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save Log", f"gpu_visualizer_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    for entry in self.log_entries:
                        f.write(f"[{entry['timestamp']}] {entry['level']}: {entry['message']}\n")
                self.log(f"Log saved to {filename}", "INFO")
            except Exception as e:
                self.log(f"Failed to save log: {e}", "ERROR")
    
    def filter_logs(self, filter_type: str):
        self.update_display()
    
    def toggle_performance_mode(self, enabled: bool):
        self.performance_mode = enabled
        if enabled:
            self.log("Performance mode enabled - reduced logging", "INFO")
        else:
            self.log("Performance mode disabled - full logging", "INFO")
    
    def log_performance(self, operation: str, duration_ms: float):
        self.log(f"{operation}: {duration_ms:.2f}ms", "PERFORMANCE")
    
    def log_gpu_info(self, gpu_name: str, cores: int, sms: int, gpcs: int):
        self.log(f"GPU: {gpu_name} | Cores: {cores} | SMs: {sms} | GPCs: {gpcs}", "INFO")
    
    def log_simulation_event(self, event: str):
        self.log(f"Simulation: {event}", "INFO")
    
    def log_rendering_stats(self, fps: float, draw_calls: int, lod_level: int):
        self.log(f"Render: {fps:.1f} FPS | Draw calls: {draw_calls} | LOD: {lod_level}", "PERFORMANCE")
    
    def log_warning(self, message: str):
        self.log(message, "WARNING")
    
    def log_error(self, message: str):
        self.log(message, "ERROR")


class LogWindowButton(QtWidgets.QPushButton):
    
    def __init__(self, log_window: LogWindow):
        super().__init__("📋 Log Window")
        self.log_window = log_window
        self.setCheckable(True)
        self.toggled.connect(self.on_toggled)
        
        self.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                background-color:
                color:
                border: 1px solid
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color:
            }
            QPushButton:checked {
                background-color:
                border-color:
            }
        """)
    
    def on_toggled(self, checked: bool):
        if checked:
            self.log_window.show()
            self.log_window.raise_()
            self.log_window.activateWindow()
        else:
            self.log_window.hide()