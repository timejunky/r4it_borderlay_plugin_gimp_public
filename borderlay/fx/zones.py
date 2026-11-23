# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import math
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
from fx.zones_lighting import _m0012
from fx.zones_miter import _m0013
from fx.zones_slopes import _m0014
from selection import SelectionManager
from shapes import is_curved_or_freeform_mode

class _m0011:

    def __init__(self, image, outer_box, inner_box, border_width, outer_radius, inner_radius, profile_preset, is_glass=False, material='gold'):
        self.image = image
        self.outer_box = outer_box
        self.inner_box = inner_box
        self.border_width = border_width
        self.outer_radius = outer_radius
        self.inner_radius = inner_radius
        self.profile_preset = profile_preset
        self.is_glass = is_glass
        self.material = material

    def _m0044(self):
        if is_curved_or_freeform_mode():
            return 100.0
        if self.profile_preset in ('logo_classic', 'atelier_look'):
            return float(self.inner_radius) if self.profile_preset == 'atelier_look' else 0.0
        if self.outer_radius <= 1:
            return 0.0
        if self.inner_radius > 0:
            return float(self.inner_radius)
        return max(28.0, float(self.outer_radius) - self.border_width * 0.46)

    def _m0331(self, t, _m0178='auto'):
        if is_curved_or_freeform_mode():
            return 100.0
        if self.profile_preset == 'logo_classic' or (self.outer_radius <= 1 and self.inner_radius <= 1):
            return 0.0
        if _m0178 == 'sharp':
            return 0.0
        _m0466 = float(self.outer_radius)
        _m0467 = self._m0044()
        _m0572 = max(0.0, min(1.0, float(t)))
        return max(0.0, _m0466 * (1.0 - _m0572) + _m0467 * _m0572)

    def _m0174(self, _m0178, _m0574, _m0573):
        if is_curved_or_freeform_mode():
            return (100.0, 100.0)
        if self.profile_preset == 'logo_classic' or (self.outer_radius <= 1 and self.inner_radius <= 1):
            return (0.0, 0.0)
        if _m0178 == 'sharp':
            return (0.0, 0.0)
        if _m0178 == 'round_to_sharp':
            return (self._m0331(_m0574, 'round'), 0.0)
        return (self._m0331(_m0574, _m0178), self._m0331(_m0573, _m0178))

    @staticmethod
    def _m0060(r_out, r_in, _m0364):
        if r_out <= 0.5 and r_in <= 0.5:
            return 0.0
        t = max(0.0, min(1.0, float(_m0364)))
        return max(0.0, r_out * (1.0 - t) + r_in * t)

    def _m0429(self, _m0130, _m0298, _m0524, _m0608, _m0607, r_out, r_in, _m0613, _m0596, _m0369, _m0371, _m0370, _m0372):
        _m0014._m0428(self.image, _m0130, _m0298, _m0524, _m0608, _m0607, r_out, r_in, _m0613, _m0596, _m0369, _m0371, _m0370, _m0372)

    def _m0424(self, _m0130, _m0298, _m0524, _m0608, _m0607, r_out, r_in, _m0613, _m0369, _m0371, _m0370, _m0372):
        _m0014._m0423(self.image, _m0013, _m0130, _m0298, _m0524, _m0608, _m0607, r_out, r_in, _m0613, is_glass=self.is_glass)

    def _m0422(self, _m0130, _m0298, _m0524, _m0608, _m0607, r_out, r_in, _m0613, _m0369, _m0371, _m0370, _m0372):
        _m0014._m0421(self.image, _m0013, _m0130, _m0298, _m0524, _m0608, _m0607, r_out, r_in, _m0613, _m0369, _m0371, _m0370, _m0372, is_glass=self.is_glass)

    def _m0426(self, _m0130, _m0298, _m0524, _m0608, _m0607, r_out, r_in, _m0613, _m0121, _m0432, _m0369, _m0371, _m0370, _m0372):
        _m0013._m0425(self.image, _m0130, _m0298, _m0524, _m0608, _m0607, r_out, r_in, _m0613, _m0121, _m0432, _m0369, _m0371, _m0370, _m0372)

    def _m0236(self, _m0130, layer, _m0608, _m0607, _m0302, _m0355, _m0333=False):
        _m0013._m0236(self.image, _m0130, layer, _m0608, _m0607, _m0302, _m0355, _m0333=_m0333)

    def _m0204(self, _m0130, _m0524, _m0504):
        _m0013._m0204(self.image, self.outer_box, self.inner_box, _m0130, _m0524, _m0504)

    def _m0091(self, _m0130, _m0298, _m0612, _m0339, _m0337, _m0613, _m0432, ox1, oy1, ox2, oy2, ix1, iy1, ix2, iy2, r_out, r_in, _m0607):
        _m0544 = max(1, min(3, round(_m0613 * 0.08))) if _m0337 else max(1, min(2, round(_m0613 * 0.05)))
        _m0543 = max(62, round(_m0432 * 0.86))
        _m0130._m0234(_m0298, _m0543)
        if _m0613 >= 5 and (not _m0339):
            for s in range(1, _m0544 + 1):
                u = s / float(_m0544)
                _m0263 = round(_m0543 + (_m0432 - _m0543) * math.sin(u * (math.pi / 2.0)))
                _m0364 = s / float(_m0613)
                _m0147 = (ox1 + s, oy1 + s, ox2 - s, oy2 - s)
                _m0508 = self._m0060(r_out, r_in, _m0364)
                _m0146 = (ix1 - s, iy1 - s, ix2 + s, iy2 + s) if _m0337 else _m0607
                _m0497 = self._m0060(r_out, r_in, 1.0 - _m0364) if _m0337 else r_in
                if _m0146[0] <= _m0147[0] or _m0146[1] <= _m0147[1]:
                    break
                SelectionManager.select_zone_ring(self.image, _m0147, _m0146, _m0508, _m0497)
                if _m0612 is not None:
                    self.image.select_item(Gimp.ChannelOps.INTERSECT, _m0612)
                if not Gimp.Selection.is_empty(self.image):
                    _m0130._m0234(_m0298, _m0263)
        else:
            _m0130._m0234(_m0298, _m0432)
        if _m0612 is not None:
            self.image.select_item(Gimp.ChannelOps.REPLACE, _m0612)

    def _m0076(self, _m0130, _m0524, _m0612, _m0339, _m0337, _m0613, _m0608, _m0607, ox1, oy1, ox2, oy2, ix1, iy1, ix2, iy2, r_out, r_in, _m0369, _m0371, _m0370, _m0372):
        if self.is_glass:
            if _m0339:
                self._m0236(_m0130, _m0524, _m0608, _m0607, _m0302=190 if _m0337 else 210, _m0355=86 if _m0337 else 104, _m0333=False)
            else:
                _m0130._m0235(_m0524, (186, 186, 186), (130, 130, 130), (76, 76, 76), _m0369, _m0371, _m0370, _m0372, 0.45)
            return
        if _m0339:
            self._m0236(_m0130, _m0524, _m0608, _m0607, _m0302=238 if _m0337 else 216, _m0355=44 if _m0337 else 54, _m0333=False)
            return
        _m0012._m0427(_m0130, _m0524, _m0608, material=self.material, _m0337=_m0337, _m0369=_m0369, _m0371=_m0371, _m0370=_m0370, _m0372=_m0372)
        if _m0613 >= 8:
            _m0211 = max(2, min(3, round(_m0613 * 0.09)))
            _m0362 = _m0211 / float(_m0613)
            _m0210 = (ox1 + _m0211, oy1 + _m0211, ox2 - _m0211, oy2 - _m0211)
            _m0507 = self._m0060(r_out, r_in, _m0362)
            SelectionManager.select_zone_ring(self.image, _m0608, _m0210, r_out, _m0507)
            if _m0612 is not None:
                self.image.select_item(Gimp.ChannelOps.INTERSECT, _m0612)
            if not Gimp.Selection.is_empty(self.image):
                Gimp.Selection.feather(self.image, 0.75)
                _m0130._m0235(_m0524, (238, 238, 238), (136, 136, 136), (52, 52, 52), _m0369, _m0371, _m0370, _m0372, _m0433=0.44)
            if _m0337:
                _m0313 = (ix1 - _m0211, iy1 - _m0211, ix2 + _m0211, iy2 + _m0211)
                _m0496 = self._m0060(r_out, r_in, 1.0 - _m0362)
                SelectionManager.select_zone_ring(self.image, _m0313, _m0607, _m0496, r_in)
                if _m0612 is not None:
                    self.image.select_item(Gimp.ChannelOps.INTERSECT, _m0612)
                if not Gimp.Selection.is_empty(self.image):
                    Gimp.Selection.feather(self.image, 0.75)
                    _m0130._m0235(_m0524, (224, 224, 224), (128, 128, 128), (156, 156, 156), _m0369, _m0371, _m0370, _m0372, _m0433=0.45)

    def _m0420(self, _m0130, _m0298, _m0524, _m0608, _m0607, r_out, r_in, _m0613, _m0432, _m0369, _m0371, _m0370, _m0372, _m0335=True):
        ox1, oy1, ox2, oy2 = _m0608
        ix1, iy1, ix2, iy2 = _m0607
        _m0339 = not is_curved_or_freeform_mode() and (r_out <= 1.0 and r_in <= 1.0)
        _m0337 = _m0432 >= 225
        SelectionManager.select_zone_ring(self.image, _m0608, _m0607, r_out, r_in)
        if Gimp.Selection.is_empty(self.image):
            return
        _m0612 = Gimp.Selection.save(self.image)
        try:
            self._m0091(_m0130, _m0298, _m0612, _m0339, _m0337, _m0613, _m0432, ox1, oy1, ox2, oy2, ix1, iy1, ix2, iy2, r_out, r_in, _m0607)
            self._m0076(_m0130, _m0524, _m0612, _m0339, _m0337, _m0613, _m0608, _m0607, ox1, oy1, ox2, oy2, ix1, iy1, ix2, iy2, r_out, r_in, _m0369, _m0371, _m0370, _m0372)
        finally:
            if _m0612 is not None:
                self.image.remove_channel(_m0612)
