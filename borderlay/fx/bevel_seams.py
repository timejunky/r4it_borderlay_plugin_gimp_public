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
    def _m0485(_m0130, _m0614):
        if _m0130.is_glass:
            return
        from community_material_seal import apply_community_materials
        apply_community_materials()
        for zone, _m0608, _m0607, r_out, r_in, _ in _m0614:
            mat = zone['mat']
            if mat in ('main', 'shadow', '', None) or mat == _m0130.material:
                continue
            SelectionManager.select_zone_ring(_m0130.image, _m0608, _m0607, r_out, r_in)
            if Gimp.Selection.is_empty(_m0130.image):
                continue
            if mat == 'inlay':
                _m0317 = _m0002._m0404(_m0130.image, _m0130.group, 'Inlay Groove Color', 82.0, Gimp.LayerMode.MULTIPLY)
                Gimp.context_set_foreground(_m0002._m0299(_m0130.inlay_rgb))
                _m0317.edit_fill(Gimp.FillType.FOREGROUND)
            elif mat in config.METALS:
                _m0582 = Gimp.LayerMode.HSL_COLOR if hasattr(Gimp.LayerMode, 'HSL_COLOR') else Gimp.LayerMode.OVERLAY
                _m0581 = _m0002._m0404(_m0130.image, _m0130.group, f'Alloy Tint ({mat})', 42.0, _m0582)
                Gimp.context_set_foreground(_m0002._m0299(config.sample_grad_stops(config.METALS[mat], 5)[2]))
                _m0581.edit_fill(Gimp.FillType.FOREGROUND)

    @staticmethod
    def _m0078(_m0130, _m0614, _m0525, _m0338, _m0558, _m0390, _m0190, _m0192, ox1, oy1, w, h, _m0369, _m0371, _m0370, _m0372):
        for idx, (zone, _m0608, _m0607, r_out, r_in, _m0613) in enumerate(_m0614):
            kind = zone['kind']
            if kind == 'bevel_out' and _m0613 >= 6 and (not _m0338):
                _m0617, _m0619, _m0618, _m0620 = _m0607
                _m0184 = (_m0617 - 2, _m0619 - 2, _m0618 + 2, _m0620 + 2)
                SelectionManager.select_zone_ring(_m0130.image, _m0184, _m0607, max(0.0, r_in + 1.0), r_in)
                if not Gimp.Selection.is_empty(_m0130.image):
                    _m0130._m0235(_m0525, _m0558, _m0390, _m0190, float(ox1 + w * 0.56), float(oy1), float(ox1), float(oy1 + h * 0.48), _m0433=0.4)
            elif kind == 'groove':
                SelectionManager.select_zone_ring(_m0130.image, _m0608, _m0607, r_out, r_in)
                if not Gimp.Selection.is_empty(_m0130.image):
                    _m0253 = _m0130._m0086('inlay' if zone['mat'] == 'inlay' else 'shadow')
                    _m0130._m0235(_m0525, _m0192, _m0253[0], _m0192, _m0369, _m0371, _m0370, _m0372, 0.45)
            elif kind == 'flat' and _m0613 >= 8 and (not _m0338):
                _m0617, _m0619, _m0618, _m0620 = _m0608
                _m0532 = (_m0617 + 2, _m0619 + 2, _m0618 - 2, _m0620 - 2)
                _m0471 = r_out * (1.0 - 2.0 / float(_m0613)) + r_in * (2.0 / float(_m0613))
                SelectionManager.select_zone_ring(_m0130.image, _m0608, _m0532, r_out, max(0.0, _m0471))
                if not Gimp.Selection.is_empty(_m0130.image):
                    _m0130._m0235(_m0525, _m0558, _m0390, _m0190, float(ox1 + w * 0.56), float(oy1), float(ox1), float(oy1 + h * 0.48), _m0433=0.38)
            elif kind in ('step', 'pipe') and idx == len(_m0614) - 1:
                _m0617, _m0619, _m0618, _m0620 = _m0608
                _m0352 = (_m0617 + 2, _m0619 + 2, _m0618 - 2, _m0620 - 2)
                SelectionManager.select_zone_ring(_m0130.image, _m0608, _m0352, r_out, max(0.0, r_out - 1.5))
                if not Gimp.Selection.is_empty(_m0130.image):
                    _m0130._m0235(_m0525, _m0558, _m0351, _m0190, _m0369, _m0371, _m0370, _m0372, 0.46)

    @staticmethod
    def _m0483(_m0130, _m0614, _m0470, _m0369, _m0371, _m0370, _m0372, _m0338=False):
        ox1, oy1, ox2, oy2 = _m0130.outer_box
        ix1, iy1, ix2, iy2 = _m0130.inner_box
        w = float(ox2 - ox1)
        h = float(oy2 - oy1)
        _m0190, _m0390, _m0351 = _m0130._m0086('main')
        _m0192 = tuple((round(c * 0.38) for c in _m0190))
        _m0558 = (255, 255, 255) if _m0130.is_glass or _m0130.material in ('titan', 'platinum', 'chrom', 'edelstahl', 'aluminium') else _m0000._m0348(_m0351, (255, 250, 232), 0.45)
        _m0526 = Gimp.LayerMode.SOFTLIGHT_LEGACY if hasattr(Gimp.LayerMode, 'SOFTLIGHT_LEGACY') else Gimp.LayerMode.OVERLAY
        _m0527 = 44.0 if _m0338 else 58.0
        _m0525 = _m0002._m0404(_m0130.image, _m0130.group, 'Crisp Facet & Terrace Breaklines', _m0527, _m0526)
        _m0415 = (ox1 + 2, oy1 + 2, ox2 - 2, oy2 - 2)
        SelectionManager.select_zone_ring(_m0130.image, _m0130.outer_box, _m0415, _m0130.outer_radius, max(0.0, _m0130.outer_radius - 2.0))
        if not Gimp.Selection.is_empty(_m0130.image):
            _m0130._m0235(_m0525, _m0390, _m0190, _m0192, _m0369, _m0371, _m0370, _m0372, 0.4)
        _m0001._m0078(_m0130, _m0614, _m0525, _m0338, _m0558, _m0390, _m0190, _m0192, ox1, oy1, w, h, _m0369, _m0371, _m0370, _m0372)
        _m0324 = (ix1 - 2, iy1 - 2, ix2 + 2, iy2 + 2)
        SelectionManager.select_zone_ring(_m0130.image, _m0324, _m0130.inner_box, max(0.0, _m0470 + 1.5), _m0470)
        if not Gimp.Selection.is_empty(_m0130.image):
            _m0130._m0235(_m0525, _m0192, _m0190, _m0192, _m0369, _m0371, _m0370, _m0372, 0.5)
        Gimp.Selection.none(_m0130.image)
        _m0133 = 0.45 if _m0338 else 0.75
        _m0002._m0530(_m0525, 'gegl:gaussian-blur', **{'std-dev-x': _m0133, 'std-dev-y': _m0133})
