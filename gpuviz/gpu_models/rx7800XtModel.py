"""
RX 7800 XT GPU Model - Ultra Realistic with All Real-World Components
Complete 1:1 replica with every component found on actual RX 7800 XT
"""

from .baseGpuModel import BaseGPUModel
from typing import Dict, Tuple
import math

class RX7800XTModel(BaseGPUModel):
    """Ultra-realistic RX 7800 XT GPU model with all real-world components."""

    # Component specifications
    LENGTH_MM = 267.0
    WIDTH_MM = 120.0
    HEIGHT_MM = 50.0
    GPU_DIE_SIZE_MM = 20.0
    GPU_DIE_THICKNESS_MM = 0.8
    MCD_DIE_SIZE_MM = 7.0
    VRAM_CHIPS = 8
    VRAM_CHIP_SIZE_MM = 12.0
    HEATSINK_FINS = 42
    HEAT_PIPES = 4
    FAN_COUNT = 3
    PCB_LENGTH_MM = 247.0
    PCB_WIDTH_MM = 106.0
    PCB_THICKNESS_MM = 1.5

    def __init__(self, view3d_instance):
        super().__init__(view3d_instance)
        self.interactive_components = {}
        self.animation_state = {
            'current_animation': None,
            'animation_frame': 0,
            'animation_speed': 1.0,
            'pulsing_components': set(),
            'highlighted_component': None
        }
        self._define_interactive_components()

    def _define_interactive_components(self):
        """Define interactive components for RX 7800 XT with tooltips and workflows."""
        self.interactive_components = {
            'gpu_die': {
                'position': (0, 0, 0.18),
                'bounds': (-1.0, -1.0, 0.18, 2.0, 2.0, 0.08),
                'tooltip': 'Navi32 GPU Die: 3,840 CUDA cores, 5nm GCD + 6nm MCDs, 2.3 GHz boost clock',
                'workflow': 'gpu_compute'
            },
            'vram_chips': {
                'position': (-4, -2.5, 0.1),
                'bounds': (-5, -3.5, 0.1, 8, 6, 0.1),
                'tooltip': '8x Samsung GDDR6 VRAM: 16GB total, 256-bit bus, 19.5 Gbps, 624 GB/s bandwidth',
                'workflow': 'memory_bandwidth'
            },
            'vrm_modules': {
                'position': (-9, -3, 0.1),
                'bounds': (-10, -4, 0.1, 20, 8, 0.2),
                'tooltip': '12-phase VRM: Digital PWM, 40A power stages, supports 263W TDP',
                'workflow': 'power_delivery'
            },
            'fans': {
                'position': (-4.5, 0, 0.4),
                'bounds': (-7, -2.6, 0.35, 11, 5.2, 0.3),
                'tooltip': 'Triple Axial-tech fans: 11 blades each, fluid dynamic bearings, optimized tri-fan airflow',
                'workflow': 'cooling_system'
            },
            'heat_pipes': {
                'position': (-3, -1.5, 2),
                'bounds': (-3.5, -2, 0.3, 6, 3, 24),
                'tooltip': '4x 8mm nickel-plated copper heat pipes: Vapor chamber cooling, full die coverage',
                'workflow': 'thermal_management'
            },
            'display_ports': {
                'position': (13.65, -2, -1),
                'bounds': (13.5, -3, -1.5, 1, 6, 1),
                'tooltip': 'Display outputs: 2x DP 2.1, 1x HDMI 2.1a, 8K@60Hz HDR support',
                'workflow': 'display_output'
            },
            'power_connectors': {
                'position': (13.65, 5.25, -1),
                'bounds': (13.5, 4, -1.5, 1.5, 3, 1),
                'tooltip': 'Power connectors: Dual 8-pin, 263W TDP, dual BIOS switch',
                'workflow': 'power_input'
            },
            'thermal_sensors': {
                'position': (0, -4, 0.05),
                'bounds': (-4.5, -4.5, 0.05, 9, 0.5, 0.1),
                'tooltip': 'Thermal monitoring: Multiple sensors, 95°C max temp, real-time temperature control',
                'workflow': 'thermal_monitoring'
            },
            'bios_chip': {
                'position': (-4, -4, 0.05),
                'bounds': (-4.8, -4.6, 0.05, 0.8, 0.6, 0.1),
                'tooltip': 'Dual BIOS: Safe firmware updates, AMD optimized settings',
                'workflow': 'firmware_management'
            },
            'clock_generator': {
                'position': (4, -4, 0.05),
                'bounds': (3.3, -4.6, 0.05, 0.6, 0.6, 0.1),
                'tooltip': 'High-precision clock generator: Stable frequencies, dynamic clock scaling',
                'workflow': 'clock_management'
            }
        }

    def handle_hover_event(self, component_name):
        """Handle hover event for interactive components."""
        if component_name in self.interactive_components:
            self.animation_state['highlighted_component'] = component_name
            self.animation_state['pulsing_components'].add(component_name)
            return self.interactive_components[component_name]['tooltip']
        return None

    def handle_click_event(self, component_name):
        """Handle click event for interactive components."""
        if component_name in self.interactive_components:
            workflow = self.interactive_components[component_name]['workflow']
            self._start_workflow_animation(workflow)
            return f"Showing {workflow.replace('_', ' ').title()} workflow"
        return None

    def handle_hover_leave_event(self, component_name):
        """Handle hover leave event for interactive components."""
        if component_name in self.animation_state['pulsing_components']:
            self.animation_state['pulsing_components'].discard(component_name)
        if self.animation_state['highlighted_component'] == component_name:
            self.animation_state['highlighted_component'] = None

    def update_animation(self, delta_time):
        """Update animation state."""
        if self.animation_state['current_animation']:
            self.animation_state['animation_frame'] += delta_time * self.animation_state['animation_speed']
            if self.animation_state['animation_frame'] > 1.0:
                self.animation_state['animation_frame'] = 0.0

    def _start_workflow_animation(self, workflow_name):
        """Start a workflow animation."""
        self.animation_state['current_animation'] = workflow_name
        self.animation_state['animation_frame'] = 0.0

        # Show workflow animation dialog
        if hasattr(self.view3d, 'parent') and hasattr(self.view3d.parent, 'show_workflow_animation'):
            workflow_text = self._get_workflow_text(workflow_name)
            self.view3d.parent.show_workflow_animation(workflow_name.replace('_', ' ').title(), workflow_text)

    def _get_workflow_text(self, workflow_name):
        """Get workflow description text."""
        workflows = {
            'gpu_compute': 'GPU Compute Workflow: Shader instructions flow through 24 Workgroup Processors, each containing 2 Compute Units with 4 wavefronts. Matrix operations are accelerated by dedicated tensor cores.',
            'memory_bandwidth': 'Memory Bandwidth: 256-bit GDDR6 bus transfers data at 19.5 Gbps per pin. Infinity Cache reduces latency while MCDs handle memory compression and ECC.',
            'power_delivery': 'Power Delivery: 12-phase VRM converts 12V input to GPU voltages. Digital PWM provides precise voltage control with real-time telemetry.',
            'cooling_system': 'Cooling System: Triple Axial-tech fans create positive pressure airflow. Heat pipes transfer thermal energy from die to heatsink fins for dissipation.',
            'thermal_management': 'Thermal Management: Multiple sensors monitor temperatures. Fan curves adjust based on thermal load, maintaining optimal operating temperatures.',
            'display_output': 'Display Output: DisplayPort 2.1 and HDMI 2.1a controllers handle 8K@60Hz signals. DSC compression enables high-resolution displays.',
            'power_input': 'Power Input: Dual 8-pin connectors provide up to 263W. Efficiency optimization reduces power consumption during light workloads.',
            'thermal_monitoring': 'Thermal Monitoring: Real-time temperature tracking enables dynamic clock scaling. Hotspot detection prevents thermal throttling.',
            'firmware_management': 'Firmware Management: Dual BIOS provides fail-safe updates. Optimized settings maximize performance within thermal limits.',
            'clock_management': 'Clock Management: Precision clock generation enables dynamic frequency scaling. Boost clocks reach 2.3 GHz under optimal conditions.'
        }
        return workflows.get(workflow_name, 'Workflow animation not available')

    def _draw_matmul_animation(self):
        """Draw matrix multiplication animation."""
        frame = self.animation_state['animation_frame']
        intensity = abs(math.sin(frame * math.pi * 2)) * 0.5 + 0.5

        # Animate compute units
        for i in range(24):  # 24 WGPs
            x = (i % 6 - 2.5) * 0.6
            y = (i // 6 - 1.5) * 0.6
            color = (0.8 * intensity, 0.6 * intensity, 0.2 * intensity, 1.0)
            self.view3d._draw_3d_box(x - 0.15, y - 0.15, 0.18, 0.3, 0.3, 0.02, color)

    def _draw_memory_flow_animation(self):
        """Draw memory bandwidth animation."""
        frame = self.animation_state['animation_frame']

        # Animate data flow between GPU and VRAM
        for i in range(8):
            progress = (frame + i * 0.125) % 1.0
            x = -4 + progress * 12
            y = -2.5 + i * 0.625
            color = (0.2, 0.8 * progress, 0.9 * progress, 1.0)
            self.view3d._draw_3d_box(x - 0.1, y - 0.1, 0.15, 0.2, 0.2, 0.05, color)

    def _draw_power_delivery_animation(self):
        """Draw power delivery animation."""
        frame = self.animation_state['animation_frame']
        intensity = abs(math.sin(frame * math.pi * 4)) * 0.7 + 0.3

        # Animate VRM phases
        for i in range(12):
            x = -9 + (i % 6) * 3
            y = -3 + (i // 6) * 2
            color = (0.9 * intensity, 0.7 * intensity, 0.1 * intensity, 1.0)
            self.view3d._draw_3d_box(x - 0.3, y - 0.3, 0.1, 0.6, 0.6, 0.15, color)

    def _draw_cooling_animation(self):
        """Draw cooling system animation."""
        frame = self.animation_state['animation_frame']

        # Animate fan rotation
        for fan_idx, (x, y) in enumerate([(-4.5, 0), (0, 0), (4.5, 0)]):
            angle_offset = frame * math.pi * 2 * (1 if fan_idx % 2 == 0 else -1)
            for blade in range(11):
                angle = angle_offset + (blade / 11) * 2 * math.pi
                blade_x = x + 0.8 * math.cos(angle)
                blade_y = y + 0.8 * math.sin(angle)
                color = (0.3, 0.3, 0.4, 1.0)
                self.view3d._draw_3d_box(blade_x - 0.05, blade_y - 0.05, 0.4, 0.1, 0.1, 0.05, color)

    def _draw_thermal_animation(self):
        """Draw thermal management animation."""
        frame = self.animation_state['animation_frame']
        intensity = abs(math.sin(frame * math.pi * 2)) * 0.6 + 0.4

        # Animate heat flow through pipes
        for i, (x, y) in enumerate([(-3, -1.5), (0, -1.5), (3, -1.5), (-3, 1.5), (3, 1.5)]):
            progress = (frame + i * 0.2) % 1.0
            heat_x = x
            heat_y = y
            heat_z = 0.3 + progress * 24
            color = (1.0 * intensity, 0.3 * intensity, 0.1 * intensity, 0.8)
            self.view3d._draw_3d_cylinder(heat_x, heat_y, heat_z, 0.15, 0.5, color)

    def _draw_display_animation(self):
        """Draw display output animation."""
        frame = self.animation_state['animation_frame']

        # Animate signal flow to display ports
        for i, (x, y) in enumerate([(13.65, -2), (13.65, 0), (13.65, 2)]):
            progress = (frame + i * 0.33) % 1.0
            signal_z = -1 + progress * 2
            color = (0.1 * progress, 0.8 * progress, 0.2 * progress, 1.0)
            self.view3d._draw_3d_box(x - 0.2, y - 0.3, signal_z, 0.4, 0.6, 0.1, color)

    def _draw_power_input_animation(self):
        """Draw power input animation."""
        frame = self.animation_state['animation_frame']
        intensity = abs(math.sin(frame * math.pi * 3)) * 0.8 + 0.2

        # Animate power flow from connectors
        for i, (x, y) in enumerate([(13.65, 4.5), (13.65, 6.0)]):
            progress = (frame + i * 0.5) % 1.0
            power_x = x - progress * 18
            color = (1.0 * intensity, 0.8 * intensity, 0.0, 1.0)
            self.view3d._draw_3d_box(power_x - 0.2, y - 0.4, -1, 0.4, 0.8, 0.3, color)

    def _draw_thermal_monitoring_animation(self):
        """Draw thermal monitoring animation."""
        frame = self.animation_state['animation_frame']

        # Animate sensor readings
        for i, (x, y) in enumerate([(0, -4), (0, 4), (-4, 0), (4, 0)]):
            intensity = abs(math.sin(frame * math.pi * 2 + i)) * 0.7 + 0.3
            color = (0.1 * intensity, 0.9 * intensity, 0.1 * intensity, 1.0)
            self.view3d._draw_3d_box(x - 0.15, y - 0.15, 0.05, 0.3, 0.3, 0.08, color)

    def _draw_firmware_animation(self):
        """Draw firmware management animation."""
        frame = self.animation_state['animation_frame']

        # Animate BIOS chip activity
        intensity = abs(math.sin(frame * math.pi * 4)) * 0.6 + 0.4
        color = (0.1 * intensity, 0.8 * intensity, 0.1 * intensity, 1.0)
        self.view3d._draw_3d_box(-4 - 0.4, -4 - 0.3, 0.05, 0.8, 0.6, 0.08, color)

    def _draw_clock_animation(self):
        """Draw clock management animation."""
        frame = self.animation_state['animation_frame']

        # Animate clock signal distribution
        intensity = abs(math.sin(frame * math.pi * 6)) * 0.8 + 0.2
        color = (0.9 * intensity, 0.7 * intensity, 0.1 * intensity, 1.0)
        self.view3d._draw_3d_box(4 - 0.3, -4 - 0.3, 0.05, 0.6, 0.6, 0.08, color)

    def handle_component_click(self, component_name):
        """Handle component click for workflow animations."""
        if component_name in self.interactive_components:
            workflow = self.interactive_components[component_name]['workflow']
            self._start_workflow_animation(workflow)

    def _draw_current_animation(self):
        """Draw the current active animation."""
        animation = self.animation_state['current_animation']
        if animation == 'gpu_compute':
            self._draw_matmul_animation()
        elif animation == 'memory_bandwidth':
            self._draw_memory_flow_animation()
        elif animation == 'power_delivery':
            self._draw_power_delivery_animation()
        elif animation == 'cooling_system':
            self._draw_cooling_animation()
        elif animation == 'thermal_management':
            self._draw_thermal_animation()
        elif animation == 'display_output':
            self._draw_display_animation()
        elif animation == 'power_input':
            self._draw_power_input_animation()
        elif animation == 'thermal_monitoring':
            self._draw_thermal_monitoring_animation()
        elif animation == 'firmware_management':
            self._draw_firmware_animation()
        elif animation == 'clock_management':
            self._draw_clock_animation()

    def get_model_name(self) -> str:
        return "AMD Radeon RX 7800 XT (Ultra Realistic)"

    def get_chassis_dimensions(self) -> Tuple[float, float, float]:
        """RX 7800 XT exact dimensions: 267mm x 120mm x 50mm"""
        return (self.LENGTH_MM/10, self.WIDTH_MM/10, self.HEIGHT_MM/10)

    def get_component_list(self) -> Dict[str, str]:
        """Get RX 7800 XT specific components with detailed explanations."""
        return {
            "Chassis": "267mm x 120mm x 50mm aluminum chassis with AMD signature design",
            "Triple Fans": "3x AMD Axial-tech fans with 11 blades, fluid dynamic bearing",
            "Vapor Chamber": "Large vapor chamber with 4 heat pipes covering full die",
            "GPU Die": "Navi32 GPU, 3,840 CUDA cores, 16GB GDDR6 memory, chiplet architecture",
            "VRAM Layout": "8x Samsung GDDR6 chips in 256-bit configuration",
            "Power Delivery": "12-phase VRM with 40A power stages and digital PWM",
            "Backplate": "Reinforced aluminum with AMD logo and 25% ventilation area",
            "PCB Design": "12-layer custom PCB with 3oz copper layers, AMD red PCB",
            "Display Outputs": "2x DisplayPort 2.1, 1x HDMI 2.1a, supports 8K@60Hz HDR",
            "Power Connector": "8-pin + 8-pin connectors supporting up to 263W",
            "Heat Pipes": "4x 8mm nickel-plated copper heat pipes",
            "VRM Cooling": "Extended heatsinks with fin arrays for power stages",
            "Memory Interface": "256-bit memory bus, 19.5 Gbps effective, 624 GB/s bandwidth",
            "Clock Speeds": "2.3 GHz boost, 1.7 GHz base, 35.4 TFLOPS single precision",
            "Illumination": "Red LED lighting on fan shroud and side logo",
            "Thermal Design": "2.5-slot design, 263W TDP, 95°C max operating temperature",
            "Ventilation": "Optimized airflow path with 75% open area, tri-fan design",
            "BIOS Chip": "Dual BIOS switch for safe firmware updates",
            "Clock Generator": "High-precision clock generator for stable frequencies",
            "Power Management": "Advanced power management ICs for efficiency",
            "Thermal Sensors": "Multiple temperature sensors for monitoring",
            "Display Controllers": "TMDS and DisplayPort 2.1 controllers for outputs",
            "Chiplet Design": "5nm GCD + 6nm MCDs for optimal performance and efficiency",
            "Voltage Regulators": "12-phase voltage regulation modules",
            "Capacitors": "High-quality polymer capacitors for power delivery",
            "Inductors": "Power inductors for voltage regulation",
            "Resistors": "Surface mount resistors for signal conditioning",
            "PCB Traces": "Copper traces for power and data distribution"
        }

    def draw_chassis(self, lod: int):
        """Draw RX 7800 XT chassis."""
        if self.view3d and hasattr(self.view3d, 'show_chassis') and self.view3d.show_chassis and self.should_render_component("chassis"):
            self._draw_rx7800xt_chassis()

    def draw_cooling_system(self, lod: int):
        """Draw RX 7800 XT cooling system."""
        if self.view3d and hasattr(self.view3d, 'show_cooling') and self.view3d.show_cooling and self.should_render_component("cooling"):
            self._draw_rx7800xt_heatsink()
            self._draw_rx7800xt_heat_pipes()
            self._draw_rx7800xt_fans()

    def draw_pcb_and_components(self, lod: int):
        """Draw RX 7800 XT PCB and all components."""
        if self.view3d and hasattr(self.view3d, 'show_pcb') and self.view3d.show_pcb and self.should_render_component("pcb"):
            self._draw_rx7800xt_pcb()
        if self.view3d and hasattr(self.view3d, 'show_gpu_die') and self.view3d.show_gpu_die and self.should_render_component("gpu_die"):
            self._draw_rx7800xt_gpu_die()
        if self.view3d and hasattr(self.view3d, 'show_vram') and self.view3d.show_vram and self.should_render_component("vram"):
            self._draw_rx7800xt_vram()
        if self.view3d and hasattr(self.view3d, 'show_power_delivery') and self.view3d.show_power_delivery and self.should_render_component("power_delivery"):
            self._draw_rx7800xt_power_delivery()

    def draw_backplate(self, lod: int):
        """Draw RX 7800 XT backplate."""
        if self.view3d and hasattr(self.view3d, 'show_backplate') and self.view3d.show_backplate and self.should_render_component("backplate"):
            self._draw_rx7800xt_backplate()
        if self.view3d and hasattr(self.view3d, 'show_io_bracket') and self.view3d.show_io_bracket and self.should_render_component("io_bracket"):
            self._draw_rx7800xt_io_bracket()

    def draw_complete_model(self, lod: int):
        """Draw the complete RX 7800 XT model with all real-world components."""
        # Draw from back to front for proper depth
        self.draw_backplate(lod)
        self.draw_pcb_and_components(lod)
        self.draw_cooling_system(lod)
        self.draw_chassis(lod)

        # Draw current animation if active
        if self.animation_state['current_animation']:
            self._draw_current_animation()

    def draw_ultra_realistic_model(self):
        """Draw ultra-realistic 1:1 replica with microscopic details."""
        self.draw_complete_model(0)

    def _draw_rx7800xt_pcb(self):
        """Draw ultra-detailed RX 7800 XT PCB with all real-world components."""
        if not self.view3d:
            return

        # Main PCB board - realistic dimensions (247mm x 106mm x 1.5mm)
        pcb_length = self.PCB_LENGTH_MM / 10
        pcb_width = self.PCB_WIDTH_MM / 10
        pcb_thickness = self.PCB_THICKNESS_MM / 10

        # PCB substrate with AMD signature red color
        pcb_color = (0.25, 0.1, 0.1, 1.0)
        self.view3d._draw_3d_box(-pcb_length/2, -pcb_width/2, -pcb_thickness/2,
                                 pcb_length, pcb_width, pcb_thickness, pcb_color)

        # Draw PCB traces and microscopic components
        if hasattr(self.view3d, 'show_traces') and self.view3d.show_traces:
            self._draw_pcb_traces(pcb_length, pcb_width)

        if hasattr(self.view3d, 'show_microscopic') and self.view3d.show_microscopic:
            self._draw_microscopic_components(pcb_length, pcb_width)

        # Draw all real-world PCB components
        self._draw_rx7800xt_pcb_components(pcb_length, pcb_width)

    def _draw_pcb_traces(self, pcb_length, pcb_width):
        """Draw realistic PCB traces."""
        trace_color = (0.7, 0.6, 0.3, 0.8)

        # Main power traces (thicker)
        for i in range(5):
            y = -pcb_width/2 + (i + 1) * (pcb_width / 6)
            self.view3d._draw_3d_box(-pcb_length/2 + 2, y - 0.1, 0.08,
                                     pcb_length - 4, 0.2, 0.05, trace_color)

        # Data traces (medium thickness)
        for i in range(10):
            y = -pcb_width/2 + i * (pcb_width / 10)
            for j in range(12):
                x = -pcb_length/2 + j * (pcb_length / 12)
                self.view3d._draw_3d_box(x, y - 0.05, 0.08, 0.3, 0.1, 0.03, trace_color)

    def _draw_microscopic_components(self, pcb_length, pcb_width):
        """Draw resistors, capacitors, and other tiny components."""
        # Surface mount resistors (0402 size: 1.0mm x 0.5mm)
        resistor_color = (0.3, 0.2, 0.1, 1.0)

        for i in range(100):
            x = -pcb_length/2 + 2 + (i % 18) * (pcb_length - 4) / 18
            y = -pcb_width/2 + 1 + (i // 18) * (pcb_width - 2) / 6

            self.view3d._draw_3d_box(x, y, 0.05, 0.1, 0.05, 0.02, resistor_color)

        # Surface mount capacitors
        capacitor_color = (0.1, 0.1, 0.2, 1.0)

        for i in range(50):
            x = -pcb_length/2 + 2 + (i % 10) * (pcb_length - 4) / 10
            y = -pcb_width/2 + 1 + (i // 10) * (pcb_width - 2) / 5

            self.view3d._draw_3d_cylinder(x, y, 0.05, 0.03, 0.1, capacitor_color)

        # Inductors
        inductor_color = (0.2, 0.15, 0.1, 1.0)

        for i in range(10):
            x = -pcb_length/2 + 3 + i * (pcb_length - 6) / 10
            y = -pcb_width/2 + pcb_width - 2

            self.view3d._draw_3d_cylinder(x, y, 0.05, 0.08, 0.15, inductor_color)

    def _draw_rx7800xt_pcb_components(self, pcb_length, pcb_width):
        """Draw all real-world RX 7800 XT PCB components."""
        # GPU Die (Navi32 chiplet)
        self._draw_rx7800xt_gpu_die()

        # GDDR6 VRAM chips (8 chips for 256-bit bus)
        self._draw_rx7800xt_vram()

        # VRM (Voltage Regulator Modules)
        self._draw_rx7800xt_vrms()

        # Power delivery components
        self._draw_rx7800xt_power_delivery()

        # DisplayPort and HDMI controllers
        self._draw_rx7800xt_display_controllers()

        # Thermal sensors and monitoring chips
        self._draw_rx7800xt_thermal_sensors()

        # BIOS chip
        self._draw_rx7800xt_bios()

        # Clock generator
        self._draw_rx7800xt_clock_generator()

        # Power management ICs
        self._draw_rx7800xt_power_management()

    def _draw_rx7800xt_gpu_die(self):
        """Draw Navi32 GPU die with chiplet architecture."""
        # Main Graphics Compute Die (GCD) - 5nm
        gcd_size = self.GPU_DIE_SIZE_MM / 10

        # GCD package substrate
        self.view3d._draw_3d_box(-gcd_size/2, -gcd_size/2, 0, gcd_size, gcd_size, 0.1,
                                 (0.05, 0.08, 0.05, 1.0))

        # GCD silicon die
        self.view3d._draw_3d_box(-gcd_size/2, -gcd_size/2, 0.1, gcd_size, gcd_size, self.GPU_DIE_THICKNESS_MM/10,
                                 (0.15, 0.15, 0.2, 1.0))

        # Draw WGP layout (4 WGPs per shader engine, 6 shader engines = 24 WGPs total for RX 7800 XT)
        self._draw_navi32_wgp_layout_7800xt(gcd_size, 0.18)

        # Memory Cache Dies (MCDs) - 6nm
        mcd_size = self.MCD_DIE_SIZE_MM / 10
        mcd_positions = [(-3, 0), (3, 0)]

        for x, y in mcd_positions:
            # MCD package
            self.view3d._draw_3d_box(x - mcd_size/2, y - mcd_size/2, 0, mcd_size, mcd_size, 0.08,
                                     (0.08, 0.05, 0.05, 1.0))

            # MCD silicon die
            self.view3d._draw_3d_box(x - mcd_size*0.75, y - mcd_size*0.75, 0.08, mcd_size*1.5, mcd_size*1.5, 0.06,
                                     (0.2, 0.15, 0.15, 1.0))

        # Heat spreader covering all dies
        hs_size = 3.5
        hs_thickness = 0.05
        self.view3d._draw_3d_box(-hs_size/2, -hs_size/2, 0.18,
                                 hs_size, hs_size, hs_thickness,
                                 (0.6, 0.6, 0.65, 1.0))

    def _draw_navi32_wgp_layout_7800xt(self, die_size, z_offset):
        """Draw exact Navi32 WGP layout for RX 7800 XT (24 WGPs)."""
        # RX 7800 XT has 6 Shader Engines, each with 4 WGPs (24 total)
        shader_engines = 6
        wgps_per_se = 4

        # Calculate WGP dimensions
        wgp_cols = 6
        wgp_rows = 4
        wgp_width = die_size / (wgp_cols + 1)
        wgp_height = die_size / (wgp_rows + 1)

        for se in range(shader_engines):
            for wgp in range(wgps_per_se):
                wgp_index = se * wgps_per_se + wgp
                row = wgp_index // wgp_cols
                col = wgp_index % wgp_cols

                x = -die_size/2 + (col + 0.5) * wgp_width
                y = -die_size/2 + (row + 0.5) * wgp_height

                # WGP tile
                wgp_color = (0.35, 0.25, 0.15, 0.9)
                self.view3d._draw_3d_box(x - wgp_width/3, y - wgp_height/3, z_offset,
                                         wgp_width*0.66, wgp_height*0.66, 0.015, wgp_color)

                # Draw compute units within WGP (2 CUs per WGP)
                self._draw_compute_units_in_wgp(x, y, wgp_width, wgp_height, z_offset + 0.015)

    def _draw_compute_units_in_wgp(self, wgp_x, wgp_y, wgp_width, wgp_height, z_offset):
        """Draw individual compute units within a WGP."""
        # Each WGP has 2 Compute Units
        for cu in range(2):
            cu_x = wgp_x - wgp_width/4 + cu * wgp_width/2
            cu_y = wgp_y

            # CU cluster
            cu_color = (0.45, 0.35, 0.25, 1.0)
            self.view3d._draw_3d_box(cu_x - wgp_width/6, cu_y - wgp_height/6, z_offset,
                                     wgp_width/3, wgp_height/3, 0.008, cu_color)

            # Draw wavefronts within CU (simplified representation)
            for wave in range(4):
                wave_x = cu_x - wgp_width/12 + (wave % 2) * wgp_width/12
                wave_y = cu_y - wgp_height/12 + (wave // 2) * wgp_height/12
                wave_color = (0.55, 0.45, 0.35, 1.0)
                self.view3d._draw_3d_box(wave_x - 0.02, wave_y - 0.02, z_offset + 0.008,
                                         0.04, 0.04, 0.004, wave_color)

    def _draw_rx7800xt_vram(self):
        """Draw 8 GDDR6 VRAM chips in exact RX 7800 XT layout (256-bit bus)."""
        # RX 7800 XT has 8 VRAM chips
        vram_positions = [
            # Front chips
            (-4, -2.5), (0, -2.5), (4, -2.5),
            (-4, 0), (0, 0), (4, 0),
            # Back chips
            (-2, 2.5), (2, 2.5)
        ]

        for i, (x, y) in enumerate(vram_positions):
            self._draw_gddr6_chip(x, y, 0.1 if i < 6 else -0.2, front=i < 6)

    def _draw_gddr6_chip(self, x, y, z, front=True):
        """Draw individual GDDR6 VRAM chip with microscopic details."""
        # GDDR6 package (12mm x 8mm x 1mm)
        package_color = (0.05, 0.05, 0.1, 1.0) if front else (0.03, 0.03, 0.06, 1.0)
        self.view3d._draw_3d_box(x - 0.6, y - 0.4, z, 1.2, 0.8, 0.1, package_color)

        # GDDR6 die (8mm x 6mm x 0.8mm)
        die_color = (0.25, 0.25, 0.35, 1.0) if front else (0.15, 0.15, 0.25, 1.0)
        self.view3d._draw_3d_box(x - 0.4, y - 0.3, z + 0.1, 0.8, 0.6, 0.08, die_color)

        # Microscopic bonding wires
        if front:
            wire_color = (0.8, 0.8, 0.7, 1.0)
            for i in range(8):
                wire_x = x - 0.35 + i * 0.07
                self._draw_bonding_wire(wire_x, y, z + 0.18, wire_x, y - 0.25, z + 0.05, wire_color)

    def _draw_bonding_wire(self, x1, y1, z1, x2, y2, z2, color):
        """Draw microscopic bonding wire."""
        # Simplified bonding wire representation
        self.view3d._draw_3d_box(x1 - 0.01, y1 - 0.01, z1, 0.02, (y2-y1) + 0.02, 0.01, color)

    def _draw_rx7800xt_vrms(self):
        """Draw 12-phase VRM power delivery system."""
        # VRM positions around the GPU die
        vrm_positions = [
            # Left side VRMs (6 phases)
            (-9, -3), (-9, -1), (-9, 1),
            (-7, -3), (-7, -1), (-7, 1),
            # Right side VRMs (6 phases)
            (7, -3), (7, -1), (7, 1),
            (9, -3), (9, -1), (9, 1)
        ]

        for i, (x, y) in enumerate(vrm_positions):
            # Main VRM chip
            vrm_color = (0.2, 0.2, 0.2, 1.0)
            self.view3d._draw_3d_box(x - 0.5, y - 0.5, 0.1, 1.0, 1.0, 0.2, vrm_color)

            # Heatsink fins on VRM
            for fin in range(4):
                fin_x = x - 0.4 + fin * 0.1
                fin_color = (0.7, 0.7, 0.8, 1.0)
                self.view3d._draw_3d_box(fin_x, y - 0.6, 0.3, 0.06, 0.2, 0.25, fin_color)

    def _draw_rx7800xt_power_delivery(self):
        """Draw additional power delivery components."""
        # Power inductors
        inductor_positions = [(-9, -5), (-9, 5), (9, -5), (9, 5)]
        inductor_color = (0.15, 0.1, 0.05, 1.0)

        for x, y in inductor_positions:
            self.view3d._draw_3d_cylinder(x, y, 0.15, 0.3, 0.4, inductor_color)

        # Power capacitors
        capacitor_positions = [(-6, -5), (-2, -5), (2, -5), (6, -5)]
        capacitor_color = (0.1, 0.1, 0.15, 1.0)

        for x, y in capacitor_positions:
            self.view3d._draw_3d_cylinder(x, y, 0.1, 0.2, 0.3, capacitor_color)

    def _draw_rx7800xt_display_controllers(self):
        """Draw DisplayPort and HDMI controller chips."""
        # DisplayPort 2.1 controllers
        dp_positions = [(10.5, -2), (10.5, 0)]
        dp_color = (0.1, 0.1, 0.2, 1.0)

        for x, y in dp_positions:
            self.view3d._draw_3d_box(x - 0.3, y - 0.2, 0.1, 0.6, 0.4, 0.15, dp_color)

        # HDMI 2.1a controller
        hdmi_color = (0.15, 0.1, 0.2, 1.0)
        self.view3d._draw_3d_box(10.5 - 0.3, 2 - 0.2, 0.1, 0.6, 0.4, 0.15, hdmi_color)

    def _draw_rx7800xt_thermal_sensors(self):
        """Draw thermal sensor chips."""
        # Thermal sensor positions
        sensor_positions = [(0, -4), (0, 4), (-4, 0), (4, 0)]
        sensor_color = (0.1, 0.2, 0.1, 1.0)

        for x, y in sensor_positions:
            self.view3d._draw_3d_box(x - 0.2, y - 0.2, 0.05, 0.4, 0.4, 0.1, sensor_color)

    def _draw_rx7800xt_bios(self):
        """Draw BIOS chip."""
        bios_color = (0.05, 0.1, 0.05, 1.0)
        self.view3d._draw_3d_box(-4, -4, 0.05, 0.8, 0.6, 0.1, bios_color)

    def _draw_rx7800xt_clock_generator(self):
        """Draw clock generator chip."""
        clock_color = (0.1, 0.15, 0.1, 1.0)
        self.view3d._draw_3d_box(4, -4, 0.05, 0.6, 0.6, 0.1, clock_color)

    def _draw_rx7800xt_power_management(self):
        """Draw power management ICs."""
        pmic_positions = [(-2, -4), (0, -4), (2, -4)]
        pmic_color = (0.15, 0.1, 0.1, 1.0)

        for x, y in pmic_positions:
            self.view3d._draw_3d_box(x - 0.3, y - 0.3, 0.05, 0.6, 0.6, 0.1, pmic_color)

    def _draw_rx7800xt_heatsink(self):
        """Draw large heatsink with vapor chamber and fins."""
        # Heatsink base
        base_color = (0.75, 0.75, 0.8, 1.0)
        self.view3d._draw_3d_box(-13.35, -6, 0.5, 26.7, 12, 2.8, base_color)

        # Heatsink fins (42 fins for RX 7800 XT)
        fin_count = self.HEATSINK_FINS
        fin_thickness = 0.08
        fin_spacing = 26.7 / fin_count

        for i in range(fin_count):
            x = -13.35 + i * fin_spacing
            fin_color = (0.8, 0.8, 0.85, 1.0)
            self.view3d._draw_3d_box(x, -5.8, 0.5, fin_thickness, 11.6, 4.0, fin_color)

    def _draw_rx7800xt_heat_pipes(self):
        """Draw 4 heat pipes with realistic routing."""
        # Heat pipe positions across the heatsink
        heat_pipe_positions = [
            (-3, -1.5), (0, -1.5), (3, -1.5),
            (-3, 1.5), (3, 1.5)
        ]

        pipe_color = (0.8, 0.5, 0.2, 1.0)

        for x, y in heat_pipe_positions[:4]:  # Only 4 heat pipes for RX 7800 XT
            # Main heat pipe
            self.view3d._draw_3d_cylinder(x, y, 2, 0.25, 24, pipe_color)

            # Heat pipe contact with GPU
            contact_color = (0.8, 0.5, 0.2, 1.0)
            self.view3d._draw_3d_cylinder(x, y, 0.3, 0.2, 1.7, contact_color)

    def _draw_rx7800xt_fans(self):
        """Draw triple AMD Axial-tech fans with 11 blades each."""
        fan_positions = [(-4.5, 0), (0, 0), (4.5, 0)]
        fan_radius = 2.6

        for i, (x, y) in enumerate(fan_positions):
            # Fan hub
            hub_color = (0.12, 0.12, 0.15, 1.0)
            self.view3d._draw_3d_cylinder(x, y, 0.4, 0.8, 0.3, hub_color)

            # Fan blades (11 blades per fan)
            blade_color = (0.18, 0.18, 0.22, 1.0)
            for blade in range(11):
                angle = (blade / 11) * 2 * math.pi
                self._draw_fan_blade(x, y, 0.4, fan_radius, angle, blade_color)

            # Fan frame
            frame_color = (0.25, 0.25, 0.3, 1.0)
            self.view3d._draw_3d_cylinder(x, y, 0.35, fan_radius + 0.1, 0.2, frame_color)

    def _draw_fan_blade(self, cx, cy, cz, radius, angle, color):
        """Draw individual fan blade."""
        blade_length = radius - 0.7
        blade_width = 0.3

        x1 = cx + 0.7 * math.cos(angle)
        y1 = cy + 0.7 * math.sin(angle)
        x2 = cx + radius * math.cos(angle)
        y2 = cy + radius * math.sin(angle)

        self.view3d._draw_3d_box(x1 - blade_width/2, y1 - 0.1, cz,
                                 blade_width, blade_length, 0.05, color)

    def _draw_rx7800xt_chassis(self):
        """Draw AMD signature chassis with optimized ventilation."""
        chassis_color = (0.85, 0.85, 0.9, 1.0)

        # Main chassis body
        self.view3d._draw_3d_box(-13.35, -6, 0, 26.7, 12, 5.0, chassis_color)

        # AMD signature ventilation (75% open area)
        vent_color = (0.05, 0.05, 0.08, 1.0)
        for i in range(30):
            x = -13 + i * (26.7 / 30)
            for j in range(5):
                y = -6 + j * 2.4
                self.view3d._draw_3d_box(x, y, 2.5, 0.5, 1.0, 0.1, vent_color)

    def _draw_rx7800xt_backplate(self):
        """Draw RX 7800 XT reinforced backplate with AMD logo."""
        # Backplate
        backplate_color = (0.75, 0.75, 0.8, 1.0)
        self.view3d._draw_3d_box(-13.35, -6, -2, 26.7, 12, 2, backplate_color)

        # Ventilation holes (25% open area)
        vent_color = (0.02, 0.02, 0.03, 1.0)
        for i in range(30):
            x = -13 + i * (26.7 / 30)
            for j in range(3):
                y = -5 + j * 3.3
                self.view3d._draw_3d_box(x, y, -2, 0.3, 0.8, 0.1, vent_color)

        # AMD logo area (simplified)
        logo_color = (0.8, 0.1, 0.1, 1.0)
        self.view3d._draw_3d_box(-2, -1.5, -1.9, 4, 3, 0.1, logo_color)

    def _draw_rx7800xt_io_bracket(self):
        """Draw I/O bracket with display ports and power connectors."""
        # I/O bracket
        bracket_color = (0.7, 0.7, 0.75, 1.0)
        self.view3d._draw_3d_box(13.35, -6, -2, 2.0, 12, 3.0, bracket_color)

        # Display ports (2x DisplayPort 2.1, 1x HDMI 2.1a)
        port_positions = [(13.65, -2, "DP"), (13.65, 0, "DP"), (13.65, 2, "HDMI")]

        for x, y, port_type in port_positions:
            port_color = (0.2, 0.2, 0.25, 1.0)
            self.view3d._draw_3d_box(x, y - 0.6, -1, 0.8, 1.2, 0.8, port_color)

        # 8-pin power connectors (2x)
        power_color = (0.15, 0.15, 0.2, 1.0)
        self.view3d._draw_3d_box(13.65, 4.5, -1, 1.0, 1.5, 0.8, power_color)
        self.view3d._draw_3d_box(13.65, 6.0, -1, 1.0, 1.5, 0.8, power_color)