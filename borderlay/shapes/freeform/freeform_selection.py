# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import math
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp

class FreeformSelectionHelper:
    _m0025 = None
    _m0058 = None
    _m0043 = None
    _m0057 = None
    _m0042 = None
    _m0026 = 0

    @classmethod
    def clear_state(cls, image=None):
        for ch_attr in ('_base_channel', '_outer_channel', '_inner_channel'):
            _m0146 = getattr(cls, ch_attr, None)
            setattr(cls, ch_attr, None)
            if _m0146 is not None and image is not None:
                try:
                    if _m0146.is_valid():
                        image.remove_channel(_m0146)
                except Exception:
                    pass
        cls._m0057 = None
        cls._m0042 = None
        cls._m0026 = 0

    @classmethod
    def init_contour(cls, image, orig_sel, width: int, position: str, outer_box, inner_box):
        cls.clear_state(image)
        cls._m0057 = outer_box
        cls._m0042 = inner_box
        cls._m0026 = max(1, int(width))
        image.select_item(Gimp.ChannelOps.REPLACE, orig_sel)
        cls._m0025 = Gimp.Selection.save(image)
        image.select_item(Gimp.ChannelOps.REPLACE, cls._m0025)
        if position == 'aussen':
            Gimp.Selection.grow(image, cls._m0026)
        elif position in ('zentriert', 'mitte'):
            w_out = int(math.ceil(float(cls._m0026) / 2.0))
            if w_out > 0:
                Gimp.Selection.grow(image, w_out)
        cls._m0058 = Gimp.Selection.save(image)
        image.select_item(Gimp.ChannelOps.REPLACE, cls._m0058)
        Gimp.Selection.shrink(image, cls._m0026)
        cls._m0043 = Gimp.Selection.save(image)

    @classmethod
    def _m0079(cls, image, op, _m0176: int):
        if cls._m0058 is None or not cls._m0058.is_valid():
            return False
        d = int(round(_m0176))
        if d <= 0:
            if op == Gimp.ChannelOps.REPLACE:
                image.select_item(Gimp.ChannelOps.REPLACE, cls._m0058)
                if d < 0:
                    Gimp.Selection.grow(image, abs(d))
            else:
                _m0540 = cls._m0058.copy()
                image.insert_channel(_m0540, None, 0)
                try:
                    image.select_item(op, _m0540)
                finally:
                    image.remove_channel(_m0540)
            return True
        _m0418 = None
        if op != Gimp.ChannelOps.REPLACE:
            _m0418 = Gimp.Selection.save(image)
        try:
            image.select_item(Gimp.ChannelOps.REPLACE, cls._m0058)
            Gimp.Selection.shrink(image, d)
            _m0505 = Gimp.Selection.is_empty(image)
            if _m0418 is None:
                return True
            _m0504 = None if _m0505 else Gimp.Selection.save(image)
            try:
                image.select_item(Gimp.ChannelOps.REPLACE, _m0418)
                if _m0504 is not None:
                    image.select_item(op, _m0504)
            finally:
                if _m0504 is not None:
                    image.remove_channel(_m0504)
        finally:
            if _m0418 is not None:
                image.remove_channel(_m0418)
        return True

    @classmethod
    def select_contour_box(cls, image, op, x1, y1, x2, y2):
        if cls._m0057 is None or cls._m0058 is None:
            w = max(1.0, float(x2 - x1))
            h = max(1.0, float(y2 - y1))
            image.select_rectangle(op, float(x1), float(y1), w, h)
            return
        ox1, oy1, _m0059, _m0060 = cls._m0057
        _m0176 = round((float(x1) - float(ox1) + (float(y1) - float(oy1))) / 2.0)
        cls._m0079(image, op, _m0176)
