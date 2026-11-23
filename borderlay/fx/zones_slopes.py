# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import math
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
from selection import SelectionManager

class _m0014:

    @staticmethod
    def _m0060(r_out, r_in, _m0364):
        if r_out <= 0.5 and r_in <= 0.5:
            return 0.0
        t = max(0.0, min(1.0, float(_m0364)))
        return max(0.0, r_out * (1.0 - t) + r_in * t)

    @classmethod
    def _m0428(cls, image, _m0130, _m0298, _m0524, _m0608, _m0607, r_out, r_in, _m0613, _m0596, _m0369, _m0371, _m0370, _m0372):
        ox1, oy1, ox2, oy2 = _m0608
        ix1, iy1, ix2, iy2 = _m0607
        SelectionManager.select_zone_ring(image, _m0608, _m0607, r_out, r_in)
        if Gimp.Selection.is_empty(image):
            return
        _m0130._m0235(_m0524, (22, 22, 22), (14, 14, 14), (6, 6, 6), _m0369, _m0371, _m0370, _m0372, _m0433=0.45)
        _m0501 = min(180, _m0596 + 24)
        _m0130._m0234(_m0298, _m0501)
        if _m0613 >= 3:
            _m0155 = (ox1 + 1, oy1 + 1, ox2 - 1, oy2 - 1)
            _m0152 = (ix1 - 1, iy1 - 1, ix2 + 1, iy2 + 1)
            if _m0152[0] > _m0155[0] and _m0152[1] > _m0155[1]:
                _m0364 = 1.0 / float(_m0613)
                _m0506 = cls._m0060(r_out, r_in, _m0364)
                _m0495 = cls._m0060(r_out, r_in, 1.0 - _m0364)
                SelectionManager.select_zone_ring(image, _m0155, _m0152, _m0506, _m0495)
                if not Gimp.Selection.is_empty(image):
                    _m0130._m0234(_m0298, _m0596)
        else:
            _m0130._m0234(_m0298, _m0596)

    @classmethod
    def _m0423(cls, image, _m0398, _m0130, _m0298, _m0524, _m0608, _m0607, r_out, r_in, _m0613, is_glass=False):
        ox1, oy1, ox2, oy2 = _m0608
        w = float(ox2 - ox1)
        _m0339 = r_out <= 1.0 and r_in <= 1.0
        SelectionManager.select_zone_ring(image, _m0608, _m0607, r_out, r_in)
        if Gimp.Selection.is_empty(image):
            return
        if _m0339:
            _m0130._m0234(_m0298, _m0130._m0521(64.0))
            _m0302 = 215 if is_glass else 196
            _m0355 = 48 if is_glass else 42
            _m0398._m0236(image, _m0130, _m0524, _m0608, _m0607, _m0302=_m0302, _m0355=_m0355, _m0333=False)
            return
        _m0612 = Gimp.Selection.save(image)
        try:
            _m0367 = _m0130._m0521(14.0)
            _m0309 = _m0130._m0521(76.0)
            _m0130._m0234(_m0298, _m0367)
            _m0130._m0235(_m0524, (142, 142, 142), (98, 98, 98), (26, 26, 26), float(ox1 + w * 0.48), float(oy1), float(ox2 - w * 0.12), float(oy2), _m0433=0.44)
            _m0566 = 2 if _m0613 >= 12 else 1
            for m0 in range(_m0566, _m0613, _m0566):
                t = m0 / float(_m0613)
                _m0147 = (ox1 + m0, oy1 + m0, ox2 - m0, oy2 - m0)
                if _m0147[2] <= _m0607[2] or _m0147[3] <= _m0607[3]:
                    break
                _m0505 = cls._m0060(r_out, r_in, t)
                SelectionManager.select_zone_ring(image, _m0147, _m0607, _m0505, r_in)
                if _m0612 is not None:
                    image.select_item(Gimp.ChannelOps.INTERSECT, _m0612)
                if Gimp.Selection.is_empty(image):
                    continue
                _m0254 = round(_m0367 + (_m0309 - _m0367) * t)
                _m0130._m0234(_m0298, _m0254)
                if is_glass:
                    _m0130._m0234(_m0524, round(75 + 135 * t))
                else:
                    _m0473 = math.pow(t, 0.85)
                    _m0264 = round(108 + 96 * _m0473)
                    _m0258 = round(84 + 54 * _m0473)
                    _m0249 = round(24 + 28 * _m0473)
                    _m0130._m0235(_m0524, (_m0264, _m0264, _m0264), (_m0258, _m0258, _m0258), (_m0249, _m0249, _m0249), float(ox1 + w * 0.48), float(oy1), float(ox2 - w * 0.12), float(oy2), _m0433=0.44)
        finally:
            if _m0612 is not None:
                image.remove_channel(_m0612)

    @classmethod
    def _m0075(cls, image, _m0398, _m0130, _m0298, _m0524, _m0608, _m0607, is_glass):
        _m0130._m0234(_m0298, _m0130._m0521(24.0))
        if is_glass:
            _m0398._m0236(image, _m0130, _m0524, _m0608, _m0607, _m0302=228, _m0355=164, _m0333=False)
        else:
            _m0398._m0236(image, _m0130, _m0524, _m0608, _m0607, _m0302=112, _m0355=20, _m0333=True)

    @classmethod
    def _m0074(cls, image, _m0398, _m0130, _m0298, _m0524, _m0612, _m0608, _m0607, r_out, r_in, _m0613, _m0369, _m0371, _m0370, _m0372, is_glass, ox1, oy1, ox2, oy2, ix1, iy1, ix2, iy2, w):
        _m0587 = _m0130._m0521(86.0)
        _m0138 = _m0130._m0521(26.0)
        _m0130._m0234(_m0298, _m0138)
        if is_glass:
            _m0130._m0234(_m0524, 210)
        else:
            _m0130._m0235(_m0524, (174, 174, 174), (106, 106, 106), (36, 36, 36), float(ox1 + w * 0.52), float(oy1), float(ox2 - w * 0.12), float(oy2), _m0433=0.42)
        _m0566 = 2 if _m0613 >= 12 else 1
        for m_in in range(_m0613 - _m0566, 0, -_m0566):
            t = m_in / float(_m0613)
            _m0146 = (ox1 + m_in, oy1 + m_in, ox2 - m_in, oy2 - m_in)
            if _m0146[0] <= ox1 or _m0146[1] <= oy1:
                continue
            _m0494 = cls._m0060(r_out, r_in, t)
            SelectionManager.select_zone_ring(image, _m0608, _m0146, r_out, _m0494)
            if _m0612 is not None:
                image.select_item(Gimp.ChannelOps.INTERSECT, _m0612)
            if Gimp.Selection.is_empty(image):
                continue
            _m0254 = round(_m0587 - (_m0587 - _m0138) * t)
            _m0130._m0234(_m0298, _m0254)
            if is_glass:
                _m0130._m0234(_m0524, round(155 + 60 * t))
            else:
                _m0552 = math.pow(t, 0.8)
                _m0264 = round(124 + 48 * _m0552)
                _m0258 = round(80 + 28 * _m0552)
                _m0249 = round(32 + 24 * _m0552)
                _m0130._m0235(_m0524, (_m0264, _m0264, _m0264), (_m0258, _m0258, _m0258), (_m0249, _m0249, _m0249), float(ox1 + w * 0.52), float(oy1), float(ox2 - w * 0.12), float(oy2), _m0433=0.44)
        if not is_glass and _m0613 >= 6:
            _m0528 = max(3, min(4, round(_m0613 * 0.18)))
            _m0416 = (ox1 + _m0528, oy1 + _m0528, ox2 - _m0528, oy2 - _m0528)
            _m0469 = cls._m0060(r_out, r_in, _m0528 / float(_m0613))
            SelectionManager.select_zone_ring(image, _m0608, _m0416, r_out, _m0469)
            if _m0612 is not None:
                image.select_item(Gimp.ChannelOps.INTERSECT, _m0612)
            if not Gimp.Selection.is_empty(image):
                _m0130._m0235(_m0524, (18, 18, 18), (12, 12, 12), (6, 6, 6), _m0369, _m0371, _m0370, _m0372, 0.45)
            _m0326 = (ix1 - _m0528, iy1 - _m0528, ix2 + _m0528, iy2 + _m0528)
            _m0465 = cls._m0060(r_out, r_in, 1.0 - _m0528 / float(_m0613))
            SelectionManager.select_zone_ring(image, _m0326, _m0607, _m0465, r_in)
            if _m0612 is not None:
                image.select_item(Gimp.ChannelOps.INTERSECT, _m0612)
            if not Gimp.Selection.is_empty(image):
                _m0130._m0235(_m0524, (24, 24, 24), (16, 16, 16), (8, 8, 8), _m0369, _m0371, _m0370, _m0372, 0.45)

    @classmethod
    def _m0421(cls, image, _m0398, _m0130, _m0298, _m0524, _m0608, _m0607, r_out, r_in, _m0613, _m0369, _m0371, _m0370, _m0372, is_glass=False):
        ox1, oy1, ox2, oy2 = _m0608
        ix1, iy1, ix2, iy2 = _m0607
        w = float(ox2 - ox1)
        _m0339 = r_out <= 1.0 and r_in <= 1.0
        SelectionManager.select_zone_ring(image, _m0608, _m0607, r_out, r_in)
        if Gimp.Selection.is_empty(image):
            return
        if _m0339:
            cls._m0075(image, _m0398, _m0130, _m0298, _m0524, _m0608, _m0607, is_glass)
            return
        _m0612 = Gimp.Selection.save(image)
        try:
            cls._m0074(image, _m0398, _m0130, _m0298, _m0524, _m0612, _m0608, _m0607, r_out, r_in, _m0613, _m0369, _m0371, _m0370, _m0372, is_glass, ox1, oy1, ox2, oy2, ix1, iy1, ix2, iy2, w)
        finally:
            if _m0612 is not None:
                image.remove_channel(_m0612)
