"""
GPU Component Highlighter

Author: 𝙅𝙖𝙠𝙤𝙗 / 𝙎𝙚𝙣𝙨𝙚𝙞 𝙄𝙨𝙨𝙚𝙞

Overview:
- Centralized component metadata and highlighting state for 3D view
- Rich technical details for UI panels, with HTML formatting helpers
- Lightweight API: get/set highlight, query/component lists
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class ComponentType(Enum):
    CHASSIS = "chassis"
    COOLING = "cooling"
    PCB = "pcb"
    GPU_DIE = "gpu_die"
    VRAM = "vram"
    POWER_DELIVERY = "power_delivery"
    BACKPLATE = "backplate"
    IO_BRACKET = "io_bracket"
    MICROSCOPIC = "microscopic"
    TRACES = "traces"
    BIOS = "bios"
    CLOCK_GENERATOR = "clock_generator"
    THERMAL_SENSORS = "thermal_sensors"
    POWER_MANAGEMENT_IC = "power_management_ic"
    DISPLAY_ENGINES = "display_engines"
    PCI_BRIDGE = "pci_bridge"
    AUXILIARY_IC = "auxiliary_ic"

@dataclass
class ComponentInfo:
    name: str
    description: str
    technical_specs: Dict[str, str]
    physical_properties: Dict[str, str]
    function: str
    importance: str
    manufacturing_details: str
    performance_impact: str
    failure_modes: List[str]
    maintenance_notes: str

class ComponentHighlighter:
    
    def __init__(self):
        self.component_database = self._initialize_component_database()
        self.current_highlight: Optional[ComponentType] = None
        
    def _initialize_component_database(self) -> Dict[ComponentType, ComponentInfo]:
        return {
            ComponentType.CHASSIS: ComponentInfo(
                name="GPU Chassis/Enclosure",
                description="External protective housing that provides structural integrity, EMI shielding, and thermal management for all internal components.",
                technical_specs={
                    "Material": "Aluminum alloy 6063-T5",
                    "Thickness": "0.8-1.2mm",
                    "Finish": "Anodized coating",
                    "Weight": "1.2-1.8kg",
                    "Mounting": "PCIe bracket screws",
                    "Ventilation": "30-40% open area"
                },
                physical_properties={
                    "Dimensions": "Varies by GPU model",
                    "Color": "Black/silver/custom",
                    "Surface": "Brushed/matte finish",
                    "Logos": "Laser etched or printed",
                    "Ports": "Cutout precision",
                    "Tolerance": "±0.1mm manufacturing"
                },
                function="Protects internal components from physical damage, dust, and electromagnetic interference. Provides mounting points and directs airflow through cooling system.",
                importance="CRITICAL - Primary structural component and thermal management interface",
                manufacturing_details="CNC machined or stamped aluminum, anodized for corrosion resistance, precision cutouts for ports and ventilation",
                performance_impact="Affects cooling efficiency by 15-25%, weight impacts motherboard stress, ventilation design directly impacts thermals",
                failure_modes=["Physical damage", "Bent mounting points", "Blocked ventilation", "Corrosion", "Loose screws"],
                maintenance_notes="Clean dust accumulation regularly, check mounting screws, ensure ventilation paths remain clear, inspect for corrosion"
            ),
            
            ComponentType.COOLING: ComponentInfo(
                name="Cooling System (Fans + Heatsink)",
                description="Multi-stage thermal dissipation system using axial fans, aluminum heatsink fins, and copper heat pipes to remove heat from GPU die and VRAM.",
                technical_specs={
                    "Fan Type": "Axial-tech with ball bearings",
                    "Fan Speed": "500-3000 RPM variable",
                    "Fan Size": "80-92mm diameter",
                    "Heatsink Material": "Aluminum 6063",
                    "Heat Pipes": "Copper with nickel plating",
                    "Fin Count": "80-150 aluminum fins",
                    "Thermal Interface": "Liquid metal or paste"
                },
                physical_properties={
                    "Heat Pipe Diameter": "6-8mm",
                    "Fin Thickness": "0.2-0.3mm",
                    "Fin Spacing": "1.5-2.5mm",
                    "Base Thickness": "3-5mm",
                    "Fan Blade Count": "9-13 blades",
                    "Bearing Type": "Dual ball bearing"
                },
                function="Transfers heat from GPU die and VRAM to ambient air through conduction (heat pipes) and convection (heatsink fins + forced air).",
                importance="CRITICAL - Prevents thermal throttling and component damage, directly impacts performance and longevity",
                manufacturing_details="Extruded aluminum heatsink, CNC machined heat pipe contact, injection molded fan blades, precision balanced rotors",
                performance_impact="Directly limits boost clocks by 10-30%, fan noise affects user experience, thermal efficiency determines sustained performance",
                failure_modes=["Fan bearing failure", "Heatsink fin damage", "Heat pipe delamination", "Thermal interface degradation", "Fan motor failure"],
                maintenance_notes="Clean fans and heatsink monthly, replace thermal paste every 2-3 years, monitor fan bearings, check for vibration"
            ),
            
            ComponentType.PCB: ComponentInfo(
                name="Printed Circuit Board (PCB)",
                description="Multi-layer fiberglass substrate with copper traces providing electrical connections and mounting platform for all electronic components.",
                technical_specs={
                    "Layers": "12-14 layers",
                    "Material": "FR-4 fiberglass epoxy",
                    "Thickness": "1.5-2.0mm",
                    "Copper Weight": "2-4 oz per layer",
                    "Via Type": "Plated through-holes",
                    "Solder Mask": "LPI green/solder",
                    "Silkscreen": "White component markings"
                },
                physical_properties={
                    "Dimensions": "267-340mm length",
                    "Width": "110-140mm",
                    "Trace Width": "0.1-0.3mm",
                    "Via Diameter": "0.2-0.8mm",
                    "Pad Size": "0.5-2.0mm",
                    "Surface Finish": "ENIG or HASL"
                },
                function="Provides electrical interconnects between components, mechanical support, and signal integrity for high-speed data transmission.",
                importance="CRITICAL - Foundation for all electronic components, determines signal integrity and power delivery capability",
                manufacturing_details="Multi-layer lamination process, photolithography for trace patterning, chemical etching, automated optical inspection",
                performance_impact="Trace impedance affects signal integrity by 5-15%, power delivery capability limits overclocking, layer count affects EMI",
                failure_modes=["Delamination", "Trace corrosion", "Via failure", "Solder joint cracks", "Electromigration"],
                maintenance_notes="Inspect for physical damage, check for corrosion, monitor for hot spots, avoid flexing or bending"
            ),
            
            ComponentType.GPU_DIE: ComponentInfo(
                name="GPU Silicon Die",
                description="Monolithic silicon processor containing billions of transistors organized into streaming multiprocessors, memory controllers, and display engines.",
                technical_specs={
                    "Process Node": "4-5nm (TSMC/Samsung)",
                    "Transistor Count": "35-76 billion",
                    "Die Size": "15-21mm x 15-21mm",
                    "Core Count": "5,376-16,384 CUDA cores",
                    "Clock Speed": "2.1-2.6 GHz boost",
                    "Memory Controller": "192-384-bit",
                    "Manufacturing": "EUV lithography"
                },
                physical_properties={
                    "Substrate": "Organic package",
                    "Thickness": "0.8-1.0mm",
                    "Heat Spreader": "Nickel-plated copper",
                    "Underfill": "Epoxy resin",
                    "Interconnect": "Flip-chip bumps",
                    "Package Size": "30-40mm square"
                },
                function="Executes graphics rendering computations, parallel processing, AI workloads, and manages all GPU operations through thousands of processing cores.",
                importance="CRITICAL - Core processing unit, determines all performance capabilities and features",
                manufacturing_details="300mm silicon wafers, EUV lithography, chemical mechanical polishing, wafer-level testing, precision dicing",
                performance_impact="Directly determines gaming performance by 80-90%, clock speeds affect FPS by 20-40%, architecture efficiency determines performance per watt",
                failure_modes=["Electromigration", "Thermal degradation", "Overclocking damage", "Manufacturing defects", "Voltage regulator failure"],
                maintenance_notes="Monitor temperatures carefully, avoid excessive overclocking, ensure adequate cooling, update drivers regularly"
            ),
            
            ComponentType.VRAM: ComponentInfo(
                name="Video RAM (GDDR6/GDDR6X)",
                description="High-bandwidth memory chips providing fast data storage for textures, frame buffers, and compute workloads with dedicated memory controllers.",
                technical_specs={
                    "Type": "GDDR6/GDDR6X SDRAM",
                    "Capacity": "12-24GB total",
                    "Speed": "18-24 Gbps effective",
                    "Bus Width": "192-384-bit",
                    "Bandwidth": "504-1000 GB/s",
                    "Chip Count": "12-24 chips",
                    "Organization": "16Gb/32Gb per chip"
                },
                physical_properties={
                    "Package": "BGA 180-200 balls",
                    "Dimensions": "14x8mm or 10x6mm",
                    "Thickness": "1.0-1.2mm",
                    "Operating Voltage": "1.1-1.35V",
                    "Temperature Range": "0-95°C",
                    "Refresh Rate": "Auto/power-saving"
                },
                function="Stores and retrieves high-speed data for rendering operations, frame buffers, textures, and compute workloads with dedicated memory controllers.",
                importance="HIGH - Determines memory bandwidth for high-resolution textures and large datasets, affects gaming at 4K+ resolutions",
                manufacturing_details="Silicon wafer fabrication, BGA packaging, high-speed testing, binning for speed grades, thermal characterization",
                performance_impact="Memory bandwidth affects 4K gaming by 15-25%, capacity limits texture quality, speed impacts ray tracing performance",
                failure_modes=["Memory errors", "Thermal throttling", "Signal integrity issues", "BGA joint failure", "Overclocking damage"],
                maintenance_notes="Monitor memory temperatures, avoid excessive memory overclocking, ensure adequate VRAM cooling, check for artifacts"
            ),
            
            ComponentType.POWER_DELIVERY: ComponentInfo(
                name="Power Delivery System (VRM)",
                description="Multi-phase voltage regulation module converting 12V input to precise voltages for GPU die, memory, and other components with digital control.",
                technical_specs={
                    "Phases": "12-24 phases total",
                    "Controller": "Digital PWM",
                    "Power Stages": "50-75A each",
                    "Inductors": "Ferrite core",
                    "Input Voltage": "12V (PCIe)",
                    "Output Voltages": "0.8-1.2V GPU, 1.1-1.35V memory",
                    "Efficiency": "85-92% typical"
                },
                physical_properties={
                    "Inductor Size": "5-8mm diameter",
                    "Capacitor Type": "MLCC/Polymer",
                    "MOSFET Package": "5x6mm or 3x4mm",
                    "Controller IC": "QFN/TSOP",
                    "Phase Count": "6-12 per side",
                    "Thermal Pads": "Silicone-based"
                },
                function="Converts and regulates power from PCIe slot and external connectors to precise voltages required by GPU die, memory, and supporting components.",
                importance="CRITICAL - Provides stable power for all components, determines overclocking headroom and efficiency",
                manufacturing_details="Surface mount assembly, automated optical inspection, thermal profiling, voltage regulation testing",
                performance_impact="Power quality affects stability by 20-30%, phase count impacts efficiency, VRM cooling determines sustained boost clocks",
                failure_modes=["MOSFET failure", "Capacitor bulging", "Inductor saturation", "Controller failure", "Thermal damage"],
                maintenance_notes="Monitor VRM temperatures, check for capacitor bulging, ensure adequate VRM cooling, listen for coil whine"
            ),
            
            ComponentType.BACKPLATE: ComponentInfo(
                name="GPU Backplate",
                description="Rear mounting plate providing structural support, additional cooling, and protection for PCB components with ventilation for airflow.",
                technical_specs={
                    "Material": "Aluminum or stainless steel",
                    "Thickness": "0.5-1.0mm",
                    "Ventilation": "20-40% open area",
                    "Mounting": "4-6 screws",
                    "Finish": "Anodized or painted",
                    "Weight": "200-400g",
                    "Thermal Pads": "Silicone interface"
                },
                physical_properties={
                    "Dimensions": "Matches PCB size",
                    "Cutouts": "Component clearance",
                    "Logos": "Laser etched/printed",
                    "Edges": "Deburred finish",
                    "Holes": "Precision drilled",
                    "Surface": "Brushed/matte"
                },
                function="Provides structural rigidity, protects rear PCB components, assists in heat dissipation through thermal pads, and enhances aesthetics.",
                importance="MEDIUM - Prevents PCB flexing, provides additional cooling, protects components during installation",
                manufacturing_details="Stamping or CNC machining, drilling and tapping, surface finishing, quality inspection",
                performance_impact="Provides 5-10% additional cooling, prevents PCB warping, protects components from damage",
                failure_modes=["Bent mounting points", "Scratches/damage", "Loose screws", "Thermal pad degradation"],
                maintenance_notes="Check mounting screws, clean ventilation holes, inspect thermal pads, ensure proper alignment"
            ),
            
            ComponentType.IO_BRACKET: ComponentInfo(
                name="I/O Bracket and Ports",
                description="Steel bracket mounting GPU to case with display outputs, power connectors, and external interfaces for video and power delivery.",
                technical_specs={
                    "Material": "Steel 1.0mm",
                    "Mounting": "2 case screws",
                    "Display Ports": "3x DP 1.4a, 1x HDMI 2.1",
                    "Power Connector": "12VHPWR or 8-pin",
                    "Bracket Height": "120mm standard",
                    "Shielding": "EMI fingers",
                    "Finish": "Nickel plating"
                },
                physical_properties={
                    "Port Spacing": "Standard ATX",
                    "Connector Type": "Gold-plated",
                    "Retention": "Spring contacts",
                    "Labeling": "Laser etched",
                    "LED Indicators": "Activity/power",
                    "Dimensions": "ATX standard"
                },
                function="Provides secure mounting to PC case, display output interfaces, power delivery connections, and EMI shielding for signal integrity.",
                importance="HIGH - Essential for installation, display connectivity, and power delivery, affects signal quality",
                manufacturing_details="Steel stamping, precision forming, connector assembly, EMI shielding installation, testing",
                performance_impact="Connector quality affects signal integrity, mounting security prevents damage, shielding reduces interference",
                failure_modes=["Bent bracket", "Connector damage", "Poor contact", "EMI leakage", "Mounting strip"],
                maintenance_notes="Check bracket straightness, clean connector contacts, ensure secure mounting, inspect for damage"
            ),
            
            ComponentType.MICROSCOPIC: ComponentInfo(
                name="Microscopic Components",
                description="Surface mount resistors, capacitors, inductors, and integrated circuits providing power filtering, signal conditioning, and control functions.",
                technical_specs={
                    "Resistor Size": "0402/0603 packages",
                    "Capacitor Type": "MLCC/Polymer",
                    "IC Packages": "QFN/TSSOP",
                    "Inductor Values": "1-100μH",
                    "Tolerance": "1-5%",
                    "Voltage Rating": "6.3-50V",
                    "Operating Temp": "-40 to 125°C"
                },
                physical_properties={
                    "Package Size": "0.5-2.0mm",
                    "Solder Joints": "Lead-free SAC305",
                    "Placement": "Automated pick-and-place",
                    "Markings": "Laser printed",
                    "Height": "0.3-1.2mm",
                    "Pitch": "0.4-1.27mm"
                },
                function="Power filtering, signal conditioning, voltage regulation, timing control, and monitoring of GPU operation parameters.",
                importance="MEDIUM - Essential for stable operation, power quality, signal integrity, and protection circuits",
                manufacturing_details="Automated SMT assembly, reflow soldering, X-ray inspection, automated testing",
                performance_impact="Power quality affects stability by 5-10%, signal integrity affects high-speed operation, protection circuits prevent damage",
                failure_modes=["Solder joint cracks", "Component drift", "Moisture damage", "Thermal stress", "Overvoltage damage"],
                maintenance_notes="Visual inspection for damage, monitor for drift, ensure adequate cooling, avoid power surges"
            ),
            
            ComponentType.TRACES: ComponentInfo(
                name="PCB Copper Traces",
                description="Microscopic copper pathways on PCB layers providing electrical connections between components with controlled impedance for signal integrity.",
                technical_specs={
                    "Trace Width": "0.1-0.5mm",
                    "Copper Thickness": "17-70μm",
                    "Layer Count": "12-14 layers",
                    "Impedance": "50-100Ω controlled",
                    "Via Plating": "Copper filled",
                    "Spacing": "0.1-0.3mm",
                    "Current Capacity": "0.5-3A"
                },
                physical_properties={
                    "Cross-section": "Rectangular",
                    "Surface Finish": "ENIG/OSP",
                    "Aspect Ratio": "6:1 to 8:1",
                    "Trace Routing": "Differential pairs",
                    "Length Matching": "±0.1mm tolerance",
                    "Material": "Electrolytic copper"
                },
                function="Provides electrical interconnects with controlled impedance for high-speed signals, power distribution, and ground planes.",
                importance="HIGH - Determines signal integrity, power delivery capability, and electromagnetic compatibility",
                manufacturing_details="Photolithography patterning, chemical etching, plating processes, impedance testing, AOI inspection",
                performance_impact="Impedance control affects signal integrity by 10-20%, trace width limits current capacity, routing affects EMI",
                failure_modes=["Open circuits", "Short circuits", "Impedance mismatch", "Electromigration", "Delamination"],
                maintenance_notes="Visual inspection for damage, monitor for hot spots, avoid physical stress, check for corrosion"
            ),
            
            ComponentType.BIOS: ComponentInfo(
                name="BIOS/UEFI Firmware",
                description="Non-volatile memory chip containing GPU firmware, boot code, and configuration data for initialization and operation control.",
                technical_specs={
                    "Memory Type": "SPI NOR Flash",
                    "Capacity": "16-64MB",
                    "Interface": "SPI (Serial Peripheral Interface)",
                    "Voltage": "3.3V or 1.8V",
                    "Package": "SOIC-8 or WSON-8",
                    "Write Protection": "Hardware/software",
                    "Boot Time": "<100ms"
                },
                physical_properties={
                    "Dimensions": "5x6mm or 4x4mm",
                    "Thickness": "1.0-1.5mm",
                    "Pin Count": "8 pins",
                    "Markings": "Manufacturer code",
                    "Operating Temp": "-40 to 85°C",
                    "ESD Protection": "2kV HBM"
                },
                function="Stores GPU firmware, boot sequences, power management profiles, and configuration data. Controls initialization, fan curves, and overclocking limits.",
                importance="CRITICAL - Contains essential firmware for GPU operation, determines boot behavior and safety limits",
                manufacturing_details="NOR flash fabrication, programming with GPU-specific firmware, quality testing, environmental stress screening",
                performance_impact="Firmware optimizations affect boot time by 20-50%, power profiles impact efficiency by 5-15%, overclocking limits affect performance ceiling",
                failure_modes=["Corruption from power loss", "Wear from excessive writes", "Manufacturing defects", "ESD damage", "Thermal stress"],
                maintenance_notes="Avoid power interruptions during firmware updates, monitor for corruption signs, keep firmware updated, protect from ESD"
            ),
            
            ComponentType.CLOCK_GENERATOR: ComponentInfo(
                name="Clock Generator IC",
                description="Crystal oscillator and phase-locked loop circuits generating precise timing signals for GPU core, memory, and display operations.",
                technical_specs={
                    "Crystal Frequency": "25-50MHz base",
                    "PLL Multipliers": "x20-x100",
                    "Output Frequencies": "100MHz-3GHz",
                    "Jitter": "<1ps RMS",
                    "Phase Count": "2-8 differential outputs",
                    "Voltage": "1.8V or 3.3V",
                    "Package": "QFN-24 or VFQFN-24"
                },
                physical_properties={
                    "Dimensions": "4x4mm or 5x5mm",
                    "Thickness": "0.8-1.0mm",
                    "Pin Count": "24-32 pins",
                    "Heat Dissipation": "0.5-1.0W",
                    "Crystal Size": "3.2x2.5mm",
                    "Mounting": "SMT with thermal pad"
                },
                function="Generates synchronized clock signals for GPU die, memory controllers, and display engines with ultra-low jitter for signal integrity.",
                importance="CRITICAL - Timing accuracy affects all operations, determines maximum stable frequencies and signal quality",
                manufacturing_details="Crystal growth and cutting, IC fabrication with analog circuits, frequency calibration, jitter testing",
                performance_impact="Clock accuracy affects stability by 15-25%, jitter impacts signal integrity by 10-20%, frequency range determines overclocking potential",
                failure_modes=["Crystal damage", "PLL lock failure", "Jitter degradation", "Thermal drift", "Power supply noise"],
                maintenance_notes="Monitor clock signals for stability, ensure clean power supply, avoid thermal extremes, check for frequency drift"
            ),
            
            ComponentType.THERMAL_SENSORS: ComponentInfo(
                name="Thermal Sensors",
                description="Digital temperature sensors and analog thermistors monitoring GPU die, VRAM, and VRM temperatures for thermal management.",
                technical_specs={
                    "Sensor Type": "Digital I2C/SPI or analog",
                    "Accuracy": "±1°C typical",
                    "Resolution": "0.125°C",
                    "Response Time": "1-5 seconds",
                    "Operating Range": "0-125°C",
                    "Interface": "I2C/SMBus",
                    "Package": "SOT-23 or QFN"
                },
                physical_properties={
                    "Dimensions": "2x2mm or 3x3mm",
                    "Thickness": "0.5-0.8mm",
                    "Pin Count": "3-8 pins",
                    "Placement": "Die surface, VRAM, VRM",
                    "Thermal Coupling": "Direct contact or thermal paste",
                    "ESD Rating": "1kV HBM"
                },
                function="Continuously monitor temperatures across GPU components, providing data for fan control, power limiting, and thermal throttling protection.",
                importance="CRITICAL - Prevents thermal damage, controls cooling systems, affects performance through thermal throttling",
                manufacturing_details="Semiconductor temperature sensing, calibration for accuracy, thermal coupling optimization, environmental testing",
                performance_impact="Sensor accuracy affects thermal protection by 5-10%, response time impacts cooling efficiency, placement affects temperature reading accuracy",
                failure_modes=["Calibration drift", "Contact degradation", "ESD damage", "Thermal coupling failure", "Interface communication errors"],
                maintenance_notes="Verify sensor readings against known temperatures, check thermal paste condition, monitor for drift, ensure proper contact"
            ),
            
            ComponentType.POWER_MANAGEMENT_IC: ComponentInfo(
                name="Power Management IC (PMIC)",
                description="Integrated circuit managing power sequencing, voltage monitoring, and protection circuits for safe GPU operation.",
                technical_specs={
                    "Input Voltage": "12V PCIe",
                    "Output Channels": "3-6 rails",
                    "Current Monitoring": "Per rail",
                    "Protection": "OVP/UVP/OCP/SCP",
                    "Sequencing": "Programmable delays",
                    "Interface": "I2C/SMBus",
                    "Efficiency": "90-95%"
                },
                physical_properties={
                    "Dimensions": "5x5mm or 6x6mm",
                    "Thickness": "0.8-1.0mm",
                    "Pin Count": "32-48 pins",
                    "Package": "QFN or TQFN",
                    "Heat Sink": "Exposed thermal pad",
                    "Operating Temp": "-40 to 125°C"
                },
                function="Controls power-up/power-down sequencing, monitors voltages and currents, implements protection circuits, and communicates with GPU firmware.",
                importance="CRITICAL - Ensures safe power delivery, prevents damage from power faults, coordinates with VRM for optimal efficiency",
                manufacturing_details="Mixed-signal IC fabrication, power MOSFET integration, firmware programming, comprehensive testing",
                performance_impact="Protection circuits prevent damage, sequencing affects boot reliability, monitoring enables dynamic power management",
                failure_modes=["MOSFET failure", "Interface corruption", "Calibration errors", "Thermal shutdown", "Power sequencing faults"],
                maintenance_notes="Monitor voltage rails for stability, check protection circuit operation, verify sequencing timing, update firmware as needed"
            ),
            
            ComponentType.DISPLAY_ENGINES: ComponentInfo(
                name="Display Engine Controllers",
                description="Dedicated silicon blocks or separate ICs handling HDMI, DisplayPort, and other display protocol encoding and transmission.",
                technical_specs={
                    "HDMI Version": "2.1+ with FRL",
                    "DP Version": "1.4a+ with DSC",
                    "Max Resolution": "8K@60Hz or 4K@240Hz",
                    "HDR Support": "HDR10/Dolby Vision",
                    "Bandwidth": "48Gbps HDMI, 32Gbps DP",
                    "Encoding": "H.265/AV1 hardware",
                    "Package": "Integrated or discrete QFN"
                },
                physical_properties={
                    "Die Size": "10-20mm² integrated",
                    "Power Consumption": "2-5W",
                    "Heat Generation": "Moderate",
                    "Interface": "PCIe/Display Core",
                    "Connectors": "Gold-plated HDMI/DP",
                    "Cable Support": "Active/passive"
                },
                function="Encode and transmit video signals to displays, handle multiple monitor configurations, and support advanced features like HDR and high refresh rates.",
                importance="HIGH - Enables display connectivity and advanced features, affects gaming and productivity display capabilities",
                manufacturing_details="High-speed SerDes circuits, protocol encoding logic, signal conditioning, compliance testing with display standards",
                performance_impact="Bandwidth limits maximum resolution/refresh rate, encoding efficiency affects power consumption, feature support determines compatibility",
                failure_modes=["Signal integrity issues", "Protocol compliance failures", "HDCP authentication errors", "Connector damage", "Cable compatibility issues"],
                maintenance_notes="Use certified cables, ensure proper HDMI/DP versions, monitor for signal degradation, update drivers for compatibility"
            ),
            
            ComponentType.PCI_BRIDGE: ComponentInfo(
                name="PCI Express Bridge",
                description="PCIe interface controller managing communication between GPU and host system through high-speed serial links.",
                technical_specs={
                    "PCIe Version": "4.0/5.0",
                    "Lane Count": "16 lanes (x16)",
                    "Bandwidth": "64GT/s per lane",
                    "Encoding": "128b/130b",
                    "Latency": "<1μs",
                    "Power Management": "L0s/L1 states",
                    "Error Correction": "CRC/ECC"
                },
                physical_properties={
                    "Interface": "PCIe x16 slot",
                    "Connector": "Gold-plated contacts",
                    "Retention": "Spring clips",
                    "Keying": "x16 mechanical key",
                    "Length": "89mm standard",
                    "Height": "120mm bracket"
                },
                function="Provides high-speed data transfer between GPU and CPU/memory, handles PCIe protocol, and manages power states for optimal performance.",
                importance="CRITICAL - Determines system integration and performance, affects data transfer speeds and compatibility",
                manufacturing_details="High-speed SerDes design, PCIe protocol implementation, signal integrity optimization, compliance testing",
                performance_impact="PCIe version affects bandwidth by 2-4x, lane count determines maximum throughput, latency affects responsiveness",
                failure_modes=["Signal integrity degradation", "Protocol errors", "Power state issues", "Connector damage", "BIOS compatibility problems"],
                maintenance_notes="Ensure proper PCIe slot installation, check BIOS settings, monitor for errors, use compatible motherboards"
            ),
            
            ComponentType.AUXILIARY_IC: ComponentInfo(
                name="Auxiliary Controller ICs",
                description="Collection of support ICs including fan controllers, LED drivers, USB controllers, and miscellaneous system management functions.",
                technical_specs={
                    "Fan Controller": "4-wire PWM control",
                    "LED Driver": "RGB addressable",
                    "USB Hub": "USB 3.2 Gen 2x2",
                    "Audio Codec": "HDMI audio",
                    "I/O Expanders": "GPIO expansion",
                    "Package Types": "QFN/TSSOP/SOIC"
                },
                physical_properties={
                    "Dimensions": "3x3mm to 10x10mm",
                    "Thickness": "0.5-1.5mm",
                    "Pin Count": "8-64 pins",
                    "Power Consumption": "0.1-2W each",
                    "Operating Temp": "-40 to 85°C",
                    "ESD Protection": "1-2kV HBM"
                },
                function="Control fans, LEDs, USB peripherals, audio output, and provide additional I/O capabilities for enhanced functionality and user experience.",
                importance="MEDIUM - Enhances user experience and system integration, provides additional features without affecting core performance",
                manufacturing_details="Mixed-signal IC design, firmware programming, functional testing, environmental qualification",
                performance_impact="Fan control affects cooling efficiency, LED features are cosmetic, USB/audio add connectivity options",
                failure_modes=["Firmware corruption", "Interface failures", "Thermal issues", "ESD damage", "Component aging"],
                maintenance_notes="Update firmware regularly, monitor fan operation, check LED functionality, ensure proper cooling for ICs"
            )
        }
    
    def get_component_info(self, component_type: ComponentType) -> Optional[ComponentInfo]:
        return self.component_database.get(component_type)
    
    def highlight_component(self, component_type: ComponentType) -> ComponentInfo:
        self.current_highlight = component_type
        return self.get_component_info(component_type)
    
    def clear_highlight(self):
        self.current_highlight = None
    
    def get_all_components(self) -> List[ComponentType]:
        return list(ComponentType)
    
    def format_component_details(self, component_info: ComponentInfo) -> str:
        return f"""
        <div style="color: #e0e0e0; line-height: 1.6;">
            <h3 style="color: #4fc3f7; margin-bottom: 12px;">{component_info.name}</h3>
            
            <div style="margin-bottom: 15px;">
                <strong style="color: #81c784;">Description:</strong><br>
                {component_info.description}
            </div>
            
            <div style="margin-bottom: 15px;">
                <strong style="color: #81c784;">Function:</strong><br>
                {component_info.function}
            </div>
            
            <div style="margin-bottom: 15px;">
                <strong style="color: #81c784;">Importance:</strong><br>
                <span style="color: {'#ff9800' if 'CRITICAL' in component_info.importance else '#ffc107' if 'HIGH' in component_info.importance else '#4caf50'}">
                    {component_info.importance}
                </span>
            </div>
            
            <div style="margin-bottom: 15px;">
                <strong style="color: #81c784;">Technical Specifications:</strong><br>
                {self._format_spec_table(component_info.technical_specs)}
            </div>
            
            <div style="margin-bottom: 15px;">
                <strong style="color: #81c784;">Physical Properties:</strong><br>
                {self._format_spec_table(component_info.physical_properties)}
            </div>
            
            <div style="margin-bottom: 15px;">
                <strong style="color: #81c784;">Manufacturing:</strong><br>
                {component_info.manufacturing_details}
            </div>
            
            <div style="margin-bottom: 15px;">
                <strong style="color: #81c784;">Performance Impact:</strong><br>
                {component_info.performance_impact}
            </div>
            
            <div style="margin-bottom: 15px;">
                <strong style="color: #81c784;">Common Failure Modes:</strong><br>
                {', '.join(component_info.failure_modes)}
            </div>
            
            <div style="margin-bottom: 15px;">
                <strong style="color: #81c784;">Maintenance Notes:</strong><br>
                {component_info.maintenance_notes}
            </div>
        </div>
        """
    
    def _format_spec_table(self, specs: Dict[str, str]) -> str:
        rows = []
        for key, value in specs.items():
            rows.append(f"<tr><td style='color: #b0bec5; padding: 2px 8px;'>{key}:</td><td style='color: #e0e0e0; padding: 2px 8px;'>{value}</td></tr>")
        return f"<table style='border-collapse: collapse;'>{''.join(rows)}</table>"