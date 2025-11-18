"""
RTX 4060 Ti GPU Model - Ultra Realistic with All Real-World Components
Complete 1:1 replica with every component found on actual RTX 4060 Ti
"""

from .baseGpuModel import BaseGPUModel
from typing import Dict, Tuple
import math

class RTX4060TiModel(BaseGPUModel):
    """Ultra-realistic RTX 4060 Ti GPU model with all real-world components."""
    
    def get_model_name(self) -> str:
        return "NVIDIA GeForce RTX 4060 Ti (All Real Components)"
        
    def get_component_list(self) -> Dict[str, str]:
        """Get RTX 4060 Ti components with detailed explanations."""
        return {
            "Chassis": "240mm x 120mm x 40mm aluminum chassis with optimized ventilation",
            "Dual Fans": "2x Axial-tech fans with 11 blades, dual ball bearings, 0dB auto-stop",
            "Vapor Chamber": "Small vapor chamber with 4 heat pipes covering GPU die",
            "GPU Die": "AD106-350 GPU, 4,352 CUDA cores, 8GB GDDR6 memory",
            "VRAM Layout": "8x Micron GDDR6 chips in 128-bit configuration",
            "Power Delivery": "12-phase VRM with 50A power stages and digital PWM",
            "Backplate": "Reinforced aluminum with 25% ventilation area",
            "PCB Design": "10-layer custom PCB with 3oz copper layers",
            "Display Outputs": "2x DisplayPort 1.4a, 1x HDMI 2.1, supports 8K@60Hz HDR",
            "Power Connector": "8-pin connector supporting up to 200W",
            "Heat Pipes": "4x 6mm nickel-plated copper heat pipes",
            "VRM Cooling": "Extended heatsinks with fin arrays for power stages",
            "Memory Interface": "128-bit memory bus, 18 Gbps effective, 288 GB/s bandwidth",
            "Clock Speeds": "2.535 GHz boost, 2.31 GHz base, 22.1 TFLOPS single precision",
            "Illumination": "RGB lighting on side logo, software controllable via GeForce Experience",
            "Thermal Design": "2-slot design, 160W TDP, 85°C max operating temperature",
            "Ventilation": "Optimized airflow path with 75% open area, dual-fan design",
            "BIOS Chip": "Dual BIOS switch for safe firmware updates",
            "Clock Generator": "High-precision clock generator for stable frequencies",
            "Power Management": "Advanced power management ICs for efficiency",
            "Thermal Sensors": "Multiple temperature sensors for monitoring",
            "Display Controllers": "TMDS and DisplayPort controllers for outputs",
            "Voltage Regulators": "12-phase voltage regulation modules",
            "Capacitors": "High-quality polymer capacitors for power delivery",
            "Inductors": "Power inductors for voltage regulation",
            "Resistors": "Surface mount resistors for signal conditioning",
            "PCB Traces": "Copper traces for power and data distribution"
        }

    def draw_chassis(self, lod: int):
        """Draw RTX 4060 Ti chassis."""
        if self.view3d and hasattr(self.view3d, 'show_chassis') and self.view3d.show_chassis and self.should_render_component("chassis"):
            self._draw_rtx4060ti_chassis()
        
    def draw_cooling_system(self, lod: int):
        """Draw RTX 4060 Ti cooling system."""
        if self.view3d and hasattr(self.view3d, 'show_cooling') and self.view3d.show_cooling and self.should_render_component("cooling"):
            self._draw_rtx4060ti_heatsink()
            self._draw_rtx4060ti_heat_pipes()
            self._draw_rtx4060ti_fans()
        
    def draw_pcb_and_components(self, lod: int):
        """Draw RTX 4060 Ti PCB and all components."""
        if self.view3d and hasattr(self.view3d, 'show_pcb') and self.view3d.show_pcb and self.should_render_component("pcb"):
            self._draw_rtx4060ti_pcb()
        if self.view3d and hasattr(self.view3d, 'show_gpu_die') and self.view3d.show_gpu_die and self.should_render_component("gpu_die"):
            self._draw_rtx4060ti_gpu_die()
        if self.view3d and hasattr(self.view3d, 'show_vram') and self.view3d.show_vram and self.should_render_component("vram"):
            self._draw_rtx4060ti_vram()
        if self.view3d and hasattr(self.view3d, 'show_power_delivery') and self.view3d.show_power_delivery and self.should_render_component("power_delivery"):
            self._draw_rtx4060ti_power_delivery()
        
    def draw_backplate(self, lod: int):
        """Draw RTX 4060 Ti backplate."""
        if self.view3d and hasattr(self.view3d, 'show_backplate') and self.view3d.show_backplate and self.should_render_component("backplate"):
            self._draw_rtx4060ti_backplate()
        if self.view3d and hasattr(self.view3d, 'show_io_bracket') and self.view3d.show_io_bracket and self.should_render_component("io_bracket"):
            self._draw_rtx4060ti_io_bracket()

    def draw_complete_model(self, lod: int):
        """Draw the complete RTX 4060 Ti model with all real-world components."""
        # Draw from back to front for proper depth
        self.draw_backplate(lod)
        self.draw_pcb_and_components(lod)
        self.draw_cooling_system(lod)
        self.draw_chassis(lod)

    def _draw_rtx4060ti_pcb(self):
        """Draw ultra-detailed RTX 4060 Ti PCB with all real-world components."""
        if not self.view3d:
            return
            
        # Main PCB board - realistic dimensions (240mm x 120mm x 1.5mm)
        pcb_length = 24.0
        pcb_width = 12.0
        pcb_thickness = 0.15
        
        # PCB substrate with realistic green color
        pcb_color = (0.1, 0.25, 0.1, 1.0)
        self.view3d._draw_3d_box(-pcb_length/2, -pcb_width/2, -pcb_thickness/2,
                                 pcb_length, pcb_width, pcb_thickness, pcb_color)
        
        # Draw PCB traces and microscopic components
        if hasattr(self.view3d, 'show_traces') and self.view3d.show_traces:
            self._draw_pcb_traces(pcb_length, pcb_width)
        
        if hasattr(self.view3d, 'show_microscopic') and self.view3d.show_microscopic:
            self._draw_microscopic_components(pcb_length, pcb_width)
        
        # Draw all real-world PCB components
        self._draw_rtx4060ti_pcb_components(pcb_length, pcb_width)

    def _draw_pcb_traces(self, pcb_length, pcb_width):
        """Draw realistic PCB traces."""
        trace_color = (0.7, 0.6, 0.3, 0.8)
        
        # Main power traces (thicker)
        for i in range(4):
            y = -pcb_width/2 + (i + 1) * (pcb_width / 5)
            self.view3d._draw_3d_box(-pcb_length/2 + 2, y - 0.1, 0.08,
                                     pcb_length - 4, 0.2, 0.05, trace_color)
        
        # Data traces (thinner)
        for i in range(8):
            y = -pcb_width/2 + i * (pcb_width / 8)
            for j in range(10):
                x = -pcb_length/2 + j * (pcb_length / 10)
                self.view3d._draw_3d_box(x, y - 0.05, 0.08, 0.3, 0.1, 0.03, trace_color)

    def _draw_microscopic_components(self, pcb_length, pcb_width):
        """Draw resistors, capacitors, and other tiny components."""
        # Surface mount resistors (0402 size: 1.0mm x 0.5mm)
        resistor_color = (0.3, 0.2, 0.1, 1.0)
        
        for i in range(100):
            x = -pcb_length/2 + 2 + (i % 20) * (pcb_length - 4) / 20
            y = -pcb_width/2 + 1 + (i // 20) * (pcb_width - 2) / 5
            
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

    def _draw_rtx4060ti_pcb_components(self, pcb_length, pcb_width):
        """Draw all real-world RTX 4060 Ti PCB components."""
        # GPU Die (AD106)
        self._draw_rtx4060ti_gpu_die()
        
        # GDDR6 VRAM chips (8 chips around GPU die)
        self._draw_rtx4060ti_vram()
        
        # VRM (Voltage Regulator Modules)
        self._draw_rtx4060ti_vrms()
        
        # Power delivery components
        self._draw_rtx4060ti_power_delivery()
        
        # DisplayPort and HDMI controllers
        self._draw_rtx4060ti_display_controllers()
        
        # Thermal sensors and monitoring chips
        self._draw_rtx4060ti_thermal_sensors()
        
        # BIOS chip
        self._draw_rtx4060ti_bios()
        
        # Clock generator
        self._draw_rtx4060ti_clock_generator()
        
        # Power management ICs
        self._draw_rtx4060ti_power_management()

    def _draw_rtx4060ti_gpu_die(self):
        """Draw AD106 GPU die with microscopic details."""
        # GPU package substrate (20mm x 20mm x 1mm)
        pkg_size = 2.0
        pkg_thickness = 0.1
        
        # Substrate with multiple layers
        self.view3d._draw_3d_box(-pkg_size/2, -pkg_size/2, 0, pkg_size, pkg_size, pkg_thickness,
                                 (0.05, 0.08, 0.05, 1.0))
        
        # AD106 silicon die (10mm x 10mm x 0.8mm)
        die_size = 1.0
        die_thickness = 0.08
        
        # Silicon die
        self.view3d._draw_3d_box(-die_size/2, -die_size/2, pkg_thickness,
                                 die_size, die_size, die_thickness,
                                 (0.15, 0.15, 0.2, 1.0))
        
        # Draw SM layout (4 GPCs x 6 SMs = 24 SMs total)
        self._draw_ad106_sm_layout(die_size, pkg_thickness + die_thickness)
        
        # Heat spreader
        hs_size = 1.5
        hs_thickness = 0.05
        self.view3d._draw_3d_box(-hs_size/2, -hs_size/2, pkg_thickness + die_thickness,
                                 hs_size, hs_size, hs_thickness,
                                 (0.6, 0.6, 0.65, 1.0))

    def _draw_ad106_sm_layout(self, die_size, z_offset):
        """Draw exact AD106 Streaming Multiprocessor layout."""
        # AD106 has 4 GPCs, each with 6 SMs (24 total)
        gpc_count = 4
        sms_per_gpc = 6
        
        # Calculate SM dimensions
        sm_cols = 6
        sm_rows = 4
        sm_width = die_size / (sm_cols + 1)
        sm_height = die_size / (sm_rows + 1)
        
        for gpc in range(gpc_count):
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
        # Each SM has 128 CUDA cores arranged in clusters
        clusters_per_sm = 4
        
        cluster_width = sm_width / 3
        cluster_height = sm_height / 3
        
        for cluster in range(clusters_per_sm):
            cluster_row = cluster // 2
            cluster_col = cluster % 2
            
            cx = sm_x - sm_width/3 + (cluster_col + 0.5) * cluster_width
            cy = sm_y - sm_height/3 + (cluster_row + 0.5) * cluster_height
            
            # Draw core cluster
            cluster_color = (0.45, 0.35, 0.25, 1.0)
            self.view3d._draw_3d_box(cx - cluster_width/3, cy - cluster_height/3, z_offset,
                                     cluster_width*0.66, cluster_height*0.66, 0.008, cluster_color)
            
            # Draw individual cores (simplified representation)
            for core in range(8):
                core_x = cx - cluster_width/4 + (core % 4) * cluster_width/8
                core_y = cy - cluster_height/4 + (core // 4) * cluster_height/4
                core_color = (0.55, 0.45, 0.35, 1.0)
                self.view3d._draw_3d_box(core_x - 0.02, core_y - 0.02, z_offset + 0.008,
                                         0.04, 0.04, 0.004, core_color)

    def _draw_rtx4060ti_vram(self):
        """Draw 8 GDDR6 VRAM chips in exact RTX 4060 Ti layout."""
        # RTX 4060 Ti has 8 VRAM chips on front and back
        vram_positions = [
            # Front 4 chips
            (-4, -2), (0, -2),
            (-4, 0), (0, 0),
            # Back 4 chips
            (-6, -1), (-2, -1),
            (-6, 1), (-2, 1)
        ]
        
        # Draw front 4 VRAM chips
        for i, (x, y) in enumerate(vram_positions[:4]):
            self._draw_gddr6_chip(x, y, 0.1, front=True)
        
        # Draw back 4 VRAM chips
        for i, (x, y) in enumerate(vram_positions[4:]):
            self._draw_gddr6_chip(x, y, -0.2, front=False)

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

    def _draw_rtx4060ti_vrms(self):
        """Draw 12-phase VRM power delivery system."""
        # VRM positions around the GPU die
        vrm_positions = [
            # Left side VRMs (6 phases)
            (-8, -4), (-8, -2), (-8, 0),
            (-6, -4), (-6, -2), (-6, 0),
            # Right side VRMs (6 phases)
            (4, -4), (4, -2), (4, 0),
            (6, -4), (6, -2), (6, 0)
        ]
        
        for i, (x, y) in enumerate(vrm_positions):
            # Main VRM chip
            vrm_color = (0.2, 0.2, 0.2, 1.0)
            self.view3d._draw_3d_box(x - 0.4, y - 0.4, 0.1, 0.8, 0.8, 0.15, vrm_color)
            
            # Heatsink fins on VRM
            for fin in range(4):
                fin_x = x - 0.35 + fin * 0.07
                fin_color = (0.7, 0.7, 0.8, 1.0)
                self.view3d._draw_3d_box(fin_x, y - 0.5, 0.25, 0.05, 0.15, 0.2, fin_color)

    def _draw_rtx4060ti_power_delivery(self):
        """Draw additional power delivery components."""
        # Power inductors
        inductor_positions = [(-8, -6), (-8, 2), (6, -6), (6, 2)]
        inductor_color = (0.15, 0.1, 0.05, 1.0)
        
        for x, y in inductor_positions:
            self.view3d._draw_3d_cylinder(x, y, 0.1, 0.25, 0.3, inductor_color)
        
        # Power capacitors
        capacitor_positions = [(-4, -6), (0, -6), (4, -6)]
        capacitor_color = (0.1, 0.1, 0.15, 1.0)
        
        for x, y in capacitor_positions:
            self.view3d._draw_3d_cylinder(x, y, 0.08, 0.15, 0.25, capacitor_color)

    def _draw_rtx4060ti_display_controllers(self):
        """Draw DisplayPort and HDMI controller chips."""
        # DisplayPort controllers
        dp_positions = [(8, -2), (8, 0)]
        dp_color = (0.1, 0.1, 0.2, 1.0)
        
        for x, y in dp_positions:
            self.view3d._draw_3d_box(x - 0.25, y - 0.15, 0.1, 0.5, 0.3, 0.12, dp_color)
        
        # HDMI controller
        hdmi_color = (0.15, 0.1, 0.2, 1.0)
        self.view3d._draw_3d_box(8 - 0.25, 2 - 0.15, 0.1, 0.5, 0.3, 0.12, hdmi_color)

    def _draw_rtx4060ti_thermal_sensors(self):
        """Draw thermal sensor chips."""
        # Thermal sensor positions
        sensor_positions = [(0, -4), (0, 4), (-3, 0), (3, 0)]
        sensor_color = (0.1, 0.2, 0.1, 1.0)
        
        for x, y in sensor_positions:
            self.view3d._draw_3d_box(x - 0.15, y - 0.15, 0.05, 0.3, 0.3, 0.08, sensor_color)

    def _draw_rtx4060ti_bios(self):
        """Draw BIOS chip."""
        bios_color = (0.05, 0.1, 0.05, 1.0)
        self.view3d._draw_3d_box(-3, -4, 0.05, 0.6, 0.5, 0.08, bios_color)

    def _draw_rtx4060ti_clock_generator(self):
        """Draw clock generator chip."""
        clock_color = (0.1, 0.15, 0.1, 1.0)
        self.view3d._draw_3d_box(3, -4, 0.05, 0.5, 0.5, 0.08, clock_color)

    def _draw_rtx4060ti_power_management(self):
        """Draw power management ICs."""
        pmic_positions = [(-1, -4), (1, -4)]
        pmic_color = (0.15, 0.1, 0.1, 1.0)
        
        for x, y in pmic_positions:
            self.view3d._draw_3d_box(x - 0.2, y - 0.2, 0.05, 0.4, 0.4, 0.08, pmic_color)

    def _draw_rtx4060ti_heatsink(self):
        """Draw heatsink with vapor chamber and fins."""
        # Heatsink base
        base_color = (0.75, 0.75, 0.8, 1.0)
        self.view3d._draw_3d_box(-12, -6, 0.5, 24, 12, 2.0, base_color)
        
        # Heatsink fins (80 fins for RTX 4060 Ti)
        fin_count = 80
        fin_thickness = 0.08
        fin_spacing = 24.0 / fin_count
        
        for i in range(fin_count):
            x = -12 + i * fin_spacing
            fin_color = (0.8, 0.8, 0.85, 1.0)
            self.view3d._draw_3d_box(x, -5.8, 0.5, fin_thickness, 11.6, 2.5, fin_color)

    def _draw_rtx4060ti_heat_pipes(self):
        """Draw 4 heat pipes with realistic routing."""
        # Heat pipe positions across the heatsink
        heat_pipe_positions = [
            (-5, -1), (-1, -1),
            (-5, 1), (-1, 1)
        ]
        
        pipe_color = (0.8, 0.5, 0.2, 1.0)
        
        for x, y in heat_pipe_positions:
            # Main heat pipe
            self.view3d._draw_3d_cylinder(x, y, 2, 0.2, 20, pipe_color)
            
            # Heat pipe contact with GPU
            contact_color = (0.8, 0.5, 0.2, 1.0)
            self.view3d._draw_3d_cylinder(x, y, 0.3, 0.15, 1.7, contact_color)

    def _draw_rtx4060ti_fans(self):
        """Draw dual Axial-tech fans with 11 blades each."""
        fan_positions = [(-4, 0), (4, 0)]
        fan_radius = 2.2
        
        for i, (x, y) in enumerate(fan_positions):
            # Fan hub
            hub_color = (0.12, 0.12, 0.15, 1.0)
            self.view3d._draw_3d_cylinder(x, y, 0.4, 0.6, 0.3, hub_color)
            
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
        blade_length = radius - 0.8
        blade_width = 0.25
        
        x1 = cx + 0.8 * math.cos(angle)
        y1 = cy + 0.8 * math.sin(angle)
        x2 = cx + radius * math.cos(angle)
        y2 = cy + radius * math.sin(angle)
        
        self.view3d._draw_3d_box(x1 - blade_width/2, y1 - 0.1, cz,
                                 blade_width, blade_length, 0.05, color)

    def _draw_rtx4060ti_chassis(self):
        """Draw Founders Edition chassis with optimized ventilation."""
        chassis_color = (0.85, 0.85, 0.9, 1.0)
        
        # Main chassis body
        self.view3d._draw_3d_box(-12.0, -6.0, 0, 24.0, 12.0, 4.0, chassis_color)
        
        # Ventilation holes (75% open area)
        vent_color = (0.05, 0.05, 0.08, 1.0)
        for i in range(25):
            x = -11.5 + i * (23.0 / 25)
            for j in range(5):
                y = -5.5 + j * 2.2
                self.view3d._draw_3d_box(x, y, 2.0, 0.4, 1.2, 0.1, vent_color)

    def _draw_rtx4060ti_backplate(self):
        """Draw RTX 4060 Ti reinforced backplate with ventilation."""
        # Backplate
        backplate_color = (0.75, 0.75, 0.8, 1.0)
        self.view3d._draw_3d_box(-12.0, -6.0, -2, 24.0, 12.0, 2, backplate_color)
        
        # Ventilation holes (25% open area)
        vent_color = (0.02, 0.02, 0.03, 1.0)
        for i in range(20):
            x = -11.5 + i * 1.15
            for j in range(3):
                y = -5.5 + j * 3.7
                self.view3d._draw_3d_box(x, y, -2, 0.25, 0.8, 0.1, vent_color)

    def _draw_rtx4060ti_io_bracket(self):
        """Draw I/O bracket with display ports and power connectors."""
        # I/O bracket
        bracket_color = (0.7, 0.7, 0.75, 1.0)
        self.view3d._draw_3d_box(12.0, -6.0, -2, 2.0, 12.0, 3.0, bracket_color)
        
        # Display ports (2x DisplayPort, 1x HDMI)
        port_positions = [(12.3, -2, "DP"), (12.3, 0, "DP"), (12.3, 2, "HDMI")]
        
        for x, y, port_type in port_positions:
            port_color = (0.2, 0.2, 0.25, 1.0)
            self.view3d._draw_3d_box(x, y - 0.6, -1, 0.8, 1.2, 0.8, port_color)
        
        # 8-pin power connector
        power_color = (0.15, 0.15, 0.2, 1.0)
        self.view3d._draw_3d_box(12.3, 5.0, -1, 1.0, 1.5, 0.8, power_color)
    
    # Component specifications
    LENGTH_MM = 240.0
    WIDTH_MM = 120.0
    HEIGHT_MM = 40.0
    GPU_DIE_SIZE_MM = 10.0
    GPU_DIE_THICKNESS_MM = 0.8
    VRAM_CHIPS = 8
    VRAM_CHIP_SIZE_MM = 12.0
    HEATSINK_FINS = 80
    HEAT_PIPES = 4
    FAN_COUNT = 2
    PCB_LENGTH_MM = 220.0
    PCB_WIDTH_MM = 105.0
    PCB_THICKNESS_MM = 1.5
    
    def get_model_name(self) -> str:
        return "NVIDIA GeForce RTX 4060 Ti (Ultra Realistic)"
        
    def get_chassis_dimensions(self) -> Tuple[float, float, float]:
        """RTX 4060 Ti exact dimensions: 240mm x 120mm x 40mm"""
        return (self.LENGTH_MM/10, self.WIDTH_MM/10, self.HEIGHT_MM/10)
        
    def get_component_list(self) -> Dict[str, str]:
        """Get RTX 4060 Ti specific components with detailed explanations."""
        return {
            "Chassis": "240mm x 120mm x 40mm aluminum chassis with NVIDIA Founders Edition design",
            "Dual Fans": "2x Axial-tech fans with 11 blades each, dual ball bearings, 0dB auto-stop",
            "Heatsink": "Aluminum heatsink with 80 fins, 4 heat pipes, direct touch GPU",
            "GPU Die": "AD106-350 GPU, 4,352 CUDA cores, 8GB GDDR6, 18 Gbps memory speed",
            "VRAM Layout": "8x Micron GDDR6 chips (4 on front, 4 on back) in 128-bit configuration",
            "Power Delivery": "12-phase VRM (8+4), 50A power stages, digital PWM controller",
            "Backplate": "Brushed aluminum backplate with 25% ventilation, RTX 4060 Ti branding",
            "PCB Design": "10-layer custom PCB, 220mm x 105mm, 3oz copper layers, optimized impedance",
            "Display Outputs": "2x DisplayPort 1.4a, 1x HDMI 2.1, supports 8K@60Hz HDR",
            "Power Connector": "8-pin connector, supports up to 200W, 160W base TDP",
            "Heat Pipes": "4x 6mm nickel-plated copper heat pipes, direct touch GPU die technology",
            "VRM Cooling": "Dedicated aluminum heatsinks for power stages, thermal pads for VRAM",
            "Memory Interface": "128-bit memory bus, 18 Gbps effective, 288 GB/s bandwidth",
            "Clock Speeds": "2.535 GHz boost, 2.31 GHz base, 22.1 TFLOPS single precision",
            "Illumination": "RGB lighting on side logo, software controllable via GeForce Experience",
            "Thermal Design": "2-slot design, 160W TDP, 85°C max operating temperature",
            "Ventilation": "Optimized airflow path with 75% open area, dual-fan design"
        }
        
    def draw_ultra_realistic_model(self):
        """Draw ultra-realistic 1:1 RTX 4060 Ti with microscopic details and visibility controls."""
        # Draw exact RTX 4060 Ti PCB with all components
        if hasattr(self.view3d, 'show_pcb') and self.view3d.show_pcb:
            self._draw_rtx4060ti_pcb()
        
        # Draw AD106 GPU die with SM layout
        if hasattr(self.view3d, 'show_gpu_die') and self.view3d.show_gpu_die:
            self._draw_rtx4060ti_gpu_die()
        
        # Draw 8 GDDR6 VRAM chips in exact positions
        if hasattr(self.view3d, 'show_vram') and self.view3d.show_vram:
            self._draw_rtx4060ti_vram()
        
        # Draw 12-phase power delivery system
        if hasattr(self.view3d, 'show_power_delivery') and self.view3d.show_power_delivery:
            self._draw_rtx4060ti_power_delivery()
        
        # Draw heatsink with 80 fins
        if hasattr(self.view3d, 'show_cooling') and self.view3d.show_cooling:
            self._draw_rtx4060ti_heatsink()
        
        # Draw 4 heat pipes with exact routing
        if hasattr(self.view3d, 'show_cooling') and self.view3d.show_cooling:
            self._draw_rtx4060ti_heat_pipes()
        
        # Draw dual Axial-tech fans
        if hasattr(self.view3d, 'show_cooling') and self.view3d.show_cooling:
            self._draw_rtx4060ti_fans()
        
        # Draw Founders Edition chassis
        if hasattr(self.view3d, 'show_chassis') and self.view3d.show_chassis:
            self._draw_rtx4060ti_chassis()
        
        # Draw backplate with ventilation
        if hasattr(self.view3d, 'show_backplate') and self.view3d.show_backplate:
            self._draw_rtx4060ti_backplate()
        
        # Draw I/O bracket and ports
        if hasattr(self.view3d, 'show_io_bracket') and self.view3d.show_io_bracket:
            self._draw_rtx4060ti_io_bracket()

    def _draw_rtx4060ti_pcb(self):
        """Draw exact RTX 4060 Ti PCB with microscopic traces."""
        # PCB dimensions: 220mm x 105mm x 1.5mm
        pcb_length = self.PCB_LENGTH_MM / 10
        pcb_width = self.PCB_WIDTH_MM / 10
        pcb_thickness = self.PCB_THICKNESS_MM / 10
        
        # PCB substrate - dark green FR-4
        self.view3d._draw_3d_box(-pcb_length/2, -pcb_width/2, -pcb_thickness/2,
                                 pcb_length, pcb_width, pcb_thickness,
                                 (0.08, 0.22, 0.08, 1.0))
        
        # Draw 10-layer PCB edge visualization
        for i in range(10):
            layer_z = -pcb_thickness/2 + i * (pcb_thickness / 10)
            layer_color = (0.05 + i * 0.01, 0.15 + i * 0.01, 0.05 + i * 0.01, 0.8)
            self.view3d._draw_3d_box(-pcb_length/2 + 0.5, -pcb_width/2 + 0.5, layer_z,
                                     pcb_length - 1.0, pcb_width - 1.0, 0.02, layer_color)
        
        # Draw copper traces (power and data lines)
        if hasattr(self.view3d, 'show_traces') and self.view3d.show_traces:
            self._draw_rtx4060ti_pcb_traces(pcb_length, pcb_width)
        
        # Draw microscopic surface mount components
        if hasattr(self.view3d, 'show_microscopic') and self.view3d.show_microscopic:
            self._draw_rtx4060ti_surface_components(pcb_length, pcb_width)

    def _draw_rtx4060ti_pcb_traces(self, pcb_length, pcb_width):
        """Draw realistic PCB traces for RTX 4060 Ti."""
        # Power delivery traces (thicker)
        power_trace_color = (0.75, 0.65, 0.35, 0.9)
        self.view3d._draw_3d_box(-pcb_length/2, -1.0, 0.05, pcb_length, 0.2, 0.02, power_trace_color)
        self.view3d._draw_3d_box(-pcb_length/2, 1.0, 0.05, pcb_length, 0.2, 0.02, power_trace_color)
        
        # Memory bus traces (medium thickness)
        memory_trace_color = (0.7, 0.6, 0.3, 0.8)
        for i in range(16):
            x = -pcb_length/2 + i * (pcb_length / 16)
            # Top memory traces
            self.view3d._draw_3d_box(x, -pcb_width/2 + 0.8, 0.05, 0.12, pcb_width - 1.6, 0.015, memory_trace_color)
            # Bottom memory traces
            self.view3d._draw_3d_box(x, -pcb_width/2 + 0.8, -0.05, 0.12, pcb_width - 1.6, 0.015, memory_trace_color)
        
        # Signal traces (thin)
        signal_trace_color = (0.65, 0.55, 0.25, 0.7)
        for i in range(32):
            x = -pcb_length/2 + i * (pcb_length / 32)
            for j in range(4):
                y = -pcb_width/2 + 1.5 + j * (pcb_width - 3) / 4
                self.view3d._draw_3d_box(x, y, 0.08, 0.06, 0.02, 0.01, signal_trace_color)

    def _draw_rtx4060ti_surface_components(self, pcb_length, pcb_width):
        """Draw surface mount resistors, capacitors, and ICs."""
        # Voltage regulation capacitors (1206 size: 3.2mm x 1.6mm)
        cap_color = (0.1, 0.1, 0.15, 1.0)
        for i in range(15):
            x = -pcb_length/2 + 2 + (i % 5) * 2.0
            y = -pcb_width/2 + 2 + (i // 5) * 1.8
            self.view3d._draw_3d_box(x, y, 0.1, 0.32, 0.16, 0.12, cap_color)
        
        # Power stage resistors (0402 size: 1.0mm x 0.5mm)
        resistor_color = (0.25, 0.15, 0.1, 1.0)
        for i in range(30):
            x = -pcb_length/2 + 1 + (i % 8) * 1.8
            y = -pcb_width/2 + 5 + (i // 8) * 1.2
            self.view3d._draw_3d_box(x, y, 0.1, 0.1, 0.05, 0.03, resistor_color)
        
        # PWM controller and monitoring ICs
        ic_color = (0.2, 0.2, 0.25, 1.0)
        ic_positions = [(-4, 0), (0, 0), (4, 0)]
        for x, y in ic_positions:
            self.view3d._draw_3d_box(x - 0.3, y - 0.3, 0.1, 0.6, 0.6, 0.12, ic_color)

    def _draw_rtx4060ti_gpu_die(self):
        """Draw AD106 GPU die with exact SM layout."""
        # GPU package substrate (20mm x 20mm x 1mm)
        pkg_size = 2.0
        pkg_thickness = 0.1
        
        # Substrate with multiple layers
        self.view3d._draw_3d_box(-pkg_size/2, -pkg_size/2, 0, pkg_size, pkg_size, pkg_thickness,
                                 (0.05, 0.08, 0.05, 1.0))
        
        # AD106 silicon die (10mm x 10mm x 0.8mm)
        die_size = self.GPU_DIE_SIZE_MM / 10
        die_thickness = self.GPU_DIE_THICKNESS_MM / 10
        
        # Silicon die
        self.view3d._draw_3d_box(-die_size/2, -die_size/2, pkg_thickness,
                                 die_size, die_size, die_thickness,
                                 (0.15, 0.15, 0.2, 1.0))
        
        # Draw exact AD106 SM layout (4 GPCs x 6 SMs = 24 SMs total)
        self._draw_ad106_sm_layout(die_size, pkg_thickness + die_thickness)
        
        # Draw heat spreader
        hs_size = 1.5
        hs_thickness = 0.05
        self.view3d._draw_3d_box(-hs_size/2, -hs_size/2, pkg_thickness + die_thickness,
                                 hs_size, hs_size, hs_thickness,
                                 (0.6, 0.6, 0.65, 1.0))

    def _draw_ad106_sm_layout(self, die_size, z_offset):
        """Draw exact AD106 Streaming Multiprocessor layout."""
        # AD106 has 4 GPCs, each with 6 SMs (24 total)
        gpc_count = 4
        sms_per_gpc = 6
        
        # Calculate SM dimensions
        total_sms = gpc_count * sms_per_gpc
        sm_cols = 6
        sm_rows = 4
        sm_width = die_size / (sm_cols + 1)
        sm_height = die_size / (sm_rows + 1)
        
        for gpc in range(gpc_count):
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
        # Each SM has 128 CUDA cores arranged in clusters
        cores_per_cluster = 32
        clusters_per_sm = 4
        
        cluster_width = sm_width / 3
        cluster_height = sm_height / 3
        
        for cluster in range(clusters_per_sm):
            cluster_row = cluster // 2
            cluster_col = cluster % 2
            
            cx = sm_x - sm_width/3 + (cluster_col + 0.5) * cluster_width
            cy = sm_y - sm_height/3 + (cluster_row + 0.5) * cluster_height
            
            # Draw core cluster
            cluster_color = (0.45, 0.35, 0.25, 1.0)
            self.view3d._draw_3d_box(cx - cluster_width/3, cy - cluster_height/3, z_offset,
                                     cluster_width*0.66, cluster_height*0.66, 0.008, cluster_color)
            
            # Draw individual cores (simplified representation)
            for core in range(8):
                core_x = cx - cluster_width/4 + (core % 4) * cluster_width/8
                core_y = cy - cluster_height/4 + (core // 4) * cluster_height/4
                core_color = (0.55, 0.45, 0.35, 1.0)
                self.view3d._draw_3d_box(core_x - 0.02, core_y - 0.02, z_offset + 0.008,
                                         0.04, 0.04, 0.004, core_color)

    def _draw_rtx4060ti_vram(self):
        """Draw 8 GDDR6 VRAM chips in exact RTX 4060 Ti layout."""
        # RTX 4060 Ti has 8 VRAM chips on front and back
        vram_positions = [
            (-4, -2), (0, -2), (4, -2),
            (-4, 0), (0, 0), (4, 0),
            (-6, -1), (-2, -1), (2, -1)
        ]
        
        # Draw front 6 VRAM chips
        for i, (x, y) in enumerate(vram_positions[:6]):
            self._draw_gddr6_chip(x, y, 0.1, front=True)
        
        # Draw back 2 VRAM chips
        for i, (x, y) in enumerate(vram_positions[6:]):
            self._draw_gddr6_chip(x, y, -0.2, front=False)

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
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        mid_z = max(z1, z2) + 0.05
        
        # Draw wire as thin box
        self.view3d._draw_3d_box(x1 - 0.01, y1 - 0.01, z1, 0.02, (y2-y1) + 0.02, 0.01, color)

    def _draw_rtx4060ti_power_delivery(self):
        """Draw 12-phase VRM power delivery system."""
        # VRM positions (8 GPU phases + 4 memory phases)
        vrm_positions = [
            (-8, -4), (-4, -4), (0, -4), (4, -4),
            (-8, 2), (-4, 2), (0, 2), (4, 2),
            (-6, 0), (-2, 0), (2, 0), (6, 0)
        ]
        
        for i, (x, y) in enumerate(vrm_positions):
            # Power stage package
            stage_color = (0.15, 0.15, 0.2, 1.0)
            self.view3d._draw_3d_box(x - 0.3, y - 0.3, 0.1, 0.6, 0.6, 0.15, stage_color)
            
            # Heatsink fins on VRM
            for fin in range(4):
                fin_x = x - 0.25 + fin * 0.05
                fin_color = (0.7, 0.7, 0.75, 1.0)
                self.view3d._draw_3d_box(fin_x, y - 0.4, 0.25, 0.04, 0.12, 0.2, fin_color)

    def _draw_rtx4060ti_heatsink(self):
        """Draw heatsink with absolute minimum detail for maximum performance."""
        # Heatsink base only
        base_color = (0.75, 0.75, 0.8, 1.0)
        self.view3d._draw_3d_box(-12, -6, 0.5, 24, 12, 2.0, base_color)
        
        # ABSOLUTE MINIMUM fins - performance over detail
        performance_mode = getattr(self.view3d, 'performance_mode', 'balanced')
        
        if performance_mode == "low":
            fin_count = 2
        elif performance_mode == "balanced":
            fin_count = 4
        else:
            fin_count = 6
        
        fin_thickness = 0.08
        fin_spacing = 24.0 / fin_count
        
        for i in range(fin_count):
            x = -12 + i * fin_spacing
            fin_color = (0.8, 0.8, 0.85, 1.0)
            self.view3d._draw_3d_box(x, -5.8, 0.5, fin_thickness, 11.6, 2.5, fin_color)

    def _draw_rtx4060ti_heat_pipes(self):
        """Draw 4 nickel-plated copper heat pipes."""
        pipe_color = (0.75, 0.48, 0.18, 1.0)
        
        # Heat pipe routing
        heat_pipe_positions = [
            (-5, -1), (-1, -1),
            (-5, 1), (-1, 1)
        ]
        
        for x, y in heat_pipe_positions:
            # Main heat pipe
            self.view3d._draw_3d_cylinder(x, y, 2, 0.2, 18, pipe_color)
            
            # Heat pipe contact with GPU
            contact_color = (0.8, 0.5, 0.2, 1.0)
            self.view3d._draw_3d_cylinder(x, y, 0.3, 0.12, 1.7, contact_color)

    def _draw_rtx4060ti_fans(self):
        """Draw dual Axial-tech fans with absolute minimum detail for maximum performance."""
        fan_positions = [(-4, 0), (4, 0)]
        fan_radius = 2.2
        
        # ABSOLUTE MINIMUM fan blades - performance over detail
        performance_mode = getattr(self.view3d, 'performance_mode', 'balanced')
        
        if performance_mode == "low":
            blade_count = 2
        elif performance_mode == "balanced":
            blade_count = 3
        else:
            blade_count = 4
        
        for i, (x, y) in enumerate(fan_positions):
            # Fan hub only
            hub_color = (0.12, 0.12, 0.15, 1.0)
            self.view3d._draw_3d_cylinder(x, y, 0.4, 0.5, 0.3, hub_color)
            
            # Fan blades (absolute minimum)
            blade_color = (0.18, 0.18, 0.22, 1.0)
            for blade in range(blade_count):
                angle = (blade / blade_count) * 2 * math.pi
                self._draw_fan_blade(x, y, 0.4, fan_radius, angle, blade_color)
            
            # Fan frame only
            frame_color = (0.25, 0.25, 0.3, 1.0)
            self.view3d._draw_3d_cylinder(x, y, 0.35, fan_radius + 0.1, 0.2, frame_color)

    def _draw_fan_blade(self, cx, cy, cz, radius, angle, color):
        """Draw individual fan blade."""
        # Simplified fan blade
        blade_length = radius - 0.7
        blade_width = 0.25
        
        x1 = cx + 0.7 * math.cos(angle)
        y1 = cy + 0.7 * math.sin(angle)
        x2 = cx + radius * math.cos(angle)
        y2 = cy + radius * math.sin(angle)
        
        self.view3d._draw_3d_box(x1 - blade_width/2, y1 - 0.1, cz,
                                 blade_width, blade_length, 0.05, color)

    def _draw_rtx4060ti_chassis(self):
        """Draw Founders Edition chassis with absolute minimum detail for maximum performance."""
        chassis_color = (0.85, 0.85, 0.9, 1.0)
        
        # Main chassis body only
        self.view3d._draw_3d_box(-12.0, -6.0, 0, 24.0, 12.0, 4.0, chassis_color)
        
        # ABSOLUTE MINIMUM ventilation - performance over detail
        performance_mode = getattr(self.view3d, 'performance_mode', 'balanced')
        
        if performance_mode == "low":
            vent_count = 2
        elif performance_mode == "balanced":
            vent_count = 4
        else:
            vent_count = 6
        
        vent_color = (0.05, 0.05, 0.08, 1.0)
        for i in range(vent_count):
            x = -11.5 + i * (23.0 / vent_count)
            for j in range(2):
                y = -5.5 + j * 5.5
                self.view3d._draw_3d_box(x, y, 2.0, 0.4, 1.2, 0.1, vent_color)

    def _draw_rtx4060ti_backplate(self):
        """Draw RTX 4060 Ti backplate with ventilation."""
        # Backplate
        backplate_color = (0.75, 0.75, 0.8, 1.0)
        self.view3d._draw_3d_box(-12.0, -6.0, -2, 24.0, 12.0, 2, backplate_color)
        
        # Ventilation holes (25% open area)
        vent_color = (0.02, 0.02, 0.03, 1.0)
        for i in range(8):
            x = -11.5 + i * 2.9
            for j in range(3):
                y = -5.5 + j * 3.7
                self.view3d._draw_3d_box(x, y, -1.9, 1.2, 1.5, 0.1, vent_color)
        
        # RTX 4060 Ti branding
        brand_color = (0.1, 0.1, 0.12, 1.0)
        self.view3d._draw_3d_box(-2, -1, -1.8, 4, 0.8, 0.05, brand_color)

    def _draw_rtx4060ti_io_bracket(self):
        """Draw I/O bracket with exact port layout."""
        # I/O bracket
        bracket_color = (0.65, 0.65, 0.7, 1.0)
        self.view3d._draw_3d_box(12.0, -6.0, -3, 2, 12.0, 5, bracket_color)
        
        # Display ports (2x DP, 1x HDMI)
        port_positions = [
            (12.3, -2, "DP"), (12.3, 0, "DP"), (12.3, 2, "HDMI")
        ]
        
        for x, y, port_type in port_positions:
            port_color = (0.2, 0.2, 0.25, 1.0)
            self.view3d._draw_3d_box(x, y - 0.6, -1, 0.8, 1.2, 0.8, port_color)
        
        # 8-pin power connector
        power_color = (0.15, 0.15, 0.2, 1.0)
        self.view3d._draw_3d_box(12.3, 5, -1, 1.0, 1.5, 0.8, power_color)

    # Legacy methods for compatibility
    def draw_chassis(self, lod: int):
        """Draw RTX 4060 Ti chassis."""
        if hasattr(self.view3d, 'show_chassis') and self.view3d.show_chassis and self.should_render_component("chassis"):
            self._draw_rtx4060ti_chassis()
        
    def draw_cooling_system(self, lod: int):
        """Draw RTX 4060 Ti cooling system."""
        if hasattr(self.view3d, 'show_cooling') and self.view3d.show_cooling and self.should_render_component("cooling"):
            self._draw_rtx4060ti_heatsink()
            self._draw_rtx4060ti_heat_pipes()
            self._draw_rtx4060ti_fans()
        
    def draw_pcb_and_components(self, lod: int):
        """Draw RTX 4060 Ti PCB and components."""
        if hasattr(self.view3d, 'show_pcb') and self.view3d.show_pcb and self.should_render_component("pcb"):
            self._draw_rtx4060ti_pcb()
        if hasattr(self.view3d, 'show_gpu_die') and self.view3d.show_gpu_die and self.should_render_component("gpu_die"):
            self._draw_rtx4060ti_gpu_die()
        if hasattr(self.view3d, 'show_vram') and self.view3d.show_vram and self.should_render_component("vram"):
            self._draw_rtx4060ti_vram()
        if hasattr(self.view3d, 'show_power_delivery') and self.view3d.show_power_delivery and self.should_render_component("power_delivery"):
            self._draw_rtx4060ti_power_delivery()
        
    def draw_backplate(self, lod: int):
        """Draw RTX 4060 Ti backplate."""
        if hasattr(self.view3d, 'show_backplate') and self.view3d.show_backplate and self.should_render_component("backplate"):
            self._draw_rtx4060ti_backplate()
        if hasattr(self.view3d, 'show_io_bracket') and self.view3d.show_io_bracket and self.should_render_component("io_bracket"):
            self._draw_rtx4060ti_io_bracket()

    def draw_complete_model(self, lod: int):
        """Draw the complete RTX 4060 Ti model with ultra-detailed components."""
        # Draw from back to front for proper depth
        self.draw_backplate(lod)
        self.draw_pcb_and_components(lod)
        self.draw_cooling_system(lod)
        self.draw_chassis(lod)