# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import math
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
import config
from community_material_seal import community_material_key
from fx.gradmap import _m0004
from selection import SelectionManager
from utils import _m0002

class ShimmerFX:

    def __init__(self, image, group, material, border_width, _m0330, position, _m0547, outer_box=None, inner_box=None, outer_radius=84, inner_radius=38, profile_preset='atelier_look', angle=135, inner_transparency=100):
        self.image = image
        self.group = group
        self.material = community_material_key(material)
        self.border_width = border_width
        self.intensity = _m0330
        self.position = position
        self.side = (_m0547 or 'auto').strip().lower()
        self.outer_box = outer_box
        self.inner_box = inner_box
        self.outer_radius = outer_radius
        self.inner_radius = inner_radius
        self.profile_preset = profile_preset
        self.angle = angle
        self.inner_transparency = int(inner_transparency)

    def _m0044(self) -> float:
        if self.profile_preset == 'logo_classic' or (self.outer_radius <= 1 and self.inner_radius <= 1):
            return 0.0
        if self.inner_radius > 0:
            return float(self.inner_radius)
        return max(28.0, float(self.outer_radius) - self.border_width * 0.46)

    def render(self, original_selection):
        if self.intensity <= 0 or self.inner_box is None:
            return
        ix1, iy1, ix2, iy2 = self.inner_box
        if ix2 <= ix1 or iy2 <= iy1:
            return
        _m0246 = Gimp.Selection.save(self.image)
        if _m0246 is None:
            raise RuntimeError('Die Rahmenauswahl konnte für den Innenschimmer nicht gesichert werden.')
        _m0319 = None
        try:
            r_in = self._m0044()
            _m0542 = max(8, round(self.border_width * 0.26))
            SelectionManager.select_full_box(self.image, self.inner_box, r_in)
            if Gimp.Selection.is_empty(self.image):
                return
            _m0319 = Gimp.Selection.save(self.image)
            _m0116 = (ix1 + _m0542, iy1 + _m0542, ix2 - _m0542, iy2 - _m0542)
            _m0460 = max(0.0, r_in - _m0542 * 0.85) if r_in > 0.5 else 0.0
            SelectionManager.select_zone_ring(self.image, self.inner_box, _m0116, r_in, _m0460)
            if Gimp.Selection.is_empty(self.image):
                return
            _m0171 = config.METALS.get(self.material, config.METALS['gold'])
            _m0310 = (255, 240, 185) if self.material == 'gold' else max(_m0171, key=sum)
            _m0385 = _m0171[3] if len(_m0171) > 3 else _m0171[2]
            _m0541 = max(8, min(32, round(self.intensity * 0.28)))
            _m0540 = _m0002._m0404(self.image, self.group, 'Inner Edge Contour Shimmer', _m0541, Gimp.LayerMode.SCREEN)
            cx = (float(ix1) + float(ix2)) / 2.0
            cy = (float(iy1) + float(iy2)) / 2.0
            _m0199 = math.hypot(float(ix2 - ix1), float(iy2 - iy1)) / 2.0
            if self.side == 'unten_rechts':
                _m0212 = 315.0
            elif self.side == 'oben_links':
                _m0212 = 135.0
            else:
                _m0212 = float(self.angle)
            rad = math.radians(_m0212)
            _m0369 = cx + math.cos(rad) * _m0199
            _m0371 = cy - math.sin(rad) * _m0199
            _m0370 = cx - math.cos(rad) * _m0199
            _m0372 = cy + math.sin(rad) * _m0199
            if self.side in ('rundum', 'beide', 'rahmen'):
                grad = _m0004._m0374(_m0310, _m0385, _m0310, _m0433=0.5)
            else:
                grad = _m0004._m0374(_m0310, _m0385, (0, 0, 0), _m0433=0.42)
            try:
                Gimp.context_set_gradient(grad)
                _m0540.edit_gradient_fill(Gimp.GradientType.LINEAR, 0.0, False, 1, 0.0, True, _m0369, _m0371, _m0370, _m0372)
            finally:
                grad.delete()
            Gimp.Selection.none(self.image)
            _m0132 = float(max(4.5, _m0542 * 0.48))
            _m0002._m0530(_m0540, 'gegl:gaussian-blur', **{'std-dev-x': _m0132, 'std-dev-y': _m0132})
            if _m0319 is not None:
                self.image.select_item(Gimp.ChannelOps.REPLACE, _m0319)
                Gimp.Selection.invert(self.image)
                if not Gimp.Selection.is_empty(self.image):
                    _m0540.edit_clear()
        finally:
            if _m0319 is not None:
                self.image.remove_channel(_m0319)
            Gimp.Selection.none(self.image)
            self.image.select_item(Gimp.ChannelOps.REPLACE, _m0246)
            self.image.remove_channel(_m0246)
