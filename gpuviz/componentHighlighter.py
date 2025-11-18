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