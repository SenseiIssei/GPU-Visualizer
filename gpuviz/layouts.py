"""
GPU Layout Presets and JSON IO

Author: 𝙅𝙖𝙠𝙤𝙗 / 𝙎𝙚𝙣𝙨𝙚𝙞 𝙄𝙨𝙨𝙚𝙞

Overview:
- Preset GPULayout definitions and JSON import/export helpers
"""
from typing import Dict, List
from .models import GPULayout, GPC, SM, Core

PRESETS: Dict[str, GPULayout] = {
    "RTX 4090 (Ada – illustrative)": GPULayout.from_spec("RTX 4090", gpc_count=8, sms_per_gpc=10, cores_per_sm=128),
    "RTX 4080 (Ada – illustrative)": GPULayout.from_spec("RTX 4080", gpc_count=7, sms_per_gpc=9, cores_per_sm=128),
    "RX 7900 XTX (RDNA3 – illustrative)": GPULayout.from_spec("RX 7900 XTX", gpc_count=12, sms_per_gpc=2, cores_per_sm=64),
    "Compact Demo": GPULayout.from_spec("Compact", gpc_count=3, sms_per_gpc=4, cores_per_sm=32),
}

def dump_layout_to_json(layout: GPULayout) -> Dict:
    return {
        "name": layout.name,
        "cores_per_sm": layout.cores_per_sm,
        "gpcs": [
            {
                "id": g.id,
                "sms": [
                    {"id": sm.id, "cores": [c.id for c in sm.cores]}
                    for sm in g.sms
                ]
            } for g in layout.gpcs
        ]
    }

def load_layout_from_json(data: Dict) -> GPULayout:
    name = data.get("name", "Custom")
    cores_per_sm = int(data.get("cores_per_sm", 64))
    gpcs: List[GPC] = []
    for g in data.get("gpcs", []):
        sms: List[SM] = []
        for smd in g.get("sms", []):
            cores = [Core(id=int(cid)) for cid in smd.get("cores", [])]
            sms.append(SM(id=int(smd.get("id", 0)), cores=cores))
        gpcs.append(GPC(id=int(g.get("id", 0)), sms=sms))
    return GPULayout(name=name, gpcs=gpcs, cores_per_sm=cores_per_sm)