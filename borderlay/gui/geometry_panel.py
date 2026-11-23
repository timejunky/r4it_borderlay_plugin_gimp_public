# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gui.corner_radii import CornerRadiiSelector
from locales.i18n import t

class GeometryAndReliefPanel(Gtk.Box):

    def __init__(self, cfg, on_change_callback=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.cfg = cfg
        self.on_change_callback = on_change_callback
        self._updating = False
        self.rad_frame = Gtk.Frame(label=t('frame_corner_radii'))
        self.corner_selector = CornerRadiiSelector(self.cfg, on_change_callback=self.on_change_callback, show_sliders=True)
        self.corner_selector.set_margin_top(8)
        self.corner_selector.set_margin_bottom(8)
        self.corner_selector.set_margin_start(8)
        self.corner_selector.set_margin_end(8)
        self.rad_frame.add(self.corner_selector)
        self.pack_start(self.rad_frame, False, False, 0)
        rel_frame = Gtk.Frame(label=t('frame_relief_bevel'))
        rel_grid = Gtk.Grid(column_spacing=8, row_spacing=6)
        rel_grid.set_margin_top(8)
        rel_grid.set_margin_bottom(8)
        rel_grid.set_margin_start(8)
        rel_grid.set_margin_end(8)
        self._scales = {}
        sliders = (('profil_hoehe', t('lbl_profile_height'), 0.0, 100.0, 90.0), ('profil_tiefe', t('lbl_groove_depth'), 0.0, 100.0, 92.0), ('fasenbreite', t('lbl_bevel_softness'), 5.0, 100.0, 34.0), ('fasenkontrast', t('lbl_bevel_contrast'), 0.0, 100.0, 84.0), ('relief', t('lbl_total_relief'), 0.0, 100.0, 96.0))
        for row_idx, (prop_name, label_txt, lo, hi, default_val) in enumerate(sliders):
            rel_grid.attach(Gtk.Label(label=label_txt, xalign=0), 0, row_idx, 1, 1)
            adj = Gtk.Adjustment(value=float(self._get_prop(prop_name, default_val)), lower=lo, upper=hi, step_increment=2.0)
            sc = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adj)
            sc.set_digits(0)
            sc.set_hexpand(True)
            sc.connect('value-changed', self._on_generic_slider_changed, prop_name)
            rel_grid.attach(sc, 1, row_idx, 2, 1)
            self._scales[prop_name] = adj
        rel_frame.add(rel_grid)
        self.pack_start(rel_frame, False, False, 0)

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
        self.corner_selector.sync_from_config()
        for prop_name, adj in self._scales.items():
            adj.set_value(float(self._get_prop(prop_name, adj.get_value())))
        self._updating = False

    def _on_generic_slider_changed(self, scale, prop_name):
        if self._updating:
            return
        self._set_prop(prop_name, int(round(scale.get_value())))
        if callable(self.on_change_callback):
            self.on_change_callback()
