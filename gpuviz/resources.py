"""
GPU Visualization Resources (Colormaps)

Author: 𝙅𝙖𝙠𝙤𝙗 / 𝙎𝙚𝙣𝙨𝙚𝙞 𝙄𝙨𝙨𝙚𝙞

Overview:
- Colormap utilities for mapping metrics to RGB
"""
from typing import Tuple
def clamp01(x: float) -> float: return max(0.0, min(1.0, x))

class ColorMap:
    @staticmethod
    def turbo(t: float) -> Tuple[float, float, float]:
        t = clamp01(t)
        r = 34.61 + t*(1172.33 + t*(-10793.56 + t*(33300.12 + t*(-38394.49 + t*15054.31))))
        g = 23.31 + t*(557.33 + t*(1225.33 + t*(-3574.96 + t*(3083.81 - t*852.12))))
        b = 27.2 + t*(3211.1 + t*(-15327.97 + t*(27814.0 + t*(-22569.18 + t*6838.66))))
        return (clamp01(r/255.0), clamp01(g/255.0), clamp01(b/255.0))
    @staticmethod
    def viridis(t: float) -> Tuple[float, float, float]:
        anchors=[(0.0,(68/255,1/255,84/255)),(0.25,(59/255,82/255,139/255)),(0.5,(33/255,145/255,140/255)),(0.75,(94/255,201/255,97/255)),(1.0,(253/255,231/255,37/255))]
        t=clamp01(t)
        for i in range(len(anchors)-1):
            a_t,a_c=anchors[i]; b_t,b_c=anchors[i+1]
            if a_t<=t<=b_t:
                k=(t-a_t)/(b_t-a_t+1e-9)
                return (a_c[0]+(b_c[0]-a_c[0])*k, a_c[1]+(b_c[1]-a_c[1])*k, a_c[2]+(b_c[2]-a_c[2])*k)
        return anchors[-1][1]
    @staticmethod
    def gray(t: float) -> Tuple[float, float, float]:
        v=clamp01(t); return (v,v,v)
    @staticmethod
    def plasma(t: float)->Tuple[float,float,float]:
        t=clamp01(t); return (clamp01(2.0*t), clamp01(2.0*(1.0-abs(t-0.5))), clamp01(2.0*(1.0-t)))
    @staticmethod
    def inferno(t: float)->Tuple[float,float,float]:
        t=clamp01(t); return (clamp01(0.8*t+0.2), clamp01(t*0.4), clamp01(0.1+0.9*(1.0-t)))

COLORMAPS = {
    "Turbo": ColorMap.turbo,
    "Viridis": ColorMap.viridis,
    "Gray":   ColorMap.gray,
    "Plasma": ColorMap.plasma,
    "Inferno": ColorMap.inferno,
}