# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
from utils import _m0002

class _m0009:

    def __init__(self, image, group):
        self.image = image
        self.group = group

    def render(self, _m0396, material='bronze', _m0252=40):
        if _m0396 <= 0:
            return
        _m0107 = Gimp.Selection.save(self.image)
        if _m0107 is None:
            raise RuntimeError('Die Auswahl für die Patina konnte nicht gespeichert werden.')
        try:
            _m0366 = max(12.0, min(28.0, float(_m0396) * 0.5))
            _m0365 = _m0002._m0369(self.image, self.group, 'Subtle Antique Oxide Shading', _m0366, Gimp.LayerMode.MULTIPLY)
            Gimp.Selection.none(self.image)
            _m0002._m0489(_m0365, 'gegl:noise-solid', {'detail': 4, 'turbulent': True, 'x-size': 15.0, 'y-size': 15.0})
            _m0002._m0489(_m0365, 'gegl:levels', {'in-low': 0.26, 'in-high': 0.74, 'out-low': 0.48, 'out-high': 1.0})
            _m0411 = max(16.0, min(36.0, float(_m0396) * 0.6))
            _m0410 = Gimp.LayerMode.SOFTLIGHT_LEGACY if hasattr(Gimp.LayerMode, 'SOFTLIGHT_LEGACY') else Gimp.LayerMode.OVERLAY
            _m0409 = _m0002._m0369(self.image, self.group, 'Fine Cast Bronze Micro-Grain', _m0411, _m0410)
            Gimp.context_set_foreground(_m0002._m0269((128, 128, 128)))
            _m0409.edit_fill(Gimp.FillType.FOREGROUND)
            _m0002._m0489(_m0409, 'gegl:noise-hsv', {'holdness': 3, 'hue-distance': 0.0, 'saturation-distance': 0.0, 'value-distance': 0.68})
            _m0002._m0489(_m0409, 'gegl:gaussian-blur', **{'std-dev-x': 0.75, 'std-dev-y': 0.75})
            _m0002._m0489(_m0409, 'gegl:levels', **{'in-low': 0.34, 'in-high': 0.66, 'out-low': 0.18, 'out-high': 0.86})
            self._m0030(_m0107)
        finally:
            Gimp.Selection.none(self.image)
            self.image.select_item(Gimp.ChannelOps.REPLACE, _m0107)
            self.image.remove_channel(_m0107)

    def _m0030(self, _m0107):
        self.image.select_item(Gimp.ChannelOps.REPLACE, _m0107)
        Gimp.Selection.invert(self.image)
        if not Gimp.Selection.is_empty(self.image):
            for child in self.group.get_children():
                if child is not None and child.is_valid() and (not child.is_group()):
                    name = child.get_name() or ''
                    if any((tag in name for tag in ('Oxide', 'Micro-Grain', 'Leather', 'Burl', 'Veins', 'Tint', 'Carbon', 'Gem'))):
                        child.edit_clear()
