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
        self.scene_ = QtWidgets.QGraphicsScene(self); self.setScene(self.scene_)
        self._layout: Optional[GPULayout] = None
        self._color_map = COLORMAPS["Turbo"]
        self.coloring_mode = "Utilization"
        self.show_labels = True
        self.show_grid = True
        self.view_mode = "Logical"
        
        self.core_items: List[CoreItem] = []
        self.sm_items: List[SMItem] = []
        self.gpc_items: List[GPCItem] = []
        self._item_pool = {
            'core': [], 'sm': [], 'gpc': []
        }
        self._cached_layout = None
        self._layout_dirty = True
        self._color_dirty = True
        self._view_dirty = True

        self._frame_counter = 0
        self._frame_skip = 1
        self._glow_enabled = False
        self._last_core_count = 0

    def _get_pooled_item(self, item_type: str, item_class, *args, **kwargs):
        """Get an item from pool or create new one"""
        if self._item_pool[item_type]:
            item = self._item_pool[item_type].pop()
            if hasattr(item, 'reinitialize'):
                item.reinitialize(*args, **kwargs)
            return item
        return item_class(*args, **kwargs)

    def _return_to_pool(self, item, item_type: str):
        """Return item to pool for reuse"""
        if len(self._item_pool[item_type]) < 100:
            item.setVisible(False)
            item.setParentItem(None)
            if hasattr(item, 'core'):
                item.core = None
            if hasattr(item, 'sm'):
                item.sm = None
            if hasattr(item, 'gpc'):
                item.gpc = None
            if hasattr(item, 'get_color'):
                item.get_color = None
            if hasattr(item, 'text'):
                item.text = None
            self._item_pool[item_type].append(item)

    def _clear_scene_efficiently(self):
        """Clear scene while returning items to pool"""
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
        
        self.core_items.clear()
        self.sm_items.clear()
        self.gpc_items.clear()

    def _calculate_layout_cache(self):
        """Cache expensive layout calculations"""
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
        
        if self.view_mode == "Logical":
            self._calculate_logical_positions(cache)
        elif self.view_mode == "SM Focus":
            self._calculate_die_positions(cache)
        else:
            self._calculate_die_positions(cache)
            
        self._cached_layout = cache
        self._layout_dirty = False
        return cache

    def _calculate_logical_positions(self, cache):
        """Calculate positions for logical view mode"""
        if not self._layout:
            return
            
        rect = cache['available_rect']
        gpc_count = len(self._layout.gpcs)
        cols = math.ceil(math.sqrt(gpc_count))
        rows = math.ceil(gpc_count / cols)
        gpc_w = rect.width() / cols
        gpc_h = rect.height() / rows
        
        idx = 0
        for r in range(rows):
            for c in range(cols):
                if idx >= gpc_count:
                    break
                gpc = self._layout.gpcs[idx]
                g_rect = QtCore.QRectF(rect.x() + c*gpc_w + 6, rect.y() + r*gpc_h + 6, gpc_w - 12, gpc_h - 12)
                cache['gpc_positions'].append((gpc, g_rect))
                
                sm_count = len(gpc.sms)
                sm_cols = math.ceil(math.sqrt(sm_count))
                sm_rows = math.ceil(sm_count / sm_cols)
                sm_w = g_rect.width() / sm_cols
                sm_h = g_rect.height() / sm_rows
                
                sm_idx = 0
                for rr in range(sm_rows):
                    for cc in range(sm_cols):
                        if sm_idx >= sm_count:
                            break
                        sm = gpc.sms[sm_idx]
                        s_rect = QtCore.QRectF(g_rect.x() + cc*sm_w + 4, g_rect.y() + rr*sm_h + 4, sm_w - 8, sm_h - 8)
                        cache['sm_positions'].append((sm, s_rect))
                        
                        core_cols = max(4, int(math.sqrt(len(sm.cores))))
                        core_rows = math.ceil(len(sm.cores) / core_cols)
                        cw = s_rect.width() / core_cols
                        ch = s_rect.height() / core_rows
                        
                        for k, core in enumerate(sm.cores):
                            rr2 = k // core_cols
                            cc2 = k % core_cols
                            cell = QtCore.QRectF(s_rect.x() + cc2*cw + 1, s_rect.y() + rr2*ch + 1, cw - 2, ch - 2)
                            cache['core_positions'].append((core, cell))
                        sm_idx += 1
                idx += 1

    def _calculate_die_positions(self, cache):
        """Calculate positions for die view modes"""
        if not self._layout:
            return
            
        rect = cache['available_rect']
        all_sms = [sm for g in self._layout.gpcs for sm in g.sms]
        sm_count = len(all_sms)
        cols = math.ceil(math.sqrt(sm_count))
        rows = math.ceil(sm_count / cols)
        sm_w = rect.width() / cols
        sm_h = rect.height() / rows
        
        for i, sm in enumerate(all_sms):
            r = i // cols
            c = i % cols
            s_rect = QtCore.QRectF(rect.x() + c*sm_w + 6, rect.y() + r*sm_h + 6, sm_w - 12, sm_h - 12)
            cache['sm_positions'].append((sm, s_rect))
            
            core_cols = max(4, int(math.sqrt(len(sm.cores))))
            core_rows = math.ceil(len(sm.cores) / core_cols)
            cw = s_rect.width() / core_cols
            ch = s_rect.height() / core_rows
            
            for k, core in enumerate(sm.cores):
                rr2 = k // core_cols
                cc2 = k % core_cols
                cell = QtCore.QRectF(s_rect.x() + cc2*cw + 1, s_rect.y() + rr2*ch + 1, cw - 2, ch - 2)
                cache['core_positions'].append((core, cell))

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
        if not self._color_dirty and not self._layout_dirty:
            return
            
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
            
            self._view_dirty = False
            
            total_cores = len(cache['core_positions'])
            self._frame_skip = 1 if total_cores <= 6000 else 2 if total_cores <= 12000 else 3
            self._last_core_count = total_cores
        else:
            self._update_item_properties()

    def _update_item_properties(self):
        """Update item properties without rebuilding scene"""
        for gpc_item in self.gpc_items:
            pass
        for sm_item in self.sm_items:
            pass
        
        for sm_item in self.sm_items:
            if self.show_grid and self.view_mode != "Logical":
                pen = QtGui.QPen(QtGui.QColor(255, 255, 255, 40))
                pen.setWidthF(0)
                sm_item.setPen(pen)
            else:
                sm_item.setPen(QtGui.QPen(QtCore.Qt.NoPen))

    def set_layout(self, layout: GPULayout):
        self._layout = layout
        self._layout_dirty = True
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
        if self.view_mode != mode:
            self.view_mode = mode
            self._view_dirty = True
            self._layout_dirty = True
            self.rebuild_scene()

    def set_show_labels(self, show: bool):
        if self.show_labels != show:
            self.show_labels = show
            self._view_dirty = True
            self.rebuild_scene()

    def set_show_grid(self, show: bool):
        if self.show_grid != show:
            self.show_grid = show
            self._update_item_properties()

    def set_glow_enabled(self, enabled: bool):
        if self._glow_enabled != enabled:
            self._glow_enabled = enabled
            self._view_dirty = True
            self.rebuild_scene()