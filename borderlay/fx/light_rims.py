# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
from selection import SelectionManager
from utils import _m0002

class _m0006:

    @staticmethod
    def _m0441(_m0316, _m0399, _m0527, _m0306: bool):
        ox1, oy1, ox2, oy2 = _m0316.outer_box
        w = float(ox2 - ox1)
        h = float(oy2 - oy1)
        _m0431 = 0.0 if _m0306 else float(_m0316.inner_radius) if _m0316.inner_radius > 0 else max(28.0, _m0316.outer_radius - _m0316.border_width * 0.46)
        _m0462 = _m0002._m0369(_m0316.image, _m0316.group, 'Bronze Burnished Specular Rims', 58.0, Gimp.LayerMode.SCREEN)
        for frac in (0.215, 0.54, 0.785):
            px = round(_m0316.border_width * frac)
            _m0097 = (ox1 + px, oy1 + px, ox2 - px, oy2 - px)
            _m0096 = (ox1 + px + 2, oy1 + px + 2, ox2 - px - 2, oy2 - px - 2)
            _m0426 = 0.0 if _m0306 else max(0.0, _m0316.outer_radius * (1.0 - frac) + _m0431 * frac)
            SelectionManager.select_zone_ring(_m0316.image, _m0097, _m0096, _m0426, max(0.0, _m0426 - 1.5))
            if not Gimp.Selection.is_empty(_m0316.image):
                grad = _m0316._m0053(_m0399, _m0527, (24, 14, 6))
                try:
                    Gimp.context_set_gradient(grad)
                    _m0462.edit_gradient_fill(Gimp.GradientType.LINEAR, 0.0, False, 1, 0.0, True, float(ox1 + w * 0.54), float(oy1), float(ox1), float(oy1 + h * 0.65))
                finally:
                    grad.delete()
        Gimp.Selection.none(_m0316.image)
        _m0002._m0489(_m0462, 'gegl:gaussian-blur', **{'std-dev-x': 0.75, 'std-dev-y': 0.75})

    @staticmethod
    def _m0443(_m0316, _m0399, _m0527, _m0306: bool):
        ox1, oy1, ox2, oy2 = _m0316.outer_box
        w = float(ox2 - ox1)
        _m0431 = 0.0 if _m0306 else float(_m0316.inner_radius) if _m0316.inner_radius > 0 else max(28.0, _m0316.outer_radius - _m0316.border_width * 0.46)
        _m0273 = _m0002._m0369(_m0316.image, _m0316.group, 'Chrome Liquid Mirror Highlight Rims', 68.0, Gimp.LayerMode.SCREEN)
        for frac in (0.215, 0.785):
            px = round(_m0316.border_width * frac)
            _m0097 = (ox1 + px, oy1 + px, ox2 - px, oy2 - px)
            _m0096 = (ox1 + px + 2, oy1 + px + 2, ox2 - px - 2, oy2 - px - 2)
            _m0426 = 0.0 if _m0306 else max(0.0, _m0316.outer_radius * (1.0 - frac) + _m0431 * frac)
            SelectionManager.select_zone_ring(_m0316.image, _m0097, _m0096, _m0426, max(0.0, _m0426 - 1.5))
            if not Gimp.Selection.is_empty(_m0316.image):
                grad = _m0316._m0053(_m0399, _m0527, (0, 0, 0))
                try:
                    Gimp.context_set_gradient(grad)
                    _m0273.edit_gradient_fill(Gimp.GradientType.LINEAR, 0.0, False, 1, 0.0, True, float(ox1 + w * 0.25), float(oy1), float(ox2), float(oy2))
                finally:
                    grad.delete()
        Gimp.Selection.none(_m0316.image)
        _m0002._m0489(_m0273, 'gegl:gaussian-blur', **{'std-dev-x': 0.55, 'std-dev-y': 0.55})

    @staticmethod
    def _m0445(_m0316, _m0107, _m0399, _m0527):
        ox1, oy1, _m0059, _m0060 = _m0316.outer_box
        ix1, iy1, _m0046, _m0047 = _m0316.inner_box
        _m0246 = max(24, min(58, round(_m0316.glanz * 0.52)))
        _m0245 = _m0002._m0369(_m0316.image, _m0316.group, 'Specular Edge Glints & Flare', _m0246, Gimp.LayerMode.SCREEN)
        _m0364 = [float(ox1), float(oy1 + 0.6), float(ox1 + 0.6), float(oy1), float(ix1 + 0.6), float(iy1), float(ix1), float(iy1 + 0.6)]
        Gimp.Selection.none(_m0316.image)
        if _m0316.image.select_polygon(Gimp.ChannelOps.REPLACE, _m0364):
            _m0316.image.select_item(Gimp.ChannelOps.INTERSECT, _m0107)
            if not Gimp.Selection.is_empty(_m0316.image):
                grad = _m0316._m0053(_m0399, _m0527, (0, 0, 0))
                try:
                    Gimp.context_set_gradient(grad)
                    _m0245.edit_gradient_fill(Gimp.GradientType.LINEAR, 0.0, False, 1, 0.0, True, float(ox1), float(oy1), float(ix1), float(iy1))
                finally:
                    grad.delete()
        if _m0316.luxus:
            _m0525 = max(14.0, float(_m0316.border_width * 0.36))
            _m0215 = [(float(ix1), float(iy1)), (float(ox1 + _m0316.border_width * 0.14), float(oy1 + _m0316.border_width * 0.14))]
            for fx, _m0222 in _m0215:
                _m0180 = [fx - _m0525 * 0.3, _m0222 + _m0525 * 0.3, fx - 1.0, _m0222 - 1.0, fx + _m0525 * 0.45, _m0222 - _m0525 * 0.45, fx + 1.0, _m0222 + 1.0]
                Gimp.Selection.none(_m0316.image)
                if _m0316.image.select_polygon(Gimp.ChannelOps.REPLACE, _m0180):
                    _m0316.image.select_item(Gimp.ChannelOps.INTERSECT, _m0107)
                    if not Gimp.Selection.is_empty(_m0316.image):
                        _m0247 = _m0316._m0053(_m0399, _m0527, (0, 0, 0))
                        try:
                            Gimp.context_set_gradient(_m0247)
                            _m0245.edit_gradient_fill(Gimp.GradientType.RADIAL, 0.0, False, 1, 0.0, True, fx, _m0222, fx + _m0525 * 0.5, _m0222 + _m0525 * 0.5)
                        finally:
                            _m0247.delete()
        Gimp.Selection.none(_m0316.image)
        _m0002._m0489(_m0245, 'gegl:gaussian-blur', **{'std-dev-x': 1.6, 'std-dev-y': 1.6})
