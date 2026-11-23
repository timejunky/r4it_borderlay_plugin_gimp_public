# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import math
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp

class FreeformSelectionHelper:
    _m0029 = None
    _m0070 = None
    _m0053 = None
    _m0069 = None
    _m0052 = None
    _m0031 = 0

    @classmethod
    def clear_state(cls, image=None):
        for ch_attr in ('_base_channel', '_outer_channel', '_inner_channel'):
            _m0165 = getattr(cls, ch_attr, None)
            setattr(cls, ch_attr, None)
            if _m0165 is not None and image is not None:
                try:
                    if _m0165.is_valid():
                        image.remove_channel(_m0165)
                except Exception:
                    pass
        cls._m0069 = None
        cls._m0052 = None
        cls._m0031 = 0

    @classmethod
    def init_contour(cls, image, orig_sel, width: int, position: str, outer_box, inner_box):
        cls.clear_state(image)
        cls._m0069 = outer_box
        cls._m0052 = inner_box
        cls._m0031 = max(1, int(width))
        image.select_item(Gimp.ChannelOps.REPLACE, orig_sel)
        cls._m0029 = Gimp.Selection.save(image)
        image.select_item(Gimp.ChannelOps.REPLACE, cls._m0029)
        if position == 'aussen':
            Gimp.Selection.grow(image, cls._m0031)
        elif position in ('zentriert', 'mitte'):
            w_out = int(math.ceil(float(cls._m0031) / 2.0))
            if w_out > 0:
                Gimp.Selection.grow(image, w_out)
        cls._m0070 = Gimp.Selection.save(image)
        image.select_item(Gimp.ChannelOps.REPLACE, cls._m0070)
        Gimp.Selection.shrink(image, cls._m0031)
        cls._m0053 = Gimp.Selection.save(image)

    @classmethod
    def _m0092(cls, image, op, _m0197: int):
        if cls._m0070 is None or not cls._m0070.is_valid():
            return False
        d = int(round(_m0197))
        if d <= 0:
            if op == Gimp.ChannelOps.REPLACE:
                image.select_item(Gimp.ChannelOps.REPLACE, cls._m0070)
                if d < 0:
                    Gimp.Selection.grow(image, abs(d))
            else:
                _m0584 = cls._m0070.copy()
                image.insert_channel(_m0584, None, 0)
                try:
                    image.select_item(op, _m0584)
                finally:
                    image.remove_channel(_m0584)
            return True
        _m0453 = None
        if op != Gimp.ChannelOps.REPLACE:
            _m0453 = Gimp.Selection.save(image)
        try:
            image.select_item(Gimp.ChannelOps.REPLACE, cls._m0070)
            Gimp.Selection.shrink(image, d)
            _m0546 = Gimp.Selection.is_empty(image)
            if _m0453 is None:
                return True
            _m0545 = None if _m0546 else Gimp.Selection.save(image)
            try:
                image.select_item(Gimp.ChannelOps.REPLACE, _m0453)
                if _m0545 is not None:
                    image.select_item(op, _m0545)
            finally:
                if _m0545 is not None:
                    image.remove_channel(_m0545)
        finally:
            if _m0453 is not None:
                image.remove_channel(_m0453)
        return True

    @classmethod
    def select_contour_box(cls, image, op, x1, y1, x2, y2):
        if cls._m0069 is None or cls._m0070 is None:
            w = max(1.0, float(x2 - x1))
            h = max(1.0, float(y2 - y1))
            image.select_rectangle(op, float(x1), float(y1), w, h)
            return
        ox1, oy1, _m0071, _m0072 = cls._m0069
        _m0197 = round((float(x1) - float(ox1) + (float(y1) - float(oy1))) / 2.0)
        cls._m0092(image, op, _m0197)
