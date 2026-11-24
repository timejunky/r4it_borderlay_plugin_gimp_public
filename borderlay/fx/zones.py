# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import math
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
from fx.zones_lighting import _m0011
from fx.zones_miter import _m0012
from fx.zones_slopes import _m0013
from selection import SelectionManager
from shapes import is_curved_or_freeform_mode

class _m0010:

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

    def _m0034(self):
        if is_curved_or_freeform_mode():
            return 100.0
        if self.profile_preset in ('logo_classic', 'atelier_look'):
            return float(self.inner_radius) if self.profile_preset == 'atelier_look' else 0.0
        if self.outer_radius <= 1:
            return 0.0
        if self.inner_radius > 0:
            return float(self.inner_radius)
        return max(28.0, float(self.outer_radius) - self.border_width * 0.46)

    def _m0300(self, t, _m0159='auto'):
        if is_curved_or_freeform_mode():
            return 100.0
        if self.profile_preset == 'logo_classic' or (self.outer_radius <= 1 and self.inner_radius <= 1):
            return 0.0
        if _m0159 == 'sharp':
            return 0.0
        _m0430 = float(self.outer_radius)
        _m0431 = self._m0034()
        _m0528 = max(0.0, min(1.0, float(t)))
        return max(0.0, _m0430 * (1.0 - _m0528) + _m0431 * _m0528)

    def _m0155(self, _m0159, _m0530, _m0529):
        if is_curved_or_freeform_mode():
            return (100.0, 100.0)
        if self.profile_preset == 'logo_classic' or (self.outer_radius <= 1 and self.inner_radius <= 1):
            return (0.0, 0.0)
        if _m0159 == 'sharp':
            return (0.0, 0.0)
        if _m0159 == 'round_to_sharp':
            return (self._m0300(_m0530, 'round'), 0.0)
        return (self._m0300(_m0530, _m0159), self._m0300(_m0529, _m0159))

    @staticmethod
    def _m0050(r_out, r_in, _m0330):
        if r_out <= 0.5 and r_in <= 0.5:
            return 0.0
        t = max(0.0, min(1.0, float(_m0330)))
        return max(0.0, r_out * (1.0 - t) + r_in * t)

    def _m0394(self, _m0112, _m0268, _m0483, _m0562, _m0561, r_out, r_in, _m0567, _m0551, _m0335, _m0337, _m0336, _m0338):
        _m0013._m0393(self.image, _m0112, _m0268, _m0483, _m0562, _m0561, r_out, r_in, _m0567, _m0551, _m0335, _m0337, _m0336, _m0338)

    def _m0389(self, _m0112, _m0268, _m0483, _m0562, _m0561, r_out, r_in, _m0567, _m0335, _m0337, _m0336, _m0338):
        _m0013._m0388(self.image, _m0012, _m0112, _m0268, _m0483, _m0562, _m0561, r_out, r_in, _m0567, is_glass=self.is_glass)

    def _m0387(self, _m0112, _m0268, _m0483, _m0562, _m0561, r_out, r_in, _m0567, _m0335, _m0337, _m0336, _m0338):
        _m0013._m0386(self.image, _m0012, _m0112, _m0268, _m0483, _m0562, _m0561, r_out, r_in, _m0567, _m0335, _m0337, _m0336, _m0338, is_glass=self.is_glass)

    def _m0391(self, _m0112, _m0268, _m0483, _m0562, _m0561, r_out, r_in, _m0567, _m0103, _m0397, _m0335, _m0337, _m0336, _m0338):
        _m0012._m0390(self.image, _m0112, _m0268, _m0483, _m0562, _m0561, r_out, r_in, _m0567, _m0103, _m0397, _m0335, _m0337, _m0336, _m0338)

    def _m0211(self, _m0112, layer, _m0562, _m0561, _m0272, _m0321, _m0302=False):
        _m0012._m0211(self.image, _m0112, layer, _m0562, _m0561, _m0272, _m0321, _m0302=_m0302)

    def _m0183(self, _m0112, _m0483, _m0464):
        _m0012._m0183(self.image, self.outer_box, self.inner_box, _m0112, _m0483, _m0464)

    def _m0078(self, _m0112, _m0268, _m0566, _m0307, _m0305, _m0567, _m0397, ox1, oy1, ox2, oy2, ix1, iy1, ix2, iy2, r_out, r_in, _m0561):
        _m0503 = max(1, min(3, round(_m0567 * 0.08))) if _m0305 else max(1, min(2, round(_m0567 * 0.05)))
        _m0502 = max(62, round(_m0397 * 0.86))
        _m0112._m0209(_m0268, _m0502)
        if _m0567 >= 5 and (not _m0307):
            for s in range(1, _m0503 + 1):
                u = s / float(_m0503)
                _m0237 = round(_m0502 + (_m0397 - _m0502) * math.sin(u * (math.pi / 2.0)))
                _m0330 = s / float(_m0567)
                _m0128 = (ox1 + s, oy1 + s, ox2 - s, oy2 - s)
                _m0468 = self._m0050(r_out, r_in, _m0330)
                _m0127 = (ix1 - s, iy1 - s, ix2 + s, iy2 + s) if _m0305 else _m0561
                _m0457 = self._m0050(r_out, r_in, 1.0 - _m0330) if _m0305 else r_in
                if _m0127[0] <= _m0128[0] or _m0127[1] <= _m0128[1]:
                    break
                SelectionManager.select_zone_ring(self.image, _m0128, _m0127, _m0468, _m0457)
                if _m0566 is not None:
                    self.image.select_item(Gimp.ChannelOps.INTERSECT, _m0566)
                if not Gimp.Selection.is_empty(self.image):
                    _m0112._m0209(_m0268, _m0237)
        else:
            _m0112._m0209(_m0268, _m0397)
        if _m0566 is not None:
            self.image.select_item(Gimp.ChannelOps.REPLACE, _m0566)

    def _m0064(self, _m0112, _m0483, _m0566, _m0307, _m0305, _m0567, _m0562, _m0561, ox1, oy1, ox2, oy2, ix1, iy1, ix2, iy2, r_out, r_in, _m0335, _m0337, _m0336, _m0338):
        if self.is_glass:
            if _m0307:
                self._m0211(_m0112, _m0483, _m0562, _m0561, _m0272=190 if _m0305 else 210, _m0321=86 if _m0305 else 104, _m0302=False)
            else:
                _m0112._m0210(_m0483, (186, 186, 186), (130, 130, 130), (76, 76, 76), _m0335, _m0337, _m0336, _m0338, 0.45)
            return
        if _m0307:
            self._m0211(_m0112, _m0483, _m0562, _m0561, _m0272=238 if _m0305 else 216, _m0321=44 if _m0305 else 54, _m0302=False)
            return
        _m0011._m0392(_m0112, _m0483, _m0562, material=self.material, _m0305=_m0305, _m0335=_m0335, _m0337=_m0337, _m0336=_m0336, _m0338=_m0338)
        if _m0567 >= 8:
            _m0189 = max(2, min(3, round(_m0567 * 0.09)))
            _m0328 = _m0189 / float(_m0567)
            _m0188 = (ox1 + _m0189, oy1 + _m0189, ox2 - _m0189, oy2 - _m0189)
            _m0467 = self._m0050(r_out, r_in, _m0328)
            SelectionManager.select_zone_ring(self.image, _m0562, _m0188, r_out, _m0467)
            if _m0566 is not None:
                self.image.select_item(Gimp.ChannelOps.INTERSECT, _m0566)
            if not Gimp.Selection.is_empty(self.image):
                Gimp.Selection.feather(self.image, 0.75)
                _m0112._m0210(_m0483, (238, 238, 238), (136, 136, 136), (52, 52, 52), _m0335, _m0337, _m0336, _m0338, _m0398=0.44)
            if _m0305:
                _m0283 = (ix1 - _m0189, iy1 - _m0189, ix2 + _m0189, iy2 + _m0189)
                _m0456 = self._m0050(r_out, r_in, 1.0 - _m0328)
                SelectionManager.select_zone_ring(self.image, _m0283, _m0561, _m0456, r_in)
                if _m0566 is not None:
                    self.image.select_item(Gimp.ChannelOps.INTERSECT, _m0566)
                if not Gimp.Selection.is_empty(self.image):
                    Gimp.Selection.feather(self.image, 0.75)
                    _m0112._m0210(_m0483, (224, 224, 224), (128, 128, 128), (156, 156, 156), _m0335, _m0337, _m0336, _m0338, _m0398=0.45)

    def _m0385(self, _m0112, _m0268, _m0483, _m0562, _m0561, r_out, r_in, _m0567, _m0397, _m0335, _m0337, _m0336, _m0338, _m0303=True):
        ox1, oy1, ox2, oy2 = _m0562
        ix1, iy1, ix2, iy2 = _m0561
        _m0307 = not is_curved_or_freeform_mode() and (r_out <= 1.0 and r_in <= 1.0)
        _m0305 = _m0397 >= 225
        SelectionManager.select_zone_ring(self.image, _m0562, _m0561, r_out, r_in)
        if Gimp.Selection.is_empty(self.image):
            return
        _m0566 = Gimp.Selection.save(self.image)
        try:
            self._m0078(_m0112, _m0268, _m0566, _m0307, _m0305, _m0567, _m0397, ox1, oy1, ox2, oy2, ix1, iy1, ix2, iy2, r_out, r_in, _m0561)
            self._m0064(_m0112, _m0483, _m0566, _m0307, _m0305, _m0567, _m0562, _m0561, ox1, oy1, ox2, oy2, ix1, iy1, ix2, iy2, r_out, r_in, _m0335, _m0337, _m0336, _m0338)
        finally:
            if _m0566 is not None:
                self.image.remove_channel(_m0566)
