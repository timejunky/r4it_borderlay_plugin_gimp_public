# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import math
import cairo
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gdk, GdkPixbuf, Gtk
import config
from help_texts import create_help_button

class VisualProfileSelector(Gtk.Box):
    ICON_W = 76
    ICON_H = 24

    def __init__(self, cfg, include_custom=False, on_change_callback=None):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.cfg = cfg
        self.include_custom = bool(include_custom)
        self.on_change_callback = on_change_callback
        self._updating = False
        self.store = Gtk.ListStore(str, GdkPixbuf.Pixbuf, str)
        self._populate_store()
        self.combo = Gtk.ComboBox.new_with_model(self.store)
        self.combo.set_id_column(0)
        pix_renderer = Gtk.CellRendererPixbuf()
        pix_renderer.set_padding(4, 2)
        self.combo.pack_start(pix_renderer, False)
        self.combo.add_attribute(pix_renderer, 'pixbuf', 1)
        txt_renderer = Gtk.CellRendererText()
        txt_renderer.set_padding(4, 2)
        self.combo.pack_start(txt_renderer, True)
        self.combo.add_attribute(txt_renderer, 'text', 2)
        cur_p = str(self._get_prop('profil_preset', 'stamped_plate') or 'stamped_plate')
        if not self.combo.set_active_id(cur_p):
            self.combo.set_active_id('stamped_plate')
        self.combo.connect('changed', self._on_combo_changed)
        self.pack_start(self.combo, True, True, 0)
        self.pack_end(create_help_button('dual_profile_cut'), False, False, 0)

    def _get_prop(self, name, default):
        try:
            return self.cfg.get_property(name)
        except Exception:
            return default

    def _set_prop(self, name, val):
        try:
            self.cfg.set_property(name, val)
        except Exception:
            pass

    def _resolve_material_stops(self):
        mat = str(self._get_prop('material', 'gold') or 'gold')
        if mat == 'colored_glass':
            hex_s = str(self._get_prop('inlay_hex', '#7B1FA2') or '#7B1FA2').lstrip('#')
            if len(hex_s) == 6:
                try:
                    rgb = (int(hex_s[0:2], 16), int(hex_s[2:4], 16), int(hex_s[4:6], 16))
                    from fx.glass_facets import GlassFacetsHelper
                    stops = config.sample_grad_stops(GlassFacetsHelper.build_glass_gradmap(rgb), 7)
                    return (stops[0], stops[2], stops[4], stops[6])
                except Exception:
                    pass
        stops = config.sample_grad_stops(config.GRADMAP_METALS.get(mat, config.GRADMAP_METALS['gold']), 7)
        return (stops[0], stops[2], stops[4], stops[6])

    def _render_preset_icon(self, preset_key: str) -> GdkPixbuf.Pixbuf:
        w, h = (self.ICON_W, self.ICON_H)
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        cr = cairo.Context(surface)
        cr.set_source_rgb(0.11, 0.12, 0.14)
        cr.rectangle(0, 0, w, h)
        cr.fill()
        custom_dsl = str(self._get_prop('custom_zones', '') or '')
        zones = config.parse_profile_zones(preset_key, custom_dsl if preset_key == 'custom' else '', normalize_shares=True)
        pad_x = 3.0
        top_y = 3.0
        base_y = float(h - 3)
        usable_w = float(w - 2 * pad_x)
        usable_h = base_y - top_y

        def z_to_y(z_pct):
            zn = max(0.05, min(1.0, float(z_pct) / 100.0))
            return base_y - zn * usable_h
        pts = [(pad_x, base_y)]
        cur_x = pad_x
        prev_y = base_y
        for z in zones:
            zw = max(2.0, float(z['share']) * usable_w)
            next_x = cur_x + zw
            kind = z['kind']
            zy = z_to_y(z['z'])
            if kind == 'bevel_out':
                pts.append((cur_x + zw * 0.25, (prev_y + zy) * 0.5))
                pts.append((next_x, zy))
                prev_y = zy
            elif kind == 'bevel_in':
                pts.append((cur_x + zw * 0.55, (prev_y + zy) * 0.55))
                pts.append((next_x, zy))
                prev_y = zy
            elif kind == 'groove':
                pts.append((cur_x + zw * 0.5, zy))
                pts.append((next_x, prev_y))
            elif kind == 'pipe':
                for s in range(1, 7):
                    t = s / 6.0
                    arc_y = prev_y - math.sin(t * math.pi) * (prev_y - zy)
                    pts.append((cur_x + zw * t, arc_y))
            else:
                pts.append((cur_x + 0.8, zy))
                pts.append((next_x - 0.8, zy))
                prev_y = zy
            cur_x = next_x
        pts.append((cur_x, base_y))
        c_sh, c_md, c_lt, c_pk = self._resolve_material_stops()
        cr.new_sub_path()
        cr.move_to(*pts[0])
        for px, py in pts[1:]:
            cr.line_to(px, py)
        cr.close_path()
        grad = cairo.LinearGradient(0, top_y, 0, base_y)
        grad.add_color_stop_rgb(0.0, c_pk[0] / 255.0, c_pk[1] / 255.0, c_pk[2] / 255.0)
        grad.add_color_stop_rgb(0.5, c_lt[0] / 255.0, c_lt[1] / 255.0, c_lt[2] / 255.0)
        grad.add_color_stop_rgb(1.0, c_md[0] / 255.0, c_md[1] / 255.0, c_md[2] / 255.0)
        cr.set_source(grad)
        cr.fill_preserve()
        cr.set_source_rgb(c_pk[0] / 255.0, c_pk[1] / 255.0, c_pk[2] / 255.0)
        cr.set_line_width(1.2)
        cr.stroke()
        return Gdk.pixbuf_get_from_surface(surface, 0, 0, w, h)

    def _populate_store(self):
        self.store.clear()
        from license_product import active_limits, preset_allowed
        limits = active_limits()
        for p_key, p_lbl in config.PROFILE_LABELS.items():
            if p_key == 'custom' and (not self.include_custom):
                continue
            if limits is not None and (not preset_allowed(p_key, limits)):
                continue
            short_lbl = p_lbl.split('(')[0].strip() if not self.include_custom else p_lbl
            pix = self._render_preset_icon(p_key)
            self.store.append([p_key, pix, short_lbl])

    def refresh_icons(self):
        self._updating = True
        cur_p = str(self._get_prop('profil_preset', 'stamped_plate') or 'stamped_plate')
        self._populate_store()
        if not self.combo.set_active_id(cur_p):
            self.combo.set_active_id('stamped_plate')
        self._updating = False

    def set_active_preset_quietly(self, preset_key: str):
        self._updating = True
        if not self.combo.set_active_id(preset_key):
            self.combo.set_active_id('stamped_plate')
        self._updating = False

    def _on_combo_changed(self, combo):
        if self._updating:
            return
        p_key = combo.get_active_id()
        if not p_key:
            return
        self._updating = True
        self._set_prop('profil_preset', p_key)
        if p_key in config.BUILTIN_PATTERNS:
            self._set_prop('custom_zones', config.BUILTIN_PATTERNS[p_key])
        if p_key == 'logo_classic':
            self._set_prop('eckenradius_aussen', 0)
            self._set_prop('eckenradius_innen', 0)
        elif p_key == 'atelier_look':
            self._set_prop('eckenradius_aussen', 84)
            self._set_prop('eckenradius_innen', 0)
        elif p_key != 'custom':
            if int(self._get_prop('eckenradius_aussen', 84)) == 0:
                self._set_prop('eckenradius_aussen', 84)
                self._set_prop('eckenradius_innen', 38)
        self._updating = False
        if callable(self.on_change_callback):
            self.on_change_callback()
