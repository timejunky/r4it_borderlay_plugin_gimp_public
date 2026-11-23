# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
from utils import _m0002

class LuxusBloom:

    def __init__(self, image, group, glanz, material='gold'):
        self.image = image
        self.group = group
        self.glanz = glanz
        self.material = material

    def render(self, metal_layer):
        if self.glanz <= 0:
            return
        _m0368 = metal_layer.copy()
        _m0368.set_name('Luxus Glow (Bloom)')
        _m0368.set_mode(Gimp.LayerMode.SCREEN)
        _m0368.set_opacity(max(6, min(42, round(self.glanz * 0.32))))
        self.image.insert_layer(_m0368, self.group, 0)
        _m0002._m0530(_m0368, 'gegl:levels', **{'in-low': 0.86, 'in-high': 1.0, 'out-low': 0.0, 'out-high': 1.0})
        _m0002._m0530(_m0368, 'gegl:gaussian-blur', **{'std-dev-x': 3.5, 'std-dev-y': 3.5})
