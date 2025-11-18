"""
RX 7900 XTX GPU Model - Ultra Realistic with All Real-World Components
Complete 1:1 replica with every component found on actual RX 7900 XTX
"""

from .baseGpuModel import BaseGPUModel
from typing import Dict, Tuple
import math

class RX7900XTXModel(BaseGPUModel):
    """Ultra-realistic RX 7900 XTX GPU model with all real-world components."""
    
    # Component specifications
    LENGTH_MM = 287.0  # 287mm length
    WIDTH_MM = 124.0   # 124mm width  
    HEIGHT_MM = 52.0   # 52mm height (2.5 slots)
    GPU_DIE_SIZE_MM = 21.0  # Navi 31 GCD die size
    GPU_DIE_THICKNESS_MM = 0.8  # Silicon die thickness
    MCD_DIE_SIZE_MM = 7.0   # Memory Chiplet Die size
    VRAM_CHIPS = 16  # 16 GDDR6 chips
    VRAM_CHIP_SIZE_MM = 12.0  # VRAM chip dimensions
    HEATSINK_FINS = 50  # Number of heatsink fins
    HEAT_PIPES = 6  # 6 heat pipes
    FAN_COUNT = 3  # Triple fan design
    PCB_LENGTH_MM = 267.0  # PCB length
    PCB_WIDTH_MM = 110.0   # PCB width
    PCB_THICKNESS_MM = 1.5  # PCB thickness
    
    def get_model_name(self) -> str:
        return "AMD Radeon RX 7900 XTX (Ultra Realistic)"
        
    def get_chassis_dimensions(self) -> Tuple[float, float, float]:
        """RX 7900 XTX exact dimensions: 287mm x 124mm x 52mm"""
        return (self.LENGTH_MM/10, self.WIDTH_MM/10, self.HEIGHT_MM/10)
        
    def get_component_list(self) -> Dict[str, str]:
        """Get RX 7900 XTX specific components with detailed explanations."""
        return {
            "Chassis": "287mm x 124mm x 52mm aluminum chassis with AMD signature design",
            "Triple Fans": "3x AMD Axial-tech fans with 11 blades, fluid dynamic bearing",
            "Vapor Chamber": "Large vapor chamber with 6 heat pipes covering full die",
            "GPU Die": "Navi31 GPU, 6,144 CUDA cores, 24GB GDDR6 memory, chiplet architecture",
            "VRAM Layout": "16x Samsung GDDR6 chips in 384-bit configuration",
            "Power Delivery": "18-phase VRM with 60A power stages and digital PWM",
            "Backplate": "Reinforced aluminum with AMD logo and 30% ventilation area",
            "PCB Design": "12-layer custom PCB with 3oz copper layers, AMD red PCB",
            "Display Outputs": "3x DisplayPort 2.1, 1x HDMI 2.1a, supports 8K@165Hz HDR",
            "Power Connector": "8-pin + 8-pin connectors supporting up to 355W",
            "Heat Pipes": "6x 8mm nickel-plated copper heat pipes",
            "VRM Cooling": "Extended heatsinks with fin arrays for power stages",
            "Memory Interface": "384-bit memory bus, 20 Gbps effective, 960 GB/s bandwidth",
            "Clock Speeds": "2.5 GHz boost, 2.3 GHz base, 61 TFLOPS single precision",
            "Illumination": "Red LED lighting on fan shroud and side logo",
            "Thermal Design": "2.5-slot design, 355W TDP, 95°C max operating temperature",
            "Ventilation": "Optimized airflow path with 80% open area, tri-fan design",
            "BIOS Chip": "Dual BIOS switch for safe firmware updates",
            "Clock Generator": "High-precision clock generator for stable frequencies",
            "Power Management": "Advanced power management ICs for efficiency",
            "Thermal Sensors": "Multiple temperature sensors for monitoring",
            "Display Controllers": "TMDS and DisplayPort 2.1 controllers for outputs",
            "Chiplet Design": "5nm GCD + 6nm MCDs for optimal performance and efficiency",
            "Voltage Regulators": "18-phase voltage regulation modules",
            "Capacitors": "High-quality polymer capacitors for power delivery",
            "Inductors": "Power inductors for voltage regulation",
            "Resistors": "Surface mount resistors for signal conditioning",
            "PCB Traces": "Copper traces for power and data distribution"
        }

    def draw_chassis(self, lod: int):
        """Draw RX 7900 XTX chassis."""
        if hasattr(self.view3d, 'show_chassis') and self.view3d.show_chassis and self.should_render_component("chassis"):
            self._draw_rx7900xtx_chassis()
        
    def draw_cooling_system(self, lod: int):
        """Draw RX 7900 XTX cooling system."""
        if hasattr(self.view3d, 'show_cooling') and self.view3d.show_cooling and self.should_render_component("cooling"):
            self._draw_rx7900xtx_heatsink()
            self._draw_rx7900xtx_heat_pipes()
            self._draw_rx7900xtx_fans()
        
    def draw_pcb_and_components(self, lod: int):
        """Draw RX 7900 XTX PCB and all components."""
        if hasattr(self.view3d, 'show_pcb') and self.view3d.show_pcb and self.should_render_component("pcb"):
            self._draw_rx7900xtx_pcb()
        if hasattr(self.view3d, 'show_gpu_die') and self.view3d.show_gpu_die and self.should_render_component("gpu_die"):
            self._draw_rx7900xtx_gpu_die()
        if hasattr(self.view3d, 'show_vram') and self.view3d.show_vram and self.should_render_component("vram"):
            self._draw_rx7900xtx_vram()
        if hasattr(self.view3d, 'show_power_delivery') and self.view3d.show_power_delivery and self.should_render_component("power_delivery"):
            self._draw_rx7900xtx_power_delivery()
        
    def draw_backplate(self, lod: int):
        """Draw RX 7900 XTX backplate."""
        if hasattr(self.view3d, 'show_backplate') and self.view3d.show_backplate and self.should_render_component("backplate"):
            self._draw_rx7900xtx_backplate()
        if hasattr(self.view3d, 'show_io_bracket') and self.view3d.show_io_bracket and self.should_render_component("io_bracket"):
            self._draw_rx7900xtx_io_bracket()

    def draw_complete_model(self, lod: int):
        """Draw the complete RX 7900 XTX model with all real-world components."""
        # Draw from back to front for proper depth
        self.draw_backplate(lod)
        self.draw_pcb_and_components(lod)
        self.draw_cooling_system(lod)
        self.draw_chassis(lod)

    def draw_ultra_realistic_model(self):
        """Draw ultra-realistic 1:1 replica with microscopic details."""
        self.draw_complete_model(0)

    def _draw_rx7900xtx_pcb(self):
        """Draw ultra-detailed RX 7900 XTX PCB with all real-world components."""
        # Main PCB board - realistic dimensions (267mm x 110mm x 1.5mm)
        pcb_length = self.PCB_LENGTH_MM / 10  # Scale to our coordinate system
        pcb_width = self.PCB_WIDTH_MM / 10
        pcb_thickness = self.PCB_THICKNESS_MM / 10
        
        # PCB substrate with AMD signature red color
        pcb_color = (0.25, 0.1, 0.1, 1.0)  # AMD red PCB
        self.view3d._draw_3d_box(-pcb_length/2, -pcb_width/2, -pcb_thickness/2, 
                                 pcb_length, pcb_width, pcb_thickness, pcb_color)
        
        # Draw PCB traces and microscopic components
        if hasattr(self.view3d, 'show_traces') and self.view3d.show_traces:
            self._draw_pcb_traces(pcb_length, pcb_width)
        
        if hasattr(self.view3d, 'show_microscopic') and self.view3d.show_microscopic:
            self._draw_microscopic_components(pcb_length, pcb_width)
        
        # Draw all real-world PCB components
        self._draw_rx7900xtx_pcb_components(pcb_length, pcb_width)

    def _draw_pcb_traces(self, pcb_length, pcb_width):
        """Draw realistic PCB traces."""
        trace_color = (0.7, 0.6, 0.3, 0.8)  # Copper color
        
        # Main power traces (thicker)
        for i in range(6):
            y = -pcb_width/2 + (i + 1) * (pcb_width / 7)
            self.view3d._draw_3d_box(-pcb_length/2 + 2, y - 0.1, 0.08, 
                                     pcb_length - 4, 0.2, 0.05, trace_color)
        
        # Data traces (medium thickness)
        for i in range(12):
            y = -pcb_width/2 + i * (pcb_width / 12)
            for j in range(15):
                x = -pcb_length/2 + j * (pcb_length / 15)
                self.view3d._draw_3d_box(x, y - 0.05, 0.08, 0.3, 0.1, 0.03, trace_color)

    def _draw_microscopic_components(self, pcb_length, pcb_width):
        """Draw resistors, capacitors, and other tiny components."""
        # Surface mount resistors (0402 size: 1.0mm x 0.5mm)
        resistor_color = (0.3, 0.2, 0.1, 1.0)
        
        for i in range(120):
            x = -pcb_length/2 + 2 + (i % 20) * (pcb_length - 4) / 20
            y = -pcb_width/2 + 1 + (i // 20) * (pcb_width - 2) / 6
            
            self.view3d._draw_3d_box(x, y, 0.05, 0.1, 0.05, 0.02, resistor_color)
        
        # Surface mount capacitors
        capacitor_color = (0.1, 0.1, 0.2, 1.0)
        
        for i in range(60):
            x = -pcb_length/2 + 2 + (i % 12) * (pcb_length - 4) / 12
            y = -pcb_width/2 + 1 + (i // 12) * (pcb_width - 2) / 5
            
            self.view3d._draw_3d_cylinder(x, y, 0.05, 0.03, 0.1, capacitor_color)
        
        # Inductors
        inductor_color = (0.2, 0.15, 0.1, 1.0)
        
        for i in range(12):
            x = -pcb_length/2 + 3 + i * (pcb_length - 6) / 12
            y = -pcb_width/2 + pcb_width - 2
            
            self.view3d._draw_3d_cylinder(x, y, 0.05, 0.08, 0.15, inductor_color)

    def _draw_rx7900xtx_pcb_components(self, pcb_length, pcb_width):
        """Draw all real-world RX 7900 XTX PCB components."""
        # GPU Die (Navi31 chiplet)
        self._draw_rx7900xtx_gpu_die()
        
        # GDDR6 VRAM chips (16 chips around GPU die)
        self._draw_rx7900xtx_vram()
        
        # VRM (Voltage Regulator Modules)
        self._draw_rx7900xtx_vrms()
        
        # Power delivery components
        self._draw_rx7900xtx_power_delivery()
        
        # DisplayPort and HDMI controllers
        self._draw_rx7900xtx_display_controllers()
        
        # Thermal sensors and monitoring chips
        self._draw_rx7900xtx_thermal_sensors()
        
        # BIOS chip
        self._draw_rx7900xtx_bios()
        
        # Clock generator
        self._draw_rx7900xtx_clock_generator()
        
        # Power management ICs
        self._draw_rx7900xtx_power_management()

    def _draw_rx7900xtx_gpu_die(self):
        """Draw Navi31 GPU die with chiplet architecture."""
        # Main Graphics Compute Die (GCD) - 5nm
        gcd_size = self.GPU_DIE_SIZE_MM / 10  # Scale to our coordinate system
        
        # GCD package substrate
        self.view3d._draw_3d_box(-gcd_size/2, -gcd_size/2, 0, gcd_size, gcd_size, 0.1,
                                 (0.05, 0.08, 0.05, 1.0))
        
        # GCD silicon die
        self.view3d._draw_3d_box(-gcd_size/2, -gcd_size/2, 0.1, gcd_size, gcd_size, self.GPU_DIE_THICKNESS_MM/10,
                                 (0.15, 0.15, 0.2, 1.0))
        
        # Draw WGP layout (6 WGPs per shader engine, 6 shader engines = 36 WGPs total)
        self._draw_navi31_wgp_layout(gcd_size, 0.18)
        
        # Memory Cache Dies (MCDs) - 6nm
        mcd_size = self.MCD_DIE_SIZE_MM / 10
        mcd_positions = [(-3.5, 0), (3.5, 0)]  # Two MCDs on sides
        
        for x, y in mcd_positions:
            # MCD package
            self.view3d._draw_3d_box(x - mcd_size/2, y - mcd_size/2, 0, mcd_size, mcd_size, 0.08,
                                     (0.08, 0.05, 0.05, 1.0))
            
            # MCD silicon die
            self.view3d._draw_3d_box(x - mcd_size*0.75, y - mcd_size*0.75, 0.08, mcd_size*1.5, mcd_size*1.5, 0.06,
                                     (0.2, 0.15, 0.15, 1.0))
        
        # Heat spreader covering all dies
        hs_size = 4.0
        hs_thickness = 0.05
        self.view3d._draw_3d_box(-hs_size/2, -hs_size/2, 0.18,
                                 hs_size, hs_size, hs_thickness,
                                 (0.6, 0.6, 0.65, 1.0))

    def _draw_navi31_wgp_layout(self, die_size, z_offset):
        """Draw exact Navi31 Workgroup Processor layout."""
        # Navi31 has 6 Shader Engines, each with 6 WGPs (36 total)
        shader_engines = 6
        wgps_per_se = 6
        
        # Calculate WGP dimensions
        wgp_cols = 6
        wgp_rows = 6
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

    def _draw_rx7900xtx_vram(self):
        """Draw 16 GDDR6 VRAM chips in exact RX 7900 XTX layout."""
        # RX 7900 XTX has 8 VRAM chips on front, 8 on back
        vram_positions = [
            # Front 8 chips
            (-7, -3), (-3, -3), (1, -3), (5, -3),
            (-7, 0), (-3, 0), (1, 0), (5, 0),
            # Back 8 chips
            (-7, 3), (-3, 3), (1, 3), (5, 3),
            (-9, -1.5), (-5, -1.5), (5, -1.5), (9, -1.5)
        ]
        
        # Draw front 8 VRAM chips
        for i, (x, y) in enumerate(vram_positions[:8]):
            self._draw_gddr6_chip(x, y, 0.1, front=True)
        
        # Draw back 8 VRAM chips
        for i, (x, y) in enumerate(vram_positions[8:]):
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
            wire_color = (0.8, 0.8, 0.7, 1.0)  # Gold
            for i in range(10):
                wire_x = x - 0.35 + i * 0.07
                self._draw_bonding_wire(wire_x, y, z + 0.18, wire_x, y - 0.25, z + 0.05, wire_color)

    def _draw_bonding_wire(self, x1, y1, z1, x2, y2, z2, color):
        """Draw microscopic bonding wire."""
        # Simplified bonding wire representation
        self.view3d._draw_3d_box(x1 - 0.01, y1 - 0.01, z1, 0.02, (y2-y1) + 0.02, 0.01, color)

    def _draw_rx7900xtx_vrms(self):
        """Draw 18-phase VRM power delivery system."""
        # VRM positions around the GPU die
        vrm_positions = [
            # Left side VRMs (9 phases)
            (-10, -4), (-10, -2), (-10, 0), (-10, 2), (-10, 4),
            (-8, -4), (-8, -2), (-8, 0), (-8, 2),
            # Right side VRMs (9 phases)
            (8, -4), (8, -2), (8, 0), (8, 2), (8, 4),
            (10, -4), (10, -2), (10, 0), (10, 2)
        ]
        
        for i, (x, y) in enumerate(vrm_positions):
            # Main VRM chip
            vrm_color = (0.2, 0.2, 0.2, 1.0)
            self.view3d._draw_3d_box(x - 0.5, y - 0.5, 0.1, 1.0, 1.0, 0.2, vrm_color)
            
            # Heatsink fins on VRM
            for fin in range(5):
                fin_x = x - 0.4 + fin * 0.1
                fin_color = (0.7, 0.7, 0.8, 1.0)
                self.view3d._draw_3d_box(fin_x, y - 0.6, 0.3, 0.06, 0.2, 0.25, fin_color)

    def _draw_rx7900xtx_power_delivery(self):
        """Draw additional power delivery components."""
        # Power inductors
        inductor_positions = [(-10, -6), (-10, 6), (10, -6), (10, 6)]
        inductor_color = (0.15, 0.1, 0.05, 1.0)
        
        for x, y in inductor_positions:
            self.view3d._draw_3d_cylinder(x, y, 0.15, 0.3, 0.4, inductor_color)
        
        # Power capacitors
        capacitor_positions = [(-7, -6), (-3, -6), (1, -6), (5, -6), (9, -6)]
        capacitor_color = (0.1, 0.1, 0.15, 1.0)
        
        for x, y in capacitor_positions:
            self.view3d._draw_3d_cylinder(x, y, 0.1, 0.2, 0.3, capacitor_color)

    def _draw_rx7900xtx_display_controllers(self):
        """Draw DisplayPort and HDMI controller chips."""
        # DisplayPort 2.1 controllers
        dp_positions = [(11, -3), (11, -1), (11, 1)]
        dp_color = (0.1, 0.1, 0.2, 1.0)
        
        for x, y in dp_positions:
            self.view3d._draw_3d_box(x - 0.3, y - 0.2, 0.1, 0.6, 0.4, 0.15, dp_color)
        
        # HDMI 2.1a controller
        hdmi_color = (0.15, 0.1, 0.2, 1.0)
        self.view3d._draw_3d_box(11 - 0.3, 3 - 0.2, 0.1, 0.6, 0.4, 0.15, hdmi_color)

    def _draw_rx7900xtx_thermal_sensors(self):
        """Draw thermal sensor chips."""
        # Thermal sensor positions
        sensor_positions = [(0, -5), (0, 5), (-5, 0), (5, 0)]
        sensor_color = (0.1, 0.2, 0.1, 1.0)
        
        for x, y in sensor_positions:
            self.view3d._draw_3d_box(x - 0.2, y - 0.2, 0.05, 0.4, 0.4, 0.1, sensor_color)

    def _draw_rx7900xtx_bios(self):
        """Draw BIOS chip."""
        bios_color = (0.05, 0.1, 0.05, 1.0)
        self.view3d._draw_3d_box(-5, -5, 0.05, 0.8, 0.6, 0.1, bios_color)

    def _draw_rx7900xtx_clock_generator(self):
        """Draw clock generator chip."""
        clock_color = (0.1, 0.15, 0.1, 1.0)
        self.view3d._draw_3d_box(5, -5, 0.05, 0.6, 0.6, 0.1, clock_color)

    def _draw_rx7900xtx_power_management(self):
        """Draw power management ICs."""
        pmic_positions = [(-3, -5), (0, -5), (3, -5)]
        pmic_color = (0.15, 0.1, 0.1, 1.0)
        
        for x, y in pmic_positions:
            self.view3d._draw_3d_box(x - 0.3, y - 0.3, 0.05, 0.6, 0.6, 0.1, pmic_color)

    def _draw_rx7900xtx_heatsink(self):
        """Draw large heatsink with vapor chamber and fins."""
        # Heatsink base
        base_color = (0.75, 0.75, 0.8, 1.0)
        self.view3d._draw_3d_box(-14, -6, 0.5, 28, 12, 3.0, base_color)
        
        # Heatsink fins (50 fins for RX 7900 XTX)
        fin_count = self.HEATSINK_FINS
        fin_thickness = 0.08
        fin_spacing = 28.0 / fin_count
        
        for i in range(fin_count):
            x = -14 + i * fin_spacing
            fin_color = (0.8, 0.8, 0.85, 1.0)
            self.view3d._draw_3d_box(x, -5.8, 0.5, fin_thickness, 11.6, 4.5, fin_color)

    def _draw_rx7900xtx_heat_pipes(self):
        """Draw 6 heat pipes with realistic routing."""
        # Heat pipe positions across the heatsink
        heat_pipe_positions = [
            (-5, -2), (-1, -2), (3, -2), (7, -2),
            (-5, 1), (3, 1)
        ]
        
        pipe_color = (0.8, 0.5, 0.2, 1.0)
        
        for x, y in heat_pipe_positions:
            # Main heat pipe
            self.view3d._draw_3d_cylinder(x, y, 2, 0.25, 24, pipe_color)
            
            # Heat pipe contact with GPU
            contact_color = (0.8, 0.5, 0.2, 1.0)
            self.view3d._draw_3d_cylinder(x, y, 0.3, 0.2, 1.7, contact_color)

    def _draw_rx7900xtx_fans(self):
        """Draw triple AMD Axial-tech fans with 11 blades each."""
        fan_positions = [(-5, 0), (0, 0), (5, 0)]
        fan_radius = 2.8  # AMD fan size
        
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
        blade_length = radius - 0.8
        blade_width = 0.3
        
        x1 = cx + 0.8 * math.cos(angle)
        y1 = cy + 0.8 * math.sin(angle)
        x2 = cx + radius * math.cos(angle)
        y2 = cy + radius * math.sin(angle)
        
        self.view3d._draw_3d_box(x1 - blade_width/2, y1 - 0.1, cz, 
                                 blade_width, blade_length, 0.05, color)

    def _draw_rx7900xtx_chassis(self):
        """Draw AMD signature chassis with optimized ventilation."""
        chassis_color = (0.85, 0.85, 0.9, 1.0)
        
        # Main chassis body
        self.view3d._draw_3d_box(-14.35, -6.2, 0, 28.7, 12.4, 5.2, chassis_color)
        
        # AMD signature ventilation (80% open area)
        vent_color = (0.05, 0.05, 0.08, 1.0)
        for i in range(35):
            x = -14 + i * (28.0 / 35)
            for j in range(6):
                y = -6 + j * 2.0
                self.view3d._draw_3d_box(x, y, 2.6, 0.5, 1.0, 0.1, vent_color)

    def _draw_rx7900xtx_backplate(self):
        """Draw RX 7900 XTX reinforced backplate with AMD logo."""
        # Backplate
        backplate_color = (0.75, 0.75, 0.8, 1.0)
        self.view3d._draw_3d_box(-14.35, -6.2, -2, 28.7, 12.4, 2, backplate_color)
        
        # Ventilation holes (30% open area)
        vent_color = (0.02, 0.02, 0.03, 1.0)
        for i in range(35):
            x = -14 + i * (28.0 / 35)
            for j in range(4):
                y = -5 + j * 2.5
                self.view3d._draw_3d_box(x, y, -2, 0.3, 0.8, 0.1, vent_color)
        
        # AMD logo area (simplified)
        logo_color = (0.8, 0.1, 0.1, 1.0)  # AMD red
        self.view3d._draw_3d_box(-2, -1.5, -1.9, 4, 3, 0.1, logo_color)

    def _draw_rx7900xtx_io_bracket(self):
        """Draw I/O bracket with display ports and power connectors."""
        # I/O bracket
        bracket_color = (0.7, 0.7, 0.75, 1.0)
        self.view3d._draw_3d_box(14.35, -6.2, -2, 2.0, 12.4, 3.0, bracket_color)
        
        # Display ports (3x DisplayPort 2.1, 1x HDMI 2.1a)
        port_positions = [(14.65, -3, "DP"), (14.65, -1, "DP"), (14.65, 1, "DP"), (14.65, 3, "HDMI")]
        
        for x, y, port_type in port_positions:
            port_color = (0.2, 0.2, 0.25, 1.0)
            self.view3d._draw_3d_box(x, y - 0.6, -1, 0.8, 1.2, 0.8, port_color)
        
        # 8-pin power connectors (2x)
        power_color = (0.15, 0.15, 0.2, 1.0)
        self.view3d._draw_3d_box(14.65, 5.0, -1, 1.0, 1.5, 0.8, power_color)
        self.view3d._draw_3d_box(14.65, 6.5, -1, 1.0, 1.5, 0.8, power_color)
