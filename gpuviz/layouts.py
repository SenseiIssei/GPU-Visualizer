"""
GPU Layout Presets and JSON IO

Author: 𝙅𝙖𝙠𝙤𝙗 / 𝙎𝙚𝙣𝙨𝙚𝙞 𝙄𝙨𝙨𝙚𝙞

Overview:
- Preset GPULayout definitions and JSON import/export helpers
"""
from typing import Dict, List
from .models import GPULayout, GPC, SM, Core

PRESETS: Dict[str, GPULayout] = {
    "RTX 4090 (Ada – AD102-300)": GPULayout.from_spec("RTX 4090", gpc_count=7, sms_per_gpc=9, cores_per_sm=128),
    "RTX 4080 (Ada – AD103-300)": GPULayout.from_spec("RTX 4080", gpc_count=5, sms_per_gpc=7, cores_per_sm=128),
    "RTX 4070 Ti (Ada – AD104-400)": GPULayout.from_spec("RTX 4070 Ti", gpc_count=6, sms_per_gpc=8, cores_per_sm=128),
    "RTX 4070 (Ada – AD104-250)": GPULayout.from_spec("RTX 4070", gpc_count=5, sms_per_gpc=7, cores_per_sm=128),
    "RTX 4060 Ti (Ada – AD106-350)": GPULayout.from_spec("RTX 4060 Ti", gpc_count=4, sms_per_gpc=6, cores_per_sm=128),
    "RTX 4060 (Ada – AD107-400)": GPULayout.from_spec("RTX 4060", gpc_count=3, sms_per_gpc=6, cores_per_sm=128),
    "RX 7900 XTX (RDNA3 – Navi 31)": GPULayout.from_spec("RX 7900 XTX", gpc_count=12, sms_per_gpc=2, cores_per_sm=64),
    "RX 7900 XT (RDNA3 – Navi 31)": GPULayout.from_spec("RX 7900 XT", gpc_count=10, sms_per_gpc=2, cores_per_sm=64),
    "RX 7800 XT (RDNA3 – Navi 32)": GPULayout.from_spec("RX 7800 XT", gpc_count=8, sms_per_gpc=2, cores_per_sm=64),
    "RX 7700 XT (RDNA3 – Navi 33)": GPULayout.from_spec("RX 7700 XT", gpc_count=6, sms_per_gpc=2, cores_per_sm=64),
    "NVIDIA H100 SXM5 - Ultra Detailed (Interactive)": GPULayout.from_spec("H100 SXM5", gpc_count=8, sms_per_gpc=18, cores_per_sm=128),
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