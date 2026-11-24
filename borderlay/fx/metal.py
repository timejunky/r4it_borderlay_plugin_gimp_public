# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import math
from uuid import uuid4
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
import config
from community_material_seal import community_material_key
from utils import _m0002

class BaseMetal:

    def __init__(self, image, group, material, angle):
        self.image = image
        self.group = group
        self.material = community_material_key(material)
        self.angle = angle

    def _m0052(self, _m0152):
        if len(_m0152) != 5:
            _m0152 = config.sample_grad_stops(_m0152, 5)
        _m0248 = Gimp.Gradient.new(f'Borderlay FX Mapped {uuid4().hex}')
        if _m0248 is None:
            raise RuntimeError('Der Metallverlauf konnte nicht erstellt werden.')
        if not _m0248.segment_range_split_uniform(0, 0, 4):
            _m0248.delete()
            raise RuntimeError('Der Metallverlauf konnte nicht aufgeteilt werden.')
        _m0458 = (0.2, 0.5, 0.8, 1.0)
        try:
            for index in range(4):
                if not _m0248.segment_set_left_color(index, _m0002._m0269(_m0152[index])):
                    raise RuntimeError(f'Linke Farbe für Segment {index} konnte nicht gesetzt werden.')
                if not _m0248.segment_set_right_color(index, _m0002._m0269(_m0152[index + 1])):
                    raise RuntimeError(f'Rechte Farbe für Segment {index} konnte nicht gesetzt werden.')
                if _m0458[index] < 1.0:
                    if not _m0248.segment_set_right_pos(index, _m0458[index])[0]:
                        raise RuntimeError(f'Position für Segment {index} konnte nicht gesetzt werden.')
                _m0312 = _m0248.segment_get_left_pos(index)
                _m0459 = _m0248.segment_get_right_pos(index)
                if not _m0312[0] or not _m0459[0]:
                    raise RuntimeError(f'Positionen für Segment {index} konnten nicht gelesen werden.')
                _m0359 = (_m0312[1] + _m0459[1]) / 2.0
                if not _m0248.segment_set_middle_pos(index, _m0359)[0]:
                    raise RuntimeError(f'Mittelpunkt für Segment {index} konnte nicht gesetzt werden.')
        except Exception:
            _m0248.delete()
            raise
        return _m0248

    @staticmethod
    def _m0085(_m0420):
        if len(_m0420) != 5:
            _m0420 = config.sample_grad_stops(_m0420, 5)
        dark = min(_m0420[0], _m0420[4], key=sum)
        _m0358 = _m0420[2]
        light = max(_m0420[1], _m0420[3], key=sum)
        blend = lambda first, _m0488, weight=0.5: tuple((round(a * (1.0 - weight) + b * weight) for a, b in zip(first, _m0488)))
        _m0512 = blend(dark, _m0358, 0.35)
        _m0514 = blend(dark, _m0358, 0.68)
        _m0515 = blend(_m0358, light, 0.48)
        _m0513 = blend(_m0358, light, 0.82)
        return [_m0512, _m0514, _m0358, _m0515, _m0513]

    def render(self):
        _m0152 = self._m0085(config.METALS[self.material])
        _m0248 = self._m0052(list(reversed(_m0152)))
        if not Gimp.context_set_gradient(_m0248):
            _m0248.delete()
            raise RuntimeError('Der Metallverlauf konnte nicht im Kontext aktiviert werden.')
        metal_layer = _m0002._m0369(self.image, self.group, 'Base Material Directional')
        _m0267, has_selection, x1, y1, x2, y2 = Gimp.Selection.bounds(self.image)
        if not _m0267 or not has_selection:
            _m0248.delete()
            raise RuntimeError('Die Rahmenauswahl hat keine gültigen Grenzen für das Metallmaterial.')
        cx = (float(x1) + float(x2)) / 2.0
        cy = (float(y1) + float(y2)) / 2.0
        radius = math.hypot(float(x2 - x1), float(y2 - y1)) / 2.0
        angle = math.radians(float(self.angle))
        _m0335 = cx + math.cos(angle) * radius
        _m0337 = cy - math.sin(angle) * radius
        _m0336 = cx - math.cos(angle) * radius
        _m0338 = cy + math.sin(angle) * radius
        try:
            if not metal_layer.edit_gradient_fill(Gimp.GradientType.LINEAR, 0.0, True, 3, 0.2, True, _m0335, _m0337, _m0336, _m0338):
                raise RuntimeError('Der gerichtete Metallverlauf konnte nicht gezeichnet werden.')
        finally:
            _m0248.delete()
        return metal_layer
