"""
GPU Activity and DVFS Simulation

Author: 𝙅𝙖𝙠𝙤𝙗 / 𝙎𝙚𝙣𝙨𝙚𝙞 𝙄𝙨𝙨𝙚𝙞

Overview:
- Real-time GPU activity synthesis across GPC → SM → Core hierarchy
- DVFS model coupling voltage, frequency, power, and temperature
- Periodic Qt signal emissions for 2D/3D views at configurable rates

Key Components:
- DVFSModel: Computes frequency, power, and temperature evolution
- Simulation: Drives activity fields and integrates DVFS state
"""
import math, random, time
from PySide6 import QtCore
from .models import GPULayout

def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))

class DVFSModel:
    def __init__(self):
        self.C_eff = 220.0
        self.ambient = 30.0
        self.tau = 5.0
        self.T = 40.0

    def step(self, dt: float, volts: float, util01: float):
        v = max(0.6, min(1.3, volts))
        f_base = 1.2 + 2.2 * ((v - 0.6) / 0.7)**0.8
        f = f_base * (0.55 + 0.45 * util01)
        power = self.C_eff * (v**2) * f * util01 * 0.001
        target = self.ambient + 0.7 * power
        self.T += (target - self.T) * (dt / max(0.1, self.tau))
        if self.T > 80:
            f *= max(0.5, 1.0 - (self.T - 80) * 0.01)
        return f, power, self.T

class Simulation(QtCore.QObject):
    updated = QtCore.Signal()

    def __init__(self, layout: GPULayout):
        super().__init__()
        self.layout = layout
        self.running = False
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.step)
        self.speed_ms = 100
        self.phase = 0.0
        self.global_util = 0.7
        self.power_volts = 1.05
        self.dvfs = DVFSModel()
        self._last_activity = None
        self._last_wall = time.time()

    def set_speed_ms(self, ms: int):
        self.speed_ms = max(16, int(ms))
        if self.running:
            self.timer.start(self.speed_ms)

    def set_global_util(self, pct: int):
        self.global_util = clamp01(pct / 100.0)

    def set_power_mv(self, mv: int):
        self.power_volts = max(0.6, min(1.3, mv / 1000.0))

    def start(self):
        if not self.running:
            self.running = True
            self._last_wall = time.time()
            self.timer.start(self.speed_ms)

    def stop(self):
        self.running = False
        self.timer.stop()

    def step(self):
        now = time.time()
        dt = now - self._last_wall
        self._last_wall = now
        util = self.global_util
        volts = self.power_volts
        f_ghz, watts, tempC = self.dvfs.step(max(0.001, dt), volts, util)

        self.phase += 0.06
        for g in self.layout.gpcs:
            for sm in g.sms:
                base = 0.15 + 0.85 * util
                wave = 0.25 * math.sin(self.phase + sm.id * 0.19)
                thermal_drag = max(0.6, 1.0 - max(0.0, tempC - 70) * 0.01)
                sm.activity = clamp01((base + wave) * thermal_drag + random.uniform(-0.05, 0.05))
                for i, c in enumerate(sm.cores):
                    jitter = 0.18 * math.sin(self.phase * 1.7 + i * 0.13)
                    c.activity = clamp01(0.7 * sm.activity + 0.3 * (base + jitter) + random.uniform(-0.04, 0.04))
                    c.temperature = clamp01((tempC - 25) / 80.0)
                    c.mem_pressure = clamp01(0.2 + 0.8 * abs(math.sin(self.phase * 0.6 + i * 0.07)))
        self.updated.emit()