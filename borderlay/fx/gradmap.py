# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
from uuid import uuid4
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
import config
from community_material_seal import apply_community_materials, community_material_key
from utils import _m0002

class _m0004:

    def __init__(self, image, material='gold', inlay_rgb=(36, 17, 52), gimp_gradient_name=''):
        self.image = image
        self.material = community_material_key(material)
        self.inlay_rgb = inlay_rgb
        self.gimp_gradient_name = (gimp_gradient_name or '').strip()

    @staticmethod
    def _m0373(_m0346, _m0500):
        _m0277 = Gimp.Gradient.new(f'Borderlay ZoneGrad {uuid4().hex[:8]}')
        if _m0277 is None:
            raise RuntimeError('Der 2-Stopp-Zonenverlauf konnte nicht erstellt werden.')
        if not _m0277.segment_set_left_color(0, _m0002._m0299(_m0346)):
            _m0277.delete()
            raise RuntimeError('Die linke Zonenfarbe konnte nicht gesetzt werden.')
        if not _m0277.segment_set_right_color(0, _m0002._m0299(_m0500)):
            _m0277.delete()
            raise RuntimeError('Die rechte Zonenfarbe konnte nicht gesetzt werden.')
        return _m0277

    @staticmethod
    def _m0374(_m0149, _m0156, _m0150, _m0433=0.5):
        _m0277 = Gimp.Gradient.new(f'Borderlay RidgeGrad {uuid4().hex[:8]}')
        if _m0277 is None:
            raise RuntimeError('Der 3-Stopp-Zonenverlauf konnte nicht erstellt werden.')
        if not _m0277.segment_range_split_uniform(0, 0, 2):
            _m0277.delete()
            raise RuntimeError('Der 3-Stopp-Zonenverlauf konnte nicht in Segmente geteilt werden.')
        try:
            if not _m0277.segment_set_left_color(0, _m0002._m0299(_m0149)):
                raise RuntimeError('Linke Farbe in Segment 0 konnte nicht gesetzt werden.')
            if not _m0277.segment_set_right_color(0, _m0002._m0299(_m0156)):
                raise RuntimeError('Rechte Farbe in Segment 0 konnte nicht gesetzt werden.')
            if not _m0277.segment_set_right_pos(0, float(_m0433))[0]:
                raise RuntimeError('Position für Segment 0 konnte nicht gesetzt werden.')
            if not _m0277.segment_set_left_color(1, _m0002._m0299(_m0156)):
                raise RuntimeError('Linke Farbe in Segment 1 konnte nicht gesetzt werden.')
            if not _m0277.segment_set_right_color(1, _m0002._m0299(_m0150)):
                raise RuntimeError('Rechte Farbe in Segment 1 konnte nicht gesetzt werden.')
        except Exception:
            _m0277.delete()
            raise
        return _m0277

    @staticmethod
    def _m0376(stops, _m0498):
        _m0277 = Gimp.Gradient.new(f'Borderlay GradMap {uuid4().hex[:8]}')
        if _m0277 is None:
            raise RuntimeError('Der Gradient-Map-Verlauf konnte nicht erstellt werden.')
        _m0405 = len(stops) - 1
        if not _m0277.segment_range_split_uniform(0, 0, _m0405):
            _m0277.delete()
            raise RuntimeError('Der Gradient-Map-Verlauf konnte nicht aufgeteilt werden.')
        try:
            for index in range(_m0405):
                if not _m0277.segment_set_left_color(index, _m0002._m0299(stops[index])):
                    raise RuntimeError(f'Linke Farbe in Segment {index} konnte nicht gesetzt werden.')
                if not _m0277.segment_set_right_color(index, _m0002._m0299(stops[index + 1])):
                    raise RuntimeError(f'Rechte Farbe in Segment {index} konnte nicht gesetzt werden.')
                if _m0498[index] < 1.0:
                    if not _m0277.segment_set_right_pos(index, _m0498[index])[0]:
                        raise RuntimeError(f'Segmentposition {index} konnte nicht gesetzt werden.')
                left = _m0277.segment_get_left_pos(index)
                right = _m0277.segment_get_right_pos(index)
                if not left[0] or not right[0]:
                    raise RuntimeError(f'Segmentgrenzen {index} konnten nicht gelesen werden.')
                if not _m0277.segment_set_middle_pos(index, (left[1] + right[1]) / 2.0)[0]:
                    raise RuntimeError(f'Segmentmitte {index} konnte nicht gesetzt werden.')
        except Exception:
            _m0277.delete()
            raise
        return _m0277

    def _m0491(self):
        if not self.gimp_gradient_name or self.gimp_gradient_name.lower() in ('none', 'auto', ''):
            return None
        try:
            grad = Gimp.Gradient.get_by_name(self.gimp_gradient_name)
            if grad is not None:
                return grad
        except Exception:
            pass
        return None

    def _m0112(self, layer, _m0379=None):
        apply_community_materials()
        _m0403 = self._m0491()
        _m0183 = False
        if _m0403 is not None and _m0379 in (None, self.material):
            _m0277 = _m0403
        else:
            mat = _m0379 if _m0379 in config.GRADMAP_METALS else self.material
            if mat == 'colored_glass':
                from fx.glass_facets import GlassFacetsHelper
                stops = GlassFacetsHelper.build_glass_gradmap(self.inlay_rgb)
            else:
                stops = config.GRADMAP_METALS.get(mat, config.GRADMAP_METALS['gold'])
            _m0277 = self._m0376(stops, config.gradmap_positions(stops))
            _m0183 = True
        try:
            if not Gimp.context_set_gradient(_m0277):
                raise RuntimeError('Der Gradient-Map-Verlauf konnte nicht aktiviert werden.')
            procedure = Gimp.get_pdb().lookup_procedure('plug-in-gradmap')
            if procedure is None:
                raise RuntimeError("GIMPs 'plug-in-gradmap' Prozedur wurde nicht gefunden.")
            cfg = procedure.create_config()
            cfg.set_property('run-mode', Gimp.RunMode.NONINTERACTIVE)
            cfg.set_property('image', self.image)
            cfg.set_core_object_array('drawables', [layer])
            Gimp.Selection.none(self.image)
            result = procedure.run(cfg)
            if result.index(0) != Gimp.PDBStatusType.SUCCESS:
                raise RuntimeError(f'plug-in-gradmap fehlgeschlagen: {result.index(0)}')
        finally:
            if _m0183:
                _m0277.delete()

    def _m0235(self, layer, c1, c2, _m0148, _m0369, _m0371, _m0370, _m0372, _m0433=0.48):
        if _m0148 is None:
            grad = self._m0373(c1, c2)
        else:
            grad = self._m0374(c1, c2, _m0148, _m0433=_m0433)
        try:
            if not Gimp.context_set_gradient(grad):
                raise RuntimeError('Der Zonenverlauf konnte nicht im Kontext aktiviert werden.')
            if not layer.edit_gradient_fill(Gimp.GradientType.LINEAR, 0.0, False, 1, 0.0, True, _m0369, _m0371, _m0370, _m0372):
                raise RuntimeError('Der lineare Zonenverlauf konnte nicht gezeichnet werden.')
        finally:
            grad.delete()

    def _m0238(self, layer, _m0163, _m0164, radius, _m0321, _m0387, _m0414):
        c1 = (int(_m0321), int(_m0321), int(_m0321))
        c2 = (int(_m0387), int(_m0387), int(_m0387))
        _m0148 = (int(_m0414), int(_m0414), int(_m0414))
        grad = self._m0374(c1, c2, _m0148, _m0433=0.45)
        try:
            if Gimp.context_set_gradient(grad):
                layer.edit_gradient_fill(Gimp.GradientType.RADIAL, 0.0, False, 1, 0.0, True, float(_m0163), float(_m0164), float(_m0163 + radius), float(_m0164 + radius * 0.55))
        finally:
            grad.delete()
