# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
from utils import _m0002
from fx.patina import _m0010

class TextureFX:

    def __init__(self, image, group, angle, brushed_granularity=38, brushed_angle=-1, fur_density=72, fur_length=61):
        self.image = image
        self.group = group
        self.angle = angle
        self.brushed_granularity = max(1, min(100, int(brushed_granularity)))
        self.brushed_angle = int(brushed_angle)
        self.fur_density = max(1, min(100, int(fur_density)))
        self.fur_length = max(1, min(100, int(fur_length)))
        self.patina_helper = _m0010(self.image, self.group)

    def _m0043(self):
        if self.brushed_angle >= 0:
            return float(self.brushed_angle % 360)
        return float(self.angle % 360)

    def render_brushed(self, _m0281=None, _m0139=None):
        _m0280 = self.brushed_granularity if _m0281 is None else max(1, min(100, int(_m0281)))
        ang = self._m0043() if _m0139 is None or int(_m0139) < 0 else float(int(_m0139) % 360)
        _m0125 = Gimp.Selection.save(self.image)
        if _m0125 is None:
            raise RuntimeError('Die Auswahl für die gebürstete Textur konnte nicht gespeichert werden.')
        try:
            _m0259 = _m0280 / 100.0
            _m0232 = max(16.0, min(64.0, 20.0 + _m0259 * 44.0))
            _m0284 = max(12.0, min(40.0, 12.0 + _m0259 * 28.0))
            _m0570 = max(28.0, min(76.0, 32.0 + _m0259 * 44.0))
            _m0311 = max(1, min(5, round(4 - _m0259 * 3.0)))
            mode = Gimp.LayerMode.OVERLAY if hasattr(Gimp.LayerMode, 'OVERLAY') else Gimp.LayerMode.SOFTLIGHT_LEGACY
            _m0140 = _m0002._m0404(self.image, self.group, 'Brushed Metal Micro-Fibers', _m0232, mode)
            Gimp.context_set_foreground(_m0002._m0299((128, 128, 128)))
            _m0140.edit_fill(Gimp.FillType.FOREGROUND)
            Gimp.Selection.none(self.image)
            _m0002._m0530(_m0140, 'gegl:noise-hsv', {'holdness': int(_m0311), 'hue-distance': 0.0, 'saturation-distance': 0.0, 'value-distance': float(0.7 + _m0259 * 0.22)})
            if _m0280 > 45:
                _m0577 = (_m0280 - 45) / 55.0 * 0.85
                _m0002._m0530(_m0140, 'gegl:gaussian-blur', {'std-dev-x': float(_m0577), 'std-dev-y': float(_m0577)})
            _m0002._m0530(_m0140, 'gegl:motion-blur-linear', {'length': float(_m0570), 'angle': float(ang)})
            _m0002._m0530(_m0140, 'gegl:levels', {'in-low': 0.36, 'in-high': 0.64, 'out-low': 0.06, 'out-high': 0.94})
            _m0279 = _m0002._m0404(self.image, self.group, 'Brushed Fine Grain Grooves', _m0284, Gimp.LayerMode.MULTIPLY)
            Gimp.context_set_foreground(_m0002._m0299((204, 204, 204)))
            _m0279.edit_fill(Gimp.FillType.FOREGROUND)
            _m0002._m0530(_m0279, 'gegl:noise-hsv', {'holdness': max(1, int(_m0311)), 'hue-distance': 0.0, 'saturation-distance': 0.0, 'value-distance': float(0.66 + _m0259 * 0.24)})
            _m0002._m0530(_m0279, 'gegl:motion-blur-linear', {'length': float(_m0570 * 0.85), 'angle': float(ang)})
            _m0002._m0530(_m0279, 'gegl:levels', **{'in-low': 0.4, 'in-high': 0.64, 'out-low': 0.16, 'out-high': 1.0})
            self.image.select_item(Gimp.ChannelOps.REPLACE, _m0125)
            Gimp.Selection.invert(self.image)
            if not Gimp.Selection.is_empty(self.image):
                _m0140.edit_clear()
                _m0279.edit_clear()
        finally:
            Gimp.Selection.none(self.image)
            self.image.select_item(Gimp.ChannelOps.REPLACE, _m0125)
            self.image.remove_channel(_m0125)

    def render_scratches(self, _m0330):
        if _m0330 <= 0:
            return
        _m0125 = Gimp.Selection.save(self.image)
        if _m0125 is None:
            raise RuntimeError('Die Auswahl für die Kratzer-Textur konnte nicht gespeichert werden.')
        try:
            opacity = max(8.0, min(48.0, float(_m0330) * 1.25))
            _m0522 = _m0002._m0404(self.image, self.group, 'Micro Scratches', opacity, Gimp.LayerMode.OVERLAY)
            Gimp.context_set_foreground(_m0002._m0299((128, 128, 128)))
            _m0522.edit_fill(Gimp.FillType.FOREGROUND)
            ang = (self._m0043() + 35.0) % 360.0
            Gimp.Selection.none(self.image)
            _m0002._m0530(_m0522, 'gegl:noise-hsv', {'holdness': 4, 'hue-distance': 0.0, 'saturation-distance': 0.0, 'value-distance': 0.82})
            _m0002._m0530(_m0522, 'gegl:motion-blur-linear', {'length': 16.0, 'angle': float(ang)})
            _m0002._m0530(_m0522, 'gegl:levels', **{'in-low': 0.42, 'in-high': 0.58, 'out-low': 0.18, 'out-high': 0.82})
            self.image.select_item(Gimp.ChannelOps.REPLACE, _m0125)
            Gimp.Selection.invert(self.image)
            if not Gimp.Selection.is_empty(self.image):
                _m0522.edit_clear()
        finally:
            Gimp.Selection.none(self.image)
            self.image.select_item(Gimp.ChannelOps.REPLACE, _m0125)
            self.image.remove_channel(_m0125)

    def render_organic(self, kind, border_width):
        kind = str(kind or '').strip().lower()
        if kind not in ('feather', 'fur', 'scales'):
            return
        _m0296, has_selection, x1, y1, x2, y2 = Gimp.Selection.bounds(self.image)
        if not _m0296 or not has_selection:
            return
        bw = int(x2) - int(x1)
        bh = int(y2) - int(y1)
        if bw < 2 or bh < 2:
            return
        from fx.organic import _m0484
        rgba, _m0131 = _m0484(kind, bw, bh, self.brushed_granularity, max(16, int(border_width)), self._m0043(), _m0411=float(x1), _m0412=float(y1), fur_density=self.fur_density, fur_length=self.fur_length)
        if len(rgba) != bw * bh * 4:
            return
        _m0125 = Gimp.Selection.save(self.image)
        if _m0125 is None:
            raise RuntimeError('Die Auswahl für die organische Oberfläche konnte nicht gespeichert werden.')
        _m0583 = {'feather': 'Feather Vanes', 'fur': 'Fur Nap', 'scales': 'Scale Mail'}
        _m0259 = max(0.0, min(1.0, self.brushed_granularity / 100.0))
        opacity = {'feather': 58.0, 'fur': 72.0, 'scales': 66.0}[kind] + _m0259 * 10.0
        mode = Gimp.LayerMode.GRAIN_MERGE if hasattr(Gimp.LayerMode, 'GRAIN_MERGE') else Gimp.LayerMode.OVERLAY
        layer = _m0002._m0404(self.image, self.group, _m0583[kind], opacity, mode)
        try:
            Gimp.Selection.none(self.image)
            import gi
            gi.require_version('Gegl', '0.4')
            from gi.repository import Gegl
            Gegl.init(None)
            _m0142 = layer.get_buffer()
            rect = Gegl.Rectangle.new(int(x1), int(y1), bw, bh)
            try:
                _m0142.set(rect, "R'G'B'A u8", rgba)
            except Exception:
                _m0142.set(rect, 'RGBA u8', rgba)
            try:
                layer.update(int(x1), int(y1), bw, bh)
            except Exception:
                pass
            _m0549 = (0.35 if kind == 'feather' else 0.55) + max(0, int(_m0131) - 1) * 0.35
            _m0002._m0530(layer, 'gegl:gaussian-blur', **{'std-dev-x': float(_m0549), 'std-dev-y': float(_m0549)})
            self.image.select_item(Gimp.ChannelOps.REPLACE, _m0125)
            Gimp.Selection.invert(self.image)
            if not Gimp.Selection.is_empty(self.image):
                layer.edit_clear()
        finally:
            Gimp.Selection.none(self.image)
            self.image.select_item(Gimp.ChannelOps.REPLACE, _m0125)
            self.image.remove_channel(_m0125)

    def render_patina(self, _m0431, material='bronze'):
        self.patina_helper.render(_m0431, material=material, _m0281=self.brushed_granularity)
