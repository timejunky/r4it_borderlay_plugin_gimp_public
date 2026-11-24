# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import math
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
from selection import SelectionManager

class _m0012:

    @staticmethod
    def _m0050(r_out, r_in, _m0330):
        if r_out <= 0.5 and r_in <= 0.5:
            return 0.0
        t = max(0.0, min(1.0, float(_m0330)))
        return max(0.0, r_out * (1.0 - t) + r_in * t)

    @classmethod
    def _m0390(cls, image, _m0112, _m0268, _m0483, _m0562, _m0561, r_out, r_in, _m0567, _m0103, _m0397, _m0335, _m0337, _m0336, _m0338):
        ox1, oy1, ox2, oy2 = _m0562
        ix1, iy1, ix2, iy2 = _m0561
        SelectionManager.select_zone_ring(image, _m0562, _m0561, r_out, r_in)
        if Gimp.Selection.is_empty(image):
            return
        _m0566 = Gimp.Selection.save(image)
        try:
            _m0112._m0210(_m0483, (142, 142, 142), (98, 98, 98), (48, 48, 48), _m0335, _m0337, _m0336, _m0338, 0.44)
            _m0264 = max(2, _m0567 // 2)
            for s in range(_m0264):
                t = s / float(max(1, _m0264 - 1))
                _m0167 = math.sin(t * (math.pi / 2.0))
                _m0128 = (ox1 + s, oy1 + s, ox2 - s, oy2 - s)
                _m0127 = (ix1 - s, iy1 - s, ix2 + s, iy2 + s)
                if _m0127[0] <= _m0128[0] or _m0127[1] <= _m0128[1]:
                    break
                _m0330 = s / float(_m0567)
                _m0465 = cls._m0050(r_out, r_in, _m0330)
                _m0454 = cls._m0050(r_out, r_in, 1.0 - _m0330)
                SelectionManager.select_zone_ring(image, _m0128, _m0127, _m0465, _m0454)
                if _m0566 is not None:
                    image.select_item(Gimp.ChannelOps.INTERSECT, _m0566)
                if not Gimp.Selection.is_empty(image):
                    _m0242 = round(_m0103 + (_m0397 - _m0103) * _m0167)
                    _m0112._m0209(_m0268, _m0242)
            for frac, hi_l, mid_l, lo_l in ((0.18, 188, 128, 64), (0.34, 228, 152, 82)):
                m = max(1, round(_m0567 * frac))
                _m0329 = m / float(_m0567)
                _m0128 = (ox1 + m, oy1 + m, ox2 - m, oy2 - m)
                _m0127 = (ix1 - m, iy1 - m, ix2 + m, iy2 + m)
                if _m0127[0] > _m0128[0] and _m0127[1] > _m0128[1]:
                    _m0465 = cls._m0050(r_out, r_in, _m0329)
                    _m0454 = cls._m0050(r_out, r_in, 1.0 - _m0329)
                    SelectionManager.select_zone_ring(image, _m0128, _m0127, _m0465, _m0454)
                    if _m0566 is not None:
                        image.select_item(Gimp.ChannelOps.INTERSECT, _m0566)
                    if not Gimp.Selection.is_empty(image):
                        _m0112._m0210(_m0483, (hi_l, hi_l, hi_l), (mid_l, mid_l, mid_l), (lo_l, lo_l, lo_l), _m0335, _m0337, _m0336, _m0338, 0.42)
        finally:
            if _m0566 is not None:
                image.remove_channel(_m0566)

    @staticmethod
    def _m0211(image, _m0112, layer, _m0562, _m0561, _m0272, _m0321, _m0302=False):
        ox1, oy1, ox2, oy2 = _m0562
        ix1, iy1, ix2, iy2 = _m0561
        _m0557 = (float(ox1) + float(ox2)) / 2.0
        _m0559 = (float(oy1) + float(oy2)) / 2.0
        mat = getattr(_m0112, 'material', 'gold')
        if _m0302:
            _m0241 = max(16, round(_m0321 * 0.85))
            _m0240 = max(22, round(_m0321 * 0.75 + _m0272 * 0.18))
            _m0239 = max(28, round(_m0321 * 0.62 + _m0272 * 0.38))
            _m0231 = max(20, round(_m0321 * 0.78 + _m0272 * 0.1))
            _m0230 = max(28, round(_m0321 * 0.66 + _m0272 * 0.28))
            _m0229 = max(36, round(_m0321 * 0.52 + _m0272 * 0.48))
            _m0236 = round(_m0321 * 0.38 + _m0272 * 0.62)
            _m0235 = round(_m0321 * 0.22 + _m0272 * 0.78)
            _m0234 = _m0272
            _m0226 = round(_m0321 * 0.46 + _m0272 * 0.54)
            _m0225 = round(_m0321 * 0.3 + _m0272 * 0.7)
            _m0224 = round(_m0321 * 0.16 + _m0272 * 0.84)
        elif mat == 'chrom':
            _m0241, _m0240, _m0239 = (108, 218, 252)
            _m0231, _m0230, _m0229 = (84, 184, 236)
            _m0236, _m0235, _m0234 = (18, 72, 164)
            _m0226, _m0225, _m0224 = (14, 54, 142)
        elif mat == 'edelstahl':
            _m0241, _m0240, _m0239 = (144, 212, 244)
            _m0231, _m0230, _m0229 = (118, 178, 218)
            _m0236, _m0235, _m0234 = (42, 88, 146)
            _m0226, _m0225, _m0224 = (32, 68, 122)
        else:
            _m0241 = round(_m0272 * 0.88 + _m0321 * 0.12)
            _m0240 = round(_m0272 * 0.95 + _m0321 * 0.05)
            _m0239 = _m0272
            _m0231 = round(_m0272 * 0.68 + _m0321 * 0.32)
            _m0230 = round(_m0272 * 0.76 + _m0321 * 0.24)
            _m0229 = round(_m0272 * 0.84 + _m0321 * 0.16)
            _m0236 = round(_m0272 * 0.24 + _m0321 * 0.76)
            _m0235 = round(_m0272 * 0.32 + _m0321 * 0.68)
            _m0234 = round(_m0272 * 0.4 + _m0321 * 0.6)
            _m0226 = _m0321
            _m0225 = round(_m0272 * 0.1 + _m0321 * 0.9)
            _m0224 = round(_m0272 * 0.2 + _m0321 * 0.8)
        _m0569 = Gimp.Selection.save(image)
        if _m0569 is None:
            raise RuntimeError('Die Zonenauswahl für die 45°-Gehrung konnte nicht gespeichert werden.')
        try:
            Gimp.Selection.none(image)
            image.select_rectangle(Gimp.ChannelOps.REPLACE, float(ox1), float(oy1), float(ox2 - ox1), float(_m0559 - oy1 + 2.0))
            image.select_item(Gimp.ChannelOps.INTERSECT, _m0569)
            if not Gimp.Selection.is_empty(image):
                _m0112._m0210(layer, (_m0241,) * 3, (_m0240,) * 3, (_m0239,) * 3, _m0557, float(oy1), _m0557, float(iy1), _m0398=0.46)
            Gimp.Selection.none(image)
            image.select_rectangle(Gimp.ChannelOps.REPLACE, float(ox1), float(_m0559 - 2.0), float(ox2 - ox1), float(oy2 - _m0559 + 2.0))
            image.select_item(Gimp.ChannelOps.INTERSECT, _m0569)
            if not Gimp.Selection.is_empty(image):
                _m0112._m0210(layer, (_m0226,) * 3, (_m0225,) * 3, (_m0224,) * 3, _m0557, float(oy2), _m0557, float(iy2), _m0398=0.48)
            _m0507 = [([ox1, oy1, ix1, iy1, ix1, iy2, ox1, oy2], (_m0231,) * 3, (_m0230,) * 3, (_m0229,) * 3, float(ox1), _m0559, float(ix1), _m0559), ([ix2, iy1, ox2, oy1, ox2, oy2, ix2, iy2], (_m0236,) * 3, (_m0235,) * 3, (_m0234,) * 3, float(ox2), _m0559, float(ix2), _m0559)]
            for pts, col_start, col_mid, col_end, _m0257, _m0259, _m0258, _m0260 in _m0507:
                Gimp.Selection.none(image)
                if not image.select_polygon(Gimp.ChannelOps.REPLACE, [float(p) for p in pts]):
                    raise RuntimeError('Das Trapez-Polygon für die 45°-Gehrung konnte nicht erstellt werden.')
                if not image.select_item(Gimp.ChannelOps.INTERSECT, _m0569):
                    raise RuntimeError('Die Schnittmenge für das Gehrungs-Trapez konnte nicht gebildet werden.')
                if Gimp.Selection.is_empty(image):
                    continue
                _m0112._m0210(layer, col_start, col_mid, col_end, _m0257, _m0259, _m0258, _m0260, _m0398=0.46)
        finally:
            Gimp.Selection.none(image)
            image.select_item(Gimp.ChannelOps.REPLACE, _m0569)
            image.remove_channel(_m0569)

    @staticmethod
    def _m0183(image, outer_box, inner_box, _m0112, _m0483, _m0464):
        return
