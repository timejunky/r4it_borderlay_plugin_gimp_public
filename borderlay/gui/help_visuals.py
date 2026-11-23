# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
from __future__ import annotations
import math
from pathlib import Path
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from locales.i18n import t
_BRAND = Path(__file__).resolve().parents[1] / 'assets' / 'brand'
_PIVOT_OFFSET = {'tl': (-1, -1), 'tc': (0, -1), 'tr': (1, -1), 'ml': (-1, 0), 'center': (0, 0), 'mr': (1, 0), 'bl': (-1, 1), 'bc': (0, 1), 'br': (1, 1)}
_ROT_EXAMPLES = (('btn_rot_kind_sweep', [(0, 1), (8, 0.86), (16, 0.7), (24, 0.54), (32, 0.38), (40, 0.24), (48, 0.14)]), ('btn_rot_kind_until', [(a, max(0.12, 1.0 - i * 0.11)) for i, a in enumerate(range(0, 360, 40))]), ('btn_rot_kind_offset', [(0, 1), (18, 0.72), (36, 0.44), (54, 0.2), (7, 0.9), (25, 0.6), (43, 0.32)]), ('btn_rot_kind_cycle', [(0, 1), (12, 0.7), (24, 0.4), (36, 0.18), (60, 1), (72, 0.7), (84, 0.4), (96, 0.18), (120, 1), (132, 0.7), (144, 0.4), (156, 0.18)]))
_FADE_EXAMPLES = (('btn_fade_none', [(0, 1), (18, 1), (36, 1), (54, 1)]), ('btn_fade_mode_step', [(0, 1), (18, 0.55), (36, 0.2)]), ('btn_fade_mode_end', [(0, 1), (18, 0.72), (36, 0.48), (54, 0.28)]))

def _bg(cr, w: float, h: float) -> None:
    cr.set_source_rgb(0.96, 0.95, 0.93)
    cr.rectangle(0, 0, w, h)
    cr.fill()
    cr.set_source_rgba(0.45, 0.38, 0.34, 0.35)
    cr.set_line_width(1.0)
    cr.rectangle(0.5, 0.5, w - 1.0, h - 1.0)
    cr.stroke()

def _card(draw_fn, caption: str, width: int=128, height: int=74) -> Gtk.Box:
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
    area = Gtk.DrawingArea()
    area.set_size_request(width, height)
    area.connect('draw', draw_fn)
    box.pack_start(area, False, False, 0)
    lbl = Gtk.Label(label=caption)
    lbl.set_line_wrap(True)
    lbl.set_max_width_chars(18)
    lbl.set_justify(Gtk.Justification.CENTER)
    box.pack_start(lbl, False, False, 0)
    return box

def _draw_leaf_fan(cr, w: float, h: float, schedule, pivot: str='center') -> None:
    _bg(cr, w, h)
    cx, cy = (w / 2.0, h / 2.0)
    rw, rh = (min(w, h) * 0.16, min(w, h) * 0.3)
    ox, oy = _PIVOT_OFFSET.get(pivot, (0, 0))
    px, py = (cx + ox * rw, cy + oy * rh)
    cr.set_source_rgba(0.45, 0.38, 0.34, 0.28)
    cr.set_line_width(1.0)
    cr.rectangle(cx - rw, cy - rh, rw * 2.0, rh * 2.0)
    cr.stroke()
    for angle, opacity in reversed(schedule):
        alpha = max(0.16, min(1.0, float(opacity)))
        cr.save()
        cr.translate(px, py)
        cr.rotate(math.radians(float(angle)))
        cr.translate(-ox * rw, -oy * rh)
        cr.scale(rw, rh)
        cr.move_to(0, -1)
        cr.curve_to(0.62, -0.45, 0.48, 0.35, 0, 0.92)
        cr.curve_to(-0.48, 0.35, -0.62, -0.45, 0, -1)
        cr.close_path()
        cr.set_source_rgba(0.55, 0.28, 0.14, alpha)
        cr.fill_preserve()
        cr.set_source_rgba(0.28, 0.12, 0.06, min(1.0, alpha + 0.2))
        cr.set_line_width(0.06)
        cr.stroke()
        cr.restore()
    cr.set_source_rgba(0.25, 0.16, 0.1, 0.95)
    cr.set_line_width(1.5)
    cr.move_to(px - 6, py)
    cr.line_to(px + 6, py)
    cr.move_to(px, py - 6)
    cr.line_to(px, py + 6)
    cr.stroke()

def _draw_rounded_rect(cr, x: float, y: float, w: float, h: float, r: float) -> None:
    r = max(0.0, min(r, min(w, h) / 2.0))
    if r <= 0.5:
        cr.rectangle(x, y, w, h)
        return
    cr.new_sub_path()
    cr.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    cr.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    cr.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    cr.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    cr.close_path()

def _draw_corner_sample(cr, w: float, h: float, radius_out: float, radius_in: float, miter: bool) -> None:
    _bg(cr, w, h)
    m = 10.0
    bw = 16.0
    cr.set_source_rgb(0.76, 0.58, 0.24)
    _draw_rounded_rect(cr, m, m, w - 2 * m, h - 2 * m, radius_out)
    cr.fill()
    cr.set_source_rgb(0.96, 0.95, 0.93)
    _draw_rounded_rect(cr, m + bw, m + bw, w - 2 * (m + bw), h - 2 * (m + bw), radius_in)
    cr.fill()
    cr.set_source_rgb(0.45, 0.3, 0.1)
    cr.set_line_width(1.3)
    _draw_rounded_rect(cr, m, m, w - 2 * m, h - 2 * m, radius_out)
    cr.stroke()
    _draw_rounded_rect(cr, m + bw, m + bw, w - 2 * (m + bw), h - 2 * (m + bw), radius_in)
    cr.stroke()
    if miter:
        for ox, oy, ix, iy in ((m, m, m + bw, m + bw), (w - m, m, w - m - bw, m + bw), (m, h - m, m + bw, h - m - bw), (w - m, h - m, w - m - bw, h - m - bw)):
            cr.move_to(ox, oy)
            cr.line_to(ix, iy)
        cr.stroke()

def _draw_mode_sample(cr, w: float, h: float, mode: str) -> None:
    _bg(cr, w, h)
    m, bw = (10.0, 13.0)
    cr.set_source_rgb(0.76, 0.58, 0.24)
    _draw_rounded_rect(cr, m, m, w - 2 * m, h - 2 * m, 10.0)
    cr.fill()
    if mode == 'border':
        cr.set_source_rgb(0.84, 0.84, 0.84)
        _draw_rounded_rect(cr, m + bw, m + bw, w - 2 * (m + bw), h - 2 * (m + bw), 4.0)
        cr.fill()
    elif mode == 'plate':
        cr.set_source_rgb(0.86, 0.72, 0.36)
        _draw_rounded_rect(cr, m + bw, m + bw, w - 2 * (m + bw), h - 2 * (m + bw), 4.0)
        cr.fill()
    else:
        cr.set_source_rgb(0.16, 0.42, 0.62)
        _draw_rounded_rect(cr, m + bw, m + bw, w - 2 * (m + bw), h - 2 * (m + bw), 4.0)
        cr.fill()
    cr.set_source_rgb(0.35, 0.24, 0.08)
    cr.set_line_width(1.2)
    _draw_rounded_rect(cr, m, m, w - 2 * m, h - 2 * m, 10.0)
    cr.stroke()
    _draw_rounded_rect(cr, m + bw, m + bw, w - 2 * (m + bw), h - 2 * (m + bw), 4.0)
    cr.stroke()

def _draw_grow_sample(cr, w: float, h: float, direction: str) -> None:
    _bg(cr, w, h)
    sx, sy, sw, sh = (24.0, 18.0, w - 48.0, h - 36.0)
    bw = 10.0
    if direction == 'out':
        bx, by, fw, fh = (sx - bw, sy - bw, sw + 2 * bw, sh + 2 * bw)
        ix, iy, iw, ih = (sx, sy, sw, sh)
    elif direction == 'in':
        bx, by, fw, fh = (sx, sy, sw, sh)
        ix, iy, iw, ih = (sx + bw, sy + bw, sw - 2 * bw, sh - 2 * bw)
    else:
        hb = bw / 2.0
        bx, by, fw, fh = (sx - hb, sy - hb, sw + bw, sh + bw)
        ix, iy, iw, ih = (sx + hb, sy + hb, sw - bw, sh - bw)
    cr.set_source_rgb(0.76, 0.58, 0.24)
    cr.rectangle(bx, by, fw, fh)
    cr.fill()
    cr.set_source_rgb(0.96, 0.95, 0.93)
    cr.rectangle(ix, iy, iw, ih)
    cr.fill()
    cr.set_source_rgb(0.15, 0.4, 0.78)
    cr.set_dash([4.0, 3.0])
    cr.set_line_width(1.5)
    cr.rectangle(sx, sy, sw, sh)
    cr.stroke()
    cr.set_dash([])

def _draw_path_sample(cr, w: float, h: float, kind: str) -> None:
    _bg(cr, w, h)
    cx, cy = (w / 2.0, h / 2.0)
    rx, ry = (w * 0.34, h * 0.3)
    pts = []
    for i in range(41):
        u = i / 40.0
        a = u * math.tau
        if kind == 'circle':
            r = min(rx, ry)
            pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
        elif kind == 'ellipse':
            pts.append((cx + math.cos(a) * rx, cy + math.sin(a) * ry * 0.72))
        elif kind == 'sine':
            pts.append((12.0 + u * (w - 24.0), cy + math.sin(u * math.tau * 1.5) * ry * 0.8))
        else:
            x = -1.0 + 2.0 * u
            pts.append((12.0 + u * (w - 24.0), cy + ry * 0.85 - (1.0 - x * x) * ry * 1.5))
    cr.set_source_rgba(0.25, 0.35, 0.55, 0.65)
    cr.set_line_width(1.3)
    cr.move_to(*pts[0])
    for px, py in pts[1:]:
        cr.line_to(px, py)
    cr.stroke()
    for idx in range(0, len(pts), 8):
        px, py = pts[idx]
        alpha = max(0.25, 1.0 - idx / float(len(pts)) * 0.7)
        cr.set_source_rgba(0.62, 0.3, 0.12, alpha)
        cr.arc(px, py, 3.6, 0, math.tau)
        cr.fill()

def _draw_light_sample(cr, w: float, h: float, beam: bool) -> None:
    _bg(cr, w, h)
    sx, sy = (22.0, 18.0)
    tx, ty = (w - 24.0, h - 18.0)
    if beam:
        cr.set_source_rgba(0.95, 0.82, 0.25, 0.28)
        cr.set_line_width(18.0)
        cr.move_to(sx, sy)
        cr.line_to(tx, ty)
        cr.stroke()
    else:
        cr.set_source_rgba(0.95, 0.82, 0.25, 0.28)
        cr.move_to(sx, sy)
        cr.line_to(tx + 8, ty - 14)
        cr.line_to(tx - 16, ty + 10)
        cr.close_path()
        cr.fill()
    cr.set_source_rgb(0.25, 0.2, 0.14)
    cr.set_line_width(1.6)
    cr.move_to(sx, sy)
    cr.line_to(tx, ty)
    cr.stroke()
    cr.set_source_rgb(0.95, 0.78, 0.12)
    cr.arc(sx, sy, 5.0, 0, math.tau)
    cr.fill()

def _draw_profile_sample(cr, w: float, h: float) -> None:
    _bg(cr, w, h)
    base_y = h - 14.0
    pts = [(14, base_y), (42, 18), (94, 18), (112, 34), (130, 18), (168, 18), (190, base_y)]
    cr.set_source_rgb(0.76, 0.58, 0.24)
    cr.move_to(*pts[0])
    for px, py in pts[1:]:
        cr.line_to(px, py)
    cr.close_path()
    cr.fill()
    cr.set_source_rgba(0.95, 0.78, 0.1, 0.55)
    for x in (42, 94, 130, 168):
        cr.rectangle(x - 3, 14, 6, base_y - 14)
        cr.fill()
    cr.set_source_rgba(0.2, 0.46, 0.66, 0.55)
    cr.rectangle(194, base_y - 14, w - 208, 14)
    cr.fill()
    cr.set_source_rgb(0.3, 0.2, 0.08)
    cr.set_line_width(1.5)
    cr.move_to(*pts[0])
    for px, py in pts[1:]:
        cr.line_to(px, py)
    cr.stroke()

def _draw_finish_sample(cr, w: float, h: float, kind: str) -> None:
    _bg(cr, w, h)
    m = 6.0
    x, y, bw, bh = (m, m, w - 2 * m, h - 2 * m)
    cr.set_source_rgb(0.76, 0.58, 0.24)
    cr.rectangle(x, y, bw, bh)
    cr.fill()
    cr.save()
    cr.rectangle(x, y, bw, bh)
    cr.clip()
    if kind == 'brushed':
        cr.set_line_width(1.0)
        for idx in range(18):
            yy = y + (idx + 0.5) * (bh / 18.0)
            cr.set_source_rgba(1.0, 0.94, 0.72, 0.42 if idx % 2 == 0 else 0.16)
            cr.move_to(x, yy)
            cr.line_to(x + bw, yy - 3.0)
            cr.stroke()
    elif kind == 'grained':
        for ix in range(12):
            for iy in range(7):
                px = x + 4 + ix * (bw - 8) / 11.0 + iy % 2 * 2.0
                py = y + 4 + iy * (bh - 8) / 6.0
                shade = 1.0 if (ix + iy * 3) % 2 == 0 else 0.25
                cr.set_source_rgba(shade, shade * 0.88, shade * 0.55, 0.45)
                cr.arc(px, py, 1.3, 0, math.tau)
                cr.fill()
    elif kind == 'feather':
        cr.set_line_width(1.2)
        for col in range(3):
            cx = x + (col + 0.5) * (bw / 3.0)
            cr.set_source_rgba(0.32, 0.18, 0.06, 0.75)
            cr.move_to(cx, y + bh - 4)
            cr.line_to(cx, y + 6)
            cr.stroke()
            for step in range(5):
                sy = y + 10 + step * ((bh - 18) / 4.0)
                cr.set_source_rgba(1.0, 0.92, 0.7, 0.55)
                cr.move_to(cx, sy)
                cr.line_to(cx - 10, sy - 5)
                cr.move_to(cx, sy)
                cr.line_to(cx + 10, sy - 5)
                cr.stroke()
    elif kind == 'fur':
        cr.set_line_width(1.1)
        for idx in range(28):
            sx = x + idx * 17 % int(max(1, bw))
            sy = y + idx * 23 % int(max(1, bh))
            cr.set_source_rgba(0.3, 0.16, 0.05, 0.55 if idx % 2 else 0.28)
            cr.move_to(sx, sy)
            cr.curve_to(sx + 5, sy + 5, sx + 9, sy + 9, sx + 14, sy + 12)
            cr.stroke()
    else:
        r = 10.0
        for row in range(6):
            for col in range(6):
                cx = x + col * (r * 1.65) + (r * 0.8 if row % 2 else 0.0)
                cy = y + row * (r * 0.85) + 4.0
                cr.set_source_rgba(0.95, 0.82, 0.45, 0.35)
                cr.arc(cx, cy, r, 0, math.pi)
                cr.fill()
                cr.set_source_rgba(0.32, 0.18, 0.06, 0.72)
                cr.set_line_width(1.1)
                cr.arc(cx, cy, r, 0, math.pi)
                cr.stroke()
    cr.restore()

def _draw_glow_sample(cr, w: float, h: float, mode: str) -> None:
    _bg(cr, w, h)
    m, bw = (12.0, 14.0)
    if mode == 'bloom':
        for pad, alpha in ((6.0, 0.14), (3.5, 0.24), (1.5, 0.36)):
            cr.set_source_rgba(1.0, 0.88, 0.42, alpha)
            _draw_rounded_rect(cr, m - pad, m - pad, w - 2 * (m - pad), h - 2 * (m - pad), 11.0 + pad)
            cr.fill()
    cr.set_source_rgb(0.74, 0.56, 0.22)
    _draw_rounded_rect(cr, m, m, w - 2 * m, h - 2 * m, 10.0)
    cr.fill()
    cr.set_source_rgb(0.96, 0.95, 0.93)
    _draw_rounded_rect(cr, m + bw, m + bw, w - 2 * (m + bw), h - 2 * (m + bw), 4.0)
    cr.fill()
    if mode == 'shimmer':
        cr.set_source_rgba(1.0, 0.86, 0.36, 0.45)
        cr.set_line_width(5.0)
        _draw_rounded_rect(cr, m + bw + 2, m + bw + 2, w - 2 * (m + bw + 2), h - 2 * (m + bw + 2), 4.0)
        cr.stroke()
    else:
        cr.set_source_rgba(1.0, 0.97, 0.82, 0.9)
        cr.set_line_width(2.4)
        cr.move_to(m + 8, m + 4)
        cr.line_to(w - m - 14, m + 4)
        cr.move_to(m + 4, m + 8)
        cr.line_to(m + 4, h - m - 14)
        cr.stroke()

def _build_surface_finish_box() -> Gtk.Box:
    row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
    for kind, key in (('brushed', 'finish_brushed'), ('grained', 'finish_grained'), ('feather', 'finish_feathered'), ('fur', 'finish_fur'), ('scales', 'finish_scales')):
        row.pack_start(_card(lambda w, cr, k=kind: _draw_finish_sample(cr, w.get_allocated_width(), w.get_allocated_height(), k), t(key), 98, 60), False, False, 0)
    return row

def _build_lighting_glow_box() -> Gtk.Box:
    row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    row.pack_start(_card(lambda w, cr: _draw_glow_sample(cr, w.get_allocated_width(), w.get_allocated_height(), 'gloss'), t('lbl_gloss') if t('lbl_gloss') != 'lbl_gloss' else 'Glanz', 124, 68), False, False, 0)
    row.pack_start(_card(lambda w, cr: _draw_glow_sample(cr, w.get_allocated_width(), w.get_allocated_height(), 'bloom'), 'Bloom / Schein', 124, 68), False, False, 0)
    row.pack_start(_card(lambda w, cr: _draw_glow_sample(cr, w.get_allocated_width(), w.get_allocated_height(), 'shimmer'), t('chk_shimmer'), 124, 68), False, False, 0)
    return row

def _build_repeat_rotation_box() -> Gtk.Box:
    outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
    row1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
    for key, schedule in _ROT_EXAMPLES:
        row1.pack_start(_card(lambda w, cr, s=schedule: _draw_leaf_fan(cr, w.get_allocated_width(), w.get_allocated_height(), s), t(key), 118, 70), False, False, 0)
    outer.pack_start(row1, False, False, 0)
    row2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
    for key, schedule in _FADE_EXAMPLES:
        row2.pack_start(_card(lambda w, cr, s=schedule: _draw_leaf_fan(cr, w.get_allocated_width(), w.get_allocated_height(), s), t(key), 118, 62), False, False, 0)
    outer.pack_start(row2, False, False, 0)
    return outer

def _build_shape_rotation_box() -> Gtk.Box:
    row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    row.pack_start(_card(lambda w, cr: _draw_leaf_fan(cr, w.get_allocated_width(), w.get_allocated_height(), [(0, 0.32), (30, 1.0)], 'center'), t('pivot_center'), 124, 74), False, False, 0)
    row.pack_start(_card(lambda w, cr: _draw_leaf_fan(cr, w.get_allocated_width(), w.get_allocated_height(), [(0, 0.32), (30, 1.0)], 'bc'), t('pivot_bc'), 124, 74), False, False, 0)
    row.pack_start(_card(lambda w, cr: _draw_leaf_fan(cr, w.get_allocated_width(), w.get_allocated_height(), [(0, 0.32), (-30, 1.0)], 'tl'), t('pivot_tl'), 124, 74), False, False, 0)
    return row

def _build_overview_box() -> Gtk.Box:
    row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
    icon = _BRAND / 'borderlay-48.png'
    if icon.is_file():
        img = Gtk.Image.new_from_file(str(icon))
        row.pack_start(img, False, False, 0)
    row.pack_start(_card(lambda w, cr: _draw_corner_sample(cr, w.get_allocated_width(), w.get_allocated_height(), 12.0, 6.0, False), t('mode_border'), 112, 62), False, False, 0)
    row.pack_start(_card(lambda w, cr: _draw_leaf_fan(cr, w.get_allocated_width(), w.get_allocated_height(), [(0, 0.3), (30, 1.0)], 'center'), t('btn_rot_simple'), 112, 62), False, False, 0)
    row.pack_start(_card(lambda w, cr: _draw_leaf_fan(cr, w.get_allocated_width(), w.get_allocated_height(), _ROT_EXAMPLES[0][1], 'center'), t('btn_rot_multi'), 112, 62), False, False, 0)
    return row

def _build_visual_for_topic(topic_key: str) -> Gtk.Widget | None:
    if topic_key == 'overview':
        return _build_overview_box()
    if topic_key == 'repeat_rotation':
        return _build_repeat_rotation_box()
    if topic_key == 'shape_rotation':
        return _build_shape_rotation_box()
    if topic_key == 'corner_radii':
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row.pack_start(_card(lambda w, cr: _draw_corner_sample(cr, w.get_allocated_width(), w.get_allocated_height(), 0.0, 0.0, True), '45° (0 / 0 px)', 132, 72), False, False, 0)
        row.pack_start(_card(lambda w, cr: _draw_corner_sample(cr, w.get_allocated_width(), w.get_allocated_height(), 16.0, 8.0, False), 'Radius > 0 px', 132, 72), False, False, 0)
        return row
    if topic_key == 'mode_border_plate':
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row.pack_start(_card(lambda w, cr: _draw_mode_sample(cr, w.get_allocated_width(), w.get_allocated_height(), 'border'), t('mode_border'), 124, 70), False, False, 0)
        row.pack_start(_card(lambda w, cr: _draw_mode_sample(cr, w.get_allocated_width(), w.get_allocated_height(), 'plate'), t('mode_plate'), 124, 70), False, False, 0)
        row.pack_start(_card(lambda w, cr: _draw_mode_sample(cr, w.get_allocated_width(), w.get_allocated_height(), 'inlay'), 'Inlay', 124, 70), False, False, 0)
        return row
    if topic_key == 'grow_direction':
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row.pack_start(_card(lambda w, cr: _draw_grow_sample(cr, w.get_allocated_width(), w.get_allocated_height(), 'out'), t('pos_out'), 124, 70), False, False, 0)
        row.pack_start(_card(lambda w, cr: _draw_grow_sample(cr, w.get_allocated_width(), w.get_allocated_height(), 'mid'), t('pos_mid'), 124, 70), False, False, 0)
        row.pack_start(_card(lambda w, cr: _draw_grow_sample(cr, w.get_allocated_width(), w.get_allocated_height(), 'in'), t('pos_in'), 124, 70), False, False, 0)
        return row
    if topic_key == 'path_toolbox':
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        for kind, lbl_key in (('circle', 'path_circle'), ('ellipse', 'path_ellipse'), ('sine', 'path_sine'), ('parabola', 'path_parabola')):
            row.pack_start(_card(lambda w, cr, k=kind: _draw_path_sample(cr, w.get_allocated_width(), w.get_allocated_height(), k), t(lbl_key), 112, 66), False, False, 0)
        return row
    if topic_key == 'light_vector':
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row.pack_start(_card(lambda w, cr: _draw_light_sample(cr, w.get_allocated_width(), w.get_allocated_height(), False), 'Cone', 136, 72), False, False, 0)
        row.pack_start(_card(lambda w, cr: _draw_light_sample(cr, w.get_allocated_width(), w.get_allocated_height(), True), 'Beam', 136, 72), False, False, 0)
        return row
    if topic_key == 'dual_profile_cut':
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row.pack_start(_card(lambda w, cr: _draw_profile_sample(cr, w.get_allocated_width(), w.get_allocated_height()), t('tab_geometry'), 280, 74), False, False, 0)
        return row
    if topic_key == 'surface_finish':
        return _build_surface_finish_box()
    if topic_key == 'lighting_glow':
        return _build_lighting_glow_box()
    return None

def populate_help_visuals(container: Gtk.Box, topic_key: str) -> None:
    for child in list(container.get_children()):
        container.remove(child)
    widget = _build_visual_for_topic(topic_key)
    if widget is None:
        container.hide()
        return
    container.pack_start(widget, False, False, 0)
    container.show_all()

def _print_rows_for_topic(topic_key: str) -> list:
    if topic_key == 'overview':
        return [[(lambda cr, w, h: _draw_corner_sample(cr, w, h, 12.0, 6.0, False), t('mode_border'), 112.0, 62.0), (lambda cr, w, h: _draw_leaf_fan(cr, w, h, [(0, 0.3), (30, 1.0)], 'center'), t('btn_rot_simple'), 112.0, 62.0), (lambda cr, w, h: _draw_leaf_fan(cr, w, h, _ROT_EXAMPLES[0][1], 'center'), t('btn_rot_multi'), 112.0, 62.0)]]
    if topic_key == 'repeat_rotation':
        return [[(lambda cr, w, h, s=sched: _draw_leaf_fan(cr, w, h, s), t(key), 112.0, 66.0) for key, sched in _ROT_EXAMPLES], [(lambda cr, w, h, s=sched: _draw_leaf_fan(cr, w, h, s), t(key), 112.0, 58.0) for key, sched in _FADE_EXAMPLES]]
    if topic_key == 'shape_rotation':
        return [[(lambda cr, w, h: _draw_leaf_fan(cr, w, h, [(0, 0.32), (30, 1.0)], 'center'), t('pivot_center'), 118.0, 68.0), (lambda cr, w, h: _draw_leaf_fan(cr, w, h, [(0, 0.32), (30, 1.0)], 'bc'), t('pivot_bc'), 118.0, 68.0), (lambda cr, w, h: _draw_leaf_fan(cr, w, h, [(0, 0.32), (-30, 1.0)], 'tl'), t('pivot_tl'), 118.0, 68.0)]]
    if topic_key == 'corner_radii':
        return [[(lambda cr, w, h: _draw_corner_sample(cr, w, h, 0.0, 0.0, True), '45° (0 / 0 px)', 128.0, 68.0), (lambda cr, w, h: _draw_corner_sample(cr, w, h, 16.0, 8.0, False), 'Radius > 0 px', 128.0, 68.0)]]
    if topic_key == 'mode_border_plate':
        return [[(lambda cr, w, h: _draw_mode_sample(cr, w, h, 'border'), t('mode_border'), 120.0, 66.0), (lambda cr, w, h: _draw_mode_sample(cr, w, h, 'plate'), t('mode_plate'), 120.0, 66.0), (lambda cr, w, h: _draw_mode_sample(cr, w, h, 'inlay'), 'Inlay', 120.0, 66.0)]]
    if topic_key == 'grow_direction':
        return [[(lambda cr, w, h: _draw_grow_sample(cr, w, h, 'out'), t('pos_out'), 120.0, 66.0), (lambda cr, w, h: _draw_grow_sample(cr, w, h, 'mid'), t('pos_mid'), 120.0, 66.0), (lambda cr, w, h: _draw_grow_sample(cr, w, h, 'in'), t('pos_in'), 120.0, 66.0)]]
    if topic_key == 'path_toolbox':
        return [[(lambda cr, w, h, k=kind: _draw_path_sample(cr, w, h, k), t(lbl_key), 108.0, 62.0) for kind, lbl_key in (('circle', 'path_circle'), ('ellipse', 'path_ellipse'), ('sine', 'path_sine'), ('parabola', 'path_parabola'))]]
    if topic_key == 'light_vector':
        return [[(lambda cr, w, h: _draw_light_sample(cr, w, h, False), 'Cone', 132.0, 68.0), (lambda cr, w, h: _draw_light_sample(cr, w, h, True), 'Beam', 132.0, 68.0)]]
    if topic_key == 'dual_profile_cut':
        return [[(_draw_profile_sample, t('tab_geometry'), 260.0, 68.0)]]
    if topic_key == 'surface_finish':
        return [[(lambda cr, w, h, k=kind: _draw_finish_sample(cr, w, h, k), t(key), 88.0, 56.0) for kind, key in (('brushed', 'finish_brushed'), ('grained', 'finish_grained'), ('feather', 'finish_feathered'), ('fur', 'finish_fur'), ('scales', 'finish_scales'))]]
    if topic_key == 'lighting_glow':
        return [[(lambda cr, w, h: _draw_glow_sample(cr, w, h, 'gloss'), t('lbl_gloss') if t('lbl_gloss') != 'lbl_gloss' else 'Glanz', 120.0, 64.0), (lambda cr, w, h: _draw_glow_sample(cr, w, h, 'bloom'), 'Bloom / Schein', 120.0, 64.0), (lambda cr, w, h: _draw_glow_sample(cr, w, h, 'shimmer'), t('chk_shimmer'), 120.0, 64.0)]]
    return []

def help_visual_height_pt(topic_key: str) -> float:
    rows = _print_rows_for_topic(topic_key)
    if not rows:
        return 0.0
    total = 4.0
    for row in rows:
        row_h = max((h for _fn, _cap, _w, h in row))
        total += row_h * 0.72 + 22.0
    return total

def draw_help_visual_print(cr, topic_key: str, x: float, y: float, max_w: float, scale: float, family: str, slant) -> None:
    rows = _print_rows_for_topic(topic_key)
    if not rows:
        return
    gap_pt = 8.0
    cur_y = float(y)
    for row in rows:
        total_w_pt = sum((w * 0.72 for _fn, _cap, w, _h in row)) + gap_pt * max(0, len(row) - 1)
        fit = min(1.0, max_w / max(1.0, scale) / max(1.0, total_w_pt))
        card_scale = 0.72 * fit * scale
        row_h_px = max((h for _fn, _cap, _w, h in row)) * card_scale
        cur_x = float(x)
        for draw_fn, caption, w_pt, h_pt in row:
            cw = w_pt * card_scale
            cr.save()
            cr.translate(cur_x, cur_y)
            cr.scale(card_scale, card_scale)
            draw_fn(cr, w_pt, h_pt)
            cr.restore()
            cr.save()
            cr.set_source_rgb(0.15, 0.15, 0.15)
            cr.select_font_face(family or 'Sans', slant, 0)
            cr.set_font_size(max(7.5, 8.5 * fit) * scale)
            short_cap = caption[:24] + ('…' if len(caption) > 24 else '')
            ext = cr.text_extents(short_cap)
            tx = cur_x + max(0.0, (cw - ext.x_advance) / 2.0)
            cr.move_to(tx, cur_y + row_h_px + 10.5 * scale)
            cr.show_text(short_cap)
            cr.restore()
            cur_x += cw + gap_pt * fit * scale
        cur_y += row_h_px + 20.0 * scale
