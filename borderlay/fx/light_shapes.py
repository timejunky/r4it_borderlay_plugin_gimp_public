# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import math
from uuid import uuid4
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
import config
from utils import _m0002

class LightSourceShapes:

    @staticmethod
    def _m0272(material: str) -> dict:
        mat_key = (material or 'gold').strip().lower()
        return dict(config.MATERIAL_LIGHT_DEFAULTS.get(mat_key, config.MATERIAL_LIGHT_DEFAULTS['gold']))

    @classmethod
    def resolve_material_lighting(cls, material: str, light_source: str='auto', light_spread: int=-1, glanz: int=-1) -> tuple:
        _m0194 = cls._m0272(material)
        _m0475 = (light_source or 'auto').strip().lower()
        if _m0475 in ('beam', 'cone'):
            _m0217 = _m0475
            _m0218 = int(light_spread) if light_spread is not None and int(light_spread) > 0 else int(_m0194['light_spread'])
        else:
            _m0217 = _m0194['light_source']
            if light_spread is None or int(light_spread) <= 0 or int(light_spread) == 45:
                _m0218 = int(_m0194['light_spread'])
            else:
                _m0218 = int(light_spread)
        _m0215 = int(glanz) if glanz is not None and int(glanz) >= 0 else int(_m0194['glanz'])
        return (_m0217, max(5, min(100, _m0218)), max(0, min(100, _m0215)))

    @staticmethod
    def _m0375(_m0434, _m0571, _m0190=(0, 0, 0)):
        _m0277 = Gimp.Gradient.new(f'Borderlay Beam {uuid4().hex[:8]}')
        if _m0277 is None:
            raise RuntimeError('Der Lichtstrahl-Verlauf konnte nicht erstellt werden.')
        if not _m0277.segment_range_split_uniform(0, 0, 2):
            _m0277.delete()
            raise RuntimeError('Der Lichtstrahl-Verlauf konnte nicht geteilt werden.')
        try:
            _m0277.segment_set_left_color(0, _m0002._m0299(_m0190))
            _m0277.segment_set_right_color(0, _m0002._m0299(_m0434))
            _m0277.segment_set_right_pos(0, 0.5)
            _m0277.segment_set_middle_pos(0, 0.32)
            _m0277.segment_set_left_color(1, _m0002._m0299(_m0434))
            _m0277.segment_set_right_color(1, _m0002._m0299(_m0190))
            _m0277.segment_set_middle_pos(1, 0.68)
        except Exception:
            _m0277.delete()
            raise
        return _m0277

    @classmethod
    def _m0477(cls, image, layer, outer_box, angle_deg, _m0561, _m0434, _m0571, _m0409=0.22):
        if Gimp.Selection.is_empty(image):
            return
        ox1, oy1, ox2, oy2 = outer_box
        w = float(ox2 - ox1)
        h = float(oy2 - oy1)
        _m0199 = math.hypot(w, h)
        cx = (float(ox1) + float(ox2)) / 2.0
        cy = (float(oy1) + float(oy2)) / 2.0
        rad = math.radians(float(angle_deg))
        _m0593 = math.cos(rad)
        _m0594 = -math.sin(rad)
        _m0126 = cx + _m0593 * (w * _m0409)
        _m0127 = cy + _m0594 * (h * _m0409)
        _m0516 = max(0.05, min(1.0, float(_m0561) / 100.0))
        _m0295 = max(14.0, _m0199 * (0.06 + 0.46 * _m0516))
        _m0286 = _m0126 + _m0593 * _m0295
        _m0288 = _m0127 + _m0594 * _m0295
        _m0287 = _m0126 - _m0593 * _m0295
        _m0289 = _m0127 - _m0594 * _m0295
        grad = cls._m0375(_m0434, _m0571, (0, 0, 0))
        try:
            Gimp.context_set_gradient(grad)
            layer.edit_gradient_fill(Gimp.GradientType.LINEAR, 0.0, False, 1, 0.0, True, float(_m0286), float(_m0288), float(_m0287), float(_m0289))
        finally:
            grad.delete()

    @staticmethod
    def _m0481(image, layer, outer_box, angle_deg, _m0561, _m0377, _m0434, _m0571, _m0397=False, _m0472=1.0):
        if Gimp.Selection.is_empty(image):
            return
        ox1, oy1, ox2, oy2 = outer_box
        w = float(ox2 - ox1)
        h = float(oy2 - oy1)
        _m0199 = math.hypot(w, h)
        cx = (float(ox1) + float(ox2)) / 2.0
        cy = (float(oy1) + float(oy2)) / 2.0
        rad = math.radians(float(angle_deg))
        _m0559 = cx + math.cos(rad) * (w * 0.28)
        _m0560 = cy - math.sin(rad) * (h * 0.28)
        if _m0397:
            _m0559 = cx - (_m0559 - cx)
            _m0560 = cy - (_m0560 - cy)
        _m0516 = max(0.05, min(1.0, float(_m0561) / 100.0))
        _m0175 = max(24.0, _m0199 * (0.18 + 0.64 * _m0516) * float(_m0472))
        grad = _m0377(_m0434, _m0571, (0, 0, 0))
        try:
            Gimp.context_set_gradient(grad)
            layer.edit_gradient_fill(Gimp.GradientType.RADIAL, 0.0, False, 1, 0.0, True, float(_m0559), float(_m0560), float(_m0559 + _m0175), float(_m0560 + _m0175 * 0.72))
        finally:
            grad.delete()
