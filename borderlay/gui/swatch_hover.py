# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import math
from pathlib import Path
import cairo
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gdk, GdkPixbuf, Gtk
import config
from gui.swatch_textures import SwatchTextureArtist

class SwatchHoverPreviewController:
    PREVIEW_PX = 200
    SHOWCASE_DIR = Path(__file__).resolve().parents[2] / 'test' / 'output' / 'material_showcase_50'
    SWATCH_DIR = Path(__file__).resolve().parents[1] / 'assets' / 'swatches'

    def __init__(self, gallery_widget):
        self.gallery_widget = gallery_widget
        self._popup_win = None
        self._img_widget = None
        self._title_lbl = None
        self._tier_lbl = None
        self._meta_lbl = None
        self._pixbuf_cache = {}

    def _ensure_popup(self):
        if self._popup_win is not None:
            return
        win = Gtk.Window(type=Gtk.WindowType.POPUP)
        win.set_decorated(False)
        win.set_resizable(False)
        win.set_accept_focus(False)
        win.set_focus_on_map(False)
        try:
            top = self.gallery_widget.get_toplevel()
            if isinstance(top, Gtk.Window):
                win.set_transient_for(top)
        except Exception:
            pass
        rim = Gdk.RGBA()
        rim.parse('#E6B34D')
        card_bg = Gdk.RGBA()
        card_bg.parse('#14110e')
        win.override_background_color(Gtk.StateFlags.NORMAL, rim)
        shell = Gtk.EventBox()
        shell.set_visible_window(True)
        shell.override_background_color(Gtk.StateFlags.NORMAL, rim)
        pad = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        pad.set_margin_top(2)
        pad.set_margin_bottom(2)
        pad.set_margin_start(2)
        pad.set_margin_end(2)
        card = Gtk.EventBox()
        card.set_visible_window(True)
        card.override_background_color(Gtk.StateFlags.NORMAL, card_bg)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        vbox.set_margin_top(8)
        vbox.set_margin_bottom(8)
        vbox.set_margin_start(10)
        vbox.set_margin_end(10)
        self._title_lbl = Gtk.Label(xalign=0)
        vbox.pack_start(self._title_lbl, False, False, 0)
        self._tier_lbl = Gtk.Label(xalign=0)
        vbox.pack_start(self._tier_lbl, False, False, 0)
        self._img_widget = Gtk.Image()
        vbox.pack_start(self._img_widget, False, False, 2)
        self._meta_lbl = Gtk.Label(xalign=0)
        self._meta_lbl.set_line_wrap(True)
        self._meta_lbl.set_max_width_chars(36)
        self._meta_lbl.set_xalign(0)
        vbox.pack_start(self._meta_lbl, False, False, 0)
        card.add(vbox)
        pad.pack_start(card, True, True, 0)
        shell.add(pad)
        win.add(shell)
        self._popup_win = win

    @classmethod
    def _find_showcase_png(cls, mat_key: str, is_rounded: bool) -> Path | None:
        mode_tag = 'round' if is_rounded else 'sharp'
        if cls.SHOWCASE_DIR.is_dir():
            for p in cls.SHOWCASE_DIR.glob(f'*_{mat_key}_{mode_tag}.png'):
                if p.is_file():
                    return p
        p_swatch = cls.SWATCH_DIR / f'{mat_key}_{mode_tag}.png'
        if p_swatch.is_file():
            return p_swatch
        return None

    @classmethod
    def _render_hover_pixbuf(cls, mat_key: str, is_rounded: bool=True) -> GdkPixbuf.Pixbuf:
        sz = cls.PREVIEW_PX
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, sz, sz)
        cr = cairo.Context(surface)
        cr.set_source_rgb(0.1, 0.11, 0.13)
        cr.rectangle(0, 0, sz, sz)
        cr.fill()
        stops = config.sample_grad_stops(config.GRADMAP_METALS.get(mat_key, config.GRADMAP_METALS['gold']), 7)
        stops_norm = [[c / 255.0 for c in st] for st in stops]
        s0, s1, s2, s3, s4, s5, s6 = stops_norm
        src_png = cls._find_showcase_png(mat_key, is_rounded)
        loaded_ok = False
        if src_png is not None:
            try:
                img_surf = cairo.ImageSurface.create_from_png(str(src_png))
                iw = float(max(1, img_surf.get_width()))
                ih = float(max(1, img_surf.get_height()))
                cr.save()
                cr.scale(sz / iw, sz / ih)
                cr.set_source_surface(img_surf, 0, 0)
                cr.paint()
                cr.restore()
                loaded_ok = True
            except Exception:
                loaded_ok = False
        if not loaded_ok:
            pat_bg = cairo.LinearGradient(12, 12, sz - 12, sz - 12)
            pat_bg.add_color_stop_rgb(0.0, *s5)
            pat_bg.add_color_stop_rgb(0.45, *s3)
            pat_bg.add_color_stop_rgb(1.0, *s1)
            cr.save()
            cr.rectangle(10, 10, sz - 20, sz - 20)
            cr.rectangle(36, 36, sz - 72, sz - 72)
            cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
            cr.clip()
            cr.set_source(pat_bg)
            cr.rectangle(10, 10, sz - 20, sz - 20)
            cr.fill()
            SwatchTextureArtist.draw_characteristic_texture(cr, mat_key, sz, 10.0, 10.0, 26.0)
            cr.restore()
            cx, cy = (128.0, 128.0)
            rx, ry = (54.0, 42.0)
            cr.save()
            cr.translate(cx, cy)
            cr.scale(rx, ry)
            cr.arc(0.0, 0.0, 1.0, 0.0, 2.0 * math.pi)
            cr.restore()
            cr.save()
            cr.clip()
            pat_el = cairo.LinearGradient(cx - rx, cy - ry, cx + rx, cy + ry)
            pat_el.add_color_stop_rgb(0.0, *s6)
            pat_el.add_color_stop_rgb(0.35, *s4)
            pat_el.add_color_stop_rgb(0.75, *s2)
            pat_el.add_color_stop_rgb(1.0, *s0)
            cr.set_source(pat_el)
            cr.rectangle(cx - rx, cy - ry, rx * 2, ry * 2)
            cr.fill()
            SwatchTextureArtist.draw_characteristic_texture(cr, mat_key, int(cx + rx), cx - rx, cy - ry, 28.0)
            for scale_r, col_r, lw in ((0.96, s0, 2.0), (0.82, s6, 1.6), (0.76, s0, 1.8)):
                cr.save()
                cr.translate(cx, cy)
                cr.scale(rx * scale_r, ry * scale_r)
                cr.arc(0.0, 0.0, 1.0, 0.0, 2.0 * math.pi)
                cr.restore()
                cr.set_source_rgba(col_r[0], col_r[1], col_r[2], 0.85)
                cr.set_line_width(lw)
                cr.stroke()
            cr.restore()
        cr.set_source_rgba(0.05, 0.06, 0.08, 0.76)
        cr.rectangle(0, sz - 18, sz, 18)
        cr.fill()
        cr.set_source_rgba(0.85, 0.88, 0.92, 0.8)
        cr.select_font_face('Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(9.0)
        cr.move_to(8, sz - 5)
        badge = 'BORDERLAY' if loaded_ok else 'BORDERLAY 72 DPI PREVIEW (RECT + ELLIPSE)'
        cr.show_text(badge)
        return Gdk.pixbuf_get_from_surface(surface, 0, 0, sz, sz)

    def _gallery_screen_rect(self):
        widget = self.gallery_widget
        alloc_w = max(1, widget.get_allocated_width())
        alloc_h = max(1, widget.get_allocated_height())
        top = widget.get_toplevel()
        top_win = top.get_window() if top is not None else None
        if top_win is not None:
            rel = widget.translate_coordinates(top, 0, 0)
            if rel is not None:
                _ok, ox, oy = top_win.get_origin()
                return (ox + rel[0], oy + rel[1], alloc_w, alloc_h, top_win)
        gdk_win = widget.get_window()
        if gdk_win is None:
            return None
        _ok, win_x, win_y = gdk_win.get_origin()
        alloc = widget.get_allocation()
        return (win_x + alloc.x, win_y + alloc.y, alloc.width, alloc.height, gdk_win)

    def _monitor_geom(self, gdk_win):
        display = gdk_win.get_display()
        monitor = display.get_monitor_at_window(gdk_win)
        if monitor is not None:
            geo = monitor.get_geometry()
            return (geo.x, geo.y, geo.width, geo.height)
        screen = gdk_win.get_screen()
        mon = screen.get_monitor_at_window(gdk_win)
        geo = screen.get_monitor_geometry(mon)
        return (geo.x, geo.y, geo.width, geo.height)

    def _move_to_fixed_central_spot(self):
        rect = self._gallery_screen_rect()
        if rect is None:
            return
        gx, gy, gw, _gh, gdk_win = rect
        _min_w, nat_w = self._popup_win.get_preferred_width()
        _min_h, nat_h = self._popup_win.get_preferred_height()
        pop_w = max(self.PREVIEW_PX + 28, nat_w)
        pop_h = max(self.PREVIEW_PX + 90, nat_h)
        fixed_x = gx + gw + 14
        fixed_y = gy + 32
        try:
            mx, my, mw, mh = self._monitor_geom(gdk_win)
        except Exception:
            mx, my, mw, mh = (0, 0, 100000, 100000)
        if fixed_x + pop_w > mx + mw - 8:
            left_x = gx - pop_w - 14
            if left_x >= mx + 8:
                fixed_x = left_x
        if fixed_y + pop_h > my + mh - 8:
            fixed_y = my + mh - pop_h - 8
        fixed_y = max(my + 8, fixed_y)
        self._popup_win.move(int(fixed_x), int(fixed_y))

    def _pass_input_through(self):
        try:
            pop_gdk = self._popup_win.get_window()
            if pop_gdk is None:
                return
            empty_reg = cairo.Region(cairo.RectangleInt(0, 0, 0, 0))
            pop_gdk.input_shape_combine_region(empty_reg, 0, 0)
        except Exception:
            pass

    def show_for_button(self, _btn: Gtk.Widget, mat_key: str, is_rounded: bool=True):
        self._ensure_popup()
        cache_key = (mat_key, bool(is_rounded))
        if cache_key not in self._pixbuf_cache:
            self._pixbuf_cache[cache_key] = self._render_hover_pixbuf(mat_key, is_rounded)
        pix = self._pixbuf_cache[cache_key]
        self._img_widget.set_from_pixbuf(pix)
        label = config.METAL_LABELS.get(mat_key, mat_key)
        tier = config.MATERIAL_TIERS.get(mat_key, 'atelier')
        tier_txt = {'free': 'Community', 'look': 'Look', 'atelier': 'Atelier'}.get(tier, tier)
        tier_col = {'free': '#58D68D', 'look': '#5DADE2', 'atelier': '#F5B041'}.get(tier, '#F5B041')
        rec = config.MATERIAL_LIGHT_DEFAULTS.get(mat_key, {})
        l_src = 'Lichtstrahl (Beam)' if rec.get('light_source') == 'beam' else 'Lichtkegel (Cone)'
        safe_label = str(label).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        self._title_lbl.set_markup(f"<span foreground='#FFF6E6'><b>{safe_label}</b></span>")
        self._tier_lbl.set_markup(f"<small><span foreground='{tier_col}'>● {tier_txt}</span></small>")
        self._meta_lbl.set_markup(f"<span foreground='#F0D7A2'><small>Standard-Licht: <span foreground='#FFFFFF'><b>{l_src}</b></span> (<span foreground='#FFFFFF'><b>{rec.get('glanz', 84)}%</b></span> Glanz)\nSchliff: <span foreground='#FFFFFF'><b>{rec.get('brushed_granularity', 0)}%</b></span> | Struktur/Patina: <span foreground='#FFFFFF'><b>{rec.get('patina', 0)}%</b></span> | Kratzer: <span foreground='#FFFFFF'><b>{rec.get('scratches', 0)}%</b></span></small></span>")
        self._move_to_fixed_central_spot()
        self._popup_win.show_all()
        self._move_to_fixed_central_spot()
        self._pass_input_through()

    def hide(self, *_args):
        if self._popup_win is not None:
            self._popup_win.hide()
