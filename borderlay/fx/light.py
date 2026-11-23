# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
from uuid import uuid4
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
from fx.light_rims import _m0007
from fx.light_shapes import LightSourceShapes
from selection import SelectionManager
from shapes import is_curved_or_freeform_mode
from utils import _m0002

class GlobalLight:

    def __init__(self, image, group, angle, material='gold', glanz=82, outer_box=None, inner_box=None, border_width=80, outer_radius=64, inner_radius=0, profile_preset='atelier_look', luxus=True, center_mode='transparent', inner_transparency=100, use_shimmer=False, shimmer_side='auto', light_source='cone', light_spread=45):
        self.image = image
        self.group = group
        self.angle = angle
        self.material = material
        self.glanz = glanz
        self.outer_box = outer_box
        self.inner_box = inner_box
        self.border_width = border_width
        self.outer_radius = outer_radius
        self.inner_radius = inner_radius
        self.profile_preset = profile_preset
        self.luxus = luxus
        self.center_mode = center_mode
        self.inner_transparency = int(inner_transparency)
        self.use_shimmer = bool(use_shimmer)
        self.shimmer_side = shimmer_side or 'auto'
        self.light_source = (light_source or 'cone').strip().lower()
        self.light_spread = max(5, min(100, int(light_spread)))

    def _m0049(self):
        if self.material in ('rosegold', 'rosegold_sunset'):
            return ((255, 246, 240), (242, 186, 156))
        if self.material == 'kupfer':
            return ((255, 244, 234), (240, 158, 116))
        if self.material == 'bronze':
            return ((255, 238, 200), (218, 156, 96))
        if self.material == 'cherry_wood':
            return ((255, 232, 204), (218, 136, 88))
        if self.material in ('titan', 'platinum', 'chrom', 'edelstahl', 'aluminium', 'colored_glass', 'ice_blue_steel', 'ebony_plain', 'onyx_black', 'schwarzchrom'):
            return ((255, 255, 255), (206, 222, 242))
        return ((255, 250, 232), (236, 198, 132))

    def _m0064(self, _m0434, _m0390, _m0190=(0, 0, 0)):
        _m0277 = Gimp.Gradient.new(f'Borderlay Specular {uuid4().hex[:8]}')
        if _m0277 is None:
            raise RuntimeError('Der Specular-Verlauf konnte nicht erstellt werden.')
        if not _m0277.segment_range_split_uniform(0, 0, 2):
            _m0277.delete()
            raise RuntimeError('Der Specular-Verlauf konnte nicht geteilt werden.')
        try:
            _m0277.segment_set_left_color(0, _m0002._m0299(_m0434))
            _m0277.segment_set_right_color(0, _m0002._m0299(_m0390))
            _m0277.segment_set_right_pos(0, 0.38)
            _m0277.segment_set_left_color(1, _m0002._m0299(_m0390))
            _m0277.segment_set_right_color(1, _m0002._m0299(_m0190))
        except Exception:
            _m0277.delete()
            raise
        return _m0277

    def _m0040(self) -> float:
        _m0237 = 100 - self.inner_transparency
        if self.center_mode in ('plate', 'inlay_well') and _m0237 <= 0:
            _m0237 = 100
        if self.use_shimmer and _m0237 < 45:
            _m0237 = max(_m0237, round(self.glanz * 0.55))
        return max(0.0, min(1.0, float(_m0237) / 100.0))

    def _m0083(self, _m0434, _m0571, _m0338):
        ox1, oy1, ox2, oy2 = self.outer_box
        ix1, iy1, ix2, iy2 = self.inner_box
        p_out = round(self.border_width * 0.18)
        p_in = round(self.border_width * 0.58)
        _m0442 = (ox1 + p_out, oy1 + p_out, ox2 - p_out, oy2 - p_out)
        _m0441 = (ox1 + p_in, oy1 + p_in, ox2 - p_in, oy2 - p_in)
        if _m0338:
            _m0468, _m0463 = (0.0, 0.0)
            _m0464 = 0.0
        else:
            _m0467 = float(self.inner_radius) if self.inner_radius > 0 else max(28.0, self.outer_radius - self.border_width * 0.46)
            _m0468 = self.outer_radius * 0.82 + _m0467 * 0.18
            _m0463 = 0.0 if self.profile_preset == 'atelier_look' else self.outer_radius * 0.42 + _m0467 * 0.58
            _m0464 = _m0467
        SelectionManager.select_zone_ring(self.image, _m0442, _m0441, _m0468, _m0463)
        if not Gimp.Selection.is_empty(self.image):
            _m0402 = 0.34 if self.material in ('bronze', 'kupfer') else 0.22
            _m0361 = max(10, min(36, round(self.glanz * _m0402)))
            _m0360 = _m0002._m0404(self.image, self.group, f'Specular Frame ({self.light_source.upper()} {self.light_spread}%)', _m0361, Gimp.LayerMode.SCREEN)
            if self.light_source == 'beam':
                LightSourceShapes._m0477(self.image, _m0360, self.outer_box, self.angle, self.light_spread, _m0434, _m0571, _m0409=0.22)
            else:
                LightSourceShapes._m0481(self.image, _m0360, self.outer_box, self.angle, self.light_spread, self._m0064, _m0434, _m0571, _m0397=False, _m0472=1.0)
        _m0320 = self._m0040()
        if _m0320 > 0.02 and ix2 > ix1 and (iy2 > iy1):
            SelectionManager.select_full_box(self.image, self.inner_box, _m0464)
            if not Gimp.Selection.is_empty(self.image):
                if self.use_shimmer and self.center_mode == 'transparent' and (self.inner_transparency >= 95):
                    _m0325 = Gimp.Selection.save(self.image)
                    if _m0325 is not None:
                        try:
                            _m0117 = max(8, round(self.border_width * 0.42))
                            SelectionManager.select_inward_band(self.image, _m0325, _m0117)
                        finally:
                            self.image.remove_channel(_m0325)
                if not Gimp.Selection.is_empty(self.image):
                    _m0124 = 0.24 if self.material in ('chrom', 'kupfer', 'bronze') else 0.18
                    _m0323 = max(4, min(34, round(self.glanz * _m0124 * _m0320)))
                    _m0322 = _m0002._m0404(self.image, self.group, 'Specular Inner Zone (Opacity Coupled)', _m0323, Gimp.LayerMode.SCREEN)
                    _m0396 = self.use_shimmer and self.shimmer_side == 'unten_rechts'
                    _m0212 = (self.angle + 180) % 360 if _m0396 else self.angle
                    if self.light_source == 'beam':
                        LightSourceShapes._m0477(self.image, _m0322, self.outer_box, _m0212, self.light_spread, _m0434, _m0571, _m0409=0.22)
                    else:
                        LightSourceShapes._m0481(self.image, _m0322, self.outer_box, self.angle, self.light_spread, self._m0064, _m0434, _m0571, _m0397=_m0396, _m0472=1.12)

    def render(self):
        if self.glanz <= 0:
            return
        _m0125 = Gimp.Selection.save(self.image)
        if _m0125 is None:
            raise RuntimeError('Die Auswahl für das Specular-Licht konnte nicht gespeichert werden.')
        try:
            if self.outer_box is None or self.inner_box is None:
                ox1, oy1, ox2, oy2 = SelectionManager.get_selection_box(self.image, _m0125)
                self.outer_box = (ox1, oy1, ox2, oy2)
                self.inner_box = (ox1 + self.border_width, oy1 + self.border_width, ox2 - self.border_width, oy2 - self.border_width)
            _m0338 = not is_curved_or_freeform_mode() and (self.profile_preset == 'logo_classic' or (self.outer_radius <= 1 and self.inner_radius <= 1))
            _m0434, _m0571 = self._m0049()
            self._m0083(_m0434, _m0571, _m0338)
            if self.material == 'bronze':
                _m0007._m0478(self, _m0434, _m0571, _m0338)
            elif self.material in ('chrom', 'kupfer'):
                _m0007._m0480(self, _m0434, _m0571, _m0338)
            if _m0338:
                _m0007._m0482(self, _m0125, _m0434, _m0571)
        finally:
            Gimp.Selection.none(self.image)
            self.image.select_item(Gimp.ChannelOps.REPLACE, _m0125)
            self.image.remove_channel(_m0125)
