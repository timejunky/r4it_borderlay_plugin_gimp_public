# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gimp', '3.0')
gi.require_version('Gegl', '0.4')
from gi.repository import Gegl, Gimp

class _m0002:

    @staticmethod
    def _m0269(rgb):
        r, g, b = (max(0, min(255, int(c))) for c in rgb)
        return Gegl.Color.new(f'#{r:02x}{g:02x}{b:02x}')

    @staticmethod
    def _m0369(image, _m0395, name, opacity=100.0, mode=Gimp.LayerMode.NORMAL):
        layer = Gimp.Layer.new(image, name, image.get_width(), image.get_height(), Gimp.ImageType.RGBA_IMAGE, float(opacity), mode)
        image.insert_layer(layer, _m0395, 0)
        layer.fill(Gimp.FillType.TRANSPARENT)
        return layer

    @staticmethod
    def _m0489(drawable, _m0375, _m0421=None, **kwargs):
        _m0217 = Gimp.DrawableFilter.new(drawable, _m0375, _m0375)
        cfg = _m0217.get_config()
        if _m0421:
            for key, value in _m0421.items():
                cfg.set_property(key, value)
        for key, value in kwargs.items():
            cfg.set_property(key, value)
        _m0217.update()
        drawable.merge_filter(_m0217)
