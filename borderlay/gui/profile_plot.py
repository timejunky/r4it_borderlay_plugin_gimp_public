# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import math
import cairo
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk, Gtk
import config

class ProfileCrossSectionWidget(Gtk.DrawingArea):

    def __init__(self, cfg, height_px=76, forced_plate_mode=None, title_override=None, show_details=False, on_zone_clicked=None):
        super().__init__()
        self.cfg = cfg
        self.forced_plate_mode = forced_plate_mode
        self.title_override = title_override
        self.show_details = bool(show_details)
        self.on_zone_clicked = on_zone_clicked
        self.selected_zone_idx = -1
        self.hover_zone_idx = -1
        self._zone_hit_boxes = []
        self.set_size_request(240, height_px)
        self.set_hexpand(True)
        self.set_tooltip_text('Interaktiver Querschnitts-Höhenverlauf (Links = Außenkante, Rechts = Innenbereich).\nTipp: Klicken Sie auf eine Zone (Z1..Zn), um sie im Editor hervorzuheben!')
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK)
        self.connect('draw', self._on_draw)
        self.connect('button-press-event', self._on_button_press)
        self.connect('motion-notify-event', self._on_motion)
        self.connect('leave-notify-event', self._on_leave)

    def _get_prop(self, name, default):
        try:
            return self.cfg.get_property(name)
        except Exception:
            return default

    def _parse_inlay_rgb(self):
        hex_s = str(self._get_prop('inlay_hex', '#7B1FA2') or '#7B1FA2').lstrip('#')
        if len(hex_s) == 6:
            try:
                return (int(hex_s[0:2], 16), int(hex_s[2:4], 16), int(hex_s[4:6], 16))
            except ValueError:
                pass
        return (123, 31, 162)

    def _resolve_stops_for_zone_mat(self, zone_mat_key: str):
        main_mat = str(self._get_prop('material', 'gold') or 'gold')
        inlay_rgb = self._parse_inlay_rgb()
        if zone_mat_key == 'inlay' or (main_mat == 'colored_glass' and zone_mat_key in ('main', '')):
            from fx.glass_facets import GlassFacetsHelper
            stops = config.sample_grad_stops(GlassFacetsHelper.build_glass_gradmap(inlay_rgb), 7)
            return (stops[0], stops[2], stops[4], stops[6])
        if zone_mat_key == 'shadow':
            stops = config.sample_grad_stops(config.GRADMAP_METALS.get(main_mat, config.GRADMAP_METALS['gold']), 7)
            return (tuple((round(c * 0.45) for c in stops[0])), stops[0], stops[1], stops[2])
        target_mat = zone_mat_key if zone_mat_key in config.GRADMAP_METALS else main_mat
        stops = config.sample_grad_stops(config.GRADMAP_METALS.get(target_mat, config.GRADMAP_METALS['gold']), 7)
        return (stops[0], stops[2], stops[4], stops[6])

    def _on_button_press(self, _widget, event):
        if event.button == 1:
            for idx, x1, x2 in self._zone_hit_boxes:
                if x1 <= event.x <= x2:
                    self.selected_zone_idx = idx
                    self.queue_draw()
                    if callable(self.on_zone_clicked):
                        self.on_zone_clicked(idx)
                    break
        return False

    def _on_motion(self, _widget, event):
        found = -1
        for idx, x1, x2 in self._zone_hit_boxes:
            if x1 <= event.x <= x2:
                found = idx
                break
        if found != self.hover_zone_idx:
            self.hover_zone_idx = found
            self.queue_draw()
        return False

    def _on_leave(self, _widget, _event):
        if self.hover_zone_idx != -1:
            self.hover_zone_idx = -1
            self.queue_draw()
        return False

    def _paint_plot_backdrop(self, cr, width, height):
        cr.set_source_rgb(0.1, 0.11, 0.13)
        cr.rectangle(0, 0, width, height)
        cr.fill()
        cr.set_source_rgba(1.0, 1.0, 1.0, 0.06)
        cr.set_line_width(1.0)
        for guide_y in (0.28, 0.55, 0.82):
            cr.move_to(0, height * guide_y)
            cr.line_to(width, height * guide_y)
        cr.stroke()

    def _plate_draw_state(self):
        center_mode = str(self._get_prop('innen_modus', 'transparent') or 'transparent')
        plate_opacity_pct = max(0, min(100, 100 - int(self._get_prop('innen_transparenz', 100))))
        if self.forced_plate_mode is not None:
            is_plate = bool(self.forced_plate_mode)
        else:
            is_plate = center_mode in ('plate', 'inlay_well') or plate_opacity_pct > 5
        if is_plate and plate_opacity_pct <= 0:
            plate_opacity_pct = 100
        return (center_mode, is_plate, plate_opacity_pct)

    @staticmethod
    def _zone_outline(kind, cur_x, zone_w, next_x, prev_y, zone_y, base_y):
        points = [(cur_x, base_y), (cur_x, prev_y)]
        if kind == 'bevel_out':
            points.append((cur_x + zone_w * 0.25, (prev_y + zone_y) * 0.5))
            points.append((next_x, zone_y))
            end_y = zone_y
        elif kind == 'bevel_in':
            points.append((cur_x + zone_w * 0.55, (prev_y + zone_y) * 0.55))
            points.append((next_x, zone_y))
            end_y = zone_y
        elif kind == 'groove':
            points.append((cur_x + zone_w * 0.5, zone_y))
            points.append((next_x, prev_y))
            end_y = prev_y
        elif kind == 'pipe':
            for step in range(1, 9):
                blend = step / 8.0
                arc_y = prev_y - math.sin(blend * math.pi) * (prev_y - zone_y)
                points.append((cur_x + zone_w * blend, arc_y))
            end_y = prev_y
        else:
            points.append((cur_x + 1.0, zone_y))
            points.append((next_x - 1.0, zone_y))
            end_y = zone_y
        points.append((next_x, base_y))
        return (points, end_y)

    def _paint_zone_face(self, cr, idx, zone, points, cur_x, next_x, top_y, base_y, zone_w):
        shadow, mid, light, peak = self._resolve_stops_for_zone_mat(zone.get('mat', 'main'))
        col_sh = [c / 255.0 for c in shadow]
        col_md = [c / 255.0 for c in mid]
        col_lt = [c / 255.0 for c in light]
        col_pk = [c / 255.0 for c in peak]
        cr.new_sub_path()
        cr.move_to(*points[0])
        for px, py in points[1:]:
            cr.line_to(px, py)
        cr.close_path()
        grad = cairo.LinearGradient(cur_x, top_y, next_x, base_y)
        grad.add_color_stop_rgba(0.0, col_pk[0], col_pk[1], col_pk[2], 0.92)
        grad.add_color_stop_rgba(0.38, col_lt[0], col_lt[1], col_lt[2], 0.82)
        grad.add_color_stop_rgba(0.75, col_md[0], col_md[1], col_md[2], 0.7)
        grad.add_color_stop_rgba(1.0, col_sh[0], col_sh[1], col_sh[2], 0.6)
        cr.set_source(grad)
        cr.fill_preserve()
        is_hi = idx == self.selected_zone_idx or idx == self.hover_zone_idx
        if is_hi:
            cr.set_source_rgba(1.0, 0.95, 0.4, 0.22)
            cr.fill_preserve()
        cr.set_source_rgb(*((1.0, 0.92, 0.3) if is_hi else col_pk))
        cr.set_line_width(2.4 if is_hi else 1.6)
        cr.move_to(*points[1])
        for px, py in points[2:-1]:
            cr.line_to(px, py)
        cr.stroke()
        if zone_w >= 18.0:
            cr.set_source_rgba(1.0, 1.0, 1.0, 0.9 if is_hi else 0.78)
            cr.set_font_size(8.5)
            pct_val = round(float(zone['share']) * 100.0)
            label = f'Z{idx + 1} ({pct_val}%)' if self.show_details and zone_w >= 44.0 else f'Z{idx + 1}'
            cr.move_to(cur_x + 4.0, base_y - 3.5)
            cr.show_text(label)

    def _paint_center_well(self, cr, cur_x, plate_y, plate_w, plate_h, width, pad_l, base_y, top_y, center_mode, is_plate, plate_opacity_pct):
        cell = 5.0
        cols = int(plate_w // cell) + 1
        rows = int(plate_h // cell) + 1
        cr.save()
        cr.rectangle(cur_x, plate_y, plate_w, plate_h)
        cr.clip()
        for row in range(rows):
            for col in range(cols):
                shade = 0.22 if (row + col) % 2 == 0 else 0.14
                cr.set_source_rgb(shade, shade, shade + 0.02)
                cr.rectangle(cur_x + col * cell, plate_y + row * cell, cell, cell)
                cr.fill()
        cr.restore()
        if not is_plate:
            return
        plate_mat = 'inlay' if center_mode == 'inlay_well' else 'main'
        _shadow, mid, light, peak = self._resolve_stops_for_zone_mat(plate_mat)
        alpha_mul = max(0.08, min(1.0, float(plate_opacity_pct) / 100.0))
        cr.rectangle(cur_x, plate_y, plate_w, plate_h)
        plate_grad = cairo.LinearGradient(cur_x, plate_y, width - pad_l, base_y)
        plate_grad.add_color_stop_rgba(0.0, peak[0] / 255.0, peak[1] / 255.0, peak[2] / 255.0, 0.92 * alpha_mul)
        plate_grad.add_color_stop_rgba(0.5, light[0] / 255.0, light[1] / 255.0, light[2] / 255.0, 0.82 * alpha_mul)
        plate_grad.add_color_stop_rgba(1.0, mid[0] / 255.0, mid[1] / 255.0, mid[2] / 255.0, 0.72 * alpha_mul)
        cr.set_source(plate_grad)
        cr.fill_preserve()
        cr.set_source_rgba(peak[0] / 255.0, peak[1] / 255.0, peak[2] / 255.0, max(0.35, alpha_mul))
        cr.set_line_width(1.5)
        cr.stroke()

    def _paint_plot_title(self, cr, width, pad_l, pad_r, is_plate, plate_opacity_pct):
        cr.set_source_rgba(0.9, 0.92, 0.95, 0.88)
        cr.select_font_face('Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(9.5)
        header_txt = self.title_override if self.title_override else f'Querschnitt: PLATTE / INLAY (Deckkraft {plate_opacity_pct}%)' if is_plate else 'Querschnitt: RAHMEN (Freies Bildfeld)'
        cr.move_to(pad_l, 12.0)
        cr.show_text(header_txt)
        cr.select_font_face('Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(8.5)
        right_txt = f'Platte ({plate_opacity_pct}%)' if is_plate else 'Bildfeld (0%)'
        cr.move_to(width - pad_r + 4, 12.0)
        cr.show_text(right_txt)

    def _on_draw(self, _widget, cr):
        alloc = self.get_allocation()
        w = float(max(120, alloc.width))
        h = float(max(62, alloc.height))
        self._zone_hit_boxes = []
        self._paint_plot_backdrop(cr, w, h)
        preset = str(self._get_prop('profil_preset', 'stamped_plate') or 'stamped_plate')
        custom_dsl = str(self._get_prop('custom_zones', '') or '')
        zones = config.parse_profile_zones(preset, custom_dsl, normalize_shares=True)
        p_hoehe = max(0.1, float(self._get_prop('profil_hoehe', 90)) / 100.0)
        p_tiefe = max(0.1, float(self._get_prop('profil_tiefe', 92)) / 100.0)
        fasen_w_pct = max(5.0, min(100.0, float(self._get_prop('fasenbreite', 34))))
        center_mode, is_plate, plate_opacity_pct = self._plate_draw_state()
        pad_l = 12.0
        pad_r = 76.0
        top_y = 18.0
        base_y = h - 10.0
        usable_w = max(40.0, w - pad_l - pad_r)
        usable_h = max(20.0, base_y - top_y)

        def z_to_y(z_pct):
            zn = max(0.0, min(100.0, float(z_pct))) / 100.0
            scaled = 0.5 + (zn - 0.5) * (p_hoehe if zn >= 0.5 else p_tiefe)
            scaled = max(0.05, min(1.0, scaled))
            return base_y - scaled * usable_h
        cur_x = pad_l
        prev_y = base_y
        seam_x_positions = []
        for idx, z in enumerate(zones):
            zw = max(4.0, float(z['share']) * usable_w)
            next_x = cur_x + zw
            self._zone_hit_boxes.append((idx, cur_x, next_x))
            zy = z_to_y(z['z'])
            z_pts, prev_y = self._zone_outline(z['kind'], cur_x, zw, next_x, prev_y, zy, base_y)
            self._paint_zone_face(cr, idx, z, z_pts, cur_x, next_x, top_y, base_y, zw)
            if idx < len(zones) - 1:
                seam_x_positions.append((next_x, min(zw, usable_w * 0.12)))
            cur_x = next_x
        blend_factor = fasen_w_pct / 100.0 * 0.45
        for sx, max_w in seam_x_positions:
            bw = max(1.5, max_w * blend_factor)
            cr.set_source_rgba(1.0, 0.92, 0.55, 0.18)
            cr.rectangle(sx - bw, top_y + 4, bw * 2.0, usable_h - 4)
            cr.fill()
        plate_y = z_to_y(48.0)
        plate_w = max(10.0, w - pad_l - cur_x)
        plate_h = max(6.0, base_y - plate_y)
        self._paint_center_well(cr, cur_x, plate_y, plate_w, plate_h, w, pad_l, base_y, top_y, center_mode, is_plate, plate_opacity_pct)
        self._paint_plot_title(cr, w, pad_l, pad_r, is_plate, plate_opacity_pct)
        return False
