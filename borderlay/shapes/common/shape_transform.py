# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import math
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
_m0008 = ('tl', 'tc', 'tr', 'ml', 'center', 'mr', 'bl', 'bc', 'br')
_m0014 = 'step'

class ShapeTransformHelper:
    _m0007 = 36

    @staticmethod
    def set_active_fade_mode(mode: str):
        global _m0014
        clean = str(mode or 'step').strip().lower()
        _m0014 = 'end_target' if clean == 'end_target' else 'step'

    @staticmethod
    def _m0243() -> str:
        return _m0014

    @staticmethod
    def _m0068():
        for name in ('NOHALO', 'LOHALO', 'CUBIC'):
            mode = getattr(Gimp.InterpolationType, name, None)
            if mode is None:
                continue
            try:
                Gimp.context_set_interpolation(mode)
                return
            except Exception:
                continue

    @staticmethod
    def _m0452(box: tuple, pivot_mode: str='center') -> tuple:
        x1, y1, x2, y2 = [float(v) for v in box]
        cx = (x1 + x2) / 2.0
        cy = (y1 + y2) / 2.0
        mode = (pivot_mode or 'center').strip().lower()
        _m0405 = {'tl': (x1, y1), 'tc': (cx, y1), 'tr': (x2, y1), 'ml': (x1, cy), 'center': (cx, cy), 'mr': (x2, cy), 'bl': (x1, y2), 'bc': (cx, y2), 'br': (x2, y2)}
        return _m0405.get(mode, (cx, cy))

    @staticmethod
    def _m0067(text: str, _m0172: int) -> tuple:
        parts = str(text or '').split(':')
        fade = 'step'
        times = int(_m0172)
        if len(parts) > 1 and parts[1] in ('step', 'end_target'):
            fade = parts[1]
        if len(parts) > 2:
            try:
                times = int(parts[2])
            except ValueError:
                times = int(_m0172)
        return (fade, times)

    @classmethod
    def parse_rotation_mode(cls, _m0202, cycle_times: int, cycle_until: int) -> tuple:
        text = str(_m0202 or '').strip().lower()
        fade = 'step'
        times = max(1, int(cycle_times or 1))
        kind = ''
        if text.startswith('cycle:'):
            fade, times = cls._m0067(text, 6)
            kind = 'cycle'
        elif text.startswith('offset:'):
            fade, times = cls._m0067(text, 2)
            kind = 'offset'
            times = max(2, min(4, times))
        elif text == 'end_target':
            fade = 'end_target'
        if not kind:
            if int(cycle_until or 0) != 0:
                kind = 'until'
            elif times > 1:
                kind = 'offset'
            else:
                kind = 'sweep'
        return (kind, fade, max(1, min(12, times)))

    @classmethod
    def compute_rotation_series(cls, repeat_enabled: bool, single_angle: int, angle_start: int, angle_end: int, angle_step: int, fade_pct: int, fade_mode: str='', cycle_times: int=1, cycle_until: int=0, array_kind: str='') -> list:
        if not repeat_enabled:
            return [(int(single_angle), 1.0)]
        return [(int(single_angle), 1.0)]

    @classmethod
    def _m0154(cls, box: tuple, angle_deg: float, pivot_mode: str='center', extra_margin: int=0) -> tuple:
        x1, y1, x2, y2 = [float(v) for v in box]
        px, py = cls._m0452(box, pivot_mode)
        rad = math.radians(float(angle_deg))
        _m0162 = math.cos(rad)
        _m0509 = math.sin(rad)
        _m0161 = ((x1, y1), (x2, y1), (x2, y2), (x1, y2))
        _m0473 = []
        _m0474 = []
        for cx, cy in _m0161:
            dx = cx - px
            dy = cy - py
            rx = px + dx * _m0162 - dy * _m0509
            ry = py + dx * _m0509 + dy * _m0162
            _m0473.append(rx)
            _m0474.append(ry)
        m = float(max(0, int(extra_margin)))
        return (int(math.floor(min(_m0473) - m)), int(math.floor(min(_m0474) - m)), int(math.ceil(max(_m0473) + m)), int(math.ceil(max(_m0474) + m)))

    @classmethod
    def _m0201(cls, image, box: tuple, schedule: list, pivot_mode: str, extra_margin: int=0) -> tuple:
        return (0, 0)

    @classmethod
    def ensure_canvas_for_rotated_box(cls, image, box: tuple, angle_deg: float, pivot_mode: str='center', extra_margin: int=4) -> tuple:
        if abs(float(angle_deg)) < 0.05:
            return (0, 0)
        return cls._m0201(image, box, [(int(round(float(angle_deg))), 1.0)], pivot_mode, extra_margin=extra_margin)

    @staticmethod
    def _m0029(image, _m0147: tuple, _m0417: list) -> None:
        seen = set()
        for _m0146 in _m0147:
            if _m0146 is None or id(_m0146) in seen:
                continue
            seen.add(id(_m0146))
            if _m0146.is_valid():
                try:
                    image.remove_channel(_m0146)
                except Exception:
                    pass
        _m0550 = [lyr for lyr in _m0417 if lyr is not None and lyr.is_valid()]
        if _m0550:
            try:
                image.set_selected_layers(_m0550)
            except Exception:
                pass

    @classmethod
    def rotate_current_selection(cls, image, angle_deg: float, pivot_mode: str='center', ref_box: tuple=None):
        if abs(float(angle_deg)) < 0.05 or Gimp.Selection.is_empty(image):
            return
        if ref_box is None:
            x1, y1, x2, y2 = Gimp.Selection.bounds(image)[-4:]
            ref_box = (int(x1), int(y1), int(x2), int(y2))
        px, py = cls._m0452(ref_box, pivot_mode)
        rad = math.radians(float(angle_deg))
        try:
            _m0417 = list(image.get_selected_layers())
        except Exception:
            _m0417 = []
        _m0479 = Gimp.Selection.save(image)
        if _m0479 is None:
            return
        _m0531 = _m0479.copy()
        image.insert_channel(_m0531, None, 0)
        _m0472 = None
        try:
            Gimp.Selection.none(image)
            Gimp.context_push()
            try:
                Gimp.context_set_transform_resize(Gimp.TransformResize.CLIP)
            except Exception:
                pass
            ShapeTransformHelper._m0068()
            _m0472 = _m0531.transform_rotate(rad, False, float(px), float(py))
            Gimp.context_pop()
            image.select_item(Gimp.ChannelOps.REPLACE, _m0472 if _m0472 is not None else _m0531)
        finally:
            cls._m0029(image, (_m0472, _m0531, _m0479), _m0417)

    @staticmethod
    def _m0075(image, drawable, angle_deg: float, px: float, py: float):
        if abs(float(angle_deg)) < 0.05 or drawable is None or (not drawable.is_valid()):
            return drawable
        rad = math.radians(float(angle_deg))
        Gimp.Selection.none(image)
        Gimp.context_push()
        try:
            Gimp.context_set_transform_resize(Gimp.TransformResize.CLIP)
        except Exception:
            pass
        ShapeTransformHelper._m0068()
        try:
            _m0450 = drawable.transform_rotate(rad, False, float(px), float(py))
            target = _m0450 if _m0450 is not None else drawable
            if hasattr(target, 'resize_to_image_size') and (not target.is_group()):
                try:
                    target.resize_to_image_size()
                except Exception:
                    pass
            return target
        finally:
            Gimp.context_pop()

    @classmethod
    def _m0072(cls, children) -> None:
        for child in children:
            if hasattr(child, 'resize_to_image_size') and (not child.is_group()):
                try:
                    child.resize_to_image_size()
                except Exception:
                    pass

    @classmethod
    def _m0074(cls, image, _m0449, angle, px, py, pump_fn):
        Gimp.Selection.none(image)
        for child in list(_m0449.get_children()):
            if child is not None and child.is_valid():
                if hasattr(child, 'resize_to_image_size') and (not child.is_group()):
                    try:
                        child.resize_to_image_size()
                    except Exception:
                        pass
                cls._m0075(image, child, float(angle), px, py)
        name = _m0449.get_name() or 'Borderlay'
        _m0449.set_name(f'{name} ({angle}°)')
        if callable(pump_fn):
            pump_fn()
        return _m0449

    @classmethod
    def apply_post_render_rotation(cls, image, _m0449, outer_box: tuple, schedule: list, pivot_mode: str='center', pump_fn=None):
        if not schedule:
            return _m0449
        _m0304 = len(schedule) > 1
        _m0214, _ = schedule[0]
        if not _m0304 and abs(int(_m0214)) == 0:
            return _m0449
        pad_left, pad_top = cls._m0201(image, outer_box, schedule, pivot_mode, extra_margin=4)
        _m0498 = (outer_box[0] + pad_left, outer_box[1] + pad_top, outer_box[2] + pad_left, outer_box[3] + pad_top)
        px, py = cls._m0452(_m0498, pivot_mode)
        if not _m0304:
            return cls._m0074(image, _m0449, _m0214, px, py, pump_fn)
        return _m0449
