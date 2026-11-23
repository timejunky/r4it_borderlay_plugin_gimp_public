# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gimp', '3.0')
gi.require_version('Gegl', '0.4')
from gi.repository import Gegl, Gimp

class _m0002:

    @staticmethod
    def _m0299(rgb):
        r, g, b = (max(0, min(255, int(c))) for c in rgb)
        return Gegl.Color.new(f'#{r:02x}{g:02x}{b:02x}')

    @staticmethod
    def _m0404(image, _m0430, name, opacity=100.0, mode=Gimp.LayerMode.NORMAL):
        layer = Gimp.Layer.new(image, name, image.get_width(), image.get_height(), Gimp.ImageType.RGBA_IMAGE, float(opacity), mode)
        image.insert_layer(layer, _m0430, 0)
        layer.fill(Gimp.FillType.TRANSPARENT)
        return layer

    @staticmethod
    def _m0530(drawable, _m0410, _m0457=None, **kwargs):
        _m0243 = Gimp.DrawableFilter.new(drawable, _m0410, _m0410)
        cfg = _m0243.get_config()
        if _m0457:
            for key, value in _m0457.items():
                cfg.set_property(key, value)
        for key, value in kwargs.items():
            cfg.set_property(key, value)
        _m0243.update()
        drawable.merge_filter(_m0243)
