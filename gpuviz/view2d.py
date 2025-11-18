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
from typing import List, Optional, Tuple, Dict
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

    def reinitialize(self, core: Core, rect: QtCore.QRectF, get_color, glow: bool):
        """Reinitialize item with new data when reused from pool"""
        self.setRect(rect)
        self.core = core
        self.get_color = get_color
        if glow and not self.graphicsEffect():
            eff = QtWidgets.QGraphicsDropShadowEffect()
            eff.setBlurRadius(6); eff.setOffset(0, 0); eff.setColor(QtGui.QColor(255,255,255,40))
            self.setGraphicsEffect(eff)
        elif not glow and self.graphicsEffect():
            self.setGraphicsEffect(None)
        self.setVisible(True)

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

    def reinitialize(self, sm: SM, rect: QtCore.QRectF, label: bool):
        """Reinitialize item with new data when reused from pool"""
        self.setRect(rect)
        self.sm = sm
        if self.text:
            self.text.setText(f"SM {sm.id}")
            self.text.setVisible(label)
        elif label:
            self.text = QtWidgets.QGraphicsSimpleTextItem(f"SM {sm.id}", self)
            self.text.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255, 150)))
            self.text.setPos(rect.x() + 2, rect.y() + 2)
        self.setVisible(True)

    def hoverEnterEvent(self, event):
        util = sum(c.activity for c in self.sm.cores) / max(1, len(self.sm.cores))
        QtWidgets.QToolTip.showText(event.screenPos(), f"SM #{self.sm.id}\nAvg Util: {util:.2f}")
        super().hoverEnterEvent(event)


class InteractiveGPUComponent(QtWidgets.QGraphicsRectItem):
    """Interactive component for ultra-detailed GPU model with hover and click animations."""

    def __init__(self, component_id: str, component_data: Dict, gpu_model):
        super().__init__()
        self.component_id = component_id
        self.component_data = component_data
        self.gpu_model = gpu_model
        self.is_hovered = False
        self.animation_timer = QtCore.QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_frame = 0

        # Set up the item
        self.setAcceptHoverEvents(True)
        self.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        self.setCacheMode(QtWidgets.QGraphicsItem.DeviceCoordinateCache)

        # Set initial position and size
        pos = component_data['position']
        size = component_data['size']
        self.setRect(pos[0] - size[0]/2, pos[1] - size[1]/2, size[0], size[1])

        # Set initial color
        color = component_data['color']
        self.base_color = QtGui.QColor(int(color[0]*255), int(color[1]*255), int(color[2]*255), int(color[3]*255))
        self.hover_color = QtGui.QColor(
            int(component_data['hover_color'][0]*255),
            int(component_data['hover_color'][1]*255),
            int(component_data['hover_color'][2]*255),
            int(component_data['hover_color'][3]*255)
        )
        self.current_color = self.base_color

        # Add glow effect for hover
        self.glow_effect = QtWidgets.QGraphicsDropShadowEffect()
        self.glow_effect.setBlurRadius(0)
        self.glow_effect.setOffset(0, 0)
        self.glow_effect.setColor(QtGui.QColor(255, 255, 255, 0))
        self.setGraphicsEffect(self.glow_effect)

    def hoverEnterEvent(self, event):
        """Handle mouse hover enter."""
        self.is_hovered = True
        self.animation_timer.start(50)  # 20 FPS animation
        self.gpu_model.handle_hover_event(self.component_id)

        # Show tooltip
        QtWidgets.QToolTip.showText(
            event.screenPos(),
            f"{self.component_data['name']}\n{self.component_data['description']}"
        )
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        """Handle mouse hover leave."""
        self.is_hovered = False
        self.animation_timer.stop()
        self.animation_frame = 0
        self.update_visual()
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        """Handle mouse click."""
        if event.button() == QtCore.Qt.LeftButton:
            self.gpu_model.handle_click_event(self.component_id)
            # Show workflow animation dialog
            from .workflow_animation_dialog import WorkflowAnimationDialog
            dialog = WorkflowAnimationDialog(self.component_id, self.component_data, self.scene().views()[0].window())
            dialog.show()
        super().mousePressEvent(event)

    def update_animation(self):
        """Update animation frame."""
        self.animation_frame += 1
        self.update_visual()

    def update_visual(self):
        """Update the visual appearance based on hover state."""
        if self.is_hovered:
            # Pulsing glow effect
            pulse = 0.5 + 0.5 * math.sin(self.animation_frame * 0.3)
            glow_intensity = int(pulse * 100)
            self.glow_effect.setColor(QtGui.QColor(255, 255, 255, glow_intensity))
            self.glow_effect.setBlurRadius(8 * pulse)

            # Color interpolation between base and hover color
            factor = min(1.0, self.animation_frame / 20.0)  # Fade in over 20 frames
            r = int(self.base_color.red() + factor * (self.hover_color.red() - self.base_color.red()))
            g = int(self.base_color.green() + factor * (self.hover_color.green() - self.base_color.green()))
            b = int(self.base_color.blue() + factor * (self.hover_color.blue() - self.base_color.blue()))
            a = int(self.base_color.alpha() + factor * (self.hover_color.alpha() - self.base_color.alpha()))
            current_color = QtGui.QColor(r, g, b, a)
            self.current_color = current_color
        else:
            # Reset to base color
            self.glow_effect.setColor(QtGui.QColor(255, 255, 255, 0))
            self.glow_effect.setBlurRadius(0)
            self.current_color = self.base_color

        self.update()

    def paint(self, painter: QtGui.QPainter, option, widget=None):
        """Paint the component with current color."""
        painter.fillRect(self.rect(), self.current_color)


class GPCItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, gpc: GPC, rect: QtCore.QRectF, label: bool):
        super().__init__(rect)
        self.gpc = gpc
        self.setCacheMode(QtWidgets.QGraphicsItem.DeviceCoordinateCache)
        pen = QtGui.QPen(QtGui.QColor(255, 255, 255, 100)); pen.setWidthF(0)
        self.setPen(pen)
        self.text = None
        if label:
            self.text = QtWidgets.QGraphicsSimpleTextItem(f"GPC {gpc.id}", self)
            self.text.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255, 200)))
            self.text.setPos(rect.x() + 4, rect.y() + 4)

    def reinitialize(self, gpc: GPC, rect: QtCore.QRectF, label: bool):
        """Reinitialize item with new data when reused from pool"""
        self.setRect(rect)
        self.gpc = gpc
        if self.text:
            self.text.setText(f"GPC {gpc.id}")
            self.text.setVisible(label)
        elif label:
            self.text = QtWidgets.QGraphicsSimpleTextItem(f"GPC {gpc.id}", self)
            self.text.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255, 200)))
            self.text.setPos(rect.x() + 4, rect.y() + 4)
        self.setVisible(True)

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
        self.scene_ = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene_)
        self._layout = None
        self._color_map = COLORMAPS["Turbo"]
        self.coloring_mode = "Utilization"
        self.show_labels = True
        self.show_grid = True
        self.view_mode = "Logical"
        self.core_items = []
        self.sm_items = []
        self.gpc_items = []
        self.interactive_items = []
        self._item_pool = {"core": [], "sm": [], "gpc": [], "interactive": []}

        self._cached_layout = None
        self._layout_dirty = True
        self._color_dirty = True
        self._view_dirty = True
        self._frame_counter = 0
        self._frame_skip = 1
        self._glow_enabled = False
        self._last_core_count = 0

        self._global_anims = {}
        self._global_anim_t = 0.0
        self._global_timer = QtCore.QTimer()
        self._global_timer.timeout.connect(self._tick_global_anims)
        self._interactive_index = {}
        self._gpu_model_for_interactive = None

    def _get_pooled_item(self, item_type: str, item_class, *args, **kwargs):
        """Get an item from pool or create new one"""
        if self._item_pool[item_type]:
            item = self._item_pool[item_type].pop()
            if hasattr(item, 'reinitialize'):
                item.reinitialize(*args, **kwargs)
            return item
        return item_class(*args, **kwargs)

    def set_show_grid(self, show: bool):
        if self.show_grid != show:
            self.show_grid = show
            self._update_item_properties()

    def add_interactive_components(self, gpu_model):
        """Add interactive components for ultra-detailed GPU models."""
        if not hasattr(gpu_model, 'interactive_components'):
            return
        self._gpu_model_for_interactive = gpu_model

        for comp_id, comp_data in gpu_model.interactive_components.items():
            interactive_item = self._get_pooled_item('interactive', InteractiveGPUComponent, comp_id, comp_data, gpu_model)
            interactive_item.setVisible(True)
            self.scene_.addItem(interactive_item)
            self.interactive_items.append(interactive_item)
            self._interactive_index[comp_id] = interactive_item

    def update_colors(self):
        if not self._color_dirty and not self._layout_dirty:
            self._frame_counter += 1
            if self._frame_counter % self._frame_skip != 0:
                return
        for ci in self.core_items:
            if ci.isVisible():
                ci.update()
        self.viewport().update()
        self._color_dirty = False

    def rebuild_scene(self, hard: bool = False):
        if hard or self._layout_dirty or self._view_dirty:
            self._clear_scene_efficiently()
            cache = self._calculate_layout_cache()
            if not self._layout:
                return
            self.scene_.setSceneRect(cache['scene_rect'])
            for gpc, g_rect in cache['gpc_positions']:
                g_item = self._get_pooled_item('gpc', GPCItem, gpc, g_rect, self.show_labels)
                g_item.setVisible(True)
                self.scene_.addItem(g_item)
                self.gpc_items.append(g_item)
            for sm, s_rect in cache['sm_positions']:
                s_item = self._get_pooled_item('sm', SMItem, sm, s_rect, self.show_labels if self.view_mode == "Logical" else False)
                if self.show_grid and self.view_mode != "Logical":
                    pen = QtGui.QPen(QtGui.QColor(255, 255, 255, 40))
                    pen.setWidthF(0)
                    s_item.setPen(pen)
                else:
                    s_item.setPen(QtGui.QPen(QtCore.Qt.NoPen))
                s_item.setVisible(True)
                self.scene_.addItem(s_item)
                self.sm_items.append(s_item)
            for core, cell in cache['core_positions']:
                ci = self._get_pooled_item('core', CoreItem, core, cell, self.color_for_core, self._glow_enabled)
                ci.setVisible(True)
                self.scene_.addItem(ci)
                self.core_items.append(ci)
            if self._gpu_model_for_interactive:
                self.add_interactive_components(self._gpu_model_for_interactive)
            self._view_dirty = False
            total_cores = len(cache['core_positions'])
            self._frame_skip = 1 if total_cores <= 6000 else 2 if total_cores <= 12000 else 3
            self._last_core_count = total_cores
        else:
            self._update_item_properties()

    def _update_item_properties(self):
        for sm_item in self.sm_items:
            if self.show_grid and self.view_mode != "Logical":
                pen = QtGui.QPen(QtGui.QColor(255, 255, 255, 40))
                pen.setWidthF(0)
                sm_item.setPen(pen)
            else:
                sm_item.setPen(QtGui.QPen(QtCore.Qt.NoPen))

    def _return_to_pool(self, item, item_type: str):
        item.setVisible(False)
        self._item_pool[item_type].append(item)

    def _clear_scene_efficiently(self):
        for item in self.core_items:
            if item.scene():
                item.scene().removeItem(item)
            self._return_to_pool(item, 'core')
        for item in self.sm_items:
            if item.scene():
                item.scene().removeItem(item)
            self._return_to_pool(item, 'sm')
        for item in self.gpc_items:
            if item.scene():
                item.scene().removeItem(item)
            self._return_to_pool(item, 'gpc')
        for item in self.interactive_items:
            if item.scene():
                item.scene().removeItem(item)
            self._return_to_pool(item, 'interactive')
        self.core_items.clear()
        self.sm_items.clear()
        self.gpc_items.clear()
        self.interactive_items.clear()
        self._interactive_index.clear()

    def _calculate_layout_cache(self):
        if not self._layout or not self._layout_dirty:
            return self._cached_layout
        margin = 20
        w, h = 1400, 900
        available = QtCore.QRectF(margin, margin, w - 2*margin, h - 2*margin)
        cache = {
            'scene_rect': QtCore.QRectF(0, 0, w, h),
            'available_rect': available,
            'gpc_positions': [],
            'sm_positions': [],
            'core_positions': []
        }
        gpcs = getattr(self._layout, 'gpcs', [])
        gpc_count = len(gpcs)
        if gpc_count == 0:
            self._cached_layout = cache
            self._layout_dirty = False
            return cache
        cols = max(1, int(math.ceil(math.sqrt(gpc_count))))
        rows = int(math.ceil(gpc_count / cols))
        gpc_w = available.width() / cols
        gpc_h = available.height() / rows
        idx = 0
        for r in range(rows):
            for c in range(cols):
                if idx >= gpc_count:
                    break
                gpc = gpcs[idx]
                g_rect = QtCore.QRectF(available.x() + c*gpc_w + 6, available.y() + r*gpc_h + 6, gpc_w - 12, gpc_h - 12)
                cache['gpc_positions'].append((gpc, g_rect))
                sms = getattr(gpc, 'sms', [])
                sm_count = len(sms)
                sm_cols = max(1, int(math.ceil(math.sqrt(sm_count)))) if sm_count else 1
                sm_rows = int(math.ceil(sm_count / sm_cols)) if sm_count else 1
                sm_w = g_rect.width() / sm_cols
                sm_h = g_rect.height() / sm_rows
                sm_idx = 0
                for rr in range(sm_rows):
                    for cc in range(sm_cols):
                        if sm_idx >= sm_count:
                            break
                        sm = sms[sm_idx]
                        s_rect = QtCore.QRectF(g_rect.x() + cc*sm_w + 4, g_rect.y() + rr*sm_h + 4, sm_w - 8, sm_h - 8)
                        cache['sm_positions'].append((sm, s_rect))
                        cores = getattr(sm, 'cores', [])
                        core_cols = max(1, int(math.sqrt(max(1, len(cores)))))
                        core_rows = int(math.ceil(len(cores) / core_cols)) if cores else 1
                        cw = s_rect.width() / max(1, core_cols)
                        ch = s_rect.height() / max(1, core_rows)
                        for k, core in enumerate(cores):
                            rr2 = k // core_cols
                            cc2 = k % core_cols
                            cell = QtCore.QRectF(s_rect.x() + cc2*cw + 1, s_rect.y() + rr2*ch + 1, cw - 2, ch - 2)
                            cache['core_positions'].append((core, cell))
                        sm_idx += 1
                idx += 1
        self._cached_layout = cache
        self._layout_dirty = False
        return cache

    def set_layout(self, layout: GPULayout):
        self._layout = layout
        self._layout_dirty = True
        self._view_dirty = True
        self.rebuild_scene(hard=True)

    def set_colormap(self, name: str):
        self._color_map = COLORMAPS.get(name, COLORMAPS["Turbo"])
        self._color_dirty = True
        self.update_colors()

    def set_coloring_mode(self, mode: str):
        self.coloring_mode = mode
        self._color_dirty = True
        self.update_colors()

    def set_view_mode(self, mode: str):
        self.view_mode = mode
        self._layout_dirty = True
        self._view_dirty = True
        self.rebuild_scene()

    def metric_for_core(self, c: Core) -> float:
        if self.coloring_mode == "Utilization":
            return float(getattr(c, 'activity', 0.0))
        if self.coloring_mode == "Temperature":
            return float(getattr(c, 'temperature', 0.0))
        if self.coloring_mode == "Memory pressure":
            return float(getattr(c, 'mem_pressure', 0.0))
        return float(getattr(c, 'activity', 0.0))

    def color_for_core(self, c: Core) -> Tuple[float, float, float]:
        return self._color_map(self.metric_for_core(c))

    def start_global_animations(self, comp_ids: list, mode: str):
        if not comp_ids:
            return
        for cid in comp_ids:
            self._global_anims[cid] = mode
        if not self._global_timer.isActive():
            self._global_timer.start(50)
        self.viewport().update()

    def stop_global_animations(self, comp_ids: list = None):
        if comp_ids:
            for cid in comp_ids:
                self._global_anims.pop(cid, None)
        else:
            self._global_anims.clear()
        if not self._global_anims and self._global_timer.isActive():
            self._global_timer.stop()
        self.viewport().update()

    def _tick_global_anims(self):
        self._global_anim_t += 0.05
        self.viewport().update()

    def drawForeground(self, painter: QtGui.QPainter, rect: QtCore.QRectF):
        if not self._global_anims:
            return
        t = self._global_anim_t
        for cid, mode in list(self._global_anims.items()):
            item = self._interactive_index.get(cid)
            if not item:
                continue
            r = item.rect()
            rr = QtCore.QRectF(r)
            if mode == 'flow':
                self._draw2d_flow(painter, rr, t)
            elif mode == 'orbit':
                self._draw2d_orbit(painter, rr, t)
            elif mode == 'ripple':
                self._draw2d_ripple(painter, rr, t)
            elif mode == 'beam':
                self._draw2d_beam(painter, rr, t)
            elif mode == 'sparkle':
                self._draw2d_sparkle(painter, rr, t, seed=hash(cid) & 0xFFFF)
            else:
                self._draw2d_pulse(painter, rr, t)

    def _draw2d_pulse(self, painter: QtGui.QPainter, rect: QtCore.QRectF, t: float):
        pulse = 0.5 + 0.5 * math.sin(t * 4.0)
        alpha = int(40 + 120 * pulse)
        pen = QtGui.QPen(QtGui.QColor(51, 179, 255, alpha))
        pen.setWidthF(2.0)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRect(rect)

    def _draw2d_flow(self, painter: QtGui.QPainter, rect: QtCore.QRectF, t: float):
        n = 16
        perim = 2 * (rect.width() + rect.height())
        for i in range(n):
            phase = (t * 2.0 + i / n) % 1.0
            dist = phase * perim
            if dist < rect.width():
                x = rect.left() + dist; y = rect.top()
            elif dist < rect.width() + rect.height():
                x = rect.right(); y = rect.top() + (dist - rect.width())
            elif dist < 2*rect.width() + rect.height():
                x = rect.right() - (dist - (rect.width() + rect.height())); y = rect.bottom()
            else:
                x = rect.left(); y = rect.bottom() - (dist - (2*rect.width() + rect.height()))
            c = QtGui.QColor(int((i/n)*255), 150, 255, 200)
            painter.fillRect(QtCore.QRectF(x-1.5, y-1.5, 3, 3), c)

    def _draw2d_orbit(self, painter: QtGui.QPainter, rect: QtCore.QRectF, t: float):
        cx = rect.center().x(); cy = rect.center().y()
        r = max(rect.width(), rect.height()) * 0.3
        for k in range(6):
            ang = t * 2.0 + k * (math.pi / 3)
            x = cx + r * math.cos(ang)
            y = cy + r * math.sin(ang)
            c = QtGui.QColor(230, int(100 + 40*math.sin(ang*2)), 60, 220)
            painter.fillRect(QtCore.QRectF(x-3, y-3, 6, 6), c)

    def _draw2d_ripple(self, painter: QtGui.QPainter, rect: QtCore.QRectF, t: float):
        for i in range(3):
            phase = (t * 0.8 + i * 0.25) % 1.0
            m = 2 + phase * max(rect.width(), rect.height()) * 0.2
            a = int(30 + 90 * (1.0 - phase))
            pen = QtGui.QPen(QtGui.QColor(51, 179, 255, a))
            pen.setWidthF(1.5)
            painter.setPen(pen)
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.drawRect(rect.adjusted(-m, -m, m, m))

    def _draw2d_beam(self, painter: QtGui.QPainter, rect: QtCore.QRectF, t: float):
        u = math.sin(t * 1.5) * 0.5 + 0.5
        x = rect.left() + u * rect.width()
        w = max(3.0, rect.width() * 0.06)
        c = QtGui.QColor(255, 160, 60, 150)
        painter.fillRect(QtCore.QRectF(x - w/2, rect.top(), w, rect.height()), c)

    def _draw2d_sparkle(self, painter: QtGui.QPainter, rect: QtCore.QRectF, t: float, seed: int = 0):
        rnd = math.floor(t * 10)
        base = (seed ^ rnd) & 0xFFFFFFFF
        for i in range(12):
            h = (base + i * 2654435761) & 0xFFFFFFFF
            rx = rect.left() + (h % 1000) / 1000.0 * rect.width()
            ry = rect.top() + ((h >> 12) % 1000) / 1000.0 * rect.height()
            a = 100 + (h >> 24) % 155
            painter.fillRect(QtCore.QRectF(rx-2, ry-2, 4, 4), QtGui.QColor(255, 255, 220, a))