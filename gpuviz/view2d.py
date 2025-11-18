"""
GPU 2D Layout Visualization

Author: 𝙅𝙖𝙠𝙤𝙗 / 𝙎𝙚𝙣𝙨𝙚𝙞 𝙄𝙨𝙨𝙚𝙞

Overview:
- High-performance 2D view rendering GPU hierarchy (GPC → SM → Core)
- Real-time coloring from simulation metrics with configurable colormaps
- Optimized scene rebuilds, zoom/pan, and minimal viewport updates
"""
from PySide6 import QtCore, QtGui, QtWidgets
import math
from typing import List, Optional, Tuple
from .models import GPULayout, GPC, SM, Core
from .resources import COLORMAPS

class CoreItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, core: Core, rect: QtCore.QRectF, get_color, glow: bool):
        super().__init__(rect)
        self.core = core
        self.get_color = get_color
        self.setAcceptHoverEvents(True)
        self.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        self.setCacheMode(QtWidgets.QGraphicsItem.DeviceCoordinateCache)
        if glow:
            eff = QtWidgets.QGraphicsDropShadowEffect()
            eff.setBlurRadius(6); eff.setOffset(0, 0); eff.setColor(QtGui.QColor(255,255,255,40))
            self.setGraphicsEffect(eff)

    def hoverEnterEvent(self, event):
        QtWidgets.QToolTip.showText(
            event.screenPos(),
            f"Core #{self.core.id}\nUtil: {self.core.activity:.2f}\nTemp: {self.core.temperature*80+25:.0f}°C"
        )
        super().hoverEnterEvent(event)

    def paint(self, painter: QtGui.QPainter, option, widget=None):
        r, g, b = self.get_color(self.core)
        painter.fillRect(self.rect(), QtGui.QColor(int(r*255), int(g*255), int(b*255)))


class SMItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, sm: SM, rect: QtCore.QRectF, label: bool):
        super().__init__(rect)
        self.sm = sm
        self.setCacheMode(QtWidgets.QGraphicsItem.DeviceCoordinateCache)
        pen = QtGui.QPen(QtGui.QColor(255, 255, 255, 60)); pen.setWidthF(0)
        self.setPen(pen)
        self.text = None
        if label:
            self.text = QtWidgets.QGraphicsSimpleTextItem(f"SM {sm.id}", self)
            self.text.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255, 150)))
            self.text.setPos(rect.x() + 2, rect.y() + 2)
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        util = sum(c.activity for c in self.sm.cores) / max(1, len(self.sm.cores))
        QtWidgets.QToolTip.showText(event.screenPos(), f"SM #{self.sm.id}\nAvg Util: {util:.2f}")
        super().hoverEnterEvent(event)


class GPCItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, gpc: GPC, rect: QtCore.QRectF, label: bool):
        super().__init__(rect)
        self.gpc = gpc
        self.setCacheMode(QtWidgets.QGraphicsItem.DeviceCoordinateCache)
        pen = QtGui.QPen(QtGui.QColor(255, 255, 255, 100)); pen.setWidthF(0)
        self.setPen(pen)
        if label:
            text = QtWidgets.QGraphicsSimpleTextItem(f"GPC {gpc.id}", self)
            text.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255, 200)))
            text.setPos(rect.x() + 4, rect.y() + 4)


class GPU2DView(QtWidgets.QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setRenderHints(
            QtGui.QPainter.Antialiasing |
            QtGui.QPainter.TextAntialiasing |
            QtGui.QPainter.SmoothPixmapTransform
        )
        self.setBackgroundBrush(QtGui.QColor(16, 16, 22))
        self.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)
        self.setOptimizationFlag(QtWidgets.QGraphicsView.DontSavePainterState, True)
        self.setOptimizationFlag(QtWidgets.QGraphicsView.DontAdjustForAntialiasing, True)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.MinimalViewportUpdate)

        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.scene_ = QtWidgets.QGraphicsScene(self); self.setScene(self.scene_)
        self._layout: Optional[GPULayout] = None
        self._color_map = COLORMAPS["Turbo"]
        self.coloring_mode = "Utilization"
        self.show_labels = True
        self.show_grid = True
        self.view_mode = "Logical"
        self.core_items: List[CoreItem] = []; self.sm_items: List[SMItem] = []; self.gpc_items: List[GPCItem] = []

        self._frame_counter = 0
        self._frame_skip = 1
        self._glow_enabled = False

    def wheelEvent(self, event: QtGui.QWheelEvent):
        delta = event.angleDelta().y()
        if delta == 0: return
        factor = 1.1 if delta > 0 else (1/1.1)
        self.scale(factor, factor)

    def keyPressEvent(self, e: QtGui.QKeyEvent):
        if e.key() == QtCore.Qt.Key_R:
            self.resetTransform()
            self.centerOn(0, 0)
        super().keyPressEvent(e)

    def reset_view(self):
        self.resetTransform()
        self.centerOn(0, 0)

    def set_layout(self, layout: GPULayout):
        self._layout = layout
        self.rebuild_scene(hard=True)

    def set_colormap(self, name: str):
        self._color_map = COLORMAPS.get(name, COLORMAPS["Turbo"])
        self.update_colors()

    def set_coloring_mode(self, mode: str):
        self.coloring_mode = mode
        self.update_colors()

    def set_view_mode(self, mode: str):
        self.view_mode = mode
        self.rebuild_scene()

    def metric_for_core(self, c: Core) -> float:
        if self.coloring_mode == "Utilization":   return c.activity
        if self.coloring_mode == "Temperature":   return c.temperature
        if self.coloring_mode == "Memory pressure": return c.mem_pressure
        return c.activity

    def color_for_core(self, c: Core) -> Tuple[float, float, float]:
        return self._color_map(self.metric_for_core(c))

    def update_colors(self):
        self._frame_counter += 1
        if self._frame_counter % self._frame_skip != 0:
            return
        for ci in self.core_items:
            ci.update()
        self.viewport().update()

    def rebuild_scene(self, hard: bool = False):
        if hard:
            new_scene = QtWidgets.QGraphicsScene(self)
            self.setScene(new_scene); self.scene_ = new_scene
            self.core_items.clear(); self.sm_items.clear(); self.gpc_items.clear()
            self.reset_view()
        else:
            self.scene_.clear(); self.core_items.clear(); self.sm_items.clear(); self.gpc_items.clear()

        if not self._layout: return

        total_cores = sum(len(sm.cores) for g in self._layout.gpcs for sm in g.sms)
        self._frame_skip = 1 if total_cores <= 6000 else 2 if total_cores <= 12000 else 3

        margin = 20; w, h = 1400, 900
        self.scene_.setSceneRect(0, 0, w, h)
        available = QtCore.QRectF(margin, margin, w - 2*margin, h - 2*margin)

        if self.view_mode == "Logical":
            self._build_logical(available)
        elif self.view_mode == "SM Focus":
            self._build_sm_focus(available)
        else:
            self._build_die_view(available)

    def _build_logical(self, rect: QtCore.QRectF):
        if not self._layout: return
        gpc_count = len(self._layout.gpcs)
        cols = math.ceil(math.sqrt(gpc_count)); rows = math.ceil(gpc_count / cols)
        gpc_w = rect.width() / cols; gpc_h = rect.height() / rows
        idx = 0
        for r in range(rows):
            for c in range(cols):
                if idx >= gpc_count: break
                gpc = self._layout.gpcs[idx]
                g_rect = QtCore.QRectF(rect.x() + c*gpc_w + 6, rect.y() + r*gpc_h + 6, gpc_w - 12, gpc_h - 12)
                g_item = GPCItem(gpc, g_rect, label=self.show_labels)
                self.scene_.addItem(g_item)

                sm_count = len(gpc.sms)
                sm_cols = math.ceil(math.sqrt(sm_count)); sm_rows = math.ceil(sm_count / sm_cols)
                sm_w = g_rect.width() / sm_cols; sm_h = g_rect.height() / sm_rows
                sm_idx = 0
                for rr in range(sm_rows):
                    for cc in range(sm_cols):
                        if sm_idx >= sm_count: break
                        sm = gpc.sms[sm_idx]
                        s_rect = QtCore.QRectF(g_rect.x() + cc*sm_w + 4, g_rect.y() + rr*sm_h + 4, sm_w - 8, sm_h - 8)
                        s_item = SMItem(sm, s_rect, label=self.show_labels)
                        self.scene_.addItem(s_item); self.sm_items.append(s_item)

                        core_cols = max(4, int(math.sqrt(len(sm.cores)))); core_rows = math.ceil(len(sm.cores) / core_cols)
                        cw = s_rect.width() / core_cols; ch = s_rect.height() / core_rows
                        for k in range(len(sm.cores)):
                            rr2 = k // core_cols; cc2 = k % core_cols
                            cell = QtCore.QRectF(s_rect.x() + cc2*cw + 1, s_rect.y() + rr2*ch + 1, cw - 2, ch - 2)
                            ci = CoreItem(sm.cores[k], cell, self.color_for_core, glow=self._glow_enabled)
                            self.scene_.addItem(ci); self.core_items.append(ci)
                        sm_idx += 1
                self.gpc_items.append(g_item); idx += 1

    def _build_sm_focus(self, rect: QtCore.QRectF):
        self._build_die_view(rect)

    def _build_die_view(self, rect: QtCore.QRectF):
        if not self._layout: return
        all_sms: List[SM] = [sm for g in self._layout.gpcs for sm in g.sms]
        sm_count = len(all_sms)
        cols = math.ceil(math.sqrt(sm_count)); rows = math.ceil(sm_count / cols)
        sm_w = rect.width() / cols; sm_h = rect.height() / rows
        for i, sm in enumerate(all_sms):
            r = i // cols; c = i % cols
            s_rect = QtCore.QRectF(rect.x() + c*sm_w + 6, rect.y() + r*sm_h + 6, sm_w - 12, sm_h - 12)
            s_item = SMItem(sm, s_rect, label=False)
            if self.show_grid:
                pen = QtGui.QPen(QtGui.QColor(255, 255, 255, 40)); pen.setWidthF(0); s_item.setPen(pen)
            else:
                s_item.setPen(QtGui.QPen(QtCore.Qt.NoPen))
            self.scene_.addItem(s_item); self.sm_items.append(s_item)

            core_cols = max(4, int(math.sqrt(len(sm.cores)))); core_rows = math.ceil(len(sm.cores) / core_cols)
            cw = s_rect.width() / core_cols; ch = s_rect.height() / core_rows
            for k, core in enumerate(sm.cores):
                rr2 = k // core_cols; cc2 = k % core_cols
                cell = QtCore.QRectF(s_rect.x() + cc2*cw + 1, s_rect.y() + rr2*ch + 1, cw - 2, ch - 2)
                ci = CoreItem(core, cell, self.color_for_core, glow=self._glow_enabled)
                self.scene_.addItem(ci); self.core_items.append(ci)