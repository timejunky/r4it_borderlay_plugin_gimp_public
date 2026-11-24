# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
import config
from selection import SelectionManager
from utils import _m0002

class _m0000:

    @staticmethod
    def _m0315(c1, c2, t):
        return tuple((max(0, min(255, round(a + (b - a) * t))) for a, b in zip(c1, c2)))

    @classmethod
    def _m0453(cls, material, inlay_rgb, is_glass, mat_key):
        from community_material_seal import apply_community_materials, community_material_key
        apply_community_materials()
        material = community_material_key(material)
        if is_glass:
            from fx.glass_facets import GlassFacetsHelper
            stops = config.sample_grad_stops(GlassFacetsHelper.build_glass_gradmap(inlay_rgb), 7)
            return (stops[0], stops[3], stops[6])
        _m0101 = config.sample_grad_stops(config.METALS.get(material, config.METALS['gold']), 5)
        _m0102 = min(_m0101, key=sum)
        _m0105 = _m0101[2]
        _m0104 = max(_m0101, key=sum)
        if mat_key in ('main', '', None):
            return (_m0102, _m0105, _m0104)
        if mat_key in config.METALS:
            m = config.sample_grad_stops(config.METALS[mat_key], 5)
            if material == 'gold':
                return (min(m, key=sum), m[2], max(m, key=sum))
            return (cls._m0315(_m0102, min(m, key=sum), 0.38), cls._m0315(_m0105, m[2], 0.38), cls._m0315(_m0104, max(m, key=sum), 0.38))
        if mat_key == 'shadow':
            _m0490 = tuple((round(c * 0.28) for c in _m0102))
            _m0493 = tuple((round(c * 0.52) for c in _m0102))
            _m0492 = cls._m0315(_m0102, _m0105, 0.35)
            return (_m0490, _m0493, _m0492)
        if mat_key == 'inlay':
            _m0285 = inlay_rgb
            _m0282 = tuple((round(c * 0.38) for c in _m0285))
            _m0284 = cls._m0315(_m0285, _m0105, 0.22)
            return (_m0282, _m0285, _m0284)
        return (_m0102, _m0105, _m0104)

    @staticmethod
    def _m0027(mat):
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
    def _m0061(_m0112, _m0212, ix1, iy1, ix2, iy2, _m0425):
        _m0554 = max(4, min(8, round(_m0112.border_width * 0.06)))
        _m0298 = (ix1 + _m0554, iy1 + _m0554, ix2 - _m0554, iy2 - _m0554)
        SelectionManager.select_zone_ring(_m0112.image, _m0112.inner_box, _m0298, _m0425, max(0.0, _m0425 - _m0554))
        if Gimp.Selection.is_empty(_m0112.image):
            return
        _m0169, _, _ = _m0112._m0073('main')
        _m0553 = round(_m0212 / 100.0 * 32.0 * (_m0112.profil_tiefe / 100.0))
        if _m0553 < 3:
            return
        _m0552 = _m0002._m0369(_m0112.image, _m0112.group, 'Center Inset Shadow', _m0553, Gimp.LayerMode.MULTIPLY)
        Gimp.context_set_foreground(_m0002._m0269(_m0169))
        _m0552.edit_fill(Gimp.FillType.FOREGROUND)
        Gimp.Selection.none(_m0112.image)
        _m0116 = 3.5 if _m0212 < 95 else 2.2
        _m0002._m0489(_m0552, 'gegl:gaussian-blur', **{'std-dev-x': _m0116, 'std-dev-y': _m0116})
        SelectionManager.select_full_box(_m0112.image, _m0112.inner_box, _m0425)
        Gimp.Selection.invert(_m0112.image)
        if not Gimp.Selection.is_empty(_m0112.image):
            _m0552.edit_clear()

    @classmethod
    def _m0442(cls, _m0112, _m0565, _m0335, _m0337, _m0336, _m0338):
        if _m0112.center_mode != 'transparent':
            return
        _m0212 = 100 - int(_m0112.inner_transparency)
        if _m0212 <= 0:
            return
        ix1, iy1, ix2, iy2 = _m0112.inner_box
        if ix2 <= ix1 or iy2 <= iy1:
            return
        _m0425 = _m0565._m0300(1.0, 'auto')
        SelectionManager.select_full_box(_m0112.image, _m0112.inner_box, _m0425)
        if Gimp.Selection.is_empty(_m0112.image):
            return
        _m0192 = round(_m0212 * 0.62) if _m0112.is_glass else _m0212
        _m0143 = _m0002._m0369(_m0112.image, _m0112.group, 'Center Fill', max(1, min(100, _m0192)), Gimp.LayerMode.NORMAL)
        _m0132, _m0135, _m0134, _m0382 = cls._m0027(_m0112.material)
        _m0112._m0210(_m0143, _m0132, _m0135, _m0134, _m0335, _m0337, _m0336, _m0338, _m0382)
        _m0112.grad_helper._m0094(_m0143, _m0112.material)
        cls._m0061(_m0112, _m0212, ix1, iy1, ix2, iy2, _m0425)
