# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import config
from gui.profile_plot import ProfileCrossSectionWidget
from gui.profile_selector import VisualProfileSelector
from locales.i18n import t

class SimpleProfileAndFinishHelper:

    def __init__(self, cfg, on_change_callback=None):
        self.cfg = cfg
        self.on_change_callback = on_change_callback
        self._updating = False
        self.ensure_3d_relief_defaults()
        self.visual_selector = VisualProfileSelector(self.cfg, include_custom=False, on_change_callback=self._on_visual_selector_changed)
        self.prof_combo = self.visual_selector.combo
        self.profile_plot = ProfileCrossSectionWidget(self.cfg, height_px=72)
        self.gran_adj = None
        self.nap_adj = None
        self.nap_scale = None
        self.fur_density_adj = None
        self.fur_length_adj = None
        self._finish_buttons = {}
        self.gran_row = None
        self.gran_label = None
        self.nap_row = None
        self.nap_label = None
        self.density_row = None
        self.density_label = None
        self.length_row = None
        self.length_label = None

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

    def ensure_3d_relief_defaults(self):
        if int(self._get_prop('relief', 96)) < 50:
            self._set_prop('relief', 96)
        if int(self._get_prop('fasenkontrast', 84)) < 50:
            self._set_prop('fasenkontrast', 84)
        if int(self._get_prop('profil_hoehe', 90)) < 50:
            self._set_prop('profil_hoehe', 90)
        if int(self._get_prop('profil_tiefe', 92)) < 50:
            self._set_prop('profil_tiefe', 92)
        if int(self._get_prop('fasenbreite', 34)) < 10:
            self._set_prop('fasenbreite', 34)

    def _on_profile_preset_changed(self, combo):
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
        elif int(self._get_prop('eckenradius_aussen', 84)) == 0:
            self._set_prop('eckenradius_aussen', 84)
            self._set_prop('eckenradius_innen', 38)
        self._updating = False
        self._emit_change()

    def _on_visual_selector_changed(self):
        if self._updating:
            return
        self._emit_change()

    def build_profile_section_frame(self) -> Gtk.Frame:
        prof_frame = Gtk.Frame(label='2. Querschnitts-Profil (Rand-Höhenschnitt)')
        prof_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        prof_vbox.set_margin_top(5)
        prof_vbox.set_margin_bottom(5)
        prof_vbox.set_margin_start(8)
        prof_vbox.set_margin_end(8)
        prof_vbox.pack_start(self.visual_selector, False, False, 0)
        prof_vbox.pack_start(self.profile_plot, False, False, 0)
        prof_frame.add(prof_vbox)
        return prof_frame

    def build_finish_section_frame(self) -> Gtk.Frame:
        from help_texts import create_help_button
        frame = Gtk.Frame()
        hdr = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        lbl = Gtk.Label()
        lbl.set_markup(f"<b>{t('sec5_title')}</b>")
        hdr.pack_start(lbl, False, False, 4)
        hdr.pack_start(create_help_button('surface_finish'), False, False, 0)
        frame.set_label_widget(hdr)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox.set_margin_top(5)
        vbox.set_margin_bottom(5)
        vbox.set_margin_start(8)
        vbox.set_margin_end(8)
        rows = ((('finish_mirror', 'mirror'), ('finish_frosted', 'frosted'), ('finish_brushed', 'brushed'), ('finish_grained', 'grained')), (('finish_feathered', 'feather'), ('finish_fur', 'fur'), ('finish_scales', 'scales')))
        self._finish_buttons = {}
        for specs in rows:
            btn_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
            for label_key, mode_id in specs:
                button = Gtk.Button(label=t(label_key))
                button.connect('clicked', self._on_apply_finish_preset, mode_id)
                self._finish_buttons[mode_id] = button
                btn_row.pack_start(button, True, True, 0)
            vbox.pack_start(btn_row, False, False, 0)
        self.gran_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.gran_label = Gtk.Label(label=t('lbl_granularity'))
        self.gran_row.pack_start(self.gran_label, False, False, 0)
        self.gran_adj = Gtk.Adjustment(value=float(self._get_prop('brushed_granularity', 28)), lower=1.0, upper=100.0, step_increment=2.0)
        g_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=self.gran_adj)
        g_scale.set_digits(0)
        g_scale.connect('value-changed', lambda s: (self._set_prop('brushed_granularity', int(round(s.get_value()))), self._emit_change()))
        self.gran_row.pack_start(g_scale, True, True, 0)
        vbox.pack_start(self.gran_row, False, False, 0)
        self.nap_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.nap_label = Gtk.Label(label=t('lbl_nap_angle'))
        self.nap_row.pack_start(self.nap_label, False, False, 0)
        stored = int(self._get_prop('brushed_angle', -1))
        follows_light = stored < 0
        shown = stored % 360 if stored >= 0 else int(self._get_prop('angle', 135)) % 360
        self.nap_adj = Gtk.Adjustment(value=float(shown), lower=0.0, upper=359.0, step_increment=1.0)
        self.nap_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=self.nap_adj)
        self.nap_scale.set_digits(0)
        self.nap_scale.set_tooltip_text(t('tip_nap_angle'))
        self.nap_scale.set_sensitive(not follows_light)
        self.nap_scale.connect('value-changed', self._on_nap_angle_changed)
        self.nap_row.pack_start(self.nap_scale, True, True, 0)
        nap_auto = Gtk.CheckButton(label=t('lbl_nap_auto'))
        nap_auto.set_active(follows_light)
        nap_auto.connect('toggled', self._on_nap_auto_toggled)
        self.nap_row.pack_start(nap_auto, False, False, 0)
        vbox.pack_start(self.nap_row, False, False, 0)
        self.density_row, self.density_label, self.fur_density_adj = self._pack_percent_slider(vbox, 'lbl_fur_density', 'fur_density', 72)
        self.length_row, self.length_label, self.fur_length_adj = self._pack_percent_slider(vbox, 'lbl_fur_length', 'fur_length', 61)
        self._sync_finish_controls()
        frame.add(vbox)
        return frame

    def set_profile_combo_quietly(self, preset_key: str):
        self._updating = True
        self.visual_selector.set_active_preset_quietly(preset_key)
        self._updating = False
        self.refresh_profile_plot()

    def refresh_profile_plot(self):
        self.visual_selector.refresh_icons()
        if self.profile_plot is not None:
            self.profile_plot.queue_draw()

    def _emit_change(self):
        if self.profile_plot is not None:
            self.profile_plot.queue_draw()
        if not self._updating and callable(self.on_change_callback):
            self.on_change_callback()

    def _pack_percent_slider(self, vbox, label_key, prop, default):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        label = Gtk.Label(label=t(label_key))
        row.pack_start(label, False, False, 0)
        adj = Gtk.Adjustment(value=float(self._get_prop(prop, default)), lower=1.0, upper=100.0, step_increment=1.0)
        scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adj)
        scale.set_digits(0)
        scale.connect('value-changed', self._on_percent_changed, prop)
        row.pack_start(scale, True, True, 0)
        vbox.pack_start(row, False, False, 0)
        return (row, label, adj)

    def _set_row_visible(self, row, visible):
        if row is None:
            return
        row.set_no_show_all(not visible)
        row.set_visible(bool(visible))
        if visible:
            row.show_all()

    def _current_finish(self):
        organic = str(self._get_prop('surface_organic', '') or '').strip().lower()
        if organic in ('feather', 'fur', 'scales'):
            return organic
        stored = str(self._get_prop('finish_mode', '') or '').strip().lower()
        if stored in ('mirror', 'frosted', 'brushed', 'grained'):
            return stored
        if bool(self._get_prop('brushed', False)):
            return 'brushed'
        patina = int(self._get_prop('patina', 0) or 0)
        if patina >= 30:
            return 'grained'
        if patina > 0:
            return 'frosted'
        return 'mirror'

    def reload_from_config(self):
        self._updating = True
        if self.gran_adj is not None:
            self.gran_adj.set_value(float(self._get_prop('brushed_granularity', 28)))
        if self.nap_adj is not None:
            stored = int(self._get_prop('brushed_angle', -1))
            shown = stored % 360 if stored >= 0 else int(self._get_prop('angle', 135)) % 360
            self.nap_adj.set_value(float(shown))
        if self.fur_density_adj is not None:
            self.fur_density_adj.set_value(float(self._get_prop('fur_density', 72)))
        if self.fur_length_adj is not None:
            self.fur_length_adj.set_value(float(self._get_prop('fur_length', 61)))
        self._updating = False
        self._sync_finish_controls()

    def _sync_finish_controls(self):
        mode = self._current_finish()
        for mode_id, button in self._finish_buttons.items():
            style = button.get_style_context()
            if mode_id == mode:
                style.add_class('suggested-action')
            else:
                style.remove_class('suggested-action')
        self._set_row_visible(self.gran_row, mode in ('brushed', 'grained', 'feather', 'scales'))
        self._set_row_visible(self.nap_row, mode in ('brushed', 'feather', 'fur', 'scales'))
        self._set_row_visible(self.density_row, mode in ('feather', 'fur'))
        self._set_row_visible(self.length_row, mode in ('fur', 'scales'))
        size_key = {'brushed': 'lbl_size_brush', 'grained': 'lbl_size_grain', 'feather': 'lbl_size_feather', 'scales': 'lbl_size_scales'}.get(mode)
        if size_key and self.gran_label is not None:
            self.gran_label.set_text(t(size_key))
        dir_key = {'brushed': 'lbl_dir_brush', 'feather': 'lbl_dir_feather', 'fur': 'lbl_dir_fur', 'scales': 'lbl_dir_scales'}.get(mode)
        if dir_key and self.nap_label is not None:
            self.nap_label.set_text(t(dir_key))
        length_key = {'fur': 'lbl_len_fur', 'scales': 'lbl_len_scales'}.get(mode)
        if length_key and self.length_label is not None:
            self.length_label.set_text(t(length_key))
        density_key = {'feather': 'lbl_density_feather', 'fur': 'lbl_fur_density'}.get(mode)
        if density_key and self.density_label is not None:
            self.density_label.set_text(t(density_key))

    def _on_percent_changed(self, scale, prop):
        if self._updating:
            return
        self._set_prop(prop, int(round(scale.get_value())))
        self._emit_change()

    def _set_percent(self, prop, value, adj):
        self._set_prop(prop, int(value))
        if adj is None:
            return
        self._updating = True
        adj.set_value(float(value))
        self._updating = False

    def _on_nap_angle_changed(self, scale):
        if self._updating:
            return
        self._set_prop('brushed_angle', int(round(scale.get_value())) % 360)
        self._emit_change()

    def _on_nap_auto_toggled(self, button):
        if self._updating:
            return
        if button.get_active():
            self._set_prop('brushed_angle', -1)
            if self.nap_scale is not None:
                self.nap_scale.set_sensitive(False)
        else:
            angle = int(round(self.nap_adj.get_value())) % 360 if self.nap_adj else 0
            self._set_prop('brushed_angle', angle)
            if self.nap_scale is not None:
                self.nap_scale.set_sensitive(True)
        self._emit_change()

    def _set_granularity(self, value):
        self._set_prop('brushed_granularity', int(value))
        if self.gran_adj is not None:
            self.gran_adj.set_value(float(value))

    def _on_apply_finish_preset(self, _btn, mode_id):
        self.ensure_3d_relief_defaults()
        self._set_prop('finish_mode', mode_id)
        if mode_id == 'mirror':
            self._set_prop('relief', 98)
            self._set_prop('glanz', 100)
            self._set_prop('fasenkontrast', 96)
            self._set_prop('fasenbreite', 32)
            self._set_prop('brushed', False)
            self._set_prop('patina', 0)
            self._set_prop('scratches', 0)
            self._set_prop('surface_organic', '')
            self._set_prop('luxus', True)
        elif mode_id == 'frosted':
            self._set_prop('relief', 94)
            self._set_prop('glanz', 68)
            self._set_prop('fasenkontrast', 78)
            self._set_prop('fasenbreite', 42)
            self._set_prop('brushed', False)
            self._set_prop('patina', 12)
            self._set_prop('scratches', 0)
            self._set_prop('surface_organic', '')
            self._set_prop('luxus', True)
        elif mode_id == 'brushed':
            self._set_prop('relief', 96)
            self._set_prop('glanz', 90)
            self._set_prop('fasenkontrast', 86)
            self._set_prop('brushed', True)
            self._set_granularity(38)
            self._set_prop('scratches', 3)
            self._set_prop('surface_organic', '')
            self._set_prop('luxus', True)
        elif mode_id == 'grained':
            self._set_prop('relief', 96)
            self._set_prop('glanz', 84)
            self._set_prop('fasenkontrast', 86)
            self._set_prop('brushed', False)
            self._set_prop('patina', 48)
            self._set_prop('scratches', 2)
            self._set_prop('surface_organic', '')
            self._set_prop('luxus', True)
        elif mode_id == 'feather':
            self._set_prop('relief', 94)
            self._set_prop('glanz', 56)
            self._set_prop('fasenkontrast', 78)
            self._set_prop('brushed', False)
            self._set_prop('patina', 0)
            self._set_prop('scratches', 0)
            self._set_prop('surface_organic', 'feather')
            self._set_prop('luxus', False)
            self._set_granularity(46)
            self._set_percent('fur_density', 72, self.fur_density_adj)
        elif mode_id == 'fur':
            self._set_prop('relief', 92)
            self._set_prop('glanz', 40)
            self._set_prop('fasenkontrast', 72)
            self._set_prop('brushed', False)
            self._set_prop('patina', 0)
            self._set_prop('scratches', 0)
            self._set_prop('surface_organic', 'fur')
            self._set_prop('luxus', False)
            self._set_granularity(62)
            self._set_percent('fur_density', 72, self.fur_density_adj)
            self._set_percent('fur_length', 61, self.fur_length_adj)
        elif mode_id == 'scales':
            self._set_prop('relief', 96)
            self._set_prop('glanz', 74)
            self._set_prop('fasenkontrast', 86)
            self._set_prop('brushed', False)
            self._set_prop('patina', 0)
            self._set_prop('scratches', 0)
            self._set_prop('surface_organic', 'scales')
            self._set_prop('luxus', True)
            self._set_granularity(40)
            self._set_percent('fur_length', 61, self.fur_length_adj)
        self._sync_finish_controls()
        self._emit_change()

class SimpleProfileAndFinishBox(Gtk.Box):

    def __init__(self, cfg, on_change_callback=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.helper = SimpleProfileAndFinishHelper(cfg, on_change_callback)
        self.pack_start(self.helper.build_profile_section_frame(), False, False, 0)
        self.pack_start(self.helper.build_finish_section_frame(), False, False, 0)

    def ensure_3d_relief_defaults(self):
        self.helper.ensure_3d_relief_defaults()

    def set_profile_combo_quietly(self, preset_key: str):
        self.helper.set_profile_combo_quietly(preset_key)

    def refresh_profile_plot(self):
        self.helper.refresh_profile_plot()
