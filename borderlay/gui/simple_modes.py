# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gui.corner_radii import CornerRadiiSelector
from gui.simple_finish import SimpleProfileAndFinishHelper
from help_texts import create_help_button
from locales.i18n import t
from shapes import get_active_shape_mode
TAB_INDEX_ROTATION = 2
TAB_INDEX_LIGHTING = 3

class SimpleModeController(Gtk.Box):

    def __init__(self, cfg, on_change_callback=None, on_navigate_tab_callback=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.cfg = cfg
        self.on_change_callback = on_change_callback
        self.on_navigate_tab_callback = on_navigate_tab_callback
        self._updating = False
        self.corner_selector = None
        self.corner_lbl = None
        self.rot_zero_chk = None
        self.light_auto_chk = None
        self.finish_helper = SimpleProfileAndFinishHelper(self.cfg, on_change_callback=self._on_subbox_changed)
        shape_mode = get_active_shape_mode()
        badge_key = {'rectangular': 'badge_rectangular', 'circular': 'badge_circular', 'circle_1_1': 'badge_circular', 'leaf': 'badge_leaf', 'freeform': 'badge_freeform'}.get(shape_mode, 'badge_rectangular')
        shape_badge = t(badge_key)
        mode_frame = Gtk.Frame()
        mode_hdr = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        mode_lbl = Gtk.Label()
        mode_lbl.set_markup(f"<b>{t('sec1_title', badge=shape_badge)}</b>")
        mode_hdr.pack_start(mode_lbl, False, False, 4)
        mode_hdr.pack_start(create_help_button('mode_border_plate'), False, False, 0)
        mode_frame.set_label_widget(mode_hdr)
        mode_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        mode_hbox.set_margin_top(5)
        mode_hbox.set_margin_bottom(5)
        mode_hbox.set_margin_start(8)
        mode_hbox.set_margin_end(8)
        from license_product import active_limits
        self.btn_mode_border = Gtk.ToggleButton(label=t('btn_border'))
        limits = active_limits()
        is_plate = False
        self.btn_mode_border.set_active(True)
        self.btn_mode_border.connect('toggled', self._on_top_mode_toggled, 'border')
        mode_hbox.pack_start(self.btn_mode_border, True, True, 0)
        mode_frame.add(mode_hbox)
        self.pack_start(mode_frame, False, False, 0)
        self.pack_start(self.finish_helper.build_profile_section_frame(), False, False, 0)
        self.pack_start(self._build_permanent_main_settings_box(), False, False, 0)
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.stack.add_named(self._build_border_specific_box(), 'border')
        self.pack_start(self.stack, False, False, 0)
        self.pack_start(self.finish_helper.build_finish_section_frame(), False, False, 0)
        self.stack.set_visible_child_name('border')
        self._sync_corner_visibility()
        self.sync_quick_switches()

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

    def _navigate_to_tab(self, page_idx: int):
        if callable(self.on_navigate_tab_callback):
            self.on_navigate_tab_callback(page_idx)

    def _sync_corner_visibility(self):
        is_rect = get_active_shape_mode() == 'rectangular'
        if self.corner_lbl is not None:
            self.corner_lbl.set_visible(is_rect)
        if self.corner_selector is not None:
            self.corner_selector.set_visible(is_rect)

    def sync_quick_switches(self):
        self._updating = True
        cur_rot = int(self._get_prop('shape_rotation', 0))
        rep_on = bool(self._get_prop('rot_repeat', False))
        is_rot_zero = cur_rot == 0 and (not rep_on)
        if self.rot_zero_chk is not None:
            self.rot_zero_chk.set_active(is_rot_zero)
            if is_rot_zero:
                self.rot_zero_chk.set_label(t('chk_rot_zero_active'))
            elif rep_on:
                a1 = int(self._get_prop('rot_angle_start', 0))
                a2 = int(self._get_prop('rot_angle_end', 45))
                self.rot_zero_chk.set_label(f"0° ({t('lbl_active_array')}: {a1}°..{a2}°)")
            else:
                self.rot_zero_chk.set_label(f"0° ({t('lbl_active_angle')}: {cur_rot}°)")
        cur_light_src = str(self._get_prop('light_source', 'auto') or 'auto')
        is_light_auto = cur_light_src == 'auto'
        if self.light_auto_chk is not None:
            self.light_auto_chk.set_active(is_light_auto)
            self.light_auto_chk.set_label(t('chk_light_auto_active') if is_light_auto else f'Auto ({cur_light_src.upper()})')
        self._updating = False

    def refresh_profile_plot(self):
        if self.corner_selector is not None:
            self.corner_selector.sync_from_config()
        self._sync_corner_visibility()
        self.sync_quick_switches()
        self.finish_helper.refresh_profile_plot()

    def _on_subbox_changed(self):
        if self.corner_selector is not None:
            self.corner_selector.sync_from_config()
        self.sync_quick_switches()
        if not self._updating and callable(self.on_change_callback):
            self.on_change_callback()

    def _emit_change(self):
        if self.corner_selector is not None:
            self.corner_selector.sync_from_config()
        self.sync_quick_switches()
        self.finish_helper.refresh_profile_plot()
        if not self._updating and callable(self.on_change_callback):
            self.on_change_callback()

    def _on_rot_zero_toggled(self, chk):
        if self._updating:
            return
        if chk.get_active():
            self._updating = True
            self._set_prop('shape_rotation', 0)
            self._set_prop('rot_repeat', False)
            self._updating = False
            self._emit_change()
        else:
            self._navigate_to_tab(TAB_INDEX_ROTATION)

    def _on_light_auto_toggled(self, chk):
        if self._updating:
            return
        if chk.get_active():
            self._updating = True
            self._set_prop('light_source', 'auto')
            self._updating = False
            self._emit_change()
        else:
            self._navigate_to_tab(TAB_INDEX_LIGHTING)

    def _on_top_mode_toggled(self, btn, target_mode):
        if self._updating or not btn.get_active():
            return
        self._updating = True
        self.finish_helper.ensure_3d_relief_defaults()
        if target_mode == 'border':
            self._set_prop('innen_modus', 'transparent')
            self._set_prop('innen_transparenz', 100)
            self.stack.set_visible_child_name('border')
        else:
            self._set_prop('innen_modus', 'transparent')
            self.stack.set_visible_child_name('border')
        self._updating = False
        self._emit_change()

    def _on_pos_button_toggled(self, btn, pos_id):
        if self._updating or not btn.get_active():
            return
        self._updating = True
        for k, other in self._pos_buttons.items():
            if k != pos_id and other.get_active():
                other.set_active(False)
        self._set_prop('position', pos_id)
        self._updating = False
        self._emit_change()

    def _on_corner_selector_changed(self):
        self.finish_helper.ensure_3d_relief_defaults()
        cur_p = str(self._get_prop('profil_preset', 'stamped_plate') or 'stamped_plate')
        self.finish_helper.set_profile_combo_quietly(cur_p)
        self._emit_change()

    def _build_permanent_main_settings_box(self):
        frame = Gtk.Frame(label=t('sec3_title'))
        grid = Gtk.Grid(column_spacing=8, row_spacing=5)
        grid.set_margin_top(6)
        grid.set_margin_bottom(6)
        grid.set_margin_start(8)
        grid.set_margin_end(8)
        grid.attach(Gtk.Label(label=t('lbl_direction'), xalign=0), 0, 0, 1, 1)
        dir_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        self._pos_buttons = {}
        cur_pos = str(self._get_prop('position', 'aussen') or 'aussen')
        if cur_pos == 'zentriert':
            cur_pos = 'mitte'
        for pos_id, pos_lbl in (('aussen', t('dir_out')), ('innen', t('dir_in')), ('mitte', t('dir_both'))):
            b = Gtk.ToggleButton(label=pos_lbl)
            b.set_active(pos_id == cur_pos)
            b.connect('toggled', self._on_pos_button_toggled, pos_id)
            dir_box.pack_start(b, True, True, 0)
            self._pos_buttons[pos_id] = b
        dir_box.pack_end(create_help_button('grow_direction'), False, False, 0)
        grid.attach(dir_box, 1, 0, 2, 1)
        grid.attach(Gtk.Label(label=t('lbl_width'), xalign=0), 0, 1, 1, 1)
        bw_adj = Gtk.Adjustment(value=float(self._get_prop('randbreite', 96)), lower=8.0, upper=300.0, step_increment=4.0)
        bw_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=bw_adj)
        bw_scale.set_digits(0)
        bw_scale.connect('value-changed', lambda s: (self._set_prop('randbreite', int(round(s.get_value()))), self._emit_change()))
        grid.attach(bw_scale, 1, 1, 2, 1)
        self.corner_lbl = Gtk.Label(label=t('lbl_corners'), xalign=0)
        grid.attach(self.corner_lbl, 0, 2, 1, 1)
        self.corner_selector = CornerRadiiSelector(self.cfg, on_change_callback=self._on_corner_selector_changed, show_sliders=False)
        grid.attach(self.corner_selector, 1, 2, 2, 1)
        grid.attach(Gtk.Label(label=t('lbl_rotation_short'), xalign=0), 0, 3, 1, 1)
        rot_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.rot_zero_chk = Gtk.CheckButton(label=t('chk_rot_zero_active'))
        self.rot_zero_chk.set_tooltip_text(t('tip_uncheck_for_rot_tab'))
        self.rot_zero_chk.connect('toggled', self._on_rot_zero_toggled)
        rot_hbox.pack_start(self.rot_zero_chk, False, False, 0)
        btn_goto_rot = Gtk.Button(label=t('btn_goto_rotation_tab'))
        btn_goto_rot.connect('clicked', lambda _b: self._navigate_to_tab(TAB_INDEX_ROTATION))
        rot_hbox.pack_end(btn_goto_rot, False, False, 0)
        grid.attach(rot_hbox, 1, 3, 2, 1)
        grid.attach(Gtk.Label(label=t('lbl_light_short'), xalign=0), 0, 4, 1, 1)
        light_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.light_auto_chk = Gtk.CheckButton(label=t('chk_light_auto_active'))
        self.light_auto_chk.set_tooltip_text(t('tip_uncheck_for_light_tab'))
        self.light_auto_chk.connect('toggled', self._on_light_auto_toggled)
        light_hbox.pack_start(self.light_auto_chk, False, False, 0)
        btn_goto_light = Gtk.Button(label=t('btn_goto_light_tab'))
        btn_goto_light.connect('clicked', lambda _b: self._navigate_to_tab(TAB_INDEX_LIGHTING))
        light_hbox.pack_end(btn_goto_light, False, False, 0)
        grid.attach(light_hbox, 1, 4, 2, 1)
        frame.add(grid)
        return frame

    def _build_border_specific_box(self):
        frame = Gtk.Frame()
        hdr = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        lbl = Gtk.Label()
        lbl.set_markup(f"<b>{t('sec4_border_title')}</b>")
        hdr.pack_start(lbl, False, False, 4)
        hdr.pack_start(create_help_button('inner_shimmer'), False, False, 0)
        frame.set_label_widget(hdr)
        grid = Gtk.Grid(column_spacing=8, row_spacing=5)
        grid.set_margin_top(6)
        grid.set_margin_bottom(6)
        grid.set_margin_start(8)
        grid.set_margin_end(8)
        shim_chk = Gtk.CheckButton(label=t('chk_shimmer'))
        shim_chk.set_active(bool(self._get_prop('innen_schimmer', False)))
        shim_chk.connect('toggled', lambda c: (self._set_prop('innen_schimmer', bool(c.get_active())), self._emit_change()))
        grid.attach(shim_chk, 0, 0, 3, 1)
        grid.attach(Gtk.Label(label=t('lbl_shimmer_side'), xalign=0), 0, 1, 1, 1)
        shim_combo = Gtk.ComboBoxText()
        shim_combo.append('auto', t('shim_auto'))
        shim_combo.append('oben_links', t('shim_tl'))
        shim_combo.append('unten_rechts', t('shim_br'))
        shim_combo.append('rundum', t('shim_all'))
        cur_shim = str(self._get_prop('schimmer_seite', 'auto') or 'auto')
        if not shim_combo.set_active_id(cur_shim):
            shim_combo.set_active_id('auto')
        shim_combo.connect('changed', lambda cb: (self._set_prop('schimmer_seite', cb.get_active_id() or 'auto'), self._emit_change()))
        grid.attach(shim_combo, 1, 1, 2, 1)
        frame.add(grid)
        return frame
