# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
import config
from selection import SelectionManager
from utils import _m0002

class _m0000:

    @staticmethod
    def _m0348(c1, c2, t):
        return tuple((max(0, min(255, round(a + (b - a) * t))) for a, b in zip(c1, c2)))

    @classmethod
    def _m0493(cls, material, inlay_rgb, is_glass, mat_key):
        from community_material_seal import apply_community_materials, community_material_key
        apply_community_materials()
        material = community_material_key(material)
        if is_glass:
            from fx.glass_facets import GlassFacetsHelper
            stops = config.sample_grad_stops(GlassFacetsHelper.build_glass_gradmap(inlay_rgb), 7)
            return (stops[0], stops[3], stops[6])
        _m0119 = config.sample_grad_stops(config.METALS.get(material, config.METALS['gold']), 5)
        _m0120 = min(_m0119, key=sum)
        _m0123 = _m0119[2]
        _m0122 = max(_m0119, key=sum)
        if mat_key in ('main', '', None):
            return (_m0120, _m0123, _m0122)
        if mat_key in config.METALS:
            m = config.sample_grad_stops(config.METALS[mat_key], 5)
            if material == 'gold':
                return (min(m, key=sum), m[2], max(m, key=sum))
            return (cls._m0348(_m0120, min(m, key=sum), 0.38), cls._m0348(_m0123, m[2], 0.38), cls._m0348(_m0122, max(m, key=sum), 0.38))
        if mat_key == 'shadow':
            _m0531 = tuple((round(c * 0.28) for c in _m0120))
            _m0534 = tuple((round(c * 0.52) for c in _m0120))
            _m0533 = cls._m0348(_m0120, _m0123, 0.35)
            return (_m0531, _m0534, _m0533)
        if mat_key == 'inlay':
            _m0315 = inlay_rgb
            _m0312 = tuple((round(c * 0.38) for c in _m0315))
            _m0314 = cls._m0348(_m0315, _m0123, 0.22)
            return (_m0312, _m0315, _m0314)
        return (_m0120, _m0123, _m0122)

    @staticmethod
    def _m0034(mat):
        if mat == 'chrom':
            return ((228, 228, 228), (116, 116, 116), (26, 26, 26), 0.46)
        if mat in ('leather_nappa_black', 'carbon_fiber', 'charcoal_matte', 'charcoal_ember', 'schwarzchrom', 'diamond_black', 'granite_obsidian', 'marble_portoro_gold'):
            return ((182, 182, 182), (68, 68, 68), (14, 14, 14), 0.42)
        if mat in ('rosegold', 'kupfer'):
            return ((222, 222, 222), (140, 140, 140), (58, 58, 58), 0.48)
        if mat == 'edelstahl':
            return ((218, 218, 218), (126, 126, 126), (44, 44, 44), 0.46)
        if mat == 'platinum':
            return ((226, 226, 226), (148, 148, 148), (60, 60, 60), 0.48)
        if mat == 'aluminium':
            return ((204, 204, 204), (148, 148, 148), (100, 100, 100), 0.5)
        if mat == 'titan':
            return ((210, 210, 210), (108, 108, 108), (38, 38, 38), 0.46)
        return ((196, 196, 196), (128, 128, 128), (58, 58, 58), 0.46)

    @staticmethod
    def _m0073(_m0130, _m0237, ix1, iy1, ix2, iy2, _m0461):
        _m0599 = max(4, min(8, round(_m0130.border_width * 0.06)))
        _m0328 = (ix1 + _m0599, iy1 + _m0599, ix2 - _m0599, iy2 - _m0599)
        SelectionManager.select_zone_ring(_m0130.image, _m0130.inner_box, _m0328, _m0461, max(0.0, _m0461 - _m0599))
        if Gimp.Selection.is_empty(_m0130.image):
            return
        _m0190, _, _ = _m0130._m0086('main')
        _m0598 = round(_m0237 / 100.0 * 32.0 * (_m0130.profil_tiefe / 100.0))
        if _m0598 < 3:
            return
        _m0597 = _m0002._m0404(_m0130.image, _m0130.group, 'Center Inset Shadow', _m0598, Gimp.LayerMode.MULTIPLY)
        Gimp.context_set_foreground(_m0002._m0299(_m0190))
        _m0597.edit_fill(Gimp.FillType.FOREGROUND)
        Gimp.Selection.none(_m0130.image)
        _m0134 = 3.5 if _m0237 < 95 else 2.2
        _m0002._m0530(_m0597, 'gegl:gaussian-blur', **{'std-dev-x': _m0134, 'std-dev-y': _m0134})
        SelectionManager.select_full_box(_m0130.image, _m0130.inner_box, _m0461)
        Gimp.Selection.invert(_m0130.image)
        if not Gimp.Selection.is_empty(_m0130.image):
            _m0597.edit_clear()

    @classmethod
    def _m0479(cls, _m0130, _m0611, _m0369, _m0371, _m0370, _m0372):
        if _m0130.center_mode != 'transparent':
            return
        _m0237 = 100 - int(_m0130.inner_transparency)
        if _m0237 <= 0:
            return
        ix1, iy1, ix2, iy2 = _m0130.inner_box
        if ix2 <= ix1 or iy2 <= iy1:
            return
        _m0461 = _m0611._m0331(1.0, 'auto')
        SelectionManager.select_full_box(_m0130.image, _m0130.inner_box, _m0461)
        if Gimp.Selection.is_empty(_m0130.image):
            return
        _m0214 = round(_m0237 * 0.62) if _m0130.is_glass else _m0237
        _m0162 = _m0002._m0404(_m0130.image, _m0130.group, 'Center Fill', max(1, min(100, _m0214)), Gimp.LayerMode.NORMAL)
        _m0151, _m0154, _m0153, _m0417 = cls._m0034(_m0130.material)
        _m0130._m0235(_m0162, _m0151, _m0154, _m0153, _m0369, _m0371, _m0370, _m0372, _m0417)
        _m0130.grad_helper._m0112(_m0162, _m0130.material)
        cls._m0073(_m0130, _m0237, ix1, iy1, ix2, iy2, _m0461)
