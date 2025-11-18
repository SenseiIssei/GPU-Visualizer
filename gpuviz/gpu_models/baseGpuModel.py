"""
Base GPU Model Class
Provides the foundation for all GPU model implementations
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
from OpenGL.GL import glColor4f
import math
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
        if self.highlighted_component is None:
            return True
        if self.highlighted_component == component_name:
            return True
        return False
        
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
