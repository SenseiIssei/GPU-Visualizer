"""
GPU Workflow Animation Dialog

Shows detailed animations and explanations of GPU operations when components are clicked.
"""

from PySide6 import QtCore, QtWidgets, QtGui
import math
import time

class WorkflowAnimationDialog(QtWidgets.QDialog):
    """Dialog showing animated GPU workflow explanations."""

    def __init__(self, component_id: str, component_data: dict, parent=None, view3d=None):
        super().__init__(parent)
        self.component_id = component_id
        self.component_data = component_data
        self.animation_frame = 0
        self.animation_timer = QtCore.QTimer()
        self.animation_timer.timeout.connect(self.update_animation)

        self.setWindowTitle(f"GPU Workflow: {component_data['name']}")
        self.setModal(False)
        self.setMinimumSize(800, 600)
        self.view3d = view3d
        self.model = getattr(view3d, 'gpu_model', None) if view3d else None

        self.setup_ui()
        self.start_animation()

    def setup_ui(self):
        """Set up the dialog UI."""
        layout = QtWidgets.QVBoxLayout(self)

        # Title
        title = QtWidgets.QLabel(f" {self.component_data['name']} - Detailed Workflow")
        title.setStyleSheet("""
            QLabel {
                color: #4fc3f7;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        layout.addWidget(title)

        # Animation area
        self.animation_widget = WorkflowAnimationWidget(self.component_id, self.component_data)
        layout.addWidget(self.animation_widget)

        # 3D overlay controls
        overlay_group = QtWidgets.QGroupBox("3D Overlay Animations")
        overlay_layout = QtWidgets.QHBoxLayout(overlay_group)
        self.anim_mode_combo = QtWidgets.QComboBox()
        self.anim_mode_combo.addItem("Pulse", "pulse")
        self.anim_mode_combo.addItem("Flow", "flow")
        self.anim_mode_combo.addItem("Orbit", "orbit")
        overlay_layout.addWidget(self.anim_mode_combo)
        self.start3d_btn = QtWidgets.QPushButton(" Start 3D")
        self.start3d_btn.clicked.connect(self.on_start3d)
        overlay_layout.addWidget(self.start3d_btn)
        self.stop3d_btn = QtWidgets.QPushButton(" Stop 3D")
        self.stop3d_btn.clicked.connect(self.on_stop3d)
        overlay_layout.addWidget(self.stop3d_btn)
        layout.addWidget(overlay_group)

        # Description
        desc_label = QtWidgets.QLabel("Click and drag to explore the animation. Hover over elements for details.")
        desc_label.setStyleSheet("color: #cccccc; padding: 5px;")
        layout.addWidget(desc_label)

        # Control buttons
        button_layout = QtWidgets.QHBoxLayout()

        self.pause_btn = QtWidgets.QPushButton(" Pause")
        self.pause_btn.clicked.connect(self.toggle_pause)
        button_layout.addWidget(self.pause_btn)

        self.restart_btn = QtWidgets.QPushButton(" Restart")
        self.restart_btn.clicked.connect(self.restart_animation)
        button_layout.addWidget(self.restart_btn)

        close_btn = QtWidgets.QPushButton(" Close")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

    def start_animation(self):
        """Start the workflow animation."""
        self.animation_timer.start(50)  # 20 FPS
        self.pause_btn.setText(" Pause")

    def toggle_pause(self):
        """Toggle animation pause/play."""
        if self.animation_timer.isActive():
            self.animation_timer.stop()
            self.pause_btn.setText(" Play")
        else:
            self.animation_timer.start(50)
            self.pause_btn.setText(" Pause")

    def restart_animation(self):
        """Restart the animation from the beginning."""
        self.animation_frame = 0
        self.animation_widget.animation_frame = 0
        self.animation_widget.update()
        if not self.animation_timer.isActive():
            self.start_animation()

    def update_animation(self):
        """Update animation frame."""
        self.animation_frame += 1
        self.animation_widget.animation_frame = self.animation_frame
        self.animation_widget.update()

        # Loop continuously
        total = int(self.component_data.get('animation_frames', 240))
        if total > 0 and self.animation_frame >= total:
            self.animation_frame = 0

    def on_start3d(self):
        mode = None
        try:
            mode = self.anim_mode_combo.currentData()
        except Exception:
            mode = 'pulse'
        if self.model and hasattr(self.model, 'start_component_animation'):
            try:
                self.model.start_component_animation(self.component_id, mode or 'pulse')
            except Exception:
                pass

    def on_stop3d(self):
        if self.model and hasattr(self.model, 'stop_component_animation'):
            try:
                self.model.stop_component_animation(self.component_id)
            except Exception:
                pass


class WorkflowAnimationWidget(QtWidgets.QWidget):
    """Widget that renders the workflow animation."""

    def __init__(self, component_id: str, component_data: dict):
        super().__init__()
        self.component_id = component_id
        self.component_data = component_data
        self.animation_frame = 0
        self.setMinimumSize(780, 500)

        # Animation data
        self.workflow_type = component_data.get('workflow', 'default')
        self.particles = []
        self.initialize_animation_data()

    def initialize_animation_data(self):
        """Initialize animation data based on workflow type."""
        if self.workflow_type == 'tensor_matmul':
            self.initialize_matmul_data()
        elif self.workflow_type == 'memory_access':
            self.initialize_memory_data()
        elif self.workflow_type == 'sm_execution':
            self.initialize_sm_data()
        elif self.workflow_type == 'die_layout':
            self.initialize_die_data()

    def initialize_matmul_data(self):
        """Initialize matrix multiplication animation data."""
        self.particles = []
        # Matrix A tiles (blue)
        for i in range(16):
            self.particles.append({
                'type': 'matrix_a',
                'x': 50 + (i % 4) * 60,
                'y': 100 + (i // 4) * 60,
                'color': (0.2, 0.5, 0.8, 1.0),
                'size': 20
            })
        # Matrix B tiles (red)
        for i in range(16):
            self.particles.append({
                'type': 'matrix_b',
                'x': 350 + (i % 4) * 60,
                'y': 100 + (i // 4) * 60,
                'color': (0.8, 0.3, 0.3, 1.0),
                'size': 20
            })
        # Tensor cores (purple)
        for i in range(4):
            for j in range(4):
                self.particles.append({
                    'type': 'tensor_core',
                    'x': 200 + i * 80,
                    'y': 200 + j * 80,
                    'color': (0.6, 0.2, 0.8, 1.0),
                    'size': 30
                })

    def initialize_memory_data(self):
        """Initialize memory hierarchy animation data."""
        self.particles = []
        # HBM stacks
        for i in range(6):
            self.particles.append({
                'type': 'hbm',
                'x': 100 + i * 100,
                'y': 400,
                'color': (0.1, 0.1, 0.3, 1.0),
                'size': 40
            })
        # L2 cache
        self.particles.append({
            'type': 'l2_cache',
            'x': 350,
            'y': 300,
            'color': (0.3, 0.3, 0.1, 1.0),
            'size': 60
        })
        # L1 caches
        for i in range(4):
            self.particles.append({
                'type': 'l1_cache',
                'x': 150 + i * 150,
                'y': 200,
                'color': (0.4, 0.4, 0.2, 1.0),
                'size': 35
            })
        # Registers
        for i in range(8):
            self.particles.append({
                'type': 'registers',
                'x': 100 + i * 80,
                'y': 100,
                'color': (0.8, 0.2, 0.2, 1.0),
                'size': 25
            })

    def initialize_sm_data(self):
        """Initialize SM execution animation data."""
        self.particles = []
        # CUDA cores
        for i in range(32):
            self.particles.append({
                'type': 'cuda_core',
                'x': 100 + (i % 8) * 80,
                'y': 150 + (i // 8) * 80,
                'color': (0.2, 0.6, 0.2, 1.0),
                'size': 15
            })
        # Tensor cores
        for i in range(4):
            self.particles.append({
                'type': 'tensor_core',
                'x': 400 + (i % 2) * 100,
                'y': 200 + (i // 2) * 100,
                'color': (0.6, 0.2, 0.8, 1.0),
                'size': 25
            })
        # LD/ST units
        for i in range(4):
            self.particles.append({
                'type': 'ldst_unit',
                'x': 650,
                'y': 150 + i * 100,
                'color': (0.8, 0.6, 0.1, 1.0),
                'size': 20
            })

    def initialize_die_data(self):
        """Initialize die layout animation data."""
        self.particles = []
        # GPCs
        for i in range(8):
            self.particles.append({
                'type': 'gpc',
                'x': 150 + (i % 4) * 150,
                'y': 150 + (i // 4) * 200,
                'color': (0.3, 0.3, 0.5, 1.0),
                'size': 80
            })
        # Memory controllers
        for i in range(6):
            self.particles.append({
                'type': 'mem_ctrl',
                'x': 100 + i * 120,
                'y': 450,
                'color': (0.1, 0.1, 0.4, 1.0),
                'size': 30
            })

    def paintEvent(self, event):
        """Paint the workflow animation."""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # Clear background
        painter.fillRect(self.rect(), QtGui.QColor(20, 20, 30))

        # Draw workflow-specific animation
        if self.workflow_type == 'tensor_matmul':
            self.draw_matmul_animation(painter)
        elif self.workflow_type == 'memory_access':
            self.draw_memory_animation(painter)
        elif self.workflow_type == 'sm_execution':
            self.draw_sm_animation(painter)
        elif self.workflow_type == 'die_layout':
            self.draw_die_animation(painter)

        # Draw connecting lines and data flow
        self.draw_data_flow(painter)

    def draw_matmul_animation(self, painter):
        """Draw matrix multiplication workflow."""
        progress = (self.animation_frame % 240) / 240.0

        # Draw matrices
        self.draw_matrix(painter, 50, 100, "Matrix A", (0.2, 0.5, 0.8), progress)
        self.draw_matrix(painter, 350, 100, "Matrix B", (0.8, 0.3, 0.3), progress)
        self.draw_matrix(painter, 200, 350, "Result C", (0.3, 0.8, 0.3), progress)

        # Draw tensor cores
        for i in range(4):
            for j in range(4):
                x, y = 200 + i * 80, 200 + j * 80
                intensity = 0.5 + 0.5 * math.sin(progress * math.pi * 2 + (i + j) * 0.5)
                color = QtGui.QColor(int(intensity * 153), int(intensity * 51), int(intensity * 204))
                painter.setBrush(QtGui.QBrush(color))
                painter.drawEllipse(x - 15, y - 15, 30, 30)

        # Draw data flow arrows
        self.draw_flow_arrows(painter, progress)

    def draw_memory_animation(self, painter):
        """Draw memory hierarchy workflow."""
        progress = (self.animation_frame % 300) / 300.0

        # Draw memory hierarchy levels
        levels = [
            ("Registers", 100, 100, (0.8, 0.2, 0.2)),
            ("L1 Cache", 150, 200, (0.4, 0.4, 0.2)),
            ("L2 Cache", 350, 300, (0.3, 0.3, 0.1)),
            ("HBM", 100, 400, (0.1, 0.1, 0.3))
        ]

        for name, x, y, color in levels:
            self.draw_memory_level(painter, name, x, y, color, progress)

        # Draw data particles flowing
        for i in range(10):
            particle_progress = (progress + i * 0.1) % 1.0
            y_pos = 400 - particle_progress * 300
            x_pos = 100 + math.sin(particle_progress * math.pi * 4) * 50
            color = QtGui.QColor(100, 100, 255, 200)
            painter.setBrush(QtGui.QBrush(color))
            painter.drawEllipse(int(x_pos - 3), int(y_pos - 3), 6, 6)

    def draw_sm_animation(self, painter):
        """Draw SM execution workflow."""
        progress = (self.animation_frame % 200) / 200.0

        # Draw instruction pipeline stages
        stages = ["Fetch", "Decode", "Execute", "Memory", "Writeback"]
        for i, stage in enumerate(stages):
            x = 100 + i * 120
            y = 400
            intensity = 0.3 + 0.7 * math.sin(progress * math.pi * 2 - i * 0.5)
            color = QtGui.QColor(int(intensity * 255), int(intensity * 150), int(intensity * 100))
            painter.setBrush(QtGui.QBrush(color))
            painter.drawRect(x - 40, y - 20, 80, 40)

            painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255)))
            painter.drawText(x - 30, y + 5, stage)

        # Draw warp execution
        for warp in range(4):
            for thread in range(8):
                x = 150 + thread * 60
                y = 200 + warp * 60
                intensity = 0.5 + 0.5 * math.sin(progress * math.pi * 4 + warp + thread * 0.2)
                color = QtGui.QColor(int(intensity * 100), int(intensity * 200), int(intensity * 100))
                painter.setBrush(QtGui.QBrush(color))
                painter.drawRect(x - 8, y - 8, 16, 16)

    def draw_die_animation(self, painter):
        """Draw die layout workflow."""
        progress = (self.animation_frame % 180) / 180.0

        # Draw GPCs
        for i in range(8):
            x = 150 + (i % 4) * 150
            y = 150 + (i // 4) * 200
            intensity = 0.4 + 0.6 * math.sin(progress * math.pi * 2 + i * 0.3)
            color = QtGui.QColor(int(intensity * 76), int(intensity * 76), int(intensity * 127))
            painter.setBrush(QtGui.QBrush(color))
            painter.drawRect(x - 40, y - 40, 80, 80)

            painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255)))
            painter.drawText(x - 20, y + 5, f"GPC {i}")

        # Draw interconnect
        painter.setPen(QtGui.QPen(QtGui.QColor(150, 150, 150, 100), 2))
        for i in range(7):
            x1 = 150 + (i % 4) * 150
            y1 = 150 + (i // 4) * 200
            x2 = 150 + ((i + 1) % 4) * 150
            y2 = 150 + ((i + 1) // 4) * 200
            painter.drawLine(x1, y1, x2, y2)

    def draw_matrix(self, painter, x, y, label, color_tuple, progress):
        """Draw a matrix representation."""
        color = QtGui.QColor(int(color_tuple[0] * 255), int(color_tuple[1] * 255), int(color_tuple[2] * 255))
        painter.setBrush(QtGui.QBrush(color))

        # Draw matrix grid
        for i in range(4):
            for j in range(4):
                cell_x = x + i * 15
                cell_y = y + j * 15
                intensity = 0.5 + 0.5 * math.sin(progress * math.pi * 2 + (i + j) * 0.5)
                cell_color = QtGui.QColor(
                    int(color.red() * intensity),
                    int(color.green() * intensity),
                    int(color.blue() * intensity)
                )
                painter.setBrush(QtGui.QBrush(cell_color))
                painter.drawRect(cell_x - 7, cell_y - 7, 14, 14)

        # Draw label
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255)))
        painter.drawText(x - 20, y - 10, label)

    def draw_memory_level(self, painter, name, x, y, color_tuple, progress):
        """Draw a memory hierarchy level."""
        color = QtGui.QColor(int(color_tuple[0] * 255), int(color_tuple[1] * 255), int(color_tuple[2] * 255))
        painter.setBrush(QtGui.QBrush(color))
        painter.drawRect(x - 40, y - 15, 80, 30)

        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255)))
        painter.drawText(x - 30, y + 5, name)

    def draw_flow_arrows(self, painter, progress):
        """Draw data flow arrows."""
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 0, 150), 3, QtCore.Qt.DashLine))

        # Arrows from matrices to tensor cores
        arrows = [
            (150, 180, 200, 200),  # A to TC
            (350, 180, 280, 200),  # B to TC
            (240, 320, 240, 350)   # TC to C
        ]

        for x1, y1, x2, y2 in arrows:
            painter.drawLine(x1, y1, x2, y2)
            # Arrow head
            angle = math.atan2(y2 - y1, x2 - x1)
            painter.drawLine(x2, y2,
                          x2 - 10 * math.cos(angle - 0.3),
                          y2 - 10 * math.sin(angle - 0.3))
            painter.drawLine(x2, y2,
                          x2 - 10 * math.cos(angle + 0.3),
                          y2 - 10 * math.sin(angle + 0.3))

    def draw_data_flow(self, painter):
        """Draw data flow particles."""
        for particle in self.particles:
            x, y = particle['x'], particle['y']
            size = particle['size']
            color = particle['color']

            # Add some animation
            offset = math.sin(self.animation_frame * 0.1 + x * 0.01) * 2
            y += offset

            painter.setBrush(QtGui.QBrush(QtGui.QColor(
                int(color[0] * 255),
                int(color[1] * 255),
                int(color[2] * 255),
                int(color[3] * 255)
            )))
            painter.drawEllipse(int(x - size/2), int(y - size/2), size, size)