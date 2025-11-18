"""
RTX 4090 GPU Model - Ultra Realistic with Smart Caching Support
Complete 1:1 replica with every component found on actual RTX 4090
Optimized for smooth rendering with display list caching
"""

from .baseGpuModel import BaseGPUModel
from typing import Dict, Tuple
import math

class RTX4090Model(BaseGPUModel):
    """Ultra-realistic RTX 4090 GPU model optimized for smooth rendering."""
    
    # Component specifications
    LENGTH_MM = 336.0
    WIDTH_MM = 140.0
    HEIGHT_MM = 61.0
    GPU_DIE_SIZE_MM = 18.0
    GPU_DIE_THICKNESS_MM = 0.8
    VRAM_CHIPS = 24
    VRAM_CHIP_SIZE_MM = 14.0
    HEATSINK_FINS = 150
    HEAT_PIPES = 10
    FAN_COUNT = 3
    PCB_LENGTH_MM = 304.0
    PCB_WIDTH_MM = 137.0
    PCB_THICKNESS_MM = 1.5
    
    def get_model_name(self) -> str:
        return "NVIDIA GeForce RTX 4090 (Ultra Realistic)"
        
    def get_chassis_dimensions(self) -> Tuple[float, float, float]:
        """RTX 4090 exact dimensions: 336mm x 140mm x 61mm"""
        return (self.LENGTH_MM/10, self.WIDTH_MM/10, self.HEIGHT_MM/10)
        
    def get_component_list(self) -> Dict[str, str]:
        """Get RTX 4090 specific components with detailed explanations."""
        return {
            "Chassis": "336mm x 140mm x 61mm aluminum chassis with optimized ventilation",
            "Triple Fans": "3x Axial-tech fans with 13 blades, dual ball bearings for quiet operation",
            "Vapor Chamber": "Large vapor chamber with 10 heat pipes covering full AD102 die",
            "GPU Die": "AD102-300 GPU, 16,384 CUDA cores, 24GB GDDR6X memory, 4nm process",
            "VRAM Layout": "24x Micron GDDR6X chips in 384-bit configuration, 21 Gbps effective",
            "Power Delivery": "24-phase VRM with 90A power stages and digital PWM controller",
            "Backplate": "Reinforced aluminum with 40% ventilation area for thermal performance",
            "PCB Design": "14-layer custom PCB with 6oz copper layers, optimized for power delivery",
            "Display Outputs": "3x DisplayPort 1.4a, 1x HDMI 2.1, supports 8K@60Hz HDR",
            "Power Connector": "12VHPWR connector supporting up to 600W with overcurrent protection",
            "Heat Pipes": "10x 8mm nickel-plated copper heat pipes with direct die contact",
            "VRM Cooling": "Extended heatsinks with fin arrays for power stage cooling",
            "Memory Interface": "384-bit memory bus, 21 Gbps effective, 1008 GB/s bandwidth",
            "Clock Speeds": "2.52 GHz boost, 2.23 GHz base, 82.6 TFLOPS single precision",
            "Illumination": "RGB lighting on side logo, software controllable via GeForce Experience",
            "Thermal Design": "3-slot design, 450W TDP, 90°C max operating temperature",
            "Ventilation": "Optimized airflow path with 90% open area for maximum cooling",
            "BIOS Chip": "Dual BIOS switch for safe firmware updates and overclocking profiles",
            "Clock Generator": "High-precision clock generator for stable frequencies",
            "Power Management": "Advanced power management ICs for efficiency monitoring",
            "Thermal Sensors": "Multiple temperature sensors for real-time monitoring",
            "Display Controllers": "TMDS and DisplayPort controllers for output management",
            "Voltage Regulators": "24-phase voltage regulation modules for stable power",
            "Capacitors": "High-quality polymer capacitors for clean power delivery",
            "Inductors": "Power inductors for voltage regulation and filtering",
            "Resistors": "Surface mount resistors for signal conditioning",
            "PCB Traces": "Copper traces for power and data distribution"
        }

    def draw_chassis(self, lod: int):
        """Draw RTX 4090 chassis with optimized ventilation."""
        if self.view3d and hasattr(self.view3d, 'show_chassis') and self.view3d.show_chassis and self.should_render_component("chassis"):
            self._draw_rtx4090_chassis()
        
    def draw_cooling_system(self, lod: int):
        """Draw RTX 4090 cooling system."""
        if self.view3d and hasattr(self.view3d, 'show_cooling') and self.view3d.show_cooling and self.should_render_component("cooling"):
            self._draw_rtx4090_heatsink()
            self._draw_rtx4090_heat_pipes()
            self._draw_rtx4090_fans()
        
    def draw_pcb_and_components(self, lod: int):
        """Draw RTX 4090 PCB and all components."""
        if self.view3d and hasattr(self.view3d, 'show_pcb') and self.view3d.show_pcb and self.should_render_component("pcb"):
            self._draw_rtx4090_pcb()
        if self.view3d and hasattr(self.view3d, 'show_gpu_die') and self.view3d.show_gpu_die and self.should_render_component("gpu_die"):
            self._draw_rtx4090_gpu_die()
        if self.view3d and hasattr(self.view3d, 'show_vram') and self.view3d.show_vram and self.should_render_component("vram"):
            self._draw_rtx4090_vram()
        if self.view3d and hasattr(self.view3d, 'show_power_delivery') and self.view3d.show_power_delivery and self.should_render_component("power_delivery"):
            self._draw_rtx4090_power_delivery()
        
    def draw_backplate(self, lod: int):
        """Draw RTX 4090 backplate."""
        if self.view3d and hasattr(self.view3d, 'show_backplate') and self.view3d.show_backplate and self.should_render_component("backplate"):
            self._draw_rtx4090_backplate()
        if self.view3d and hasattr(self.view3d, 'show_io_bracket') and self.view3d.show_io_bracket and self.should_render_component("io_bracket"):
            self._draw_rtx4090_io_bracket()

    def draw_complete_model(self, lod: int):
        """Draw the complete RTX 4090 model with all components optimized for caching."""
        # Draw from back to front for proper depth
        self.draw_backplate(lod)
        self.draw_pcb_and_components(lod)
        self.draw_cooling_system(lod)
        self.draw_chassis(lod)

    def draw_ultra_realistic_model(self):
        """Draw ultra-realistic 1:1 replica with microscopic details."""
        self.draw_complete_model(0)

    def _draw_rtx4090_pcb(self):
        """Draw ultra-detailed RTX 4090 PCB with all real-world components."""
        if not self.view3d:
            return
            
        # Main PCB board - realistic dimensions (304mm x 137mm x 1.5mm)
        pcb_length = self.PCB_LENGTH_MM / 10
        pcb_width = self.PCB_WIDTH_MM / 10
        pcb_thickness = self.PCB_THICKNESS_MM / 10
        
        # PCB substrate with NVIDIA black color
        pcb_color = (0.05, 0.05, 0.08, 1.0)
        self.view3d._draw_3d_box(-pcb_length/2, -pcb_width/2, -pcb_thickness/2,
                                 pcb_length, pcb_width, pcb_thickness, pcb_color)
        
        # Draw PCB traces and microscopic components
        if hasattr(self.view3d, 'show_traces') and self.view3d.show_traces:
            self._draw_pcb_traces(pcb_length, pcb_width)
        
        if hasattr(self.view3d, 'show_microscopic') and self.view3d.show_microscopic:
            self._draw_microscopic_components(pcb_length, pcb_width)
        
        # Draw all real-world PCB components
        self._draw_rtx4090_pcb_components(pcb_length, pcb_width)

    def _draw_pcb_traces(self, pcb_length, pcb_width):
        """Draw realistic PCB traces."""
        trace_color = (0.7, 0.6, 0.3, 0.8)
        
        # Main power traces (thicker)
        for i in range(8):
            y = -pcb_width/2 + (i + 1) * (pcb_width / 9)
            self.view3d._draw_3d_box(-pcb_length/2 + 2, y - 0.1, 0.08,
                                     pcb_length - 4, 0.2, 0.05, trace_color)
        
        # Data traces (medium thickness)
        for i in range(16):
            y = -pcb_width/2 + i * (pcb_width / 16)
            for j in range(20):
                x = -pcb_length/2 + j * (pcb_length / 20)
                self.view3d._draw_3d_box(x, y - 0.05, 0.08, 0.3, 0.1, 0.03, trace_color)

    def _draw_microscopic_components(self, pcb_length, pcb_width):
        """Draw resistors, capacitors, and other tiny components."""
        # Surface mount resistors (0402 size: 1.0mm x 0.5mm)
        resistor_color = (0.3, 0.2, 0.1, 1.0)
        
        for i in range(150):
            x = -pcb_length/2 + 2 + (i % 25) * (pcb_length - 4) / 25
            y = -pcb_width/2 + 1 + (i // 25) * (pcb_width - 2) / 6
            
            self.view3d._draw_3d_box(x, y, 0.05, 0.1, 0.05, 0.02, resistor_color)
        
        # Surface mount capacitors
        capacitor_color = (0.1, 0.1, 0.2, 1.0)
        
        for i in range(80):
            x = -pcb_length/2 + 2 + (i % 16) * (pcb_length - 4) / 16
            y = -pcb_width/2 + 1 + (i // 16) * (pcb_width - 2) / 5
            
            self.view3d._draw_3d_cylinder(x, y, 0.05, 0.03, 0.1, capacitor_color)
        
        # Inductors
        inductor_color = (0.2, 0.15, 0.1, 1.0)
        
        for i in range(16):
            x = -pcb_length/2 + 3 + i * (pcb_length - 6) / 16
            y = -pcb_width/2 + pcb_width - 2
            
            self.view3d._draw_3d_cylinder(x, y, 0.05, 0.08, 0.15, inductor_color)

    def _draw_rtx4090_pcb_components(self, pcb_length, pcb_width):
        """Draw all real-world RTX 4090 PCB components."""
        # GPU Die (AD102)
        self._draw_rtx4090_gpu_die()
        
        # GDDR6X VRAM chips (24 chips around GPU die)
        self._draw_rtx4090_vram()
        
        # VRM (Voltage Regulator Modules)
        self._draw_rtx4090_vrms()
        
        # Power delivery components
        self._draw_rtx4090_power_delivery()
        
        # DisplayPort and HDMI controllers
        self._draw_rtx4090_display_controllers()
        
        # Thermal sensors and monitoring chips
        self._draw_rtx4090_thermal_sensors()
        
        # BIOS chip
        self._draw_rtx4090_bios()
        
        # Clock generator
        self._draw_rtx4090_clock_generator()
        
        # Power management ICs
        self._draw_rtx4090_power_management()

    def _draw_rtx4090_gpu_die(self):
        """Draw AD102 GPU die with detailed architecture."""
        # AD102 die package
        die_size = self.GPU_DIE_SIZE_MM / 10
        
        # GPU package substrate
        self.view3d._draw_3d_box(-die_size/2, -die_size/2, 0, die_size, die_size, 0.1,
                                 (0.05, 0.08, 0.05, 1.0))
        
        # AD102 silicon die
        self.view3d._draw_3d_box(-die_size/2, -die_size/2, 0.1, die_size, die_size, self.GPU_DIE_THICKNESS_MM/10,
                                 (0.15, 0.15, 0.2, 1.0))
        
        # Draw SM layout (12 SMs per GPC, 8 GPCs = 96 SMs total)
        self._draw_ad102_sm_layout(die_size, 0.18)
        
        # Heat spreader
        hs_size = 2.5
        hs_thickness = 0.05
        self.view3d._draw_3d_box(-hs_size/2, -hs_size/2, 0.18,
                                 hs_size, hs_size, hs_thickness,
                                 (0.6, 0.6, 0.65, 1.0))

    def _draw_ad102_sm_layout(self, die_size, z_offset):
        """Draw exact AD102 Streaming Multiprocessor layout."""
        # AD102 has 8 GPCs, each with 12 SMs (96 total)
        gpcs = 8
        sms_per_gpc = 12
        
        # Calculate SM dimensions
        sm_cols = 12
        sm_rows = 8
        sm_width = die_size / (sm_cols + 1)
        sm_height = die_size / (sm_rows + 1)
        
        for gpc in range(gpcs):
            for sm in range(sms_per_gpc):
                sm_index = gpc * sms_per_gpc + sm
                row = sm_index // sm_cols
                col = sm_index % sm_cols
                
                x = -die_size/2 + (col + 0.5) * sm_width
                y = -die_size/2 + (row + 0.5) * sm_height
                
                # SM tile
                sm_color = (0.35, 0.25, 0.15, 0.9)
                self.view3d._draw_3d_box(x - sm_width/3, y - sm_height/3, z_offset,
                                         sm_width*0.66, sm_height*0.66, 0.015, sm_color)
                
                # Draw CUDA cores within SM (128 cores per SM)
                self._draw_cuda_cores_in_sm(x, y, sm_width, sm_height, z_offset + 0.015)

    def _draw_cuda_cores_in_sm(self, sm_x, sm_y, sm_width, sm_height, z_offset):
        """Draw individual CUDA cores within an SM."""
        # Each SM has 128 CUDA cores arranged in 4x32 arrays
        for subarray in range(4):
            for core in range(32):
                array_x = sm_x - sm_width/3 + (subarray % 2) * sm_width/3
                array_y = sm_y - sm_height/3 + (subarray // 2) * sm_height/3
                
                core_x = array_x - sm_width/8 + (core % 8) * sm_width/32
                core_y = array_y - sm_height/8 + (core // 8) * sm_height/16
                
                core_color = (0.45, 0.35, 0.25, 1.0)
                self.view3d._draw_3d_box(core_x - 0.01, core_y - 0.01, z_offset,
                                         0.02, 0.02, 0.004, core_color)

    def _draw_rtx4090_vram(self):
        """Draw 24 GDDR6X VRAM chips in exact RTX 4090 layout."""
        # RTX 4090 has 12 VRAM chips on front, 12 on back
        vram_positions = [
            # Front 12 chips
            (-8, -4), (-6, -4), (-4, -4), (-2, -4), (0, -4), (2, -4), (4, -4), (6, -4), (8, -4), (10, -4), (12, -4), (14, -4),
            # Back 12 chips
            (-8, 4), (-6, 4), (-4, 4), (-2, 4), (0, 4), (2, 4), (4, 4), (6, 4), (8, 4), (10, 4), (12, 4), (14, 4)
        ]
        
        # Draw front 12 VRAM chips
        for i, (x, y) in enumerate(vram_positions[:12]):
            self._draw_gddr6x_chip(x, y, 0.1, front=True)
        
        # Draw back 12 VRAM chips
        for i, (x, y) in enumerate(vram_positions[12:]):
            self._draw_gddr6x_chip(x, y, -0.2, front=False)

    def _draw_gddr6x_chip(self, x, y, z, front=True):
        """Draw individual GDDR6X VRAM chip with microscopic details."""
        # GDDR6X package (14mm x 10mm x 1mm)
        package_color = (0.05, 0.05, 0.1, 1.0) if front else (0.03, 0.03, 0.06, 1.0)
        self.view3d._draw_3d_box(x - 0.7, y - 0.5, z, 1.4, 1.0, 0.1, package_color)
        
        # GDDR6X die (10mm x 8mm x 0.8mm)
        die_color = (0.25, 0.25, 0.35, 1.0) if front else (0.15, 0.15, 0.25, 1.0)
        self.view3d._draw_3d_box(x - 0.5, y - 0.4, z + 0.1, 1.0, 0.8, 0.08, die_color)
        
        # Microscopic bonding wires
        if front:
            wire_color = (0.8, 0.8, 0.7, 1.0)
            for i in range(12):
                wire_x = x - 0.45 + i * 0.07
                self._draw_bonding_wire(wire_x, y, z + 0.18, wire_x, y - 0.35, z + 0.05, wire_color)

    def _draw_bonding_wire(self, x1, y1, z1, x2, y2, z2, color):
        """Draw microscopic bonding wire."""
        # Simplified bonding wire representation
        self.view3d._draw_3d_box(x1 - 0.01, y1 - 0.01, z1, 0.02, (y2-y1) + 0.02, 0.01, color)

    def _draw_rtx4090_vrms(self):
        """Draw 24-phase VRM power delivery system."""
        # VRM positions around the GPU die
        vrm_positions = [
            # Left side VRMs (12 phases)
            (-12, -5), (-12, -3), (-12, -1), (-12, 1), (-12, 3), (-12, 5),
            (-10, -5), (-10, -3), (-10, -1), (-10, 1), (-10, 3), (-10, 5),
            # Right side VRMs (12 phases)
            (10, -5), (10, -3), (10, -1), (10, 1), (10, 3), (10, 5),
            (12, -5), (12, -3), (12, -1), (12, 1), (12, 3), (12, 5)
        ]
        
        for i, (x, y) in enumerate(vrm_positions):
            # Main VRM chip
            vrm_color = (0.2, 0.2, 0.2, 1.0)
            self.view3d._draw_3d_box(x - 0.5, y - 0.5, 0.1, 1.0, 1.0, 0.2, vrm_color)
            
            # Heatsink fins on VRM
            for fin in range(6):
                fin_x = x - 0.4 + fin * 0.08
                fin_color = (0.7, 0.7, 0.8, 1.0)
                self.view3d._draw_3d_box(fin_x, y - 0.6, 0.3, 0.06, 0.2, 0.25, fin_color)

    def _draw_rtx4090_power_delivery(self):
        """Draw additional power delivery components."""
        # Power inductors
        inductor_positions = [(-12, -7), (-12, 7), (12, -7), (12, 7)]
        inductor_color = (0.15, 0.1, 0.05, 1.0)
        
        for x, y in inductor_positions:
            self.view3d._draw_3d_cylinder(x, y, 0.15, 0.3, 0.4, inductor_color)
        
        # Power capacitors
        capacitor_positions = [(-8, -7), (-4, -7), (0, -7), (4, -7), (8, -7)]
        capacitor_color = (0.1, 0.1, 0.15, 1.0)
        
        for x, y in capacitor_positions:
            self.view3d._draw_3d_cylinder(x, y, 0.1, 0.2, 0.3, capacitor_color)

    def _draw_rtx4090_display_controllers(self):
        """Draw DisplayPort and HDMI controller chips."""
        # DisplayPort 1.4a controllers
        dp_positions = [(14, -4), (14, -2), (14, 0)]
        dp_color = (0.1, 0.1, 0.2, 1.0)
        
        for x, y in dp_positions:
            self.view3d._draw_3d_box(x - 0.3, y - 0.2, 0.1, 0.6, 0.4, 0.15, dp_color)
        
        # HDMI 2.1 controller
        hdmi_color = (0.15, 0.1, 0.2, 1.0)
        self.view3d._draw_3d_box(14 - 0.3, 2 - 0.2, 0.1, 0.6, 0.4, 0.15, hdmi_color)

    def _draw_rtx4090_thermal_sensors(self):
        """Draw thermal sensor chips."""
        # Thermal sensor positions
        sensor_positions = [(0, -6), (0, 6), (-6, 0), (6, 0)]
        sensor_color = (0.1, 0.2, 0.1, 1.0)
        
        for x, y in sensor_positions:
            self.view3d._draw_3d_box(x - 0.2, y - 0.2, 0.05, 0.4, 0.4, 0.1, sensor_color)

    def _draw_rtx4090_bios(self):
        """Draw BIOS chip."""
        bios_color = (0.05, 0.1, 0.05, 1.0)
        self.view3d._draw_3d_box(-6, -6, 0.05, 0.8, 0.6, 0.1, bios_color)

    def _draw_rtx4090_clock_generator(self):
        """Draw clock generator chip."""
        clock_color = (0.1, 0.15, 0.1, 1.0)
        self.view3d._draw_3d_box(6, -6, 0.05, 0.6, 0.6, 0.1, clock_color)

    def _draw_rtx4090_power_management(self):
        """Draw power management ICs."""
        pmic_positions = [(-4, -6), (0, -6), (4, -6)]
        pmic_color = (0.15, 0.1, 0.1, 1.0)
        
        for x, y in pmic_positions:
            self.view3d._draw_3d_box(x - 0.3, y - 0.3, 0.05, 0.6, 0.6, 0.1, pmic_color)

    def _draw_rtx4090_heatsink(self):
        """Draw large heatsink with vapor chamber and optimized fins."""
        # Heatsink base
        base_color = (0.75, 0.75, 0.8, 1.0)
        self.view3d._draw_3d_box(-16.8, -7.0, 0.5, 33.6, 14.0, 4.0, base_color)
        
        # Optimized heatsink fins (150 fins for RTX 4090)
        fin_count = self.HEATSINK_FINS
        fin_thickness = 0.08
        fin_spacing = 33.6 / fin_count
        
        for i in range(fin_count):
            x = -16.8 + i * fin_spacing
            fin_color = (0.8, 0.8, 0.85, 1.0)
            self.view3d._draw_3d_box(x, -6.8, 0.5, fin_thickness, 13.6, 5.5, fin_color)

    def _draw_rtx4090_heat_pipes(self):
        """Draw 10 heat pipes with realistic routing."""
        # Heat pipe positions across the heatsink
        heat_pipe_positions = [
            (-6, -3), (-2, -3), (2, -3), (6, -3), (10, -3),
            (-6, 1), (-2, 1), (2, 1), (6, 1), (10, 1)
        ]
        
        pipe_color = (0.8, 0.5, 0.2, 1.0)
        
        for x, y in heat_pipe_positions:
            # Main heat pipe
            self.view3d._draw_3d_cylinder(x, y, 2.5, 0.25, 28, pipe_color)
            
            # Heat pipe contact with GPU
            contact_color = (0.8, 0.5, 0.2, 1.0)
            self.view3d._draw_3d_cylinder(x, y, 0.3, 0.2, 2.2, contact_color)

    def _draw_rtx4090_fans(self):
        """Draw triple Axial-tech fans with 13 blades each."""
        fan_positions = [(-6, 0), (0, 0), (6, 0)]
        fan_radius = 3.2
        
        for i, (x, y) in enumerate(fan_positions):
            # Fan hub
            hub_color = (0.12, 0.12, 0.15, 1.0)
            self.view3d._draw_3d_cylinder(x, y, 0.4, 0.8, 0.3, hub_color)
            
            # Fan blades (13 blades per fan)
            blade_color = (0.18, 0.18, 0.22, 1.0)
            for blade in range(13):
                angle = (blade / 13) * 2 * math.pi
                self._draw_fan_blade(x, y, 0.4, fan_radius, angle, blade_color)
            
            # Fan frame
            frame_color = (0.25, 0.25, 0.3, 1.0)
            self.view3d._draw_3d_cylinder(x, y, 0.35, fan_radius + 0.1, 0.2, frame_color)

    def _draw_fan_blade(self, cx, cy, cz, radius, angle, color):
        """Draw individual fan blade."""
        blade_length = radius - 0.8
        blade_width = 0.3
        
        x1 = cx + 0.8 * math.cos(angle)
        y1 = cy + 0.8 * math.sin(angle)
        x2 = cx + radius * math.cos(angle)
        y2 = cy + radius * math.sin(angle)
        
        self.view3d._draw_3d_box(x1 - blade_width/2, y1 - 0.1, cz,
                                 blade_width, blade_length, 0.05, color)

    def _draw_rtx4090_chassis(self):
        """Draw RTX 4090 chassis with optimized ventilation."""
        chassis_color = (0.85, 0.85, 0.9, 1.0)
        
        # Main chassis body
        self.view3d._draw_3d_box(-16.8, -7.0, 0, 33.6, 14.0, 6.1, chassis_color)
        
        # Optimized ventilation (90% open area for maximum cooling)
        vent_color = (0.05, 0.05, 0.08, 1.0)
        for i in range(40):
            x = -16.5 + i * (33.0 / 40)
            for j in range(8):
                y = -7 + j * 1.75
                self.view3d._draw_3d_box(x, y, 3.05, 0.5, 1.0, 0.1, vent_color)

    def _draw_rtx4090_backplate(self):
        """Draw RTX 4090 reinforced backplate with optimized ventilation."""
        # Backplate
        backplate_color = (0.75, 0.75, 0.8, 1.0)
        self.view3d._draw_3d_box(-16.8, -7.0, -2, 33.6, 14.0, 2, backplate_color)
        
        # Optimized ventilation holes (40% open area)
        vent_color = (0.02, 0.02, 0.03, 1.0)
        for i in range(30):
            x = -16 + i * (32.0 / 30)
            for j in range(5):
                y = -6.5 + j * 2.7
                self.view3d._draw_3d_box(x, y, -2, 0.8, 1.2, 0.1, vent_color)
        
        # RTX 4090 branding
        brand_color = (0.1, 0.1, 0.12, 1.0)
        self.view3d._draw_3d_box(-2.5, -1, -1.8, 5, 0.8, 0.05, brand_color)

    def _draw_rtx4090_io_bracket(self):
        """Draw I/O bracket with exact port layout."""
        # I/O bracket
        bracket_color = (0.65, 0.65, 0.7, 1.0)
        self.view3d._draw_3d_box(16.8, -7.0, -3, 2, 14.0, 5, bracket_color)
        
        # Display ports (3x DP, 1x HDMI)
        port_positions = [
            (17.1, -4, "DP"), (17.1, -2, "DP"), (17.1, 0, "DP"), (17.1, 2, "HDMI")
        ]
        
        for x, y, port_type in port_positions:
            port_color = (0.2, 0.2, 0.25, 1.0)
            self.view3d._draw_3d_box(x, y - 0.6, -1, 0.8, 1.2, 0.8, port_color)
        
        # 12VHPWR power connector
        power_color = (0.15, 0.15, 0.2, 1.0)
        self.view3d._draw_3d_box(17.1, 5.5, -1, 1.2, 2.0, 1.0, power_color)
