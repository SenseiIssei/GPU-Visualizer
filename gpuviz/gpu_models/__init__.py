"""
GPU Models Registry

Author: 𝙅𝙖𝙠𝙤𝙗 / 𝙎𝙚𝙣𝙨𝙚𝙞 𝙄𝙨𝙨𝙚𝙞

Overview:
- Registry and factory for available GPU 3D models
"""

from .baseGpuModel import BaseGPUModel
from .rtx4080Model import RTX4080Model
from .rtx4090Model import RTX4090Model
from .rtx4070Model import RTX4070Model
from .rtx4070TiModel import RTX4070TiModel
from .rtx4060TiModel import RTX4060TiModel
from .rtx4060Model import RTX4060Model
from .rx7900XtxModel import RX7900XTXModel
from .rx7900XtModel import RX7900XTModel
from .rx7900GreModel import RX7900GREModel
from .rx7800XtModel import RX7800XTModel
from .rx7700XtModel import RX7700XTModel

GPU_MODELS = {
    "RTX 4090 (Ada – AD102-300)": RTX4090Model,
    "RTX 4080 (Ada – AD103-300)": RTX4080Model,
    "RTX 4070 Ti (Ada – AD104-400)": RTX4070TiModel,
    "RTX 4070 (Ada – AD104-250)": RTX4070Model,
    "RTX 4060 Ti (Ada – AD106-350)": RTX4060TiModel,
    "RTX 4060 (Ada – AD107-400)": RTX4060Model,
    "RX 7900 XTX (RDNA3 – Navi 31)": RX7900XTXModel,
    "RX 7900 XT (RDNA3 – Navi 32)": RX7900XTModel,
    "RX 7900 GRE (RDNA3 – Navi 33)": RX7900GREModel,
    "RX 7800 XT (RDNA3 – Navi 32)": RX7800XTModel,
    "RX 7700 XT (RDNA3 – Navi 32)": RX7700XTModel,
}

def get_gpu_model(model_name: str, view3d_instance) -> BaseGPUModel:
    import gc
    gc.collect()  # Force cleanup before creating new model
    
    normalized_name = model_name.replace('–', '-').replace('—', '-')
    
    gpu_model_mapping = {
        "RTX 4090 (Ada – AD102-300)": RTX4090Model,
        "RTX 4080 (Ada – AD103-300)": RTX4080Model,
        "RTX 4070 Ti (Ada – AD104-400)": RTX4070TiModel,
        "RTX 4070 (Ada – AD104-250)": RTX4070Model,
        "RTX 4060 Ti (Ada – AD106-350)": RTX4060TiModel,
        "RTX 4060 (Ada – AD107-400)": RTX4060Model,
        "RX 7900 XTX (RDNA3 – Navi 31)": RX7900XTXModel,
        "RX 7900 XT (RDNA3 – Navi 32)": RX7900XTModel,
        "RX 7900 GRE (RDNA3 – Navi 33)": RX7900GREModel,
        "RX 7800 XT (RDNA3 – Navi 32)": RX7800XTModel,
        "RX 7700 XT (RDNA3 – Navi 32)": RX7700XTModel,
        "RTX 4090": RTX4090Model,
        "RTX 4080": RTX4080Model,
        "RTX 4070 Ti": RTX4070TiModel,
        "RTX 4070": RTX4070Model,
        "RTX 4060 Ti": RTX4060TiModel,
        "RTX 4060": RTX4060Model,
        "RX 7900 XTX": RX7900XTXModel,
        "RX 7900 XT": RX7900XTModel,
        "RX 7900 GRE": RX7900GREModel,
        "RX 7800 XT": RX7800XTModel,
        "RX 7700 XT": RX7700XTModel,
    }
    default_model = "RTX 4080 (Ada - AD103-300)"
    
    if normalized_name in gpu_model_mapping:
        model_class = gpu_model_mapping[normalized_name]
    elif model_name in gpu_model_mapping:
        model_class = gpu_model_mapping[model_name]
    else:
        model_class = gpu_model_mapping[default_model]
    
    try:
        # Create the model instance
        model_instance = model_class(view3d_instance)
        return model_instance
    except Exception as e:
        # If model creation fails, try to force cleanup and retry once
        print(f"GPU model creation failed, attempting cleanup: {e}")
        gc.collect()
        try:
            model_instance = model_class(view3d_instance)
            return model_instance
        except Exception as e2:
            print(f"GPU model creation failed again: {e2}")
            # Return a basic fallback model
            return model_class(view3d_instance)