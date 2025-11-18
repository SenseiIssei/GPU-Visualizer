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
from typing import Optional

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

    def __init__(self, layout: GPULayout, logger: Optional[object] = None):
        super().__init__()
        self.layout = layout
        self.logger = logger
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
        self._step_count = 0
        self._start_time = time.time()
        
        if self.logger:
            total_cores = sum(len(sm.cores) for g in layout.gpcs for sm in g.sms)
            self.logger.log_simulation_event(f"Simulation initialized with {len(layout.gpcs)} GPCs, {len([sm for g in layout.gpcs for sm in g.sms])} SMs, {total_cores} cores")

    def set_speed_ms(self, ms: int):
        old_speed = self.speed_ms
        self.speed_ms = max(16, int(ms))
        if self.running:
            self.timer.start(self.speed_ms)
        if self.logger:
            self.logger.log(f"Simulation speed changed from {old_speed}ms to {self.speed_ms}ms", "INFO")

    def set_global_util(self, pct: int):
        old_util = self.global_util * 100
        self.global_util = clamp01(pct / 100.0)
        if self.logger:
            self.logger.log(f"Global utilization changed from {old_util:.1f}% to {pct:.1f}%", "INFO")

    def set_power_mv(self, mv: int):
        old_volts = self.power_volts
        self.power_volts = max(0.6, min(1.3, mv / 1000.0))
        if self.logger:
            self.logger.log(f"Power voltage changed from {old_volts:.3f}V to {self.power_volts:.3f}V", "INFO")

    def start(self):
        if not self.running:
            self.running = True
            self._last_wall = time.time()
            self._start_time = time.time()
            self._step_count = 0
            self.timer.start(self.speed_ms)
            if self.logger:
                self.logger.log_simulation_event("Simulation started")

    def stop(self):
        if self.running:
            self.running = False
            self.timer.stop()
            runtime = time.time() - self._start_time
            if self.logger:
                self.logger.log_simulation_event(f"Simulation stopped after {runtime:.1f}s ({self._step_count} steps)")

    def step(self):
        start_time = time.time()
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
        
        self._step_count += 1
        step_duration = (time.time() - start_time) * 1000
        
        if self.logger and self._step_count % 100 == 0:
            avg_activity = sum(sm.activity for g in self.layout.gpcs for sm in g.sms) / max(1, len([sm for g in self.layout.gpcs for sm in g.sms]))
            self.logger.log_performance("Simulation step", step_duration)
            self.logger.log(f"Avg SM activity: {avg_activity:.2f}, Temp: {tempC:.1f}°C, Power: {watts:.1f}W, Freq: {f_ghz:.2f}GHz", "PERFORMANCE")
        
        self.updated.emit()