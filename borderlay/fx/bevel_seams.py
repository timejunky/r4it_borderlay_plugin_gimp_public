# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
import config
from fx.bevel_center import _m0000
from selection import SelectionManager
from utils import _m0002

class _m0001:

    @staticmethod
    def _m0448(_m0112, _m0568):
        if _m0112.is_glass:
            return
        from community_material_seal import apply_community_materials
        apply_community_materials()
        for zone, _m0562, _m0561, r_out, r_in, _ in _m0568:
            mat = zone['mat']
            if mat in ('main', 'shadow', '', None) or mat == _m0112.material:
                continue
            SelectionManager.select_zone_ring(_m0112.image, _m0562, _m0561, r_out, r_in)
            if Gimp.Selection.is_empty(_m0112.image):
                continue
            if mat == 'inlay':
                _m0287 = _m0002._m0369(_m0112.image, _m0112.group, 'Inlay Groove Color', 82.0, Gimp.LayerMode.MULTIPLY)
                Gimp.context_set_foreground(_m0002._m0269(_m0112.inlay_rgb))
                _m0287.edit_fill(Gimp.FillType.FOREGROUND)
            elif mat in config.METALS:
                _m0538 = Gimp.LayerMode.HSL_COLOR if hasattr(Gimp.LayerMode, 'HSL_COLOR') else Gimp.LayerMode.OVERLAY
                _m0537 = _m0002._m0369(_m0112.image, _m0112.group, f'Alloy Tint ({mat})', 42.0, _m0538)
                Gimp.context_set_foreground(_m0002._m0269(config.sample_grad_stops(config.METALS[mat], 5)[2]))
                _m0537.edit_fill(Gimp.FillType.FOREGROUND)

    @staticmethod
    def _m0066(_m0112, _m0568, _m0484, _m0306, _m0517, _m0355, _m0169, _m0171, ox1, oy1, w, h, _m0335, _m0337, _m0336, _m0338):
        for idx, (zone, _m0562, _m0561, r_out, r_in, _m0567) in enumerate(_m0568):
            kind = zone['kind']
            if kind == 'bevel_out' and _m0567 >= 6 and (not _m0306):
                _m0571, _m0573, _m0572, _m0574 = _m0561
                _m0165 = (_m0571 - 2, _m0573 - 2, _m0572 + 2, _m0574 + 2)
                SelectionManager.select_zone_ring(_m0112.image, _m0165, _m0561, max(0.0, r_in + 1.0), r_in)
                if not Gimp.Selection.is_empty(_m0112.image):
                    _m0112._m0210(_m0484, _m0517, _m0355, _m0169, float(ox1 + w * 0.56), float(oy1), float(ox1), float(oy1 + h * 0.48), _m0398=0.4)
            elif kind == 'groove':
                SelectionManager.select_zone_ring(_m0112.image, _m0562, _m0561, r_out, r_in)
                if not Gimp.Selection.is_empty(_m0112.image):
                    _m0227 = _m0112._m0073('inlay' if zone['mat'] == 'inlay' else 'shadow')
                    _m0112._m0210(_m0484, _m0171, _m0227[0], _m0171, _m0335, _m0337, _m0336, _m0338, 0.45)
            elif kind == 'flat' and _m0567 >= 8 and (not _m0306):
                _m0571, _m0573, _m0572, _m0574 = _m0562
                _m0491 = (_m0571 + 2, _m0573 + 2, _m0572 - 2, _m0574 - 2)
                _m0435 = r_out * (1.0 - 2.0 / float(_m0567)) + r_in * (2.0 / float(_m0567))
                SelectionManager.select_zone_ring(_m0112.image, _m0562, _m0491, r_out, max(0.0, _m0435))
                if not Gimp.Selection.is_empty(_m0112.image):
                    _m0112._m0210(_m0484, _m0517, _m0355, _m0169, float(ox1 + w * 0.56), float(oy1), float(ox1), float(oy1 + h * 0.48), _m0398=0.38)
            elif kind in ('step', 'pipe') and idx == len(_m0568) - 1:
                _m0571, _m0573, _m0572, _m0574 = _m0562
                _m0318 = (_m0571 + 2, _m0573 + 2, _m0572 - 2, _m0574 - 2)
                SelectionManager.select_zone_ring(_m0112.image, _m0562, _m0318, r_out, max(0.0, r_out - 1.5))
                if not Gimp.Selection.is_empty(_m0112.image):
                    _m0112._m0210(_m0484, _m0517, _m0317, _m0169, _m0335, _m0337, _m0336, _m0338, 0.46)

    @staticmethod
    def _m0446(_m0112, _m0568, _m0434, _m0335, _m0337, _m0336, _m0338, _m0306=False):
        ox1, oy1, ox2, oy2 = _m0112.outer_box
        ix1, iy1, ix2, iy2 = _m0112.inner_box
        w = float(ox2 - ox1)
        h = float(oy2 - oy1)
        _m0169, _m0355, _m0317 = _m0112._m0073('main')
        _m0171 = tuple((round(c * 0.38) for c in _m0169))
        _m0517 = (255, 255, 255) if _m0112.is_glass or _m0112.material in ('titan', 'platinum', 'chrom', 'edelstahl', 'aluminium') else _m0000._m0315(_m0317, (255, 250, 232), 0.45)
        _m0485 = Gimp.LayerMode.SOFTLIGHT_LEGACY if hasattr(Gimp.LayerMode, 'SOFTLIGHT_LEGACY') else Gimp.LayerMode.OVERLAY
        _m0486 = 44.0 if _m0306 else 58.0
        _m0484 = _m0002._m0369(_m0112.image, _m0112.group, 'Crisp Facet & Terrace Breaklines', _m0486, _m0485)
        _m0380 = (ox1 + 2, oy1 + 2, ox2 - 2, oy2 - 2)
        SelectionManager.select_zone_ring(_m0112.image, _m0112.outer_box, _m0380, _m0112.outer_radius, max(0.0, _m0112.outer_radius - 2.0))
        if not Gimp.Selection.is_empty(_m0112.image):
            _m0112._m0210(_m0484, _m0355, _m0169, _m0171, _m0335, _m0337, _m0336, _m0338, 0.4)
        _m0001._m0066(_m0112, _m0568, _m0484, _m0306, _m0517, _m0355, _m0169, _m0171, ox1, oy1, w, h, _m0335, _m0337, _m0336, _m0338)
        _m0294 = (ix1 - 2, iy1 - 2, ix2 + 2, iy2 + 2)
        SelectionManager.select_zone_ring(_m0112.image, _m0294, _m0112.inner_box, max(0.0, _m0434 + 1.5), _m0434)
        if not Gimp.Selection.is_empty(_m0112.image):
            _m0112._m0210(_m0484, _m0171, _m0169, _m0171, _m0335, _m0337, _m0336, _m0338, 0.5)
        Gimp.Selection.none(_m0112.image)
        _m0115 = 0.45 if _m0306 else 0.75
        _m0002._m0489(_m0484, 'gegl:gaussian-blur', **{'std-dev-x': _m0115, 'std-dev-y': _m0115})
