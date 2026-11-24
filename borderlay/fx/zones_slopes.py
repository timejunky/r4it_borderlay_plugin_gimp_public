# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import math
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
from selection import SelectionManager

class _m0013:

    @staticmethod
    def _m0050(r_out, r_in, _m0330):
        if r_out <= 0.5 and r_in <= 0.5:
            return 0.0
        t = max(0.0, min(1.0, float(_m0330)))
        return max(0.0, r_out * (1.0 - t) + r_in * t)

    @classmethod
    def _m0393(cls, image, _m0112, _m0268, _m0483, _m0562, _m0561, r_out, r_in, _m0567, _m0551, _m0335, _m0337, _m0336, _m0338):
        ox1, oy1, ox2, oy2 = _m0562
        ix1, iy1, ix2, iy2 = _m0561
        SelectionManager.select_zone_ring(image, _m0562, _m0561, r_out, r_in)
        if Gimp.Selection.is_empty(image):
            return
        _m0112._m0210(_m0483, (22, 22, 22), (14, 14, 14), (6, 6, 6), _m0335, _m0337, _m0336, _m0338, _m0398=0.45)
        _m0461 = min(180, _m0551 + 24)
        _m0112._m0209(_m0268, _m0461)
        if _m0567 >= 3:
            _m0136 = (ox1 + 1, oy1 + 1, ox2 - 1, oy2 - 1)
            _m0133 = (ix1 - 1, iy1 - 1, ix2 + 1, iy2 + 1)
            if _m0133[0] > _m0136[0] and _m0133[1] > _m0136[1]:
                _m0330 = 1.0 / float(_m0567)
                _m0466 = cls._m0050(r_out, r_in, _m0330)
                _m0455 = cls._m0050(r_out, r_in, 1.0 - _m0330)
                SelectionManager.select_zone_ring(image, _m0136, _m0133, _m0466, _m0455)
                if not Gimp.Selection.is_empty(image):
                    _m0112._m0209(_m0268, _m0551)
        else:
            _m0112._m0209(_m0268, _m0551)

    @classmethod
    def _m0388(cls, image, _m0363, _m0112, _m0268, _m0483, _m0562, _m0561, r_out, r_in, _m0567, is_glass=False):
        ox1, oy1, ox2, oy2 = _m0562
        w = float(ox2 - ox1)
        _m0307 = r_out <= 1.0 and r_in <= 1.0
        SelectionManager.select_zone_ring(image, _m0562, _m0561, r_out, r_in)
        if Gimp.Selection.is_empty(image):
            return
        if _m0307:
            _m0112._m0209(_m0268, _m0112._m0480(64.0))
            _m0272 = 215 if is_glass else 196
            _m0321 = 48 if is_glass else 42
            _m0363._m0211(image, _m0112, _m0483, _m0562, _m0561, _m0272=_m0272, _m0321=_m0321, _m0302=False)
            return
        _m0566 = Gimp.Selection.save(image)
        try:
            _m0333 = _m0112._m0480(14.0)
            _m0279 = _m0112._m0480(76.0)
            _m0112._m0209(_m0268, _m0333)
            _m0112._m0210(_m0483, (142, 142, 142), (98, 98, 98), (26, 26, 26), float(ox1 + w * 0.48), float(oy1), float(ox2 - w * 0.12), float(oy2), _m0398=0.44)
            _m0522 = 2 if _m0567 >= 12 else 1
            for m0 in range(_m0522, _m0567, _m0522):
                t = m0 / float(_m0567)
                _m0128 = (ox1 + m0, oy1 + m0, ox2 - m0, oy2 - m0)
                if _m0128[2] <= _m0561[2] or _m0128[3] <= _m0561[3]:
                    break
                _m0465 = cls._m0050(r_out, r_in, t)
                SelectionManager.select_zone_ring(image, _m0128, _m0561, _m0465, r_in)
                if _m0566 is not None:
                    image.select_item(Gimp.ChannelOps.INTERSECT, _m0566)
                if Gimp.Selection.is_empty(image):
                    continue
                _m0228 = round(_m0333 + (_m0279 - _m0333) * t)
                _m0112._m0209(_m0268, _m0228)
                if is_glass:
                    _m0112._m0209(_m0483, round(75 + 135 * t))
                else:
                    _m0437 = math.pow(t, 0.85)
                    _m0238 = round(108 + 96 * _m0437)
                    _m0232 = round(84 + 54 * _m0437)
                    _m0223 = round(24 + 28 * _m0437)
                    _m0112._m0210(_m0483, (_m0238, _m0238, _m0238), (_m0232, _m0232, _m0232), (_m0223, _m0223, _m0223), float(ox1 + w * 0.48), float(oy1), float(ox2 - w * 0.12), float(oy2), _m0398=0.44)
        finally:
            if _m0566 is not None:
                image.remove_channel(_m0566)

    @classmethod
    def _m0063(cls, image, _m0363, _m0112, _m0268, _m0483, _m0562, _m0561, is_glass):
        _m0112._m0209(_m0268, _m0112._m0480(24.0))
        if is_glass:
            _m0363._m0211(image, _m0112, _m0483, _m0562, _m0561, _m0272=228, _m0321=164, _m0302=False)
        else:
            _m0363._m0211(image, _m0112, _m0483, _m0562, _m0561, _m0272=112, _m0321=20, _m0302=True)

    @classmethod
    def _m0062(cls, image, _m0363, _m0112, _m0268, _m0483, _m0566, _m0562, _m0561, r_out, r_in, _m0567, _m0335, _m0337, _m0336, _m0338, is_glass, ox1, oy1, ox2, oy2, ix1, iy1, ix2, iy2, w):
        _m0543 = _m0112._m0480(86.0)
        _m0120 = _m0112._m0480(26.0)
        _m0112._m0209(_m0268, _m0120)
        if is_glass:
            _m0112._m0209(_m0483, 210)
        else:
            _m0112._m0210(_m0483, (174, 174, 174), (106, 106, 106), (36, 36, 36), float(ox1 + w * 0.52), float(oy1), float(ox2 - w * 0.12), float(oy2), _m0398=0.42)
        _m0522 = 2 if _m0567 >= 12 else 1
        for m_in in range(_m0567 - _m0522, 0, -_m0522):
            t = m_in / float(_m0567)
            _m0127 = (ox1 + m_in, oy1 + m_in, ox2 - m_in, oy2 - m_in)
            if _m0127[0] <= ox1 or _m0127[1] <= oy1:
                continue
            _m0454 = cls._m0050(r_out, r_in, t)
            SelectionManager.select_zone_ring(image, _m0562, _m0127, r_out, _m0454)
            if _m0566 is not None:
                image.select_item(Gimp.ChannelOps.INTERSECT, _m0566)
            if Gimp.Selection.is_empty(image):
                continue
            _m0228 = round(_m0543 - (_m0543 - _m0120) * t)
            _m0112._m0209(_m0268, _m0228)
            if is_glass:
                _m0112._m0209(_m0483, round(155 + 60 * t))
            else:
                _m0511 = math.pow(t, 0.8)
                _m0238 = round(124 + 48 * _m0511)
                _m0232 = round(80 + 28 * _m0511)
                _m0223 = round(32 + 24 * _m0511)
                _m0112._m0210(_m0483, (_m0238, _m0238, _m0238), (_m0232, _m0232, _m0232), (_m0223, _m0223, _m0223), float(ox1 + w * 0.52), float(oy1), float(ox2 - w * 0.12), float(oy2), _m0398=0.44)
        if not is_glass and _m0567 >= 6:
            _m0487 = max(3, min(4, round(_m0567 * 0.18)))
            _m0381 = (ox1 + _m0487, oy1 + _m0487, ox2 - _m0487, oy2 - _m0487)
            _m0433 = cls._m0050(r_out, r_in, _m0487 / float(_m0567))
            SelectionManager.select_zone_ring(image, _m0562, _m0381, r_out, _m0433)
            if _m0566 is not None:
                image.select_item(Gimp.ChannelOps.INTERSECT, _m0566)
            if not Gimp.Selection.is_empty(image):
                _m0112._m0210(_m0483, (18, 18, 18), (12, 12, 12), (6, 6, 6), _m0335, _m0337, _m0336, _m0338, 0.45)
            _m0296 = (ix1 - _m0487, iy1 - _m0487, ix2 + _m0487, iy2 + _m0487)
            _m0429 = cls._m0050(r_out, r_in, 1.0 - _m0487 / float(_m0567))
            SelectionManager.select_zone_ring(image, _m0296, _m0561, _m0429, r_in)
            if _m0566 is not None:
                image.select_item(Gimp.ChannelOps.INTERSECT, _m0566)
            if not Gimp.Selection.is_empty(image):
                _m0112._m0210(_m0483, (24, 24, 24), (16, 16, 16), (8, 8, 8), _m0335, _m0337, _m0336, _m0338, 0.45)

    @classmethod
    def _m0386(cls, image, _m0363, _m0112, _m0268, _m0483, _m0562, _m0561, r_out, r_in, _m0567, _m0335, _m0337, _m0336, _m0338, is_glass=False):
        ox1, oy1, ox2, oy2 = _m0562
        ix1, iy1, ix2, iy2 = _m0561
        w = float(ox2 - ox1)
        _m0307 = r_out <= 1.0 and r_in <= 1.0
        SelectionManager.select_zone_ring(image, _m0562, _m0561, r_out, r_in)
        if Gimp.Selection.is_empty(image):
            return
        if _m0307:
            cls._m0063(image, _m0363, _m0112, _m0268, _m0483, _m0562, _m0561, is_glass)
            return
        _m0566 = Gimp.Selection.save(image)
        try:
            cls._m0062(image, _m0363, _m0112, _m0268, _m0483, _m0566, _m0562, _m0561, r_out, r_in, _m0567, _m0335, _m0337, _m0336, _m0338, is_glass, ox1, oy1, ox2, oy2, ix1, iy1, ix2, iy2, w)
        finally:
            if _m0566 is not None:
                image.remove_channel(_m0566)
