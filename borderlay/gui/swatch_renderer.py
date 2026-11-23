# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import math
from pathlib import Path
import cairo
import gi
gi.require_version('Gdk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gdk
import config

class SwatchThumbnailRenderer:
    THUMB_SIZE = 60
    SWATCH_ASSETS_DIR = Path(__file__).resolve().parents[1] / 'assets' / 'swatches'

    @staticmethod
    def parse_glass_hex(hex_str: str) -> tuple:
        s = (hex_str or '').strip().lstrip('#')
        if len(s) == 6:
            try:
                return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))
            except ValueError:
                pass
        return (123, 31, 162)

    @classmethod
    def _try_load_baked_png_surface(cls, mat_key: str, is_rounded: bool, is_plate: bool, glass_hex: str, profile_mode: str):
        if mat_key == 'colored_glass' and glass_hex.upper() != '#7B1FA2':
            return None
        if profile_mode == 'pipe' or is_plate:
            return None
        mode_tag = 'round' if is_rounded else 'sharp'
        png_path = cls.SWATCH_ASSETS_DIR / f'{mat_key}_{mode_tag}.png'
        if not png_path.is_file():
            return None
        try:
            return cairo.ImageSurface.create_from_png(str(png_path))
        except Exception:
            return None

    @staticmethod
    def _build_dynamic_stops(stops_norm: list, profile_mode: str):
        s0, s1, s2, s3, s4, s5, s6 = stops_norm
        if profile_mode == 'simple':
            return ((0.0, s2), (0.18, s6), (0.48, s4), (0.78, s2), (1.0, s0))
        if profile_mode == 'pipe':
            return ((0.0, s1), (0.15, s0), (0.32, s4), (0.5, s6), (0.68, s4), (0.85, s0), (1.0, s1))
        return ((0.0, s3), (0.18, s5), (0.23, s0), (0.3, s6), (0.52, s4), (0.68, s2), (0.75, s0), (0.82, s5), (1.0, s1))

    @staticmethod
    def _rounded_top_left_path(cr, x, y, sz, r):
        eff_r = max(0.0, min(float(r), float(sz - x - 1), float(sz - y - 1)))
        if eff_r <= 0.5:
            cr.rectangle(x, y, sz - x, sz - y)
            return
        cr.new_sub_path()
        cr.arc(x + eff_r, y + eff_r, eff_r, math.pi, 1.5 * math.pi)
        cr.line_to(sz, y)
        cr.line_to(sz, sz)
        cr.line_to(x, sz)
        cr.close_path()

    @classmethod
    def _draw_characteristic_material_texture(cls, cr, mat_key: str, sz: int, ox: float, oy: float, thick: float):
        from gui.swatch_textures import SwatchTextureArtist
        SwatchTextureArtist.draw_characteristic_texture(cr, mat_key, sz, ox, oy, thick)

    @classmethod
    def _draw_rounded_corner_zones(cls, cr, mat_key, sz, ox, oy, thick, stops_norm, is_plate, profile_mode):
        s0, s1, s2, s3, s4, s5, s6 = stops_norm
        r_outer = 22.0
        ix, iy = (ox + thick, oy + thick)
        r_inner = max(5.0, r_outer - thick * 0.44)
        if profile_mode == 'simple':
            zone_layers = ((0.0, (s3, s5, s1)), (0.2, (s6, s4, s2)), (0.84, (s4, s2, s0)))
        elif profile_mode == 'pipe':
            zone_layers = ((0.0, (s2, s1, s0)), (0.16, (s5, s6, s3)), (0.84, (s2, s1, s0)))
        else:
            zone_layers = ((0.0, (s3, s5, s1)), (0.2, (s0, s0, s0)), (0.27, (s6, s4, s2)), (0.7, (s0, s0, s0)), (0.77, (s5, s3, s1)))
        for idx, (t_pos, (col_tl, col_mid, col_br)) in enumerate(zone_layers):
            zx = ox + thick * t_pos
            zy = oy + thick * t_pos
            zr = r_outer * (1.0 - t_pos) + r_inner * t_pos
            cr.save()
            cls._rounded_top_left_path(cr, zx, zy, sz, zr)
            cr.clip()
            pat = cairo.LinearGradient(zx, zy, sz, sz)
            pat.add_color_stop_rgb(0.0, *col_tl)
            pat.add_color_stop_rgb(0.42, *col_mid)
            pat.add_color_stop_rgb(1.0, *col_br)
            cr.set_source(pat)
            cr.rectangle(zx, zy, sz - zx, sz - zy)
            cr.fill()
            if idx == (1 if profile_mode in ('simple', 'pipe') else 2):
                rad_lobe = cairo.RadialGradient(zx + 8, zy + 8, 2.0, zx + 12, zy + 12, 34.0)
                rad_lobe.add_color_stop_rgba(0.0, s6[0], s6[1], s6[2], 0.68)
                rad_lobe.add_color_stop_rgba(1.0, s4[0], s4[1], s4[2], 0.0)
                cr.set_source(rad_lobe)
                cr.rectangle(zx, zy, sz - zx, sz - zy)
                cr.fill()
            cr.restore()
        cr.save()
        cls._rounded_top_left_path(cr, ox, oy, sz, r_outer)
        cr.clip()
        cls._draw_characteristic_material_texture(cr, mat_key, sz, ox, oy, thick)
        cr.restore()
        cr.save()
        cls._rounded_top_left_path(cr, ix, iy, sz, r_inner)
        cr.clip()
        if is_plate:
            pat_plate = cairo.LinearGradient(ox, oy, sz, sz)
            pat_plate.add_color_stop_rgb(0.0, *s5)
            pat_plate.add_color_stop_rgb(0.48, *s3)
            pat_plate.add_color_stop_rgb(1.0, *s1)
            cr.set_source(pat_plate)
            cr.rectangle(ix, iy, sz - ix, sz - iy)
            cr.fill()
            cls._rounded_top_left_path(cr, ix, iy, sz, r_inner)
            cr.set_source_rgba(s0[0], s0[1], s0[2], 0.65)
            cr.set_line_width(2.2)
            cr.stroke()
        else:
            cr.set_source_rgb(0.11, 0.12, 0.14)
            cr.rectangle(ix, iy, sz - ix, sz - iy)
            cr.fill()
        cr.restore()

    @classmethod
    def _draw_sharp_miter_zones(cls, cr, mat_key, sz, ox, oy, thick, stops_norm, is_plate, profile_mode):
        s0, s1, _s2, s3, _s4, s5, _s6 = stops_norm
        ix, iy = (ox + thick, oy + thick)
        if is_plate:
            cr.save()
            cr.rectangle(ix, iy, sz - ix, sz - iy)
            cr.clip()
            pat_plate = cairo.LinearGradient(ox, oy, sz, sz)
            pat_plate.add_color_stop_rgb(0.0, *s5)
            pat_plate.add_color_stop_rgb(0.48, *s3)
            pat_plate.add_color_stop_rgb(1.0, *s1)
            cr.set_source(pat_plate)
            cr.rectangle(ix, iy, sz - ix, sz - iy)
            cr.fill()
            cr.set_source_rgba(s0[0], s0[1], s0[2], 0.65)
            cr.set_line_width(2.0)
            cr.move_to(ix, sz)
            cr.line_to(ix, iy)
            cr.line_to(sz, iy)
            cr.stroke()
            cr.restore()
        cr.save()
        cr.move_to(ox, oy)
        cr.line_to(sz, oy)
        cr.line_to(sz, iy)
        cr.line_to(ix, iy)
        cr.line_to(ix, sz)
        cr.line_to(ox, sz)
        cr.close_path()
        cr.clip()
        pat_top = cairo.LinearGradient(ox, oy, ox, iy)
        for pos, col in cls._build_dynamic_stops(stops_norm, profile_mode):
            pat_top.add_color_stop_rgb(pos, *col)
        cr.set_source(pat_top)
        cr.rectangle(ox, oy, sz - ox, sz - oy)
        cr.fill()
        pat_left = cairo.LinearGradient(ox, oy, ix, oy)
        for pos, col in cls._build_dynamic_stops(stops_norm, profile_mode):
            pat_left.add_color_stop_rgb(pos, *col)
        cr.set_source(pat_left)
        cr.move_to(ox, oy)
        cr.line_to(ix, iy)
        cr.line_to(ix, sz)
        cr.line_to(ox, sz)
        cr.close_path()
        cr.fill()
        cls._draw_characteristic_material_texture(cr, mat_key, sz, ox, oy, thick)
        cr.restore()

    @classmethod
    def render_pixbuf(cls, mat_key: str, is_pro: bool, pro_unlocked: bool, is_rounded: bool=True, is_plate: bool=False, glass_hex: str='#7B1FA2', profile_mode: str='grooved', tier_badge: str=''):
        sz = cls.THUMB_SIZE
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, sz, sz)
        cr = cairo.Context(surface)
        baked_surf = cls._try_load_baked_png_surface(mat_key, is_rounded, is_plate, glass_hex, profile_mode)
        if baked_surf is not None:
            cr.set_source_surface(baked_surf, 0, 0)
            cr.paint()
        else:
            cr.set_source_rgb(0.11, 0.12, 0.14)
            cr.rectangle(0, 0, sz, sz)
            cr.fill()
            if mat_key == 'colored_glass':
                from fx.glass_facets import GlassFacetsHelper
                stops = GlassFacetsHelper.build_glass_gradmap(cls.parse_glass_hex(glass_hex))
            else:
                stops = config.sample_grad_stops(config.GRADMAP_METALS.get(mat_key, config.GRADMAP_METALS['gold']), 7)
            stops_norm = [[c / 255.0 for c in st] for st in stops]
            ox, oy = (6.0, 6.0)
            thick = 32.0
            if is_rounded:
                cls._draw_rounded_corner_zones(cr, mat_key, sz, ox, oy, thick, stops_norm, is_plate, profile_mode)
            else:
                cls._draw_sharp_miter_zones(cr, mat_key, sz, ox, oy, thick, stops_norm, is_plate, profile_mode)
        if is_pro:
            if pro_unlocked:
                cr.set_source_rgba(0.18, 0.55, 0.28, 0.92)
            else:
                cr.set_source_rgba(0.85, 0.62, 0.12, 0.95)
            cr.rectangle(sz - 28, 2, 26, 13)
            cr.fill()
            cr.set_source_rgb(0.08, 0.08, 0.08)
            cr.select_font_face('Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            cr.set_font_size(8.5)
            cr.move_to(sz - 25, 11.5)
            badge = {'look': 'LOOK', 'atelier': 'ATEL'}.get(tier_badge, 'PAY')
            cr.show_text(badge)
        return Gdk.pixbuf_get_from_surface(surface, 0, 0, sz, sz)
