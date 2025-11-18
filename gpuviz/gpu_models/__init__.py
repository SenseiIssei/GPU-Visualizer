"""
GPU Models Registry

Author: 𝙅𝙖𝙠𝙤𝙗 / 𝙎𝙚𝙣𝙨𝙚𝙞 𝙄𝙨𝙨𝙚𝙞

Overview:
- Registry and factory for available GPU 3D models
"""

from .baseGpuModel import BaseGPUModel
from .rtx4080Model import RTX4080Model
from .rtx4090Model import RTX4090Model
from .rx7900XtxModel import RX7900XTXModel

GPU_MODELS = {
    "RTX 4080 (Ada – illustrative)": RTX4080Model,
    "RTX 4090 (Ada – illustrative)": RTX4090Model,
    "RX 7900 XTX (RDNA3 – illustrative)": RX7900XTXModel,
}

def get_gpu_model(model_name: str, view3d_instance) -> BaseGPUModel:
    normalized_name = model_name.replace('–', '-').replace('—', '-')
    
    gpu_model_mapping = {
        "RTX 4090 (Ada – illustrative)": RTX4090Model,
        "RTX 4080 (Ada – illustrative)": RTX4080Model,
        "RX 7900 XTX (RDNA3 – illustrative)": RX7900XTXModel,
        "RTX 4090": RTX4090Model,
        "RTX 4080": RTX4080Model,
        "RX 7900 XTX": RX7900XTXModel,
    }
    default_model = "RTX 4080 (Ada - illustrative)"
    
    if normalized_name in gpu_model_mapping:
        model_class = gpu_model_mapping[normalized_name]
    elif model_name in gpu_model_mapping:
        model_class = gpu_model_mapping[model_name]
    else:
        model_class = gpu_model_mapping[default_model]
    
    return model_class(view3d_instance)