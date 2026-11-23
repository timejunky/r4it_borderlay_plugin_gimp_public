# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk, Gtk
from help_texts import create_help_button
from locales.i18n import t
from shapes.common.shape_transform import ShapeTransformHelper
PIVOT_GRID_SPEC = (('tl', '↖', 'pivot_tl', 0, 0), ('tc', '↑', 'pivot_tc', 1, 0), ('tr', '↗', 'pivot_tr', 2, 0), ('ml', '←', 'pivot_ml', 0, 1), ('center', '⏺', 'pivot_center', 1, 1), ('mr', '→', 'pivot_mr', 2, 1), ('bl', '↙', 'pivot_bl', 0, 2), ('bc', '↓', 'pivot_bc', 1, 2), ('br', '↘', 'pivot_br', 2, 2))

class ShapeRotationSelector(Gtk.Box):

    def __init__(self, cfg, on_change_callback=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.cfg = cfg
        self.on_change_callback = on_change_callback
        self._updating = False
        self._pivot_buttons = {}
        self._wish_buttons = {}
        self._kind_buttons = {}
        self._fade_mode_buttons = {}
        self._kept_fade = 15
        self._kind_memory = {}
        self.pack_start(self._build_wish_and_axis(), False, False, 0)
        self.pack_start(self._build_simple_box(), False, False, 0)
        self.sync_from_config()
        from license_product import active_limits
        limits = active_limits()
        if limits is not None and (not limits.get('shape_rotation')):
            self._wish_buttons['simple'].set_sensitive(False)
            self._wish_buttons['simple'].set_tooltip_text(t('license_need_look'))
            self.simple_box.set_sensitive(False)

    def _build_wish_and_axis(self) -> Gtk.Frame:
        frame = Gtk.Frame(label=t('step_rot_wish'))
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        box.set_margin_top(8)
        box.set_margin_bottom(8)
        box.set_margin_start(10)
        box.set_margin_end(10)
        wish_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        for wish, key in (('simple', 'btn_rot_simple'),):
            button = Gtk.ToggleButton(label=t(key))
            button.connect('toggled', self._on_wish_toggled, wish)
            wish_box.pack_start(button, False, False, 0)
            self._wish_buttons[wish] = button
        box.pack_start(wish_box, False, False, 0)
        piv_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        piv_lbl = Gtk.Label(xalign=0)
        piv_lbl.set_markup(f"<b>{t('step_rot_axis')}</b>")
        piv_box.pack_start(piv_lbl, False, False, 0)
        grid = Gtk.Grid(column_spacing=4, row_spacing=4)
        cur_piv = str(self._get_prop('shape_pivot', 'center') or 'center')
        for p_key, sym, i18n_key, gx, gy in PIVOT_GRID_SPEC:
            button = Gtk.ToggleButton(label=sym)
            button.set_size_request(40, 34)
            button.set_tooltip_text(t(i18n_key))
            button.set_active(p_key == cur_piv)
            button.connect('toggled', self._on_pivot_btn_toggled, p_key)
            grid.attach(button, gx, gy, 1, 1)
            self._pivot_buttons[p_key] = button
        piv_box.pack_start(grid, False, False, 0)
        self.active_pivot_lbl = Gtk.Label(xalign=0)
        piv_box.pack_start(self.active_pivot_lbl, False, False, 0)
        box.pack_start(piv_box, False, False, 0)
        frame.add(box)
        return frame

    def _build_simple_box(self) -> Gtk.Frame:
        self.simple_box = Gtk.Frame(label=t('step_rot_detail'))
        ang_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        ang_vbox.set_margin_top(8)
        ang_vbox.set_margin_bottom(8)
        ang_vbox.set_margin_start(10)
        ang_vbox.set_margin_end(10)
        hdr = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        hdr_lbl = Gtk.Label(xalign=0)
        hdr_lbl.set_markup(f"<b>{t('lbl_shape_angle')}</b>")
        hdr.pack_start(hdr_lbl, True, True, 0)
        hdr.pack_end(create_help_button('shape_rotation'), False, False, 0)
        ang_vbox.pack_start(hdr, False, False, 0)
        self.rot_adj = Gtk.Adjustment(value=float(self._get_prop('shape_rotation', 0)), lower=-180.0, upper=180.0, step_increment=1.0, page_increment=15.0)
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.single_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=self.rot_adj)
        self.single_scale.set_digits(0)
        self.single_scale.set_hexpand(True)
        self.single_scale.connect('value-changed', self._on_single_angle_changed)
        row.pack_start(self.single_scale, True, True, 0)
        self.single_spin = Gtk.SpinButton(adjustment=self.rot_adj, climb_rate=1.0, digits=0)
        self.single_spin.set_width_chars(4)
        row.pack_start(self.single_spin, False, False, 0)
        ang_vbox.pack_start(row, False, False, 0)
        quick = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        for q_ang in (-90, -45, -15, 0, 15, 45, 90):
            label = f'+{q_ang}°' if q_ang > 0 else f'{q_ang}°'
            button = Gtk.Button(label=label)
            button.connect('clicked', lambda _b, a=q_ang: self.rot_adj.set_value(float(a)))
            quick.pack_start(button, True, True, 0)
        ang_vbox.pack_start(quick, False, False, 0)
        self.simple_box.add(ang_vbox)
        return self.simple_box

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
        try:
            self._sync_from_config()
        finally:
            self._updating = False

    def _sync_from_config(self):
        self._set_prop('rot_repeat', False)
        pivot = str(self._get_prop('shape_pivot', 'center') or 'center')
        self.rot_adj.set_value(float(int(self._get_prop('shape_rotation', 0))))
        for key, button in self._wish_buttons.items():
            button.set_active(key == 'simple')
        for key, button in self._pivot_buttons.items():
            button.set_active(key == pivot)
        self.active_pivot_lbl.set_markup('<small>' + t('pivot_' + pivot) + '</small>')
        self.simple_box.set_visible(True)

    def _emit(self) -> None:
        if callable(self.on_change_callback):
            self.on_change_callback()

    def _keep_one(self, btn, buttons) -> bool:
        if btn.get_active():
            return True
        if not any((other.get_active() for other in buttons.values())):
            self._updating = True
            btn.set_active(True)
            self._updating = False
        return False

    def _on_wish_toggled(self, btn, wish: str):
        if self._updating or not self._keep_one(btn, self._wish_buttons):
            return
        self._updating = True
        for key, other in self._wish_buttons.items():
            if key != wish and other.get_active():
                other.set_active(False)
        self._set_prop('rot_repeat', wish == 'multi')
        self._updating = False
        self.sync_from_config()
        self._emit()

    def _on_single_angle_changed(self, _widget):
        if self._updating:
            return
        self._set_prop('shape_rotation', int(round(self.rot_adj.get_value())))
        self.sync_from_config()
        self._emit()

    def _on_pivot_btn_toggled(self, btn, piv_key: str):
        if self._updating or not btn.get_active():
            return
        self._updating = True
        try:
            for key, other in self._pivot_buttons.items():
                if key != piv_key and other.get_active():
                    other.set_active(False)
            self._set_prop('shape_pivot', piv_key)
        finally:
            self._updating = False
        self.sync_from_config()
        self._emit()
