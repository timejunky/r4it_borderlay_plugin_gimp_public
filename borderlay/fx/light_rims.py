# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
from selection import SelectionManager
from utils import _m0002

class _m0007:

    @staticmethod
    def _m0478(_m0350, _m0434, _m0571, _m0338: bool):
        ox1, oy1, ox2, oy2 = _m0350.outer_box
        w = float(ox2 - ox1)
        h = float(oy2 - oy1)
        _m0467 = 0.0 if _m0338 else float(_m0350.inner_radius) if _m0350.inner_radius > 0 else max(28.0, _m0350.outer_radius - _m0350.border_width * 0.46)
        _m0502 = _m0002._m0404(_m0350.image, _m0350.group, 'Bronze Burnished Specular Rims', 58.0, Gimp.LayerMode.SCREEN)
        for frac in (0.215, 0.54, 0.785):
            px = round(_m0350.border_width * frac)
            _m0115 = (ox1 + px, oy1 + px, ox2 - px, oy2 - px)
            _m0114 = (ox1 + px + 2, oy1 + px + 2, ox2 - px - 2, oy2 - px - 2)
            _m0462 = 0.0 if _m0338 else max(0.0, _m0350.outer_radius * (1.0 - frac) + _m0467 * frac)
            SelectionManager.select_zone_ring(_m0350.image, _m0115, _m0114, _m0462, max(0.0, _m0462 - 1.5))
            if not Gimp.Selection.is_empty(_m0350.image):
                grad = _m0350._m0064(_m0434, _m0571, (24, 14, 6))
                try:
                    Gimp.context_set_gradient(grad)
                    _m0502.edit_gradient_fill(Gimp.GradientType.LINEAR, 0.0, False, 1, 0.0, True, float(ox1 + w * 0.54), float(oy1), float(ox1), float(oy1 + h * 0.65))
                finally:
                    grad.delete()
        Gimp.Selection.none(_m0350.image)
        _m0002._m0530(_m0502, 'gegl:gaussian-blur', **{'std-dev-x': 0.75, 'std-dev-y': 0.75})

    @staticmethod
    def _m0480(_m0350, _m0434, _m0571, _m0338: bool):
        ox1, oy1, ox2, oy2 = _m0350.outer_box
        w = float(ox2 - ox1)
        _m0467 = 0.0 if _m0338 else float(_m0350.inner_radius) if _m0350.inner_radius > 0 else max(28.0, _m0350.outer_radius - _m0350.border_width * 0.46)
        _m0303 = _m0002._m0404(_m0350.image, _m0350.group, 'Chrome Liquid Mirror Highlight Rims', 68.0, Gimp.LayerMode.SCREEN)
        for frac in (0.215, 0.785):
            px = round(_m0350.border_width * frac)
            _m0115 = (ox1 + px, oy1 + px, ox2 - px, oy2 - px)
            _m0114 = (ox1 + px + 2, oy1 + px + 2, ox2 - px - 2, oy2 - px - 2)
            _m0462 = 0.0 if _m0338 else max(0.0, _m0350.outer_radius * (1.0 - frac) + _m0467 * frac)
            SelectionManager.select_zone_ring(_m0350.image, _m0115, _m0114, _m0462, max(0.0, _m0462 - 1.5))
            if not Gimp.Selection.is_empty(_m0350.image):
                grad = _m0350._m0064(_m0434, _m0571, (0, 0, 0))
                try:
                    Gimp.context_set_gradient(grad)
                    _m0303.edit_gradient_fill(Gimp.GradientType.LINEAR, 0.0, False, 1, 0.0, True, float(ox1 + w * 0.25), float(oy1), float(ox2), float(oy2))
                finally:
                    grad.delete()
        Gimp.Selection.none(_m0350.image)
        _m0002._m0530(_m0303, 'gegl:gaussian-blur', **{'std-dev-x': 0.55, 'std-dev-y': 0.55})

    @staticmethod
    def _m0482(_m0350, _m0125, _m0434, _m0571):
        ox1, oy1, _m0071, _m0072 = _m0350.outer_box
        ix1, iy1, _m0057, _m0058 = _m0350.inner_box
        _m0275 = max(24, min(58, round(_m0350.glanz * 0.52)))
        _m0274 = _m0002._m0404(_m0350.image, _m0350.group, 'Specular Edge Glints & Flare', _m0275, Gimp.LayerMode.SCREEN)
        _m0399 = [float(ox1), float(oy1 + 0.6), float(ox1 + 0.6), float(oy1), float(ix1 + 0.6), float(iy1), float(ix1), float(iy1 + 0.6)]
        Gimp.Selection.none(_m0350.image)
        if _m0350.image.select_polygon(Gimp.ChannelOps.REPLACE, _m0399):
            _m0350.image.select_item(Gimp.ChannelOps.INTERSECT, _m0125)
            if not Gimp.Selection.is_empty(_m0350.image):
                grad = _m0350._m0064(_m0434, _m0571, (0, 0, 0))
                try:
                    Gimp.context_set_gradient(grad)
                    _m0274.edit_gradient_fill(Gimp.GradientType.LINEAR, 0.0, False, 1, 0.0, True, float(ox1), float(oy1), float(ix1), float(iy1))
                finally:
                    grad.delete()
        if _m0350.luxus:
            _m0569 = max(14.0, float(_m0350.border_width * 0.36))
            _m0241 = [(float(ix1), float(iy1)), (float(ox1 + _m0350.border_width * 0.14), float(oy1 + _m0350.border_width * 0.14))]
            for fx, _m0248 in _m0241:
                _m0201 = [fx - _m0569 * 0.3, _m0248 + _m0569 * 0.3, fx - 1.0, _m0248 - 1.0, fx + _m0569 * 0.45, _m0248 - _m0569 * 0.45, fx + 1.0, _m0248 + 1.0]
                Gimp.Selection.none(_m0350.image)
                if _m0350.image.select_polygon(Gimp.ChannelOps.REPLACE, _m0201):
                    _m0350.image.select_item(Gimp.ChannelOps.INTERSECT, _m0125)
                    if not Gimp.Selection.is_empty(_m0350.image):
                        _m0276 = _m0350._m0064(_m0434, _m0571, (0, 0, 0))
                        try:
                            Gimp.context_set_gradient(_m0276)
                            _m0274.edit_gradient_fill(Gimp.GradientType.RADIAL, 0.0, False, 1, 0.0, True, fx, _m0248, fx + _m0569 * 0.5, _m0248 + _m0569 * 0.5)
                        finally:
                            _m0276.delete()
        Gimp.Selection.none(_m0350.image)
        _m0002._m0530(_m0274, 'gegl:gaussian-blur', **{'std-dev-x': 1.6, 'std-dev-y': 1.6})
