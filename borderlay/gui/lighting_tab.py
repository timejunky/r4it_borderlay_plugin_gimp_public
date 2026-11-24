# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gui.light_vector import LightVectorPad
from help_texts import create_help_button

class LightingAndEffectsTab(Gtk.Box):

    def __init__(self, cfg, on_change_callback=None):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=14)
        self.cfg = cfg
        self.on_change_callback = on_change_callback
        self._updating = False
        left_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        hdr_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        hdr_lbl = Gtk.Label(xalign=0)
        hdr_lbl.set_markup('<b>Grafische Lichtquelle (Quelle → Auftreffpunkt)</b>')
        hdr_box.pack_start(hdr_lbl, True, True, 0)
        hdr_box.pack_end(create_help_button('light_vector'), False, False, 0)
        left_vbox.pack_start(hdr_box, False, False, 0)
        self.light_pad = LightVectorPad(self.cfg, on_change_callback=self._on_pad_changed)
        left_vbox.pack_start(self.light_pad, False, False, 0)
        self.pack_start(left_vbox, False, False, 0)
        right_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vec_frame = Gtk.Frame(label='Lichtstärke, Einfallswinkel & Schnell-Kompass')
        vec_grid = Gtk.Grid(column_spacing=8, row_spacing=6)
        vec_grid.set_margin_top(8)
        vec_grid.set_margin_bottom(8)
        vec_grid.set_margin_start(8)
        vec_grid.set_margin_end(8)
        vec_grid.attach(Gtk.Label(label='Lichtstärke / Glanz (%):', xalign=0), 0, 0, 1, 1)
        self.glanz_adj = Gtk.Adjustment(value=float(self._get_prop('glanz', 84)), lower=0.0, upper=100.0, step_increment=2.0)
        glanz_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=self.glanz_adj)
        glanz_scale.set_digits(0)
        glanz_scale.connect('value-changed', self._on_glanz_slider_changed)
        vec_grid.attach(glanz_scale, 1, 0, 2, 1)
        vec_grid.attach(Gtk.Label(label='Lichtwinkel (°):', xalign=0), 0, 1, 1, 1)
        self.angle_adj = Gtk.Adjustment(value=float(self._get_prop('angle', 135)), lower=0.0, upper=360.0, step_increment=5.0)
        angle_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=self.angle_adj)
        angle_scale.set_digits(0)
        angle_scale.connect('value-changed', self._on_angle_slider_changed)
        vec_grid.attach(angle_scale, 1, 1, 2, 1)
        compass_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        for lbl, ang in (('↖ Oben-Links (135°)', 135), ('↑ Zenit (90°)', 90), ('↗ Oben-Rechts (45°)', 45), ('↘ Unten-Rechts (315°)', 315)):
            b = Gtk.Button(label=lbl)
            b.connect('clicked', self._on_compass_clicked, ang)
            compass_hbox.pack_start(b, True, True, 0)
        vec_grid.attach(compass_hbox, 0, 2, 3, 1)
        vec_frame.add(vec_grid)
        right_vbox.pack_start(vec_frame, False, False, 0)
        fx_frame = Gtk.Frame()
        fx_hdr = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        fx_lbl = Gtk.Label()
        fx_lbl.set_markup('<b>Lichteffekte: Hochglanz-Bloom &amp; Innen-Schimmer</b>')
        fx_hdr.pack_start(fx_lbl, False, False, 4)
        fx_hdr.pack_start(create_help_button('inner_shimmer'), False, False, 0)
        fx_frame.set_label_widget(fx_hdr)
        fx_grid = Gtk.Grid(column_spacing=8, row_spacing=8)
        fx_grid.set_margin_top(8)
        fx_grid.set_margin_bottom(8)
        fx_grid.set_margin_start(8)
        fx_grid.set_margin_end(8)
        self.lux_chk = Gtk.CheckButton(label='Luxus-Glanz (Hochglanz-Bloom & Gehrungs-Starbursts aktivieren)')
        self.lux_chk.set_active(bool(self._get_prop('luxus', True)))
        self.lux_chk.connect('toggled', lambda c: (self._set_prop('luxus', bool(c.get_active())), self._emit_change()))
        fx_grid.attach(self.lux_chk, 0, 0, 3, 1)
        self.shim_chk = Gtk.CheckButton(label='Konturgetreuen Innen-Schimmer in das Bildfeld projizieren')
        self.shim_chk.set_active(bool(self._get_prop('innen_schimmer', False)))
        self.shim_chk.connect('toggled', lambda c: (self._set_prop('innen_schimmer', bool(c.get_active())), self._emit_change()))
        fx_grid.attach(self.shim_chk, 0, 1, 3, 1)
        fx_grid.attach(Gtk.Label(label='Schimmer-Ausrichtung:', xalign=0), 0, 2, 1, 1)
        self.shim_combo = Gtk.ComboBoxText()
        self.shim_combo.append('auto', 'Automatisch (Folgt dem Lichtvektor)')
        self.shim_combo.append('oben_links', 'Oben und Links (Klassisch)')
        self.shim_combo.append('unten_rechts', 'Unten und Rechts (Gegenlicht-Reflex)')
        self.shim_combo.append('rundum', 'Rundum (Alle 4 Innenkanten)')
        cur_shim = str(self._get_prop('schimmer_seite', 'auto') or 'auto')
        if not self.shim_combo.set_active_id(cur_shim):
            self.shim_combo.set_active_id('auto')
        self.shim_combo.connect('changed', lambda cb: (self._set_prop('schimmer_seite', cb.get_active_id() or 'auto'), self._emit_change()))
        fx_grid.attach(self.shim_combo, 1, 2, 2, 1)
        fx_frame.add(fx_grid)
        right_vbox.pack_start(fx_frame, False, False, 0)
        self.pack_start(right_vbox, True, True, 0)

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

    def sync_from_config(self):
        self._updating = True
        self.glanz_adj.set_value(float(self._get_prop('glanz', 84)))
        self.angle_adj.set_value(float(self._get_prop('angle', 135)))
        self.lux_chk.set_active(bool(self._get_prop('luxus', True)))
        self.shim_chk.set_active(bool(self._get_prop('innen_schimmer', False)))
        cur_shim = str(self._get_prop('schimmer_seite', 'auto') or 'auto')
        if not self.shim_combo.set_active_id(cur_shim):
            self.shim_combo.set_active_id('auto')
        self.light_pad._sync_points_from_config()
        self.light_pad._update_info_label()
        self.light_pad.area.queue_draw()
        self._updating = False

    def apply_material_defaults_if_auto(self):
        self.light_pad.apply_material_defaults_if_auto()
        self.sync_from_config()

    def _on_pad_changed(self):
        if self._updating:
            return
        self._updating = True
        self.glanz_adj.set_value(float(self._get_prop('glanz', 84)))
        self.angle_adj.set_value(float(self._get_prop('angle', 135)))
        self._updating = False
        self._emit_change()

    def _on_glanz_slider_changed(self, scale):
        if self._updating:
            return
        self._set_prop('glanz', int(round(scale.get_value())))
        self.light_pad._sync_points_from_config()
        self.light_pad._update_info_label()
        self.light_pad.area.queue_draw()
        self._emit_change()

    def _on_angle_slider_changed(self, scale):
        if self._updating:
            return
        self._set_prop('angle', int(round(scale.get_value())) % 360)
        self.light_pad._sync_points_from_config()
        self.light_pad._update_info_label()
        self.light_pad.area.queue_draw()
        self._emit_change()

    def _on_compass_clicked(self, _btn, angle_deg):
        self.angle_adj.set_value(float(angle_deg))

    def _emit_change(self):
        if not self._updating and callable(self.on_change_callback):
            self.on_change_callback()
