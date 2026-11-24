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
    def _m0244(material: str) -> dict:
        mat_key = (material or 'gold').strip().lower()
        return dict(config.MATERIAL_LIGHT_DEFAULTS.get(mat_key, config.MATERIAL_LIGHT_DEFAULTS['gold']))

    @classmethod
    def resolve_material_lighting(cls, material: str, light_source: str='auto', light_spread: int=-1, glanz: int=-1) -> tuple:
        _m0173 = cls._m0244(material)
        _m0439 = (light_source or 'auto').strip().lower()
        if _m0439 in ('beam', 'cone'):
            _m0195 = _m0439
            _m0196 = int(light_spread) if light_spread is not None and int(light_spread) > 0 else int(_m0173['light_spread'])
        else:
            _m0195 = _m0173['light_source']
            if light_spread is None or int(light_spread) <= 0 or int(light_spread) == 45:
                _m0196 = int(_m0173['light_spread'])
            else:
                _m0196 = int(light_spread)
        _m0193 = int(glanz) if glanz is not None and int(glanz) >= 0 else int(_m0173['glanz'])
        return (_m0195, max(5, min(100, _m0196)), max(0, min(100, _m0193)))

    @staticmethod
    def _m0341(_m0399, _m0527, _m0169=(0, 0, 0)):
        _m0248 = Gimp.Gradient.new(f'Borderlay Beam {uuid4().hex[:8]}')
        if _m0248 is None:
            raise RuntimeError('Der Lichtstrahl-Verlauf konnte nicht erstellt werden.')
        if not _m0248.segment_range_split_uniform(0, 0, 2):
            _m0248.delete()
            raise RuntimeError('Der Lichtstrahl-Verlauf konnte nicht geteilt werden.')
        try:
            _m0248.segment_set_left_color(0, _m0002._m0269(_m0169))
            _m0248.segment_set_right_color(0, _m0002._m0269(_m0399))
            _m0248.segment_set_right_pos(0, 0.5)
            _m0248.segment_set_middle_pos(0, 0.32)
            _m0248.segment_set_left_color(1, _m0002._m0269(_m0399))
            _m0248.segment_set_right_color(1, _m0002._m0269(_m0169))
            _m0248.segment_set_middle_pos(1, 0.68)
        except Exception:
            _m0248.delete()
            raise
        return _m0248

    @classmethod
    def _m0440(cls, image, layer, outer_box, angle_deg, _m0520, _m0399, _m0527, _m0374=0.22):
        if Gimp.Selection.is_empty(image):
            return
        ox1, oy1, ox2, oy2 = outer_box
        w = float(ox2 - ox1)
        h = float(oy2 - oy1)
        _m0178 = math.hypot(w, h)
        cx = (float(ox1) + float(ox2)) / 2.0
        cy = (float(oy1) + float(oy2)) / 2.0
        rad = math.radians(float(angle_deg))
        _m0548 = math.cos(rad)
        _m0549 = -math.sin(rad)
        _m0108 = cx + _m0548 * (w * _m0374)
        _m0109 = cy + _m0549 * (h * _m0374)
        _m0475 = max(0.05, min(1.0, float(_m0520) / 100.0))
        _m0266 = max(14.0, _m0178 * (0.06 + 0.46 * _m0475))
        _m0257 = _m0108 + _m0548 * _m0266
        _m0259 = _m0109 + _m0549 * _m0266
        _m0258 = _m0108 - _m0548 * _m0266
        _m0260 = _m0109 - _m0549 * _m0266
        grad = cls._m0341(_m0399, _m0527, (0, 0, 0))
        try:
            Gimp.context_set_gradient(grad)
            layer.edit_gradient_fill(Gimp.GradientType.LINEAR, 0.0, False, 1, 0.0, True, float(_m0257), float(_m0259), float(_m0258), float(_m0260))
        finally:
            grad.delete()

    @staticmethod
    def _m0444(image, layer, outer_box, angle_deg, _m0520, _m0343, _m0399, _m0527, _m0362=False, _m0436=1.0):
        if Gimp.Selection.is_empty(image):
            return
        ox1, oy1, ox2, oy2 = outer_box
        w = float(ox2 - ox1)
        h = float(oy2 - oy1)
        _m0178 = math.hypot(w, h)
        cx = (float(ox1) + float(ox2)) / 2.0
        cy = (float(oy1) + float(oy2)) / 2.0
        rad = math.radians(float(angle_deg))
        _m0518 = cx + math.cos(rad) * (w * 0.28)
        _m0519 = cy - math.sin(rad) * (h * 0.28)
        if _m0362:
            _m0518 = cx - (_m0518 - cx)
            _m0519 = cy - (_m0519 - cy)
        _m0475 = max(0.05, min(1.0, float(_m0520) / 100.0))
        _m0156 = max(24.0, _m0178 * (0.18 + 0.64 * _m0475) * float(_m0436))
        grad = _m0343(_m0399, _m0527, (0, 0, 0))
        try:
            Gimp.context_set_gradient(grad)
            layer.edit_gradient_fill(Gimp.GradientType.RADIAL, 0.0, False, 1, 0.0, True, float(_m0518), float(_m0519), float(_m0518 + _m0156), float(_m0519 + _m0156 * 0.72))
        finally:
            grad.delete()
