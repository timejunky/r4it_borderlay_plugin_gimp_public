# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import math
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
from selection import SelectionManager

class _m0013:

    @staticmethod
    def _m0060(r_out, r_in, _m0364):
        if r_out <= 0.5 and r_in <= 0.5:
            return 0.0
        t = max(0.0, min(1.0, float(_m0364)))
        return max(0.0, r_out * (1.0 - t) + r_in * t)

    @classmethod
    def _m0425(cls, image, _m0130, _m0298, _m0524, _m0608, _m0607, r_out, r_in, _m0613, _m0121, _m0432, _m0369, _m0371, _m0370, _m0372):
        ox1, oy1, ox2, oy2 = _m0608
        ix1, iy1, ix2, iy2 = _m0607
        SelectionManager.select_zone_ring(image, _m0608, _m0607, r_out, r_in)
        if Gimp.Selection.is_empty(image):
            return
        _m0612 = Gimp.Selection.save(image)
        try:
            _m0130._m0235(_m0524, (142, 142, 142), (98, 98, 98), (48, 48, 48), _m0369, _m0371, _m0370, _m0372, 0.44)
            _m0293 = max(2, _m0613 // 2)
            for s in range(_m0293):
                t = s / float(max(1, _m0293 - 1))
                _m0188 = math.sin(t * (math.pi / 2.0))
                _m0147 = (ox1 + s, oy1 + s, ox2 - s, oy2 - s)
                _m0146 = (ix1 - s, iy1 - s, ix2 + s, iy2 + s)
                if _m0146[0] <= _m0147[0] or _m0146[1] <= _m0147[1]:
                    break
                _m0364 = s / float(_m0613)
                _m0505 = cls._m0060(r_out, r_in, _m0364)
                _m0494 = cls._m0060(r_out, r_in, 1.0 - _m0364)
                SelectionManager.select_zone_ring(image, _m0147, _m0146, _m0505, _m0494)
                if _m0612 is not None:
                    image.select_item(Gimp.ChannelOps.INTERSECT, _m0612)
                if not Gimp.Selection.is_empty(image):
                    _m0268 = round(_m0121 + (_m0432 - _m0121) * _m0188)
                    _m0130._m0234(_m0298, _m0268)
            for frac, hi_l, mid_l, lo_l in ((0.18, 188, 128, 64), (0.34, 228, 152, 82)):
                m = max(1, round(_m0613 * frac))
                _m0363 = m / float(_m0613)
                _m0147 = (ox1 + m, oy1 + m, ox2 - m, oy2 - m)
                _m0146 = (ix1 - m, iy1 - m, ix2 + m, iy2 + m)
                if _m0146[0] > _m0147[0] and _m0146[1] > _m0147[1]:
                    _m0505 = cls._m0060(r_out, r_in, _m0363)
                    _m0494 = cls._m0060(r_out, r_in, 1.0 - _m0363)
                    SelectionManager.select_zone_ring(image, _m0147, _m0146, _m0505, _m0494)
                    if _m0612 is not None:
                        image.select_item(Gimp.ChannelOps.INTERSECT, _m0612)
                    if not Gimp.Selection.is_empty(image):
                        _m0130._m0235(_m0524, (hi_l, hi_l, hi_l), (mid_l, mid_l, mid_l), (lo_l, lo_l, lo_l), _m0369, _m0371, _m0370, _m0372, 0.42)
        finally:
            if _m0612 is not None:
                image.remove_channel(_m0612)

    @staticmethod
    def _m0236(image, _m0130, layer, _m0608, _m0607, _m0302, _m0355, _m0333=False):
        ox1, oy1, ox2, oy2 = _m0608
        ix1, iy1, ix2, iy2 = _m0607
        _m0603 = (float(ox1) + float(ox2)) / 2.0
        _m0605 = (float(oy1) + float(oy2)) / 2.0
        mat = getattr(_m0130, 'material', 'gold')
        if _m0333:
            _m0267 = max(16, round(_m0355 * 0.85))
            _m0266 = max(22, round(_m0355 * 0.75 + _m0302 * 0.18))
            _m0265 = max(28, round(_m0355 * 0.62 + _m0302 * 0.38))
            _m0257 = max(20, round(_m0355 * 0.78 + _m0302 * 0.1))
            _m0256 = max(28, round(_m0355 * 0.66 + _m0302 * 0.28))
            _m0255 = max(36, round(_m0355 * 0.52 + _m0302 * 0.48))
            _m0262 = round(_m0355 * 0.38 + _m0302 * 0.62)
            _m0261 = round(_m0355 * 0.22 + _m0302 * 0.78)
            _m0260 = _m0302
            _m0252 = round(_m0355 * 0.46 + _m0302 * 0.54)
            _m0251 = round(_m0355 * 0.3 + _m0302 * 0.7)
            _m0250 = round(_m0355 * 0.16 + _m0302 * 0.84)
        elif mat == 'chrom':
            _m0267, _m0266, _m0265 = (108, 218, 252)
            _m0257, _m0256, _m0255 = (84, 184, 236)
            _m0262, _m0261, _m0260 = (18, 72, 164)
            _m0252, _m0251, _m0250 = (14, 54, 142)
        elif mat == 'edelstahl':
            _m0267, _m0266, _m0265 = (144, 212, 244)
            _m0257, _m0256, _m0255 = (118, 178, 218)
            _m0262, _m0261, _m0260 = (42, 88, 146)
            _m0252, _m0251, _m0250 = (32, 68, 122)
        else:
            _m0267 = round(_m0302 * 0.88 + _m0355 * 0.12)
            _m0266 = round(_m0302 * 0.95 + _m0355 * 0.05)
            _m0265 = _m0302
            _m0257 = round(_m0302 * 0.68 + _m0355 * 0.32)
            _m0256 = round(_m0302 * 0.76 + _m0355 * 0.24)
            _m0255 = round(_m0302 * 0.84 + _m0355 * 0.16)
            _m0262 = round(_m0302 * 0.24 + _m0355 * 0.76)
            _m0261 = round(_m0302 * 0.32 + _m0355 * 0.68)
            _m0260 = round(_m0302 * 0.4 + _m0355 * 0.6)
            _m0252 = _m0355
            _m0251 = round(_m0302 * 0.1 + _m0355 * 0.9)
            _m0250 = round(_m0302 * 0.2 + _m0355 * 0.8)
        _m0615 = Gimp.Selection.save(image)
        if _m0615 is None:
            raise RuntimeError('Die Zonenauswahl für die 45°-Gehrung konnte nicht gespeichert werden.')
        try:
            Gimp.Selection.none(image)
            image.select_rectangle(Gimp.ChannelOps.REPLACE, float(ox1), float(oy1), float(ox2 - ox1), float(_m0605 - oy1 + 2.0))
            image.select_item(Gimp.ChannelOps.INTERSECT, _m0615)
            if not Gimp.Selection.is_empty(image):
                _m0130._m0235(layer, (_m0267,) * 3, (_m0266,) * 3, (_m0265,) * 3, _m0603, float(oy1), _m0603, float(iy1), _m0433=0.46)
            Gimp.Selection.none(image)
            image.select_rectangle(Gimp.ChannelOps.REPLACE, float(ox1), float(_m0605 - 2.0), float(ox2 - ox1), float(oy2 - _m0605 + 2.0))
            image.select_item(Gimp.ChannelOps.INTERSECT, _m0615)
            if not Gimp.Selection.is_empty(image):
                _m0130._m0235(layer, (_m0252,) * 3, (_m0251,) * 3, (_m0250,) * 3, _m0603, float(oy2), _m0603, float(iy2), _m0433=0.48)
            _m0548 = [([ox1, oy1, ix1, iy1, ix1, iy2, ox1, oy2], (_m0257,) * 3, (_m0256,) * 3, (_m0255,) * 3, float(ox1), _m0605, float(ix1), _m0605), ([ix2, iy1, ox2, oy1, ox2, oy2, ix2, iy2], (_m0262,) * 3, (_m0261,) * 3, (_m0260,) * 3, float(ox2), _m0605, float(ix2), _m0605)]
            for pts, col_start, col_mid, col_end, _m0286, _m0288, _m0287, _m0289 in _m0548:
                Gimp.Selection.none(image)
                if not image.select_polygon(Gimp.ChannelOps.REPLACE, [float(p) for p in pts]):
                    raise RuntimeError('Das Trapez-Polygon für die 45°-Gehrung konnte nicht erstellt werden.')
                if not image.select_item(Gimp.ChannelOps.INTERSECT, _m0615):
                    raise RuntimeError('Die Schnittmenge für das Gehrungs-Trapez konnte nicht gebildet werden.')
                if Gimp.Selection.is_empty(image):
                    continue
                _m0130._m0235(layer, col_start, col_mid, col_end, _m0286, _m0288, _m0287, _m0289, _m0433=0.46)
        finally:
            Gimp.Selection.none(image)
            image.select_item(Gimp.ChannelOps.REPLACE, _m0615)
            image.remove_channel(_m0615)

    @staticmethod
    def _m0204(image, outer_box, inner_box, _m0130, _m0524, _m0504):
        return
