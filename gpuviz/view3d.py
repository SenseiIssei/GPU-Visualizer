"""
GPU 3D Visualization

Author: 𝙅𝙖𝙠𝙤𝙗 / 𝙎𝙚𝙣𝙨𝙚𝙞 𝙄𝙨𝙨𝙚𝙞

Overview:
- OpenGL-powered 3D rendering of GPU models with camera controls
- Smart caching, component highlighting, and performance modes
- Integrates with simulation for responsive visual updates
"""
from typing import Optional, Dict
from PySide6 import QtCore, QtGui, QtWidgets
import math
import time
from .gpu_models import get_gpu_model
from .componentHighlighter import ComponentType
from OpenGL.GL import (
    glClearColor, glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
    glEnable, GL_DEPTH_TEST, glMatrixMode, GL_PROJECTION, GL_MODELVIEW,
    glLoadIdentity, glViewport, glBegin, glEnd, glColor4f, glVertex3f,
    GL_QUADS, GL_LINES, glLineWidth,
    glDisable, GL_BLEND, glBlendFunc, GL_SRC_ALPHA, GL_ONE, glDepthFunc, GL_LESS,
    glPushMatrix, glPopMatrix, glVertex2f, glVertex4f, GL_TRIANGLE_STRIP,
    GL_TRIANGLE_FAN, GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, GL_QUAD_STRIP,
    GL_LINE_SMOOTH, glHint, GL_LINE_SMOOTH_HINT, GL_NICEST, glGenLists,
    glNewList, glEndList, glCallList, GL_COMPILE, glDeleteLists
)
from OpenGL.GLU import gluPerspective, gluLookAt
from OpenGL.GLUT import *

try:
    from OpenGL.GL import (
        glClearColor, glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
        glEnable, GL_DEPTH_TEST, glMatrixMode, GL_PROJECTION, GL_MODELVIEW,
        glLoadIdentity, glOrtho, glViewport, glBegin, glEnd, glColor4f, glVertex3f,
        GL_QUADS, GL_LINES, glLineWidth, glTranslatef, glRotatef, glScalef,
        glDisable, GL_BLEND, glBlendFunc, GL_SRC_ALPHA, GL_ONE, glDepthFunc, GL_LESS,
        glPushMatrix, glPopMatrix, glVertex2f, glVertex4f, GL_TRIANGLE_STRIP,
        GL_TRIANGLE_FAN, GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, GL_QUAD_STRIP,
        GL_LINE_SMOOTH, glHint, GL_LINE_SMOOTH_HINT, GL_NICEST
    )
    from OpenGL.GLU import gluPerspective, gluLookAt
    HAVE_GL = True
except Exception:
    HAVE_GL = False

try:
    from PySide6.QtOpenGLWidgets import QOpenGLWidget
    HAVE_QOPENGLWIDGET = True
except Exception:
    HAVE_QOPENGLWIDGET = False

from .models import GPULayout, SM
from .resources import COLORMAPS

BaseGL = QOpenGLWidget if (HAVE_QOPENGLWIDGET and HAVE_GL) else QtWidgets.QWidget

class GPU3DView(BaseGL):
    def __init__(self, layout: Optional[GPULayout] = None, sim=None, logger=None):
        super().__init__()
        self.layout = layout
        self.sim = sim
        self.logger = logger
        self.gpu_model = None

        self.camera_distance = 100.0
        self.camera_orbit_x = 0.0
        self.camera_orbit_y = 20.0
        self.camera_pan_x = 0.0
        self.camera_pan_y = 0.0
        self.zoom = 1.0
        self.fov = 45.0
        
        self.last_pos = None
        self.mouse_mode = "orbit"
        self.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.highlighted_component = None
        
        # Interactive component support
        self.interactive_components = {}
        self.hovered_component = None
        self.animation_timer = QtCore.QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_frame = 0
        
        # Interaction state
        self.isolate_highlight = False
        self._drag_threshold_px = 6
        self._mouse_press_pos = None
        self._dragging = False
        self._press_component_id = None
        # Hover picking throttle
        self._hover_pick_interval_s = 0.03
        self._last_pick_time = 0.0
        
        self.show_chassis = True
        self.show_cooling = True
        self.show_pcb = True
        self.show_gpu_die = True
        self.show_vram = True
        self.show_power_delivery = True
        self.show_backplate = True
        self.show_io_bracket = True
        self.show_microscopic = True
        self.show_traces = True
        
        self.performance_mode = "balanced"
        self._max_framerate = 60
        
        visibility_flags = [
            "show_chassis", "show_cooling", "show_pcb", "show_gpu_die",
            "show_vram", "show_power_delivery", "show_backplate",
            "show_io_bracket", "show_microscopic", "show_traces"
        ]
        for flag in visibility_flags:
            setattr(self, flag, True)
        
        self._cache = {}
        self._max_cache_size = 50
        
        self._cleanup_timer = QtCore.QTimer()
        self._cleanup_timer.timeout.connect(self._cleanup_memory)
        self._cleanup_timer.start(20000)
        
        if HAVE_QOPENGLWIDGET and HAVE_GL:
            self.setMinimumSize(1200, 800)
        else:
            lay = QtWidgets.QVBoxLayout(self)
            msg = []
            if not HAVE_QOPENGLWIDGET: msg.append("Missing QOpenGLWidget (PySide6.QtOpenGLWidgets).")
            if not HAVE_GL: msg.append("Missing PyOpenGL. Install: pip install PyOpenGL")
            lbl = QtWidgets.QLabel("\n".join(msg)); lbl.setAlignment(QtCore.Qt.AlignCenter)
            lay.addWidget(lbl)
        
        if layout:
            self.set_layout(layout)

    def reset_camera(self):
        self.camera_distance = 100.0
        self.camera_orbit_x = 0.0
        self.camera_orbit_y = 20.0
        self.camera_pan_x = 0.0
        self.camera_pan_y = 0.0
        self.zoom = 1.0
        self.update()

    def highlight_component(self, component_id: str):
        try:
            component_type = ComponentType(component_id)
            self.highlighted_component = component_type
            # Rebuild static cache only if we're isolating the highlight
            if getattr(self, 'isolate_highlight', False):
                self._gpu_cache_valid = False
            
            if hasattr(self, 'gpu_model') and self.gpu_model:
                self.gpu_model.highlight_component(component_id)
            else:
                self.update()
        except ValueError:
            self.clear_highlight()
    
    def clear_highlight(self):
        self.highlighted_component = None
        # Rebuild static cache only if we're isolating the highlight
        if getattr(self, 'isolate_highlight', False):
            self._gpu_cache_valid = False
        
        if hasattr(self, 'gpu_model') and self.gpu_model:
            self.gpu_model.clear_highlight()
        else:
            self.update()
    
    def set_component_visibility(self, component_type: str, visible: bool):
        visibility_map = {
            "chassis": "show_chassis",
            "cooling": "show_cooling",
            "pcb": "show_pcb",
            "gpu_die": "show_gpu_die",
            "vram": "show_vram",
            "power_delivery": "show_power_delivery",
            "backplate": "show_backplate",
            "io_bracket": "show_io_bracket",
            "microscopic": "show_microscopic",
            "traces": "show_traces"
        }
        
        if component_type in visibility_map:
            setattr(self, visibility_map[component_type], visible)
            # Invalidate GPU display-list cache so visibility change takes effect immediately
            self._gpu_cache_valid = False
            self.update()
    
    def set_performance_mode(self, mode: str):
        old_mode = self.performance_mode
        self.performance_mode = mode
        
        if mode == "low":
            self._max_framerate = 30
            self.show_microscopic = False
            self.show_traces = False
        elif mode == "balanced":
            self._max_framerate = 60
            self.show_microscopic = True
            self.show_traces = True
        else:
            self._max_framerate = 60
            self.show_microscopic = True
            self.show_traces = True
        
        # Adjust hover pick frequency and animation FPS
        if mode == "low":
            self._hover_pick_interval_s = 0.06  # ~16 picks/sec
            if self.animation_timer.isActive():
                self.animation_timer.setInterval(80)  # 12.5 FPS overlays
        elif mode == "balanced":
            self._hover_pick_interval_s = 0.03  # ~33 picks/sec
            if self.animation_timer.isActive():
                self.animation_timer.setInterval(50)  # 20 FPS overlays
        else:  # ultra
            self._hover_pick_interval_s = 0.02  # 50 picks/sec
            if self.animation_timer.isActive():
                self.animation_timer.setInterval(50)

        if self.logger and old_mode != mode:
            self.logger.log(f"Performance mode changed from {old_mode} to {mode}", "INFO")
        
        self.update()

    def set_layout(self, layout: GPULayout):
        self.layout = layout
        
        if hasattr(self, 'gpu_model') and self.gpu_model is not None:
            try:
                if hasattr(self.gpu_model, 'view3d_ref'):
                    self.gpu_model.view3d_ref = None
                self.gpu_model = None
                import gc
                gc.collect()
            except Exception as e:
                print(f"Warning: Failed to clean up old GPU model: {e}")
        
        self.clear_caches()
        
        try:
            if hasattr(layout, 'name'):
                self.gpu_model = get_gpu_model(layout.name, self)
                if self.logger:
                    self.logger.log_gpu_info(layout.name,
                                           sum(len(sm.cores) for g in layout.gpcs for sm in g.sms),
                                           len([sm for g in layout.gpcs for sm in g.sms]),
                                           len(layout.gpcs))
            else:
                self.gpu_model = get_gpu_model("RTX 4080 (Ada – illustrative)", self)
                if self.logger:
                    self.logger.log("Using default GPU model: RTX 4080", "INFO")
        except Exception as e:
            self.gpu_model = None
            if self.logger:
                self.logger.log_error(f"Failed to load GPU model: {e}")
        
        self.highlighted_component = None
        self.hovered_component = None
        self.interactive_components = {}
        
        # Initialize interactive components if GPU model supports them
        if self.gpu_model and hasattr(self.gpu_model, 'interactive_components'):
            self.interactive_components = self.gpu_model.interactive_components
        
        self.update()

    def set_colormap(self, name: str):
        self.color_map = COLORMAPS.get(name, COLORMAPS["Turbo"]); self.update()

    def update_animation(self):
        """Update animation frame for interactive components."""
        self.animation_frame += 1
        # Forward to GPU model if it supports per-frame animation updates
        if self.gpu_model and hasattr(self.gpu_model, 'update_animation'):
            try:
                self.gpu_model.update_animation(0.05)
            except Exception:
                pass
        # Do not invalidate static cache; overlays handle animations
        self.update()

    def get_component_at_position(self, mouse_x, mouse_y):
        """Perform raycasting to find which interactive component is at the given mouse position."""
        if not self.interactive_components or not HAVE_GL:
            return None
        
        # Get viewport dimensions
        viewport = self.rect()
        width = viewport.width()
        height = viewport.height()
        
        if width <= 0 or height <= 0:
            return None
        
        # Convert mouse coordinates to OpenGL coordinates
        gl_x = mouse_x
        gl_y = height - mouse_y  # Flip Y coordinate
        
        # Set up projection matrix for unprojection
        from OpenGL.GLU import gluUnProject
        from OpenGL.GL import glGetDoublev, GL_MODELVIEW_MATRIX, GL_PROJECTION_MATRIX, GL_VIEWPORT
        
        # Get current matrices
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport_array = [0, 0, width, height]
        
        # Unproject near and far points
        try:
            near_x, near_y, near_z = gluUnProject(gl_x, gl_y, 0.0, modelview, projection, viewport_array)
            far_x, far_y, far_z = gluUnProject(gl_x, gl_y, 1.0, modelview, projection, viewport_array)
        except:
            return None
        
        # Create ray direction
        ray_dir = [far_x - near_x, far_y - near_y, far_z - near_z]
        ray_length = math.sqrt(sum(x*x for x in ray_dir))
        if ray_length > 0:
            ray_dir = [x / ray_length for x in ray_dir]
        
        ray_origin = [near_x, near_y, near_z]
        
        # Check intersection with each interactive component
        closest_hit = None
        closest_distance = float('inf')
        
        for comp_id, comp_data in self.interactive_components.items():
            hit_distance = self._ray_intersects_component(ray_origin, ray_dir, comp_data)
            if hit_distance is not None and hit_distance < closest_distance:
                closest_distance = hit_distance
                closest_hit = comp_id
        
        return closest_hit

    def _ray_intersects_component(self, ray_origin, ray_dir, comp_data):
        """Check if ray intersects with a component's bounding box."""
        position = comp_data['position']
        size = comp_data['size']
        
        # Simple AABB (Axis-Aligned Bounding Box) intersection
        # Component bounds
        min_bounds = [position[0] - size[0]/2, position[1] - size[1]/2, position[2] - size[2]/2]
        max_bounds = [position[0] + size[0]/2, position[1] + size[1]/2, position[2] + size[2]/2]
        
        # Ray-AABB intersection algorithm
        tmin = 0.0
        tmax = float('inf')
        
        for i in range(3):
            if abs(ray_dir[i]) < 1e-6:
                # Ray is parallel to this axis
                if ray_origin[i] < min_bounds[i] or ray_origin[i] > max_bounds[i]:
                    return None
            else:
                t1 = (min_bounds[i] - ray_origin[i]) / ray_dir[i]
                t2 = (max_bounds[i] - ray_origin[i]) / ray_dir[i]
                
                tmin = max(tmin, min(t1, t2))
                tmax = min(tmax, max(t1, t2))
                
                if tmin > tmax:
                    return None
        
        return tmin if tmin >= 0 else None

    def handle_hover_event(self, component_id):
        """Handle hover enter for interactive component."""
        if self.gpu_model and hasattr(self.gpu_model, 'handle_hover_event'):
            self.gpu_model.handle_hover_event(component_id)
        
        # Show tooltip
        if component_id in self.interactive_components:
            comp_data = self.interactive_components[component_id]
            tooltip_text = f"{comp_data['name']}\n{comp_data['description']}"
            
            # Get global mouse position for tooltip
            cursor_pos = QtGui.QCursor.pos()
            QtWidgets.QToolTip.showText(cursor_pos, tooltip_text)
        
        # Do not invalidate static cache on hover; overlays will handle dynamic visuals

    def handle_click_event(self, component_id):
        """Handle click for interactive component."""
        if self.gpu_model and hasattr(self.gpu_model, 'handle_click_event'):
            self.gpu_model.handle_click_event(component_id)
        
        # Show workflow animation dialog for any clicked component
        if component_id in self.interactive_components:
            comp_data = self.interactive_components[component_id]
            from .workflow_animation_dialog import WorkflowAnimationDialog
            dialog = WorkflowAnimationDialog(component_id, comp_data, self.window(), view3d=self)
            dialog.show()

    def resizeGL(self, w, h):
        if not (HAVE_QOPENGLWIDGET and HAVE_GL): return
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION); glLoadIdentity()
        
        aspect = w / max(1.0, float(h))
        gluPerspective(self.fov / self.zoom, aspect, 1.0, 1000.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        if not (HAVE_QOPENGLWIDGET and HAVE_GL): return
        
        start_time = time.time()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        self._setup_camera()
        
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        
        if self.performance_mode == "low":
            glLineWidth(1.0)
            glDisable(GL_BLEND)
            glDisable(GL_LINE_SMOOTH)
        else:
            glLineWidth(1.2)
            glEnable(GL_BLEND)
            try:
                from OpenGL.GL import GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
                glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            except:
                glDisable(GL_BLEND)
        
        self._draw_gpu_smart_cached()
        
        render_time = (time.time() - start_time) * 1000
        if self.logger and render_time > 16.67:
            self.logger.log_performance("3D render frame", render_time)

    def _setup_camera(self):
        orbit_x_rad = math.radians(self.camera_orbit_x)
        orbit_y_rad = math.radians(self.camera_orbit_y)
        
        zoomed_distance = self.camera_distance / self.zoom
        
        cam_x = zoomed_distance * math.cos(orbit_y_rad) * math.sin(orbit_x_rad)
        cam_y = zoomed_distance * math.sin(orbit_y_rad)
        cam_z = zoomed_distance * math.cos(orbit_y_rad) * math.cos(orbit_x_rad)
        
        gluLookAt(
            cam_x + self.camera_pan_x, cam_y + self.camera_pan_y, cam_z,
            self.camera_pan_x, self.camera_pan_y, 0,
            0, 1, 0
        )

    def _draw_gpu_smart_cached(self):
        if hasattr(self, 'gpu_model') and self.gpu_model:
            try:
                current_state = self.get_component_visibility_state()
                # Rebuild static cache only when visibility/highlight state changes
                if (not hasattr(self, '_gpu_cache_valid') or not self._gpu_cache_valid or
                    current_state != getattr(self, '_cached_component_state', None)):
                    self._rebuild_gpu_cache()
                    self._cached_component_state = current_state
                    self._gpu_cache_valid = True

                # Draw static cached geometry
                if hasattr(self, '_gpu_display_list') and self._gpu_display_list:
                    glCallList(self._gpu_display_list)
                else:
                    self.gpu_model.draw_complete_model(0)

                # Draw dynamic overlays (hover/workflow animations) without touching the cache
                dynamic = bool(self.hovered_component) or self.animation_timer.isActive()
                if hasattr(self.gpu_model, 'animation_state'):
                    try:
                        dynamic = dynamic or bool(self.gpu_model.animation_state.get('current_workflow'))
                    except Exception:
                        pass
                if dynamic and hasattr(self.gpu_model, 'draw_dynamic_overlays'):
                    try:
                        self.gpu_model.draw_dynamic_overlays()
                    except Exception:
                        pass
                return
            except Exception as e:
                print(f"GPU model caching failed: {e}")
                try:
                    self.gpu_model.draw_complete_model(0)
                except Exception as e2:
                    print(f"GPU model rendering failed: {e2}")
                return

        if self.layout:
            self._draw_simple_gpu()

    def get_component_visibility_state(self):
        return {
            'show_chassis': self.show_chassis,
            'show_cooling': self.show_cooling,
            'show_pcb': self.show_pcb,
            'show_gpu_die': self.show_gpu_die,
            'show_vram': self.show_vram,
            'show_power_delivery': self.show_power_delivery,
            'show_backplate': self.show_backplate,
            'show_io_bracket': self.show_io_bracket,
            'show_microscopic': self.show_microscopic,
            'show_traces': self.show_traces
        }

    def _rebuild_gpu_cache(self):
        try:
            start_time = time.time()
            
            if hasattr(self, '_gpu_display_list') and self._gpu_display_list:
                glDeleteLists(self._gpu_display_list, 1)
            
            self._gpu_display_list = glGenLists(1)
            glNewList(self._gpu_display_list, GL_COMPILE)
            
            if hasattr(self, 'gpu_model') and self.gpu_model:
                self.gpu_model.draw_complete_model(0)
            
            glEndList()
            
            rebuild_time = (time.time() - start_time) * 1000
            if self.logger:
                self.logger.log_performance("GPU cache rebuild", rebuild_time)
                self.logger.log("GPU cache rebuilt successfully", "INFO")
            
        except Exception as e:
            if self.logger:
                self.logger.log_error(f"Failed to rebuild GPU cache: {e}")
            self._gpu_cache_valid = False

    def _draw_generic_ultra_gpu(self):
        if self.show_pcb:
            self._draw_ultra_pcb()
        
        if self.show_gpu_die:
            self._draw_ultra_gpu_package()
        
        if self.show_vram:
            self._draw_ultra_vram()
        
        if self.show_power_delivery:
            self._draw_ultra_power_delivery()
        
        if self.show_cooling:
            self._draw_ultra_cooling()
        
        if self.show_io_bracket:
            self._draw_ultra_io_bracket()
            
        if self.show_chassis:
            self._draw_ultra_chassis()

    def _draw_ultra_pcb(self):
        pcb_length = 28.5
        pcb_width = 11.0
        pcb_thickness = 0.15
        
        glColor4f(0.1, 0.25, 0.1, 1.0)
        self._draw_3d_box(-pcb_length/2, -pcb_width/2, -pcb_thickness/2,
                         pcb_length, pcb_width, pcb_thickness)
        
        if self.show_traces:
            self._draw_pcb_traces(pcb_length, pcb_width)
        
        if self.show_microscopic:
            self._draw_microscopic_components(pcb_length, pcb_width)

    def _draw_pcb_traces(self, pcb_length, pcb_width):
        glColor4f(0.7, 0.6, 0.3, 0.8)
        glLineWidth(0.1)
        
        for i in range(20):
            y = -pcb_width/2 + i * (pcb_width / 20)
            glBegin(GL_LINES)
            glVertex3f(-pcb_length/2, y, 0.08)
            glVertex3f(pcb_length/2, y, 0.08)
            glEnd()
        
        for i in range(50):
            x = -pcb_length/2 + i * (pcb_length / 50)
            glBegin(GL_LINES)
            glVertex3f(x, -pcb_width/2, 0.08)
            glVertex3f(x, pcb_width/2, 0.08)
            glEnd()

    def _draw_microscopic_components(self, pcb_length, pcb_width):
        resistor_color = (0.3, 0.2, 0.1, 1.0)
        
        for i in range(100):
            x = -pcb_length/2 + (i % 20) * (pcb_length / 20)
            y = -pcb_width/2 + (i // 20) * (pcb_width / 5)
            
            glColor4f(*resistor_color)
            self._draw_3d_box(x, y, 0.05, 0.1, 0.05, 0.02)
        
        capacitor_color = (0.1, 0.1, 0.2, 1.0)
        
        for i in range(50):
            x = -pcb_length/2 + (i % 10) * (pcb_length / 10)
            y = -pcb_width/2 + 2 + (i // 10) * 0.5
            
            glColor4f(*capacitor_color)
            self._draw_3d_box(x, y, 0.05, 0.1, 0.05, 0.02)

    def _draw_ultra_gpu_package(self):
        pkg_size = 3.0
        pkg_thickness = 0.1
        
        glColor4f(0.05, 0.1, 0.05, 1.0)
        self._draw_3d_box(-pkg_size/2, -pkg_size/2, 0, pkg_size, pkg_size, pkg_thickness)
        
        die_size = 1.5
        die_thickness = 0.08
        
        glColor4f(0.2, 0.2, 0.3, 1.0)
        self._draw_3d_box(-die_size/2, -die_size/2, pkg_thickness,
                         die_size, die_size, die_thickness)
        
        if self.detail_level == "ultra":
            self._draw_die_microstructure(die_size, pkg_thickness)

    def _draw_die_microstructure(self, die_size, z_offset):
        sm_grid = 8
        sm_size = die_size / (sm_grid + 1)
        die_thickness = 0.08
        
        for i in range(sm_grid):
            for j in range(sm_grid):
                x = -die_size/2 + (i + 0.5) * sm_size
                y = -die_size/2 + (j + 0.5) * sm_size
            
                glColor4f(0.4, 0.3, 0.2, 0.9)
                self._draw_3d_box(x - sm_size/3, y - sm_size/3, z_offset + die_thickness,
                                 sm_size*0.66, sm_size*0.66, 0.01)
                
                if self.detail_level == "ultra":
                    for ci in range(4):
                        for cj in range(4):
                            cx = x - sm_size/3 + (ci + 0.5) * sm_size/6
                            cy = y - sm_size/3 + (cj + 0.5) * sm_size/6
                            glColor4f(0.6, 0.5, 0.4, 1.0)
                            self._draw_3d_box(cx - 0.02, cy - 0.02, z_offset + die_thickness + 0.01,
                                             0.04, 0.04, 0.005)

    def _draw_ultra_vram(self):
        vram_positions = [
            (-8, -4), (-4, -4), (0, -4), (4, -4), (8, -4),
            (-8, 4), (-4, 4), (0, 4), (4, 4), (8, 4),
            (-10, 0), (10, 0)
        ]
        
        for x, y in vram_positions:
            glColor4f(0.1, 0.1, 0.2, 1.0)
            self._draw_3d_box(x - 0.7, y - 0.4, 0.1, 1.4, 0.8, 0.1)
            
            glColor4f(0.3, 0.3, 0.4, 1.0)
            self._draw_3d_box(x - 0.5, y - 0.3, 0.2, 1.0, 0.6, 0.05)
            
            if self.detail_level == "ultra":
                glColor4f(0.8, 0.8, 0.7, 1.0)
                for i in range(8):
                    wire_x = x - 0.4 + i * 0.1
                    self._draw_bonding_wire(wire_x, y, 0.25, wire_x, y - 0.2, 0.1)

    def _draw_bonding_wire(self, x1, y1, z1, x2, y2, z2):
        glLineWidth(0.02)
        glColor4f(0.8, 0.8, 0.7, 1.0)
        glBegin(GL_LINES)
        glVertex3f(x1, y1, z1)
        glVertex3f((x1+x2)/2, (y1+y2)/2, max(z1, z2) + 0.1)
        glVertex3f((x1+x2)/2, (y1+y2)/2, max(z1, z2) + 0.1)
        glVertex3f(x2, y2, z2)
        glEnd()

    def _draw_ultra_power_delivery(self):
        vrm_positions = [(-12, -8), (-12, 8), (12, -8), (12, 8)]
        
        for x, y in vrm_positions:
            glColor4f(0.2, 0.2, 0.2, 1.0)
            self._draw_3d_box(x - 0.5, y - 0.5, 0.1, 1.0, 1.0, 0.2)
            
            for i in range(10):
                fin_x = x - 0.4 + i * 0.08
                glColor4f(0.7, 0.7, 0.8, 1.0)
                self._draw_3d_box(fin_x, y - 0.6, 0.3, 0.06, 0.2, 0.3)

    def _draw_ultra_cooling(self):
        glColor4f(0.8, 0.8, 0.85, 1.0)
        self._draw_3d_box(-15, -6, 0.5, 30, 12, 2)
        
        fin_count = 60
        fin_thickness = 0.1
        fin_spacing = 30.0 / fin_count
        
        for i in range(fin_count):
            x = -15 + i * fin_spacing
            glColor4f(0.85, 0.85, 0.9, 1.0)
            self._draw_3d_box(x, -5.5, 0.5, fin_thickness, 11, 4)
        
        pipe_color = (0.8, 0.5, 0.2, 1.0)
        for y in [-3, 0, 3]:
            glColor4f(*pipe_color)
            self._draw_3d_cylinder(0, y, 2, 0.3, 28)

    def _draw_simple_gpu(self):
        gpu_color = (0.7, 0.7, 0.75, 1.0)
        
        self._draw_3d_box(-15, -6, 0, 30, 12, 4, gpu_color)
        
        pcb_color = (0.1, 0.1, 0.15, 1.0)
        self._draw_3d_box(-14, -5, -0.5, 28, 10, 0.2, pcb_color)
        
        die_color = (0.2, 0.2, 0.25, 1.0)
        self._draw_3d_box(-2, -2, 0.2, 4, 4, 0.1, die_color)
        
        fan_color = (0.15, 0.15, 0.2, 1.0)
        self._draw_3d_cylinder(-8, 0, 2, 2, 0.5, fan_color)
        self._draw_3d_cylinder(0, 0, 2, 2, 0.5, fan_color)
        self._draw_3d_cylinder(8, 0, 2, 2, 0.5, fan_color)

    def _draw_ultra_io_bracket(self):
        glColor4f(0.7, 0.7, 0.75, 1.0)
        self._draw_3d_box(15, -7, -2, 2, 14, 3)
        
        port_positions = [(16, -4), (16, -2), (16, 0), (16, 2)]
        for i, (x, y) in enumerate(port_positions):
            glColor4f(0.3, 0.3, 0.4, 1.0)
            self._draw_3d_box(x, y, -1, 0.8, 1.2, 0.5)

    def _draw_3d_box(self, x, y, z, w, h, d, color=None):
        if color:
            glColor4f(*color)
        
        glBegin(GL_QUADS)
        glVertex3f(x, y, z + d)
        glVertex3f(x + w, y, z + d)
        glVertex3f(x + w, y + h, z + d)
        glVertex3f(x, y + h, z + d)
        glEnd()
        
        glBegin(GL_QUADS)
        glVertex3f(x, y, z)
        glVertex3f(x, y + h, z)
        glVertex3f(x + w, y + h, z)
        glVertex3f(x + w, y, z)
        glEnd()
        
        glBegin(GL_QUADS)
        glVertex3f(x, y + h, z)
        glVertex3f(x, y + h, z + d)
        glVertex3f(x + w, y + h, z + d)
        glVertex3f(x + w, y + h, z)
        glEnd()
        
        glBegin(GL_QUADS)
        glVertex3f(x, y, z)
        glVertex3f(x + w, y, z)
        glVertex3f(x + w, y, z + d)
        glVertex3f(x, y, z + d)
        glEnd()
        
        glBegin(GL_QUADS)
        glVertex3f(x + w, y, z)
        glVertex3f(x + w, y + h, z)
        glVertex3f(x + w, y + h, z + d)
        glVertex3f(x + w, y, z + d)
        glEnd()
        
        glBegin(GL_QUADS)
        glVertex3f(x, y, z)
        glVertex3f(x, y, z + d)
        glVertex3f(x, y + h, z + d)
        glVertex3f(x, y + h, z)
        glEnd()

    def _draw_3d_cylinder(self, cx, cy, cz, radius, height, color=None):
        if color:
            glColor4f(*color)
        
        segments = 16
        glBegin(GL_QUAD_STRIP)
        for i in range(segments + 1):
            angle = 2.0 * math.pi * i / segments
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            glVertex3f(x, y, cz)
            glVertex3f(x, y, cz + height)
        glEnd()

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        if not (HAVE_QOPENGLWIDGET and HAVE_GL): return
        self.last_pos = e.pos()
        
        if e.button() == QtCore.Qt.LeftButton:
            self.mouse_mode = "orbit"
            # Prepare for click-or-drag detection; defer click handling to mouseReleaseEvent
            self._mouse_press_pos = e.pos()
            self._press_component_id = self.get_component_at_position(e.x(), e.y())
            self._dragging = False
        elif e.button() == QtCore.Qt.RightButton:
            self.mouse_mode = "pan"
        elif e.button() == QtCore.Qt.MiddleButton:
            self.mouse_mode = "zoom"

    def mouseMoveEvent(self, event):
        if self.last_pos is None:
            self.last_pos = event.pos()
            return
        
        dx = event.x() - self.last_pos.x()
        dy = event.y() - self.last_pos.y()
        
        if event.buttons() & QtCore.Qt.LeftButton:
            # Treat as drag if movement exceeds threshold, and always orbit on drag
            if self._mouse_press_pos is not None:
                dist2 = (event.x() - self._mouse_press_pos.x())**2 + (event.y() - self._mouse_press_pos.y())**2
                if dist2 >= (self._drag_threshold_px ** 2):
                    self._dragging = True
            self.camera_orbit_x += dx * 1.0
            self.camera_orbit_y += dy * 1.0
            self.camera_orbit_y = max(-89, min(89, self.camera_orbit_y))
            self.update()
        elif event.buttons() & QtCore.Qt.RightButton:
            self.camera_pan_x += dx * 0.25
            self.camera_pan_y += dy * 0.25
            self.update()
        
        # Handle hover detection with throttling (skip while dragging to keep orbit smooth)
        current_component = self.hovered_component
        now_ts = time.time()
        if not self._dragging and (now_ts - self._last_pick_time) >= self._hover_pick_interval_s:
            current_component = self.get_component_at_position(event.x(), event.y())
            self._last_pick_time = now_ts
        
        if current_component != self.hovered_component:
            if self.hovered_component:
                # Hover leave - stop animation
                self.animation_timer.stop()
                self.animation_frame = 0
                if self.gpu_model and hasattr(self.gpu_model, 'handle_hover_leave_event'):
                    self.gpu_model.handle_hover_leave_event(self.hovered_component)
            
            self.hovered_component = current_component
            
            if current_component:
                # Hover enter - start animation and handle event
                # Set FPS based on performance mode
                if self.performance_mode == "low":
                    self.animation_timer.start(80)  # ~12.5 FPS
                else:
                    self.animation_timer.start(50)  # 20 FPS
                self.handle_hover_event(current_component)
            else:
                # Clear tooltip when not hovering over any component
                QtWidgets.QToolTip.hideText()
        
        self.last_pos = event.pos()
    
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            did_click = False
            if self._mouse_press_pos is not None:
                dist2 = (event.x() - self._mouse_press_pos.x())**2 + (event.y() - self._mouse_press_pos.y())**2
                if dist2 < (self._drag_threshold_px ** 2) and self._press_component_id:
                    # Verify still over the same component on release
                    comp_at_release = self.get_component_at_position(event.x(), event.y())
                    if comp_at_release == self._press_component_id:
                        did_click = True
            if did_click:
                self.handle_click_event(self._press_component_id)
            self._mouse_press_pos = None
            self._press_component_id = None
            self._dragging = False
    
    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if delta > 0:
            self.zoom *= 1.12
        else:
            self.zoom *= 0.88
        self.zoom = max(0.1, min(10.0, self.zoom))
        self.update()

    def reset_camera(self):
        self.camera_distance = 100.0
        self.camera_orbit_x = 0.0
        self.camera_orbit_y = 20.0
        self.camera_pan_x = 0.0
        self.camera_pan_y = 0.0
        self.zoom = 1.0
        self.update()
            
    def get_component_visibility_state(self):
        return {
            "chassis": self.show_chassis,
            "cooling": self.show_cooling,
            "pcb": self.show_pcb,
            "gpu_die": self.show_gpu_die,
            "vram": self.show_vram,
            "power_delivery": self.show_power_delivery,
            "backplate": self.show_backplate,
            "io_bracket": self.show_io_bracket,
            "microscopic": self.show_microscopic,
            "traces": self.show_traces
        }
    
    def _cleanup_memory(self):
        try:
            if len(self._cache) > 20:
                self._cache.clear()
            
            import gc
            gc.collect()
            
        except Exception:
            pass
    
    def _get_cached(self, cache_key: str, generator_func):
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        result = generator_func()
        if len(self._cache) < self._max_cache_size:
            self._cache[cache_key] = result
        
        return result
    
    def clear_caches(self):
        self._cache.clear()
        
        if hasattr(self, '_gpu_display_list') and self._gpu_display_list:
            try:
                glDeleteLists(self._gpu_display_list, 1)
                self._gpu_display_list = None
            except:
                pass
        
        if hasattr(self, '_gpu_render_cache'):
            try:
                from OpenGL.GL import glDeleteLists
                for display_list in self._gpu_render_cache.values():
                    try:
                        glDeleteLists(display_list, 1)
                    except:
                        pass
                self._gpu_render_cache.clear()
            except ImportError:
                pass
        
        self._gpu_cache_valid = False
        self._last_gpu_model_id = None
        self._cached_component_state = None
        
        import gc
        gc.collect()