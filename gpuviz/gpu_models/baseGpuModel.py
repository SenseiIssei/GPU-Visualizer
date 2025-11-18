"""
Base GPU Model Class
Provides the foundation for all GPU model implementations
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
from OpenGL.GL import glColor4f
import math
import time
import random
import weakref

class BaseGPUModel(ABC):
    """Base class for all GPU 3D models."""
    
    def __init__(self, view3d_instance):
        # Use weak reference to prevent circular references with Qt objects
        self.view3d_ref = weakref.ref(view3d_instance)
        self.components = {}
        self.component_explanations = {}
        self.highlighted_component = None
        self._open_gl_initialized = False
        
    @property
    def view3d(self):
        """Get the view3d instance, returning None if it's been garbage collected."""
        return self.view3d_ref() if self.view3d_ref() is not None else None
        
    @abstractmethod
    def get_model_name(self) -> str:
        """Get the display name of this GPU model."""
        pass
        
    @abstractmethod
    def get_chassis_dimensions(self) -> Tuple[float, float, float]:
        """Get (width, height, depth) of the GPU chassis."""
        pass
        
    @abstractmethod
    def draw_chassis(self, lod: int):
        """Draw the main chassis/casing of the GPU."""
        pass
        
    @abstractmethod
    def draw_cooling_system(self, lod: int):
        """Draw fans, heatsink, and cooling components."""
        pass
        
    @abstractmethod
    def draw_pcb_and_components(self, lod: int):
        """Draw PCB, GPU die, VRAM, and power delivery."""
        pass
        
    @abstractmethod
    def draw_backplate(self, lod: int):
        """Draw the backplate and I/O bracket."""
        pass
        
    @abstractmethod
    def get_component_list(self) -> Dict[str, str]:
        """Get dictionary of component names and their explanations."""
        pass
        
    @abstractmethod
    def draw_ultra_realistic_model(self):
        """Draw ultra-realistic 1:1 replica with microscopic details."""
        pass
        
    def draw_complete_model(self, lod: int):
        """Draw the complete GPU model with all components."""
        self.draw_backplate(lod)
        self.draw_pcb_and_components(lod)
        self.draw_cooling_system(lod)
        self.draw_chassis(lod)
        
    def set_component_color(self, component_name: str, base_color: Tuple[float, float, float, float]):
        """Set color based on highlighting state."""
        if self.highlighted_component == component_name:
            glColor4f(1.0, 0.2, 0.1, 1.0)
        elif self.highlighted_component is not None:
            glColor4f(0.5, 0.5, 0.5, 0.2)
        else:
            glColor4f(*base_color)
            
    def is_component_highlighted(self, component_name: str) -> bool:
        """Check if component is currently highlighted."""
        return self.highlighted_component == component_name
        
    def should_render_component(self, component_name: str) -> bool:
        """Check if component should be rendered based on highlighting state."""
        v = getattr(self, 'view3d', None)
        try:
            isolate = bool(getattr(v, 'isolate_highlight', False)) if v else False
        except Exception:
            isolate = False
        if not isolate:
            # Show everything; highlighting only changes color (via set_component_color)
            return True
        # When isolating, only render the highlighted component
        if self.highlighted_component is None:
            return True
        return self.highlighted_component == component_name
        
    def highlight_component(self, component_name: str):
        """Highlight a specific component."""
        self.highlighted_component = component_name
        if self.view3d:
            self.view3d.update()
        
    def clear_highlight(self):
        """Clear component highlighting."""
        self.highlighted_component = None
        if self.view3d:
            self.view3d.update()
    
    def initialize_opengl(self):
        """Initialize OpenGL state for this GPU model."""
        if not self._open_gl_initialized:
            self._open_gl_initialized = True
            pass
    
    def update_animation(self, delta_time: float):
        """Default per-frame animation updater; models can override."""
        if hasattr(self, 'animation_state') and isinstance(self.animation_state, dict):
            try:
                # Advance a generic time and frame counter
                self.animation_state['animation_time'] = self.animation_state.get('animation_time', 0.0) + delta_time
                frame = self.animation_state.get('workflow_frame', 0) + 1
                total = max(1, int(self.animation_state.get('total_frames', 120)))
                if self.animation_state.get('loop', True) or self.animation_state.get('running', False):
                    # Loop frames to keep animations running continuously
                    self.animation_state['workflow_frame'] = frame % total
                else:
                    self.animation_state['workflow_frame'] = frame
                comps = self.animation_state.get('component_animations', {})
                for k, rec in list(comps.items()):
                    rec['t'] = rec.get('t', 0.0) + delta_time
            except Exception:
                pass
    
    def draw_dynamic_overlays(self):
        """Draw lightweight dynamic overlays (highlight glow and workflow animations)."""
        v = self.view3d
        if not v:
            return
        # Highlight overlay (glow) using interactive component bounds
        try:
            comp_id = self.highlighted_component
            comps = getattr(self, 'interactive_components', {})
            if comp_id and comp_id in comps:
                data = comps[comp_id]
                (cx, cy, cz) = data.get('position', (0, 0, 0))
                (sx, sy, sz) = data.get('size', (1, 1, 0.1))
                hc = data.get('hover_color', (1.0, 0.3, 0.2, 0.7))
                # Pulse alpha for a subtle effect
                try:
                    pulse = 0.3 + 0.2 * math.sin((getattr(v, 'animation_frame', 0) or 0) * 0.3)
                except Exception:
                    pulse = 0.4
                alpha = (hc[3] if len(hc) >= 4 else 0.6) * min(1.0, max(0.2, pulse))
                color = (hc[0], hc[1], hc[2], alpha)
                margin = 0.08
                v._draw_3d_box(cx - sx/2 - margin, cy - sy/2 - margin, cz - sz/2 - margin,
                               sx + 2*margin, sy + 2*margin, sz + 2*margin, color)
        except Exception:
            pass
        
        # Workflow overlays (model-specific animation helpers if present)
        try:
            state = getattr(self, 'animation_state', {}) or {}
            wf = state.get('current_workflow')
            if state.get('matmul_demo_active') and hasattr(self, '_draw_matmul_animation'):
                self._draw_matmul_animation()
            elif state.get('memory_flow_active') and hasattr(self, '_draw_memory_flow_animation'):
                self._draw_memory_flow_animation()
            elif state.get('tensor_core_demo') and hasattr(self, '_draw_tensor_core_animation'):
                self._draw_tensor_core_animation()
            elif wf == 'tensor_matmul' and hasattr(self, '_draw_tensor_core_animation'):
                self._draw_tensor_core_animation()
            elif wf == 'memory_access' and hasattr(self, '_draw_memory_flow_animation'):
                self._draw_memory_flow_animation()
            elif wf == 'die_layout' and hasattr(self, '_draw_matmul_animation'):
                self._draw_matmul_animation()
        except Exception:
            pass

        try:
            state = getattr(self, 'animation_state', {}) or {}
            comps = getattr(self, 'interactive_components', {})
            running = state.get('component_animations')
            if isinstance(running, dict) and running:
                for comp_id, rec in list(running.items()):
                    if comp_id not in comps:
                        continue
                    data = comps[comp_id]
                    (cx, cy, cz) = data.get('position', (0, 0, 0))
                    (sx, sy, sz) = data.get('size', (1, 1, 0.1))
                    mode = rec.get('mode', 'pulse')
                    t = rec.get('t', state.get('animation_time', 0.0))
                    if mode == 'flow':
                        self._draw_generic_flow_overlay(cx, cy, cz, sx, sy, sz, t)
                    elif mode == 'orbit':
                        self._draw_generic_orbit_overlay(cx, cy, cz, sx, sy, sz, t)
                    elif mode == 'ripple':
                        self._draw_generic_ripple_overlay(cx, cy, cz, sx, sy, sz, t)
                    elif mode == 'beam':
                        self._draw_generic_beam_overlay(cx, cy, cz, sx, sy, sz, t)
                    elif mode == 'sparkle':
                        self._draw_generic_sparkle_overlay(cx, cy, cz, sx, sy, sz, t, seed=hash(comp_id) & 0xFFFF)
                    else:
                        self._draw_generic_pulse_overlay(cx, cy, cz, sx, sy, sz, t)
            else:
                if state.get('running') and state.get('selected_component'):
                    comp_id = state.get('selected_component')
                    if comp_id in comps:
                        data = comps[comp_id]
                        (cx, cy, cz) = data.get('position', (0, 0, 0))
                        (sx, sy, sz) = data.get('size', (1, 1, 0.1))
                        mode = state.get('anim_mode', 'pulse')
                        t = state.get('animation_time', 0.0)
                        if mode == 'flow':
                            self._draw_generic_flow_overlay(cx, cy, cz, sx, sy, sz, t)
                        elif mode == 'orbit':
                            self._draw_generic_orbit_overlay(cx, cy, cz, sx, sy, sz, t)
                        elif mode == 'ripple':
                            self._draw_generic_ripple_overlay(cx, cy, cz, sx, sy, sz, t)
                        elif mode == 'beam':
                            self._draw_generic_beam_overlay(cx, cy, cz, sx, sy, sz, t)
                        elif mode == 'sparkle':
                            self._draw_generic_sparkle_overlay(cx, cy, cz, sx, sy, sz, t, seed=hash(comp_id) & 0xFFFF)
                        else:
                            self._draw_generic_pulse_overlay(cx, cy, cz, sx, sy, sz, t)
        except Exception:
            pass

    def start_component_animation(self, component_id: str, mode: str = 'pulse'):
        """Start a generic per-component animation that loops until stopped."""
        if not hasattr(self, 'animation_state') or not isinstance(getattr(self, 'animation_state', None), dict):
            self.animation_state = {}
        cams = self.animation_state.get('component_animations')
        if not isinstance(cams, dict):
            cams = {}
            self.animation_state['component_animations'] = cams
        cams[component_id] = {'mode': mode, 't': self.animation_state.get('animation_time', 0.0), 'running': True}
        self.animation_state['selected_component'] = component_id
        self.animation_state['anim_mode'] = mode
        self.animation_state['running'] = True
        self.animation_state['loop'] = True
        self.animation_state['animation_time'] = self.animation_state.get('animation_time', 0.0)
        self.animation_state['workflow_frame'] = self.animation_state.get('workflow_frame', 0)
        v = self.view3d
        if v and hasattr(v, 'animation_timer'):
            try:
                interval = 80 if getattr(v, 'performance_mode', 'balanced') == 'low' else 50
                v.animation_timer.start(interval)
            except Exception:
                pass
        if v:
            v.update()

    def stop_component_animation(self, component_id: str = None):
        """Stop generic per-component animations. If component_id is None, stops all."""
        if hasattr(self, 'animation_state') and isinstance(self.animation_state, dict):
            cams = self.animation_state.get('component_animations')
            if isinstance(cams, dict):
                if component_id is None:
                    cams.clear()
                else:
                    cams.pop(component_id, None)
            if not cams or len(cams) == 0:
                self.animation_state['running'] = False
                self.animation_state['anim_mode'] = None
                self.animation_state['selected_component'] = None
                try:
                    self.animation_state['current_workflow'] = None
                except Exception:
                    pass
        v = self.view3d
        if v:
            v.update()

    def _draw_generic_pulse_overlay(self, cx, cy, cz, sx, sy, sz, t):
        v = self.view3d
        if not v:
            return
        # Pulsating box around the component
        pulse = 0.5 + 0.5 * math.sin(t * 4.0)
        alpha = 0.25 + 0.35 * pulse
        color = (0.2, 0.7, 1.0, alpha)
        margin = 0.05 + 0.15 * pulse
        v._draw_3d_box(cx - sx/2 - margin, cy - sy/2 - margin, cz - sz/2 - margin,
                       sx + 2*margin, sy + 2*margin, max(0.05, sz + 2*margin), color)

    def _draw_generic_flow_overlay(self, cx, cy, cz, sx, sy, sz, t):
        v = self.view3d
        if not v:
            return
        # Moving particles along the component perimeter
        count = 16
        for i in range(count):
            phase = (t * 2.0 + i / count) % 1.0
            # interpolate along rectangle perimeter
            perim = 2*(sx + sy)
            dist = phase * perim
            if dist < sx:
                x = cx - sx/2 + dist; y = cy - sy/2
            elif dist < sx + sy:
                x = cx + sx/2; y = cy - sy/2 + (dist - sx)
            elif dist < 2*sx + sy:
                x = cx + sx/2 - (dist - (sx + sy)); y = cy + sy/2
            else:
                x = cx - sx/2; y = cy + sy/2 - (dist - (2*sx + sy))
            z = cz + sz/2 + 0.05
            color = (0.1 + 0.9*(i/count), 0.6, 1.0, 0.8)
            v._draw_3d_box(x - 0.06, y - 0.06, z, 0.12, 0.12, 0.04, color)

    def _draw_generic_orbit_overlay(self, cx, cy, cz, sx, sy, sz, t):
        v = self.view3d
        if not v:
            return
        # Small markers orbiting around the component center
        r = max(sx, sy) * 0.7
        for k in range(6):
            ang = t * 2.0 + k * (math.pi / 3)
            x = cx + r * 0.5 * math.cos(ang)
            y = cy + r * 0.5 * math.sin(ang)
            z = cz + sz/2 + 0.06
            color = (0.9, 0.4 + 0.1*math.sin(ang*2), 0.2, 0.85)
            v._draw_3d_box(x - 0.08, y - 0.08, z, 0.16, 0.16, 0.05, color)

    def _draw_generic_ripple_overlay(self, cx, cy, cz, sx, sy, sz, t):
        v = self.view3d
        if not v:
            return
        base = 0.08
        for i in range(3):
            phase = (t * 0.8 + i * 0.25) % 1.0
            m = base + phase * max(sx, sy) * 0.5
            alpha = max(0.05, 0.35 * (1.0 - phase))
            color = (0.2, 0.7, 1.0, alpha)
            v._draw_3d_box(cx - sx/2 - m, cy - sy/2 - m, cz - sz/2 - 0.02,
                           sx + 2*m, sy + 2*m, max(0.04, sz + 0.04), color)

    def _draw_generic_beam_overlay(self, cx, cy, cz, sx, sy, sz, t):
        v = self.view3d
        if not v:
            return
        u = (math.sin(t * 1.5) * 0.5 + 0.5)
        bx = cx - sx/2 + u * sx
        w = max(0.12, sx * 0.06)
        color = (1.0, 0.6, 0.2, 0.6)
        v._draw_3d_box(bx - w/2, cy - sy/2, cz + sz/2 + 0.03, w, sy, 0.06, color)

    def _draw_generic_sparkle_overlay(self, cx, cy, cz, sx, sy, sz, t, seed=0):
        v = self.view3d
        if not v:
            return
        rnd = random.Random(seed + int(t * 10))
        count = 12
        for _ in range(count):
            rx = cx - sx/2 + rnd.random() * sx
            ry = cy - sy/2 + rnd.random() * sy
            rz = cz + sz/2 + 0.07
            a = 0.4 + 0.6 * rnd.random()
            color = (1.0, 1.0, 0.8, 0.4 * a)
            v._draw_3d_box(rx - 0.06, ry - 0.06, rz, 0.12, 0.12, 0.04, color)
    
    def __del__(self):
        """Cleanup method to ensure proper disposal of resources."""
        try:
            # Clear weak reference
            if hasattr(self, 'view3d_ref'):
                self.view3d_ref = None
            # Clear any cached data
            if hasattr(self, 'components'):
                self.components.clear()
            if hasattr(self, 'component_explanations'):
                self.component_explanations.clear()
        except:
            pass
