"""
GPU Logical Data Models

Author: 𝙅𝙖𝙠𝙤𝙗 / 𝙎𝙚𝙣𝙨𝙚𝙞 𝙄𝙨𝙨𝙚𝙞

Overview:
- Minimal dataclasses describing Core, SM, GPC, and GPULayout
- Construct layouts via GPULayout.from_spec
"""
from dataclasses import dataclass, field
from typing import List

@dataclass
class Core:
    id: int
    activity: float = 0.0
    temperature: float = 0.3
    mem_pressure: float = 0.2

@dataclass
class SM:
    id: int
    cores: List[Core] = field(default_factory=list)
    activity: float = 0.0

@dataclass
class GPC:
    id: int
    sms: List[SM] = field(default_factory=list)

@dataclass
class GPULayout:
    name: str
    gpcs: List[GPC] = field(default_factory=list)
    cores_per_sm: int = 64

    @staticmethod
    def from_spec(name: str, gpc_count: int, sms_per_gpc: int, cores_per_sm: int) -> "GPULayout":
        gpcs: List[GPC] = []
        core_id = 0
        sm_id = 0
        for g in range(gpc_count):
            sms: List[SM] = []
            for _ in range(sms_per_gpc):
                cores = [Core(id=core_id + i) for i in range(cores_per_sm)]
                core_id += cores_per_sm
                sms.append(SM(id=sm_id, cores=cores))
                sm_id += 1
            gpcs.append(GPC(id=g, sms=sms))
        return GPULayout(name=name, gpcs=gpcs, cores_per_sm=cores_per_sm)