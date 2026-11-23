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

    def _m0063(self, _m0171):
        if len(_m0171) != 5:
            _m0171 = config.sample_grad_stops(_m0171, 5)
        _m0277 = Gimp.Gradient.new(f'Borderlay FX Mapped {uuid4().hex}')
        if _m0277 is None:
            raise RuntimeError('Der Metallverlauf konnte nicht erstellt werden.')
        if not _m0277.segment_range_split_uniform(0, 0, 4):
            _m0277.delete()
            raise RuntimeError('Der Metallverlauf konnte nicht aufgeteilt werden.')
        _m0498 = (0.2, 0.5, 0.8, 1.0)
        try:
            for index in range(4):
                if not _m0277.segment_set_left_color(index, _m0002._m0299(_m0171[index])):
                    raise RuntimeError(f'Linke Farbe für Segment {index} konnte nicht gesetzt werden.')
                if not _m0277.segment_set_right_color(index, _m0002._m0299(_m0171[index + 1])):
                    raise RuntimeError(f'Rechte Farbe für Segment {index} konnte nicht gesetzt werden.')
                if _m0498[index] < 1.0:
                    if not _m0277.segment_set_right_pos(index, _m0498[index])[0]:
                        raise RuntimeError(f'Position für Segment {index} konnte nicht gesetzt werden.')
                _m0345 = _m0277.segment_get_left_pos(index)
                _m0499 = _m0277.segment_get_right_pos(index)
                if not _m0345[0] or not _m0499[0]:
                    raise RuntimeError(f'Positionen für Segment {index} konnten nicht gelesen werden.')
                _m0394 = (_m0345[1] + _m0499[1]) / 2.0
                if not _m0277.segment_set_middle_pos(index, _m0394)[0]:
                    raise RuntimeError(f'Mittelpunkt für Segment {index} konnte nicht gesetzt werden.')
        except Exception:
            _m0277.delete()
            raise
        return _m0277

    @staticmethod
    def _m0100(_m0456):
        if len(_m0456) != 5:
            _m0456 = config.sample_grad_stops(_m0456, 5)
        dark = min(_m0456[0], _m0456[4], key=sum)
        _m0393 = _m0456[2]
        light = max(_m0456[1], _m0456[3], key=sum)
        blend = lambda first, _m0529, weight=0.5: tuple((round(a * (1.0 - weight) + b * weight) for a, b in zip(first, _m0529)))
        _m0553 = blend(dark, _m0393, 0.35)
        _m0555 = blend(dark, _m0393, 0.68)
        _m0556 = blend(_m0393, light, 0.48)
        _m0554 = blend(_m0393, light, 0.82)
        return [_m0553, _m0555, _m0393, _m0556, _m0554]

    def render(self):
        _m0171 = self._m0100(config.METALS[self.material])
        _m0277 = self._m0063(list(reversed(_m0171)))
        if not Gimp.context_set_gradient(_m0277):
            _m0277.delete()
            raise RuntimeError('Der Metallverlauf konnte nicht im Kontext aktiviert werden.')
        metal_layer = _m0002._m0404(self.image, self.group, 'Base Material Directional')
        _m0296, has_selection, x1, y1, x2, y2 = Gimp.Selection.bounds(self.image)
        if not _m0296 or not has_selection:
            _m0277.delete()
            raise RuntimeError('Die Rahmenauswahl hat keine gültigen Grenzen für das Metallmaterial.')
        cx = (float(x1) + float(x2)) / 2.0
        cy = (float(y1) + float(y2)) / 2.0
        radius = math.hypot(float(x2 - x1), float(y2 - y1)) / 2.0
        angle = math.radians(float(self.angle))
        _m0369 = cx + math.cos(angle) * radius
        _m0371 = cy - math.sin(angle) * radius
        _m0370 = cx - math.cos(angle) * radius
        _m0372 = cy + math.sin(angle) * radius
        try:
            if not metal_layer.edit_gradient_fill(Gimp.GradientType.LINEAR, 0.0, True, 3, 0.2, True, _m0369, _m0371, _m0370, _m0372):
                raise RuntimeError('Der gerichtete Metallverlauf konnte nicht gezeichnet werden.')
        finally:
            _m0277.delete()
        return metal_layer
