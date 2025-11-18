"""
RX 7900 GRE GPU Model - Ultra Realistic with All Real-World Components
Complete 1:1 replica with every component found on actual RX 7900 GRE
"""

from .baseGpuModel import BaseGPUModel
from typing import Dict, Tuple
import math

class RX7900GREModel(BaseGPUModel):
    """Ultra-realistic RX 7900 GRE GPU model with all real-world components."""

    # Component specifications
    LENGTH_MM = 257.0
    WIDTH_MM = 115.0
    HEIGHT_MM = 48.0
    GPU_DIE_SIZE_MM = 18.0
    GPU_DIE_THICKNESS_MM = 0.8
    MCD_DIE_SIZE_MM = 6.0
    VRAM_CHIPS = 8
    VRAM_CHIP_SIZE_MM = 12.0
    HEATSINK_FINS = 40
    HEAT_PIPES = 4
    FAN_COUNT = 2
    PCB_LENGTH_MM = 237.0
    PCB_WIDTH_MM = 101.0
    PCB_THICKNESS_MM = 1.5

    def get_model_name(self) -> str:
        return "AMD Radeon RX 7900 GRE (Ultra Realistic)"

    def get_chassis_dimensions(self) -> Tuple[float, float, float]:
        """RX 7900 GRE exact dimensions: 257mm x 115mm x 48mm"""
        return (self.LENGTH_MM/10, self.WIDTH_MM/10, self.HEIGHT_MM/10)

    def get_component_list(self) -> Dict[str, str]:
        """Get RX 7900 GRE specific components with detailed explanations."""
        return {
            "Chassis": "257mm x 115mm x 48mm aluminum chassis with AMD signature design",
            "Dual Fans": "2x AMD Axial-tech fans with 11 blades, fluid dynamic bearing",
            "Vapor Chamber": "Medium vapor chamber with 4 heat pipes covering full die",
            "GPU Die": "Navi33 GPU, 3,584 CUDA cores, 16GB GDDR6 memory, chiplet architecture",
            "VRAM Layout": "8x Samsung GDDR6 chips in 256-bit configuration",
            "Power Delivery": "12-phase VRM with 40A power stages and digital PWM",
            "Backplate": "Reinforced aluminum with AMD logo and 20% ventilation area",
            "PCB Design": "10-layer custom PCB with 2oz copper layers, AMD red PCB",
            "Display Outputs": "2x DisplayPort 2.1, 1x HDMI 2.1a, supports 8K@60Hz HDR",
            "Power Connector": "8-pin + 6-pin connectors supporting up to 260W",
            "Heat Pipes": "4x 8mm nickel-plated copper heat pipes",
            "VRM Cooling": "Extended heatsinks with fin arrays for power stages",
            "Memory Interface": "256-bit memory bus, 18 Gbps effective, 576 GB/s bandwidth",
            "Clock Speeds": "2.2 GHz boost, 1.5 GHz base, 40 TFLOPS single precision",
            "Illumination": "Red LED lighting on fan shroud and side logo",
            "Thermal Design": "2-slot design, 260W TDP, 95°C max operating temperature",
            "Ventilation": "Optimized airflow path with 70% open area, dual-fan design",
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
        """Draw RX 7900 GRE chassis."""
        if self.view3d and hasattr(self.view3d, 'show_chassis') and self.view3d.show_chassis and self.should_render_component("chassis"):
            self._draw_rx7900gre_chassis()

    def draw_cooling_system(self, lod: int):
        """Draw RX 7900 GRE cooling system."""
        if self.view3d and hasattr(self.view3d, 'show_cooling') and self.view3d.show_cooling and self.should_render_component("cooling"):
            self._draw_rx7900gre_heatsink()
            self._draw_rx7900gre_heat_pipes()
            self._draw_rx7900gre_fans()

    def draw_pcb_and_components(self, lod: int):
        """Draw RX 7900 GRE PCB and all components."""
        if self.view3d and hasattr(self.view3d, 'show_pcb') and self.view3d.show_pcb and self.should_render_component("pcb"):
            self._draw_rx7900gre_pcb()
        if self.view3d and hasattr(self.view3d, 'show_gpu_die') and self.view3d.show_gpu_die and self.should_render_component("gpu_die"):
            self._draw_rx7900gre_gpu_die()
        if self.view3d and hasattr(self.view3d, 'show_vram') and self.view3d.show_vram and self.should_render_component("vram"):
            self._draw_rx7900gre_vram()
        if self.view3d and hasattr(self.view3d, 'show_power_delivery') and self.view3d.show_power_delivery and self.should_render_component("power_delivery"):
            self._draw_rx7900gre_power_delivery()

    def draw_backplate(self, lod: int):
        """Draw RX 7900 GRE backplate."""
        if self.view3d and hasattr(self.view3d, 'show_backplate') and self.view3d.show_backplate and self.should_render_component("backplate"):
            self._draw_rx7900gre_backplate()
        if self.view3d and hasattr(self.view3d, 'show_io_bracket') and self.view3d.show_io_bracket and self.should_render_component("io_bracket"):
            self._draw_rx7900gre_io_bracket()

    def draw_complete_model(self, lod: int):
        """Draw the complete RX 7900 GRE model with all real-world components."""
        # Draw from back to front for proper depth
        self.draw_backplate(lod)
        self.draw_pcb_and_components(lod)
        self.draw_cooling_system(lod)
        self.draw_chassis(lod)

    def draw_ultra_realistic_model(self):
        """Draw ultra-realistic 1:1 replica with microscopic details."""
        self.draw_complete_model(0)

    def _draw_rx7900gre_pcb(self):
        """Draw ultra-detailed RX 7900 GRE PCB with all real-world components."""
        if not self.view3d:
            return

        # Main PCB board - realistic dimensions (237mm x 101mm x 1.5mm)
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
        self._draw_rx7900gre_pcb_components(pcb_length, pcb_width)

    def _draw_pcb_traces(self, pcb_length, pcb_width):
        """Draw realistic PCB traces."""
        trace_color = (0.7, 0.6, 0.3, 0.8)

        # Main power traces (thicker)
        for i in range(4):
            y = -pcb_width/2 + (i + 1) * (pcb_width / 5)
            self.view3d._draw_3d_box(-pcb_length/2 + 2, y - 0.1, 0.08,
                                     pcb_length - 4, 0.2, 0.05, trace_color)

        # Data traces (medium thickness)
        for i in range(8):
            y = -pcb_width/2 + i * (pcb_width / 8)
            for j in range(10):
                x = -pcb_length/2 + j * (pcb_length / 10)
                self.view3d._draw_3d_box(x, y - 0.05, 0.08, 0.3, 0.1, 0.03, trace_color)

    def _draw_microscopic_components(self, pcb_length, pcb_width):
        """Draw resistors, capacitors, and other tiny components."""
        # Surface mount resistors (0402 size: 1.0mm x 0.5mm)
        resistor_color = (0.3, 0.2, 0.1, 1.0)

        for i in range(80):
            x = -pcb_length/2 + 2 + (i % 16) * (pcb_length - 4) / 16
            y = -pcb_width/2 + 1 + (i // 16) * (pcb_width - 2) / 5

            self.view3d._draw_3d_box(x, y, 0.05, 0.1, 0.05, 0.02, resistor_color)

        # Surface mount capacitors
        capacitor_color = (0.1, 0.1, 0.2, 1.0)

        for i in range(40):
            x = -pcb_length/2 + 2 + (i % 8) * (pcb_length - 4) / 8
            y = -pcb_width/2 + 1 + (i // 8) * (pcb_width - 2) / 5

            self.view3d._draw_3d_cylinder(x, y, 0.05, 0.03, 0.1, capacitor_color)

        # Inductors
        inductor_color = (0.2, 0.15, 0.1, 1.0)

        for i in range(8):
            x = -pcb_length/2 + 3 + i * (pcb_length - 6) / 8
            y = -pcb_width/2 + pcb_width - 2

            self.view3d._draw_3d_cylinder(x, y, 0.05, 0.08, 0.15, inductor_color)

    def _draw_rx7900gre_pcb_components(self, pcb_length, pcb_width):
        """Draw all real-world RX 7900 GRE PCB components."""
        # GPU Die (Navi33 chiplet)
        self._draw_rx7900gre_gpu_die()

        # GDDR6 VRAM chips (8 chips around GPU die)
        self._draw_rx7900gre_vram()

        # VRM (Voltage Regulator Modules)
        self._draw_rx7900gre_vrms()

        # Power delivery components
        self._draw_rx7900gre_power_delivery()

        # DisplayPort and HDMI controllers
        self._draw_rx7900gre_display_controllers()

        # Thermal sensors and monitoring chips
        self._draw_rx7900gre_thermal_sensors()

        # BIOS chip
        self._draw_rx7900gre_bios()

        # Clock generator
        self._draw_rx7900gre_clock_generator()

        # Power management ICs
        self._draw_rx7900gre_power_management()

    def _draw_rx7900gre_gpu_die(self):
        """Draw Navi33 GPU die with chiplet architecture."""
        # Main Graphics Compute Die (GCD) - 5nm
        gcd_size = self.GPU_DIE_SIZE_MM / 10

        # GCD package substrate
        self.view3d._draw_3d_box(-gcd_size/2, -gcd_size/2, 0, gcd_size, gcd_size, 0.1,
                                 (0.05, 0.08, 0.05, 1.0))

        # GCD silicon die
        self.view3d._draw_3d_box(-gcd_size/2, -gcd_size/2, 0.1, gcd_size, gcd_size, self.GPU_DIE_THICKNESS_MM/10,
                                 (0.15, 0.15, 0.2, 1.0))

        # Draw WGP layout (4 WGPs per shader engine, 6 shader engines = 24 WGPs total)
        self._draw_navi33_wgp_layout(gcd_size, 0.18)

        # Memory Cache Dies (MCDs) - 6nm
        mcd_size = self.MCD_DIE_SIZE_MM / 10
        mcd_positions = [(-2.5, 0), (2.5, 0)]

        for x, y in mcd_positions:
            # MCD package
            self.view3d._draw_3d_box(x - mcd_size/2, y - mcd_size/2, 0, mcd_size, mcd_size, 0.08,
                                     (0.08, 0.05, 0.05, 1.0))

            # MCD silicon die
            self.view3d._draw_3d_box(x - mcd_size*0.75, y - mcd_size*0.75, 0.08, mcd_size*1.5, mcd_size*1.5, 0.06,
                                     (0.2, 0.15, 0.15, 1.0))

        # Heat spreader covering all dies
        hs_size = 3.0
        hs_thickness = 0.05
        self.view3d._draw_3d_box(-hs_size/2, -hs_size/2, 0.18,
                                 hs_size, hs_size, hs_thickness,
                                 (0.6, 0.6, 0.65, 1.0))

    def _draw_navi33_wgp_layout(self, die_size, z_offset):
        """Draw exact Navi33 Workgroup Processor layout."""
        # Navi33 has 6 Shader Engines, each with 4 WGPs (24 total)
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

    def _draw_rx7900gre_vram(self):
        """Draw 8 GDDR6 VRAM chips in exact RX 7900 GRE layout."""
        # RX 7900 GRE has 8 VRAM chips
        vram_positions = [
            # Front chips
            (-5, -2), (-1, -2), (3, -2),
            (-5, 0), (-1, 0), (3, 0),
            # Back chips
            (-3, 2), (1, 2)
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
            for i in range(6):
                wire_x = x - 0.35 + i * 0.07
                self._draw_bonding_wire(wire_x, y, z + 0.18, wire_x, y - 0.25, z + 0.05, wire_color)

    def _draw_bonding_wire(self, x1, y1, z1, x2, y2, z2, color):
        """Draw microscopic bonding wire."""
        # Simplified bonding wire representation
        self.view3d._draw_3d_box(x1 - 0.01, y1 - 0.01, z1, 0.02, (y2-y1) + 0.02, 0.01, color)

    def _draw_rx7900gre_vrms(self):
        """Draw 12-phase VRM power delivery system."""
        # VRM positions around the GPU die
        vrm_positions = [
            # Left side VRMs (6 phases)
            (-8, -3), (-8, -1), (-8, 1), (-8, 3),
            (-6, -3), (-6, 1),
            # Right side VRMs (6 phases)
            (6, -3), (6, -1), (6, 1), (6, 3),
            (8, -3), (8, 1)
        ]

        for i, (x, y) in enumerate(vrm_positions):
            # Main VRM chip
            vrm_color = (0.2, 0.2, 0.2, 1.0)
            self.view3d._draw_3d_box(x - 0.5, y - 0.5, 0.1, 1.0, 1.0, 0.2, vrm_color)

            # Heatsink fins on VRM
            for fin in range(3):
                fin_x = x - 0.4 + fin * 0.1
                fin_color = (0.7, 0.7, 0.8, 1.0)
                self.view3d._draw_3d_box(fin_x, y - 0.6, 0.3, 0.06, 0.2, 0.25, fin_color)

    def _draw_rx7900gre_power_delivery(self):
        """Draw additional power delivery components."""
        # Power inductors
        inductor_positions = [(-8, -5), (-8, 5), (8, -5), (8, 5)]
        inductor_color = (0.15, 0.1, 0.05, 1.0)

        for x, y in inductor_positions:
            self.view3d._draw_3d_cylinder(x, y, 0.15, 0.3, 0.4, inductor_color)

        # Power capacitors
        capacitor_positions = [(-5, -5), (-1, -5), (3, -5)]
        capacitor_color = (0.1, 0.1, 0.15, 1.0)

        for x, y in capacitor_positions:
            self.view3d._draw_3d_cylinder(x, y, 0.1, 0.2, 0.3, capacitor_color)

    def _draw_rx7900gre_display_controllers(self):
        """Draw DisplayPort and HDMI controller chips."""
        # DisplayPort 2.1 controllers
        dp_positions = [(9.5, -2), (9.5, 0)]
        dp_color = (0.1, 0.1, 0.2, 1.0)

        for x, y in dp_positions:
            self.view3d._draw_3d_box(x - 0.3, y - 0.2, 0.1, 0.6, 0.4, 0.15, dp_color)

        # HDMI 2.1a controller
        hdmi_color = (0.15, 0.1, 0.2, 1.0)
        self.view3d._draw_3d_box(9.5 - 0.3, 2 - 0.2, 0.1, 0.6, 0.4, 0.15, hdmi_color)

    def _draw_rx7900gre_thermal_sensors(self):
        """Draw thermal sensor chips."""
        # Thermal sensor positions
        sensor_positions = [(0, -3.5), (0, 3.5), (-3.5, 0), (3.5, 0)]
        sensor_color = (0.1, 0.2, 0.1, 1.0)

        for x, y in sensor_positions:
            self.view3d._draw_3d_box(x - 0.2, y - 0.2, 0.05, 0.4, 0.4, 0.1, sensor_color)

    def _draw_rx7900gre_bios(self):
        """Draw BIOS chip."""
        bios_color = (0.05, 0.1, 0.05, 1.0)
        self.view3d._draw_3d_box(-3.5, -3.5, 0.05, 0.8, 0.6, 0.1, bios_color)

    def _draw_rx7900gre_clock_generator(self):
        """Draw clock generator chip."""
        clock_color = (0.1, 0.15, 0.1, 1.0)
        self.view3d._draw_3d_box(3.5, -3.5, 0.05, 0.6, 0.6, 0.1, clock_color)

    def _draw_rx7900gre_power_management(self):
        """Draw power management ICs."""
        pmic_positions = [(-1.5, -3.5), (0, -3.5), (1.5, -3.5)]
        pmic_color = (0.15, 0.1, 0.1, 1.0)

        for x, y in pmic_positions:
            self.view3d._draw_3d_box(x - 0.3, y - 0.3, 0.05, 0.6, 0.6, 0.1, pmic_color)

    def _draw_rx7900gre_heatsink(self):
        """Draw medium heatsink with vapor chamber and fins."""
        # Heatsink base
        base_color = (0.75, 0.75, 0.8, 1.0)
        self.view3d._draw_3d_box(-12.85, -5.75, 0.5, 25.7, 11.5, 2.5, base_color)

        # Heatsink fins (40 fins for RX 7900 GRE)
        fin_count = self.HEATSINK_FINS
        fin_thickness = 0.08
        fin_spacing = 25.7 / fin_count

        for i in range(fin_count):
            x = -12.85 + i * fin_spacing
            fin_color = (0.8, 0.8, 0.85, 1.0)
            self.view3d._draw_3d_box(x, -5.5, 0.5, fin_thickness, 11.0, 3.5, fin_color)

    def _draw_rx7900gre_heat_pipes(self):
        """Draw 4 heat pipes with realistic routing."""
        # Heat pipe positions across the heatsink
        heat_pipe_positions = [
            (-3.5, -1.5), (0, -1.5),
            (-3.5, 1.5), (0, 1.5)
        ]

        pipe_color = (0.8, 0.5, 0.2, 1.0)

        for x, y in heat_pipe_positions:
            # Main heat pipe
            self.view3d._draw_3d_cylinder(x, y, 2, 0.25, 24, pipe_color)

            # Heat pipe contact with GPU
            contact_color = (0.8, 0.5, 0.2, 1.0)
            self.view3d._draw_3d_cylinder(x, y, 0.3, 0.2, 1.7, contact_color)

    def _draw_rx7900gre_fans(self):
        """Draw dual AMD Axial-tech fans with 11 blades each."""
        fan_positions = [(-4, 0), (4, 0)]
        fan_radius = 2.5

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
        blade_length = radius - 0.6
        blade_width = 0.3

        x1 = cx + 0.6 * math.cos(angle)
        y1 = cy + 0.6 * math.sin(angle)
        x2 = cx + radius * math.cos(angle)
        y2 = cy + radius * math.sin(angle)

        self.view3d._draw_3d_box(x1 - blade_width/2, y1 - 0.1, cz,
                                 blade_width, blade_length, 0.05, color)

    def _draw_rx7900gre_chassis(self):
        """Draw AMD signature chassis with optimized ventilation."""
        chassis_color = (0.85, 0.85, 0.9, 1.0)

        # Main chassis body
        self.view3d._draw_3d_box(-12.85, -5.75, 0, 25.7, 11.5, 4.8, chassis_color)

        # AMD signature ventilation (70% open area)
        vent_color = (0.05, 0.05, 0.08, 1.0)
        for i in range(25):
            x = -12.5 + i * (25.7 / 25)
            for j in range(4):
                y = -5.5 + j * 2.9
                self.view3d._draw_3d_box(x, y, 2.4, 0.5, 1.0, 0.1, vent_color)

    def _draw_rx7900gre_backplate(self):
        """Draw RX 7900 GRE reinforced backplate with AMD logo."""
        # Backplate
        backplate_color = (0.75, 0.75, 0.8, 1.0)
        self.view3d._draw_3d_box(-12.85, -5.75, -2, 25.7, 11.5, 2, backplate_color)

        # Ventilation holes (20% open area)
        vent_color = (0.02, 0.02, 0.03, 1.0)
        for i in range(25):
            x = -12.5 + i * (25.7 / 25)
            for j in range(2):
                y = -4.5 + j * 4.5
                self.view3d._draw_3d_box(x, y, -2, 0.3, 0.8, 0.1, vent_color)

        # AMD logo area (simplified)
        logo_color = (0.8, 0.1, 0.1, 1.0)
        self.view3d._draw_3d_box(-2, -1.5, -1.9, 4, 3, 0.1, logo_color)

    def _draw_rx7900gre_io_bracket(self):
        """Draw I/O bracket with display ports and power connectors."""
        # I/O bracket
        bracket_color = (0.7, 0.7, 0.75, 1.0)
        self.view3d._draw_3d_box(12.85, -5.75, -2, 2.0, 11.5, 3.0, bracket_color)

        # Display ports (2x DisplayPort 2.1, 1x HDMI 2.1a)
        port_positions = [(13.15, -2, "DP"), (13.15, 0, "DP"), (13.15, 2, "HDMI")]

        for x, y, port_type in port_positions:
            port_color = (0.2, 0.2, 0.25, 1.0)
            self.view3d._draw_3d_box(x, y - 0.6, -1, 0.8, 1.2, 0.8, port_color)

        # 8-pin + 6-pin power connectors
        power_color = (0.15, 0.15, 0.2, 1.0)
        self.view3d._draw_3d_box(13.15, 4.0, -1, 1.0, 1.5, 0.8, power_color)
        self.view3d._draw_3d_box(13.15, 5.5, -1, 0.8, 1.2, 0.8, power_color)