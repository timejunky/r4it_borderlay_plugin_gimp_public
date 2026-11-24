# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import config
from help_texts import create_help_button
CORNER_PRESETS = (('Weich (84/38)', 84, 38), ('Mittel (44/20)', 44, 20), ('Dezent (18/8)', 18, 8), ('45°-Gehrung', 0, 0))

class CornerRadiiSelector(Gtk.Box):

    def __init__(self, cfg, on_change_callback=None, show_sliders=False):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.cfg = cfg
        self.on_change_callback = on_change_callback
        self.show_sliders = bool(show_sliders)
        self._updating = False
        self._preset_buttons = {}
        self.r_out_adj = None
        self.r_in_adj = None
        preset_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        for lbl, r_out, r_in in CORNER_PRESETS:
            btn = Gtk.ToggleButton(label=lbl)
            btn.connect('toggled', self._on_preset_toggled, r_out, r_in)
            preset_hbox.pack_start(btn, True, True, 0)
            self._preset_buttons[r_out, r_in] = btn
        preset_hbox.pack_end(create_help_button('corner_radii'), False, False, 0)
        self.pack_start(preset_hbox, False, False, 0)
        if self.show_sliders:
            slider_grid = Gtk.Grid(column_spacing=8, row_spacing=6)
            slider_grid.set_margin_top(4)
            slider_grid.attach(Gtk.Label(label='Außenradius (px):', xalign=0), 0, 0, 1, 1)
            self.r_out_adj = Gtk.Adjustment(value=float(self._get_prop('eckenradius_aussen', 84)), lower=0.0, upper=300.0, step_increment=2.0)
            r_out_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=self.r_out_adj)
            r_out_scale.set_digits(0)
            r_out_scale.set_hexpand(True)
            r_out_scale.connect('value-changed', self._on_radius_slider_changed, 'eckenradius_aussen')
            slider_grid.attach(r_out_scale, 1, 0, 2, 1)
            slider_grid.attach(Gtk.Label(label='Innenradius (px):', xalign=0), 0, 1, 1, 1)
            self.r_in_adj = Gtk.Adjustment(value=float(self._get_prop('eckenradius_innen', 38)), lower=0.0, upper=300.0, step_increment=2.0)
            r_in_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=self.r_in_adj)
            r_in_scale.set_digits(0)
            r_in_scale.set_hexpand(True)
            r_in_scale.connect('value-changed', self._on_radius_slider_changed, 'eckenradius_innen')
            slider_grid.attach(r_in_scale, 1, 1, 2, 1)
            self.pack_start(slider_grid, False, False, 0)
        self.sync_from_config()
        from license_product import active_limits
        limits = active_limits()
        if limits is not None and (not limits.get('corners')):
            self.set_sensitive(False)
            self.set_tooltip_text(t('license_need_look'))

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

    def _sync_profile_with_radii(self, r_out: int, r_in: int):
        if r_out == 0 and r_in == 0:
            self._set_prop('profil_preset', 'logo_classic')
            self._set_prop('custom_zones', config.BUILTIN_PATTERNS['logo_classic'])
        elif r_out > 0 and r_in == 0:
            self._set_prop('profil_preset', 'atelier_look')
            self._set_prop('custom_zones', config.BUILTIN_PATTERNS['atelier_look'])
        else:
            cur_p = str(self._get_prop('profil_preset', 'stamped_plate') or 'stamped_plate')
            if cur_p in ('logo_classic', 'atelier_look'):
                self._set_prop('profil_preset', 'stamped_plate')
                self._set_prop('custom_zones', config.BUILTIN_PATTERNS['stamped_plate'])

    def sync_from_config(self):
        self._updating = True
        cur_out = int(self._get_prop('eckenradius_aussen', 84))
        cur_in = int(self._get_prop('eckenradius_innen', 38))
        if self.r_out_adj is not None:
            self.r_out_adj.set_value(float(cur_out))
        if self.r_in_adj is not None:
            self.r_in_adj.set_value(float(cur_in))
        for (p_out, p_in), btn in self._preset_buttons.items():
            btn.set_active(cur_out == p_out and cur_in == p_in)
        self._updating = False

    def _on_preset_toggled(self, btn, r_out: int, r_in: int):
        if self._updating or not btn.get_active():
            return
        self._updating = True
        self._set_prop('eckenradius_aussen', int(r_out))
        self._set_prop('eckenradius_innen', int(r_in))
        self._sync_profile_with_radii(int(r_out), int(r_in))
        self._updating = False
        self.sync_from_config()
        if callable(self.on_change_callback):
            self.on_change_callback()

    def _on_radius_slider_changed(self, scale, prop_name: str):
        if self._updating:
            return
        val = int(round(scale.get_value()))
        self._updating = True
        self._set_prop(prop_name, val)
        r_out = int(self._get_prop('eckenradius_aussen', 84))
        r_in = int(self._get_prop('eckenradius_innen', 38))
        self._sync_profile_with_radii(r_out, r_in)
        self._updating = False
        self.sync_from_config()
        if callable(self.on_change_callback):
            self.on_change_callback()
