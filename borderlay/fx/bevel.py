# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import math
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
import config
from fx.bevel_center import _m0000
from fx.bevel_seams import _m0001
from fx.gradmap import _m0004
from fx.zones import _m0011
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
    def _m0061(c1, c2, t):
        return _m0000._m0348(c1, c2, t)

    def _m0086(self, mat_key):
        return _m0000._m0493(self.material, self.inlay_rgb, self.is_glass, mat_key)

    def _m0235(self, layer, c1, c2, _m0148, _m0369, _m0371, _m0370, _m0372, _m0433=0.48):
        self.grad_helper._m0235(layer, c1, c2, _m0148, _m0369, _m0371, _m0370, _m0372, _m0433=_m0433)

    def _m0238(self, layer, _m0163, _m0164, radius, _m0321, _m0387, _m0414):
        self.grad_helper._m0238(layer, _m0163, _m0164, radius, _m0321, _m0387, _m0414)

    @staticmethod
    def _m0234(layer, _m0283):
        g = max(0, min(255, int(round(_m0283))))
        if not Gimp.context_set_foreground(_m0002._m0299((g, g, g))):
            raise RuntimeError('Der Grauwert für die 3D-Höhenkarte konnte nicht gesetzt werden.')
        if not layer.edit_fill(Gimp.FillType.FOREGROUND):
            raise RuntimeError('Die 3D-Höhenkarte konnte nicht gefüllt werden.')

    def _m0521(self, _m0609):
        _m0290 = self.profil_hoehe / 100.0
        _m0189 = self.profil_tiefe / 100.0
        _m0395 = round(76.0 * (1.0 - _m0189))
        _m0381 = round(140.0 + 115.0 * _m0290)
        val = round(_m0395 + _m0609 / 100.0 * (_m0381 - _m0395))
        return max(0, min(255, val))

    def _m0026(self, _m0614, _m0470, _m0369, _m0371, _m0370, _m0372, _m0338=False):
        _m0001._m0483(self, _m0614, _m0470, _m0369, _m0371, _m0370, _m0372, _m0338=_m0338)

    def _m0082(self, _m0611, _m0369, _m0371, _m0370, _m0372):
        _m0000._m0479(self, _m0611, _m0369, _m0371, _m0370, _m0372)

    def _m0045(self, _m0125):
        if self.outer_box is not None and self.inner_box is not None:
            return
        ox1, oy1, ox2, oy2 = SelectionManager.get_selection_box(self.image, _m0125)
        self.outer_box = (ox1, oy1, ox2, oy2)
        self.inner_box = (ox1 + self.border_width, oy1 + self.border_width, ox2 - self.border_width, oy2 - self.border_width)

    def _m0056(self):
        return not is_curved_or_freeform_mode() and (self.profile_preset == 'logo_classic' or (self.outer_radius <= 1 and self.inner_radius <= 1))

    def _m0042(self, _m0611, kind, _m0298, _m0524, _m0608, _m0607, r_out, r_in, _m0613, _m0432, _m0589, _m0369, _m0371, _m0370, _m0372):
        if kind == 'groove':
            _m0611._m0429(self, _m0298, _m0524, _m0608, _m0607, r_out, r_in, _m0613, _m0432, _m0369, _m0371, _m0370, _m0372)
            return
        if kind in ('flat', 'step'):
            _m0611._m0420(self, _m0298, _m0524, _m0608, _m0607, r_out, r_in, _m0613, _m0432, _m0369, _m0371, _m0370, _m0372, _m0335=kind == 'flat')
            return
        if kind == 'bevel_out':
            _m0611._m0424(self, _m0298, _m0524, _m0608, _m0607, r_out, r_in, _m0613, _m0369, _m0371, _m0370, _m0372)
            return
        if kind == 'bevel_in':
            _m0611._m0422(self, _m0298, _m0524, _m0608, _m0607, r_out, r_in, _m0613, _m0369, _m0371, _m0370, _m0372)
            return
        if kind == 'pipe':
            _m0611._m0426(self, _m0298, _m0524, _m0608, _m0607, r_out, r_in, _m0613, _m0121=max(_m0589, round(_m0432 * 0.36)), _m0432=_m0432, _m0369=_m0369, _m0371=_m0371, _m0370=_m0370, _m0372=_m0372)

    def _m0077(self, zones, ox1, oy1, ox2, oy2, _m0611, _m0298, _m0524, _m0369, _m0371, _m0370, _m0372):
        cursor = 0.0
        _m0614 = []
        for idx, zone in enumerate(zones):
            _m0574 = cursor
            _m0573 = min(1.0, cursor + zone['share'])
            cursor = _m0573
            _m0459 = round(_m0574 * self.border_width)
            _m0458 = round(_m0573 * self.border_width)
            if _m0458 <= _m0459 and idx == len(zones) - 1:
                _m0458 = self.border_width
            _m0613 = _m0458 - _m0459
            if _m0613 <= 0:
                continue
            _m0608 = (ox1 + _m0459, oy1 + _m0459, ox2 - _m0459, oy2 - _m0459)
            _m0607 = (ox1 + _m0458, oy1 + _m0458, ox2 - _m0458, oy2 - _m0458)
            r_out, r_in = _m0611._m0174(zone.get('corner', 'auto'), _m0574, _m0573)
            _m0614.append((zone, _m0608, _m0607, r_out, r_in, _m0613))
            if r_out > 1.0 and r_in <= 1.0:
                SelectionManager.select_zone_ring(self.image, _m0608, _m0607, 0.0, 0.0)
                self._m0234(_m0298, self._m0521(18.0))
                self._m0234(_m0524, 42)
            SelectionManager.select_zone_ring(self.image, _m0608, _m0607, r_out, r_in)
            if Gimp.Selection.is_empty(self.image):
                continue
            self._m0042(_m0611, zone['kind'], _m0298, _m0524, _m0608, _m0607, r_out, r_in, _m0613, self._m0521(zone['z']), self._m0521(14.0), _m0369, _m0371, _m0370, _m0372)
        return _m0614

    def render(self):
        _m0125 = Gimp.Selection.save(self.image)
        if _m0125 is None:
            raise RuntimeError('Die Rahmenauswahl konnte für das 3D-Bevel nicht gespeichert werden.')
        _m0504 = None
        try:
            self._m0045(_m0125)
            _m0338 = self._m0056()
            _m0611 = _m0011(self.image, self.outer_box, self.inner_box, self.border_width, self.outer_radius, self.inner_radius, self.profile_preset, is_glass=self.is_glass, material=self.material)
            ox1, oy1, ox2, oy2 = self.outer_box
            _m0213 = float(self.angle) - 14.0 if self.angle == 135 else float(self.angle)
            rad = math.radians(_m0213)
            cx = (float(ox1) + float(ox2)) / 2.0
            cy = (float(oy1) + float(oy2)) / 2.0
            _m0200 = math.hypot(float(ox2 - ox1), float(oy2 - oy1)) / 2.0
            _m0369 = cx + math.cos(rad) * _m0200
            _m0371 = cy - math.sin(rad) * _m0200
            _m0370 = cx - math.cos(rad) * _m0200
            _m0372 = cy + math.sin(rad) * _m0200
            self._m0082(_m0611, _m0369, _m0371, _m0370, _m0372)
            _m0470 = _m0611._m0331(1.0, 'auto')
            SelectionManager.select_zone_ring(self.image, self.outer_box, self.inner_box, self.outer_radius, _m0470)
            _m0504 = Gimp.Selection.save(self.image)
            _m0135 = round(self.relief * 0.68) if self.is_glass else max(75, min(100, round(self.relief)))
            _m0524 = _m0002._m0404(self.image, self.group, '3D GradMap Metal Frame', _m0135, Gimp.LayerMode.NORMAL)
            _m0222 = Gimp.LayerMode.SOFTLIGHT_LEGACY if hasattr(Gimp.LayerMode, 'SOFTLIGHT_LEGACY') else Gimp.LayerMode.OVERLAY
            _m0298 = _m0002._m0404(self.image, self.group, '3D Elevation Emboss', max(34, min(72, round(self.relief * 0.64))), _m0222)
            self.image.select_item(Gimp.ChannelOps.REPLACE, _m0504)
            self._m0235(_m0524, (216, 216, 216), (134, 134, 134), (48, 48, 48), _m0369, _m0371, _m0370, _m0372, 0.44)
            self._m0234(_m0298, 32)
            zones = config.parse_profile_zones(self.profile_preset, self.custom_dsl)
            _m0614 = self._m0077(zones, ox1, oy1, ox2, oy2, _m0611, _m0298, _m0524, _m0369, _m0371, _m0370, _m0372)
            Gimp.Selection.none(self.image)
            _m0523 = 0.35 if _m0338 else 0.75
            _m0002._m0530(_m0524, 'gegl:gaussian-blur', **{'std-dev-x': _m0523, 'std-dev-y': _m0523})
            _m0551 = 0.85 if _m0338 else 1.15
            _m0002._m0530(_m0298, 'gegl:gaussian-blur', **{'std-dev-x': _m0551, 'std-dev-y': _m0551})
            _m0221 = max(22, min(96, round(22 + (self.profil_hoehe + self.profil_tiefe) * 0.28)))
            _m0002._m0530(_m0298, 'gegl:emboss', {'type': 'emboss', 'azimuth': _m0213, 'elevation': 20.0, 'depth': int(_m0221)})
            _m0176 = self.fasenkontrast / 100.0 * 0.14
            _m0002._m0530(_m0298, 'gegl:levels', **{'in-low': min(0.28, _m0176), 'in-high': max(0.72, 1.0 - _m0176), 'out-low': 0.0, 'out-high': 1.0})
            if not _m0338:
                _m0002._m0530(_m0298, 'gegl:gaussian-blur', **{'std-dev-x': 0.4, 'std-dev-y': 0.4})
            self.grad_helper._m0112(_m0524, self.material)
            self.grad_helper._m0112(_m0298, self.material)
            self.image.select_item(Gimp.ChannelOps.REPLACE, _m0504)
            Gimp.Selection.invert(self.image)
            if not Gimp.Selection.is_empty(self.image):
                _m0524.edit_clear()
                _m0298.edit_clear()
            _m0001._m0485(self, _m0614)
            self._m0026(_m0614, _m0470, _m0369, _m0371, _m0370, _m0372, _m0338=_m0338)
        finally:
            Gimp.Selection.none(self.image)
            self.image.select_item(Gimp.ChannelOps.REPLACE, _m0125)
            self.image.remove_channel(_m0125)
            if _m0504 is not None:
                self.image.remove_channel(_m0504)
