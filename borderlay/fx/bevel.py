# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import math
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
import config
from fx.bevel_center import _m0000
from fx.bevel_seams import _m0001
from fx.gradmap import _m0004
from fx.zones import _m0010
from selection import SelectionManager
from shapes import is_curved_or_freeform_mode
from utils import _m0002

class Bevel3D:

    def __init__(self, image, group, material, relief, angle, border_width, fasenbreite, fasenkontrast, outer_box=None, inner_box=None, outer_radius=64, inner_radius=0, profile_preset='atelier_look', custom_dsl='', inlay_rgb=(36, 17, 52), center_mode='transparent', inner_transparency=100, profil_hoehe=88, profil_tiefe=88, gimp_gradient_name=''):
        self.image = image
        self.group = group
        self.material = material
        self.relief = relief
        self.angle = angle
        self.border_width = border_width
        self.fasenbreite = fasenbreite
        self.fasenkontrast = fasenkontrast
        self.outer_box = outer_box
        self.inner_box = inner_box
        self.outer_radius = outer_radius
        self.inner_radius = inner_radius
        self.profile_preset = profile_preset
        self.custom_dsl = custom_dsl
        self.inlay_rgb = inlay_rgb
        self.center_mode = center_mode
        self.inner_transparency = inner_transparency
        self.profil_hoehe = profil_hoehe
        self.profil_tiefe = profil_tiefe
        self.gimp_gradient_name = (gimp_gradient_name or '').strip()
        self.is_glass = self.material == 'colored_glass'
        self.grad_helper = _m0004(self.image, self.material, self.inlay_rgb, self.gimp_gradient_name)

    @staticmethod
    def _m0051(c1, c2, t):
        return _m0000._m0315(c1, c2, t)

    def _m0073(self, mat_key):
        return _m0000._m0453(self.material, self.inlay_rgb, self.is_glass, mat_key)

    def _m0210(self, layer, c1, c2, _m0129, _m0335, _m0337, _m0336, _m0338, _m0398=0.48):
        self.grad_helper._m0210(layer, c1, c2, _m0129, _m0335, _m0337, _m0336, _m0338, _m0398=_m0398)

    def _m0213(self, layer, _m0144, _m0145, radius, _m0291, _m0352, _m0379):
        self.grad_helper._m0213(layer, _m0144, _m0145, radius, _m0291, _m0352, _m0379)

    @staticmethod
    def _m0209(layer, _m0254):
        g = max(0, min(255, int(round(_m0254))))
        if not Gimp.context_set_foreground(_m0002._m0269((g, g, g))):
            raise RuntimeError('Der Grauwert für die 3D-Höhenkarte konnte nicht gesetzt werden.')
        if not layer.edit_fill(Gimp.FillType.FOREGROUND):
            raise RuntimeError('Die 3D-Höhenkarte konnte nicht gefüllt werden.')

    def _m0480(self, _m0563):
        _m0261 = self.profil_hoehe / 100.0
        _m0168 = self.profil_tiefe / 100.0
        _m0360 = round(76.0 * (1.0 - _m0168))
        _m0346 = round(140.0 + 115.0 * _m0261)
        val = round(_m0360 + _m0563 / 100.0 * (_m0346 - _m0360))
        return max(0, min(255, val))

    def _m0023(self, _m0568, _m0434, _m0335, _m0337, _m0336, _m0338, _m0306=False):
        _m0001._m0446(self, _m0568, _m0434, _m0335, _m0337, _m0336, _m0338, _m0306=_m0306)

    def _m0070(self, _m0565, _m0335, _m0337, _m0336, _m0338):
        _m0000._m0442(self, _m0565, _m0335, _m0337, _m0336, _m0338)

    def _m0035(self, _m0107):
        if self.outer_box is not None and self.inner_box is not None:
            return
        ox1, oy1, ox2, oy2 = SelectionManager.get_selection_box(self.image, _m0107)
        self.outer_box = (ox1, oy1, ox2, oy2)
        self.inner_box = (ox1 + self.border_width, oy1 + self.border_width, ox2 - self.border_width, oy2 - self.border_width)

    def _m0045(self):
        return not is_curved_or_freeform_mode() and (self.profile_preset == 'logo_classic' or (self.outer_radius <= 1 and self.inner_radius <= 1))

    def _m0032(self, _m0565, kind, _m0268, _m0483, _m0562, _m0561, r_out, r_in, _m0567, _m0397, _m0544, _m0335, _m0337, _m0336, _m0338):
        if kind == 'groove':
            _m0565._m0394(self, _m0268, _m0483, _m0562, _m0561, r_out, r_in, _m0567, _m0397, _m0335, _m0337, _m0336, _m0338)
            return
        if kind in ('flat', 'step'):
            _m0565._m0385(self, _m0268, _m0483, _m0562, _m0561, r_out, r_in, _m0567, _m0397, _m0335, _m0337, _m0336, _m0338, _m0303=kind == 'flat')
            return
        if kind == 'bevel_out':
            _m0565._m0389(self, _m0268, _m0483, _m0562, _m0561, r_out, r_in, _m0567, _m0335, _m0337, _m0336, _m0338)
            return
        if kind == 'bevel_in':
            _m0565._m0387(self, _m0268, _m0483, _m0562, _m0561, r_out, r_in, _m0567, _m0335, _m0337, _m0336, _m0338)
            return
        if kind == 'pipe':
            _m0565._m0391(self, _m0268, _m0483, _m0562, _m0561, r_out, r_in, _m0567, _m0103=max(_m0544, round(_m0397 * 0.36)), _m0397=_m0397, _m0335=_m0335, _m0337=_m0337, _m0336=_m0336, _m0338=_m0338)

    def _m0065(self, zones, ox1, oy1, ox2, oy2, _m0565, _m0268, _m0483, _m0335, _m0337, _m0336, _m0338):
        cursor = 0.0
        _m0568 = []
        for idx, zone in enumerate(zones):
            _m0530 = cursor
            _m0529 = min(1.0, cursor + zone['share'])
            cursor = _m0529
            _m0423 = round(_m0530 * self.border_width)
            _m0422 = round(_m0529 * self.border_width)
            if _m0422 <= _m0423 and idx == len(zones) - 1:
                _m0422 = self.border_width
            _m0567 = _m0422 - _m0423
            if _m0567 <= 0:
                continue
            _m0562 = (ox1 + _m0423, oy1 + _m0423, ox2 - _m0423, oy2 - _m0423)
            _m0561 = (ox1 + _m0422, oy1 + _m0422, ox2 - _m0422, oy2 - _m0422)
            r_out, r_in = _m0565._m0155(zone.get('corner', 'auto'), _m0530, _m0529)
            _m0568.append((zone, _m0562, _m0561, r_out, r_in, _m0567))
            if r_out > 1.0 and r_in <= 1.0:
                SelectionManager.select_zone_ring(self.image, _m0562, _m0561, 0.0, 0.0)
                self._m0209(_m0268, self._m0480(18.0))
                self._m0209(_m0483, 42)
            SelectionManager.select_zone_ring(self.image, _m0562, _m0561, r_out, r_in)
            if Gimp.Selection.is_empty(self.image):
                continue
            self._m0032(_m0565, zone['kind'], _m0268, _m0483, _m0562, _m0561, r_out, r_in, _m0567, self._m0480(zone['z']), self._m0480(14.0), _m0335, _m0337, _m0336, _m0338)
        return _m0568

    def render(self):
        _m0107 = Gimp.Selection.save(self.image)
        if _m0107 is None:
            raise RuntimeError('Die Rahmenauswahl konnte für das 3D-Bevel nicht gespeichert werden.')
        _m0464 = None
        try:
            self._m0035(_m0107)
            _m0306 = self._m0045()
            _m0565 = _m0010(self.image, self.outer_box, self.inner_box, self.border_width, self.outer_radius, self.inner_radius, self.profile_preset, is_glass=self.is_glass, material=self.material)
            ox1, oy1, ox2, oy2 = self.outer_box
            _m0191 = float(self.angle) - 14.0 if self.angle == 135 else float(self.angle)
            rad = math.radians(_m0191)
            cx = (float(ox1) + float(ox2)) / 2.0
            cy = (float(oy1) + float(oy2)) / 2.0
            _m0179 = math.hypot(float(ox2 - ox1), float(oy2 - oy1)) / 2.0
            _m0335 = cx + math.cos(rad) * _m0179
            _m0337 = cy - math.sin(rad) * _m0179
            _m0336 = cx - math.cos(rad) * _m0179
            _m0338 = cy + math.sin(rad) * _m0179
            self._m0070(_m0565, _m0335, _m0337, _m0336, _m0338)
            _m0434 = _m0565._m0300(1.0, 'auto')
            SelectionManager.select_zone_ring(self.image, self.outer_box, self.inner_box, self.outer_radius, _m0434)
            _m0464 = Gimp.Selection.save(self.image)
            _m0117 = round(self.relief * 0.68) if self.is_glass else max(75, min(100, round(self.relief)))
            _m0483 = _m0002._m0369(self.image, self.group, '3D GradMap Metal Frame', _m0117, Gimp.LayerMode.NORMAL)
            _m0200 = Gimp.LayerMode.SOFTLIGHT_LEGACY if hasattr(Gimp.LayerMode, 'SOFTLIGHT_LEGACY') else Gimp.LayerMode.OVERLAY
            _m0268 = _m0002._m0369(self.image, self.group, '3D Elevation Emboss', max(34, min(72, round(self.relief * 0.64))), _m0200)
            self.image.select_item(Gimp.ChannelOps.REPLACE, _m0464)
            self._m0210(_m0483, (216, 216, 216), (134, 134, 134), (48, 48, 48), _m0335, _m0337, _m0336, _m0338, 0.44)
            self._m0209(_m0268, 32)
            zones = config.parse_profile_zones(self.profile_preset, self.custom_dsl)
            _m0568 = self._m0065(zones, ox1, oy1, ox2, oy2, _m0565, _m0268, _m0483, _m0335, _m0337, _m0336, _m0338)
            Gimp.Selection.none(self.image)
            _m0482 = 0.35 if _m0306 else 0.75
            _m0002._m0489(_m0483, 'gegl:gaussian-blur', **{'std-dev-x': _m0482, 'std-dev-y': _m0482})
            _m0510 = 0.85 if _m0306 else 1.15
            _m0002._m0489(_m0268, 'gegl:gaussian-blur', **{'std-dev-x': _m0510, 'std-dev-y': _m0510})
            _m0199 = max(22, min(96, round(22 + (self.profil_hoehe + self.profil_tiefe) * 0.28)))
            _m0002._m0489(_m0268, 'gegl:emboss', {'type': 'emboss', 'azimuth': _m0191, 'elevation': 20.0, 'depth': int(_m0199)})
            _m0157 = self.fasenkontrast / 100.0 * 0.14
            _m0002._m0489(_m0268, 'gegl:levels', **{'in-low': min(0.28, _m0157), 'in-high': max(0.72, 1.0 - _m0157), 'out-low': 0.0, 'out-high': 1.0})
            if not _m0306:
                _m0002._m0489(_m0268, 'gegl:gaussian-blur', **{'std-dev-x': 0.4, 'std-dev-y': 0.4})
            self.grad_helper._m0094(_m0483, self.material)
            self.grad_helper._m0094(_m0268, self.material)
            self.image.select_item(Gimp.ChannelOps.REPLACE, _m0464)
            Gimp.Selection.invert(self.image)
            if not Gimp.Selection.is_empty(self.image):
                _m0483.edit_clear()
                _m0268.edit_clear()
            _m0001._m0448(self, _m0568)
            self._m0023(_m0568, _m0434, _m0335, _m0337, _m0336, _m0338, _m0306=_m0306)
        finally:
            Gimp.Selection.none(self.image)
            self.image.select_item(Gimp.ChannelOps.REPLACE, _m0107)
            self.image.remove_channel(_m0107)
            if _m0464 is not None:
                self.image.remove_channel(_m0464)
