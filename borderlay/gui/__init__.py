# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gimp', '3.0')
gi.require_version('GimpUi', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, GimpUi, Gtk
from cache_guard import CacheGuard
from gui.canvas_preview import CanvasPreviewController
from gui.geometry_panel import GeometryAndReliefPanel
from gui.lighting_tab import LightingAndEffectsTab
from gui.shape_rotation import ShapeRotationSelector
from gui.simple_modes import SimpleModeController
from gui.studio_dialogs import StudioInfoDialogs, apply_window_icon
from gui.swatches import MaterialSwatchGallery
from locales.i18n import SUPPORTED_LANGUAGES, get_language, set_language, t
from shapes import get_active_shape_mode
_CONFIG_SKIP = {'procedure', 'run-mode', 'image', 'drawables', 'drawable'}

def _argument_name(pspec) -> str:
    name = getattr(pspec, 'name', None)
    if name:
        return str(name)
    try:
        return str(pspec.get_name())
    except Exception:
        return ''

def _default_argument(pspec):
    value = pspec.get_default_value()
    for method in ('get_string', 'get_boolean', 'get_int', 'get_int64', 'get_double', 'get_enum'):
        reader = getattr(value, method, None)
        if reader is None:
            continue
        try:
            return reader()
        except Exception:
            continue
    return value

def _config_names(procedure) -> list:
    names = []
    try:
        arguments = procedure.get_arguments()
    except Exception:
        return names
    for pspec in arguments:
        name = _argument_name(pspec)
        if name and name not in _CONFIG_SKIP:
            names.append(name)
    return names

def _snapshot_config(procedure, cfg) -> dict:
    values = {}
    for name in _config_names(procedure):
        try:
            values[name] = cfg.get_property(name)
        except Exception:
            continue
    return values

def _write_config(cfg, values: dict) -> None:
    for name, value in values.items():
        try:
            cfg.set_property(name, value)
        except Exception:
            continue

def _factory_values(procedure) -> dict:
    values = {}
    try:
        arguments = procedure.get_arguments()
    except Exception:
        return values
    for pspec in arguments:
        name = _argument_name(pspec)
        if not name or name in _CONFIG_SKIP:
            continue
        try:
            values[name] = _default_argument(pspec)
        except Exception:
            continue
    return values

def _button_text(widget) -> str:
    chunks = []
    for prop in ('label', 'text'):
        try:
            value = widget.get_property(prop)
        except Exception:
            value = ''
        if value:
            chunks.append(str(value))
    if not chunks:
        child_getter = getattr(widget, 'get_child', None)
        child = child_getter() if child_getter is not None else None
        if child is not None and hasattr(child, 'get_text'):
            try:
                text = child.get_text() or ''
            except Exception:
                text = ''
            if text:
                chunks.append(str(text))
    return ' '.join(chunks).replace('_', '').lower()

def _reset_kind(label: str) -> str:
    if 'factory' in label or 'werkseinstellung' in label:
        return 'factory'
    if 'initial' in label or 'anfangswert' in label:
        return 'initial'
    return ''

def _iter_widgets(widget, seen: set):
    if widget is None or id(widget) in seen:
        return
    seen.add(id(widget))
    yield widget
    popover_getter = getattr(widget, 'get_popover', None)
    if popover_getter is not None:
        try:
            yield from _iter_widgets(popover_getter(), seen)
        except Exception:
            pass
    children_getter = getattr(widget, 'get_children', None)
    if children_getter is None:
        return
    try:
        children = children_getter()
    except Exception:
        return
    for child in children or []:
        yield from _iter_widgets(child, seen)

def _cover_scroll(scroll, child) -> None:
    child.set_vexpand(False)
    child.set_valign(Gtk.Align.START)

    def _cover(_widget, _alloc):
        _minimum, natural = child.get_preferred_height()
        adj = scroll.get_vadjustment()
        if adj is not None and adj.get_upper() < float(natural):
            adj.set_upper(float(natural))
    child.connect('size-allocate', _cover)

def _wait_nonmodal(dialog) -> bool:
    loop = GLib.MainLoop()
    result = {'ok': False}
    closing = {int(Gtk.ResponseType.OK), int(Gtk.ResponseType.CANCEL), int(Gtk.ResponseType.CLOSE), int(Gtk.ResponseType.DELETE_EVENT)}

    def _on_response(_dlg, response_id):
        rid = int(response_id)
        if rid not in closing:
            return
        result['ok'] = rid == int(Gtk.ResponseType.OK)
        if loop.is_running():
            loop.quit()
    handler = dialog.connect('response', _on_response)
    try:
        dialog.present()
        loop.run()
    finally:
        dialog.disconnect(handler)
    return result['ok']

class BorderlayGUI:

    def __init__(self, procedure, image, drawables, cfg):
        from community_material_seal import apply_community_materials
        apply_community_materials()
        self.procedure = procedure
        self.image = image
        self.drawables = drawables
        self.cfg = cfg
        self.preview_ctrl = CanvasPreviewController(image, drawables, cfg)
        self.notebook = None
        self.swatch_gallery = None
        self.mode_ctrl = None
        self.geom_panel = None
        self.rot_tab = None
        self.lighting_tab = None
        self.zones_editor = None
        self._seen_light_material = ''

    def _reload_tabs(self):
        if self.swatch_gallery is not None:
            self.swatch_gallery._rebuild_swatch_grid()
            self.swatch_gallery._sync_color_selector_visibility()
            self.swatch_gallery.refresh_geometry_previews()
        if self.mode_ctrl is not None:
            self.mode_ctrl.refresh_profile_plot()
            finish = getattr(self.mode_ctrl, 'finish_helper', None)
            if finish is not None:
                finish.reload_from_config()
        if self.geom_panel is not None:
            self.geom_panel.sync_from_config()
        if self.rot_tab is not None:
            self.rot_tab.sync_from_config()
        if self.lighting_tab is not None:
            self.lighting_tab.sync_from_config()
        if self.zones_editor is not None:
            self.zones_editor.sync_from_config()
        self.preview_ctrl.schedule_update()

    def _apply_reset(self, kind: str):
        if kind == 'initial':
            _write_config(self.cfg, self._initial_values)
        else:
            _write_config(self.cfg, _factory_values(self.procedure))
        self._reload_tabs()

    def _connect_reset_buttons(self, dialog):
        for widget in _iter_widgets(dialog, set()):
            kind = _reset_kind(_button_text(widget))
            if not kind or getattr(widget, '_borderlay_reset_wired', False):
                continue
            widget._borderlay_reset_wired = True
            if hasattr(widget, 'connect'):
                widget.connect('clicked', lambda _btn, mode=kind: self._apply_reset(mode))
                try:
                    widget.connect('activate', lambda _btn, mode=kind: self._apply_reset(mode))
                except Exception:
                    pass

    def _wire_reset_buttons(self, dialog):
        self._connect_reset_buttons(dialog)
        for widget in _iter_widgets(dialog, set()):
            getter = getattr(widget, 'get_popover', None)
            if getter is None:
                continue
            try:
                popover = getter()
            except Exception:
                continue
            if popover is None or getattr(popover, '_borderlay_reset_show', False):
                continue
            popover._borderlay_reset_show = True
            popover.connect('show', lambda *_a: self._connect_reset_buttons(dialog))

    def navigate_to_tab(self, page_idx: int):
        if self.notebook is not None:
            self.notebook.set_current_page(int(page_idx))

    def _material_key(self) -> str:
        try:
            return str(self.cfg.get_property('material') or '')
        except Exception:
            return ''

    def _refresh_light_for_material(self) -> None:
        if self.lighting_tab is None:
            return
        material = self._material_key()
        if material == getattr(self, '_seen_light_material', None):
            return
        self._seen_light_material = material
        self.lighting_tab.apply_material_defaults_if_auto()

    def _on_subwidget_changed(self):
        if self.swatch_gallery is not None:
            self.swatch_gallery.refresh_geometry_previews()
            self.swatch_gallery.color_selector._sync_button_from_cfg()
        if self.mode_ctrl is not None:
            self.mode_ctrl.refresh_profile_plot()
        if self.geom_panel is not None:
            self.geom_panel.sync_from_config()
        if self.rot_tab is not None:
            self.rot_tab.sync_from_config()
        self._refresh_light_for_material()
        if self.zones_editor is not None:
            self.zones_editor.color_selector._sync_button_from_cfg()
            self.zones_editor.profile_plot.queue_draw()
        self.preview_ctrl.schedule_update()

    def _on_auto_canvas_toggled(self, chk):
        self.preview_ctrl.auto_enabled = bool(chk.get_active())
        if self.preview_ctrl.auto_enabled:
            self.preview_ctrl.render_now()

    def _on_lang_changed(self, combo):
        lang_id = combo.get_active_id() or 'de'
        set_language(lang_id)

    def show(self):
        from license_product import active_limits, clamp_procedure_config
        clamp_procedure_config(self.cfg)
        self._seen_light_material = self._material_key()
        self._initial_values = _snapshot_config(self.procedure, self.cfg)
        CacheGuard.trigger_domain('gui', reload_memory=True)
        GimpUi.init('borderlay')
        title = t('window_title')
        from shapes.toolbox.apply import selection_from_toolbox
        if selection_from_toolbox(self.image):
            title = f"{title} — {t('from_shape_toolbox')}"
        dialog = GimpUi.ProcedureDialog.new(self.procedure, self.cfg, title)
        dialog.set_default_size(980, 760)
        apply_window_icon(dialog)
        content_area = dialog.get_content_area()
        expert_props = ['brushed', 'brushed_granularity', 'brushed_angle', 'scratches', 'patina', 'surface_organic', 'fur_density', 'fur_length', 'custom_zones', 'preset_save_name']
        expert_box = None
        try:
            expert_box = dialog.fill_box('borderlay-expert-box', expert_props)
            dialog.fill(['borderlay-expert-box'])
            parent = expert_box.get_parent()
            if parent is not None:
                parent.remove(expert_box)
        except Exception:
            expert_box = None
        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        main_vbox.set_margin_top(8)
        main_vbox.set_margin_bottom(8)
        main_vbox.set_margin_start(10)
        main_vbox.set_margin_end(10)
        top_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        auto_chk = Gtk.CheckButton(label=t('live_preview_chk'))
        auto_chk.set_active(False)
        auto_chk.connect('toggled', self._on_auto_canvas_toggled)
        top_bar.pack_start(auto_chk, False, False, 0)
        apply_btn = Gtk.Button(label=t('live_preview_btn'))
        apply_btn.connect('clicked', self.preview_ctrl.render_now)
        top_bar.pack_end(apply_btn, False, False, 0)
        help_btn = Gtk.Button(label=t('help_open'))
        help_btn.connect('clicked', lambda _b: StudioInfoDialogs.show_help_dialog())
        top_bar.pack_end(help_btn, False, False, 0)
        about_btn = Gtk.Button(label='ℹ About')
        about_btn.connect('clicked', lambda _b: StudioInfoDialogs.show_about_dialog())
        top_bar.pack_end(about_btn, False, False, 0)
        lic_btn = Gtk.Button(label='🔑 License')
        lic_btn.connect('clicked', lambda _b: StudioInfoDialogs.show_license_dialog())
        top_bar.pack_end(lic_btn, False, False, 0)
        lang_combo = Gtk.ComboBoxText()
        for lang_code, lang_label in SUPPORTED_LANGUAGES:
            lang_combo.append(lang_code, lang_label)
        lang_combo.set_active_id(get_language())
        lang_combo.connect('changed', self._on_lang_changed)
        top_bar.pack_end(lang_combo, False, False, 0)
        main_vbox.pack_start(top_bar, False, False, 0)
        self.preview_ctrl.attach_dialog_widgets(dialog, apply_btn)
        self.notebook = Gtk.Notebook()
        self.notebook.set_hexpand(True)
        self.notebook.set_vexpand(True)
        simple_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        simple_hbox.set_margin_top(8)
        simple_hbox.set_margin_bottom(8)
        simple_hbox.set_margin_start(8)
        simple_hbox.set_margin_end(8)
        self.swatch_gallery = MaterialSwatchGallery(self.cfg, license_limits=active_limits(), on_change_callback=self._on_subwidget_changed)
        simple_hbox.pack_start(self.swatch_gallery, True, True, 0)
        self.mode_ctrl = SimpleModeController(self.cfg, on_change_callback=self._on_subwidget_changed, on_navigate_tab_callback=self.navigate_to_tab)
        simple_hbox.pack_start(self.mode_ctrl, True, True, 0)
        self.notebook.append_page(simple_hbox, Gtk.Label(label=t('tab_simple')))
        tab_geom_scroll = Gtk.ScrolledWindow()
        tab_geom_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.geom_panel = GeometryAndReliefPanel(self.cfg, on_change_callback=self._on_subwidget_changed)
        self.geom_panel.set_margin_top(8)
        self.geom_panel.set_margin_start(8)
        self.geom_panel.set_margin_end(8)
        tab_geom_scroll.add(self.geom_panel)
        self.notebook.append_page(tab_geom_scroll, Gtk.Label(label=t('tab_geometry')))
        tab_rot_scroll = Gtk.ScrolledWindow()
        tab_rot_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        tab_rot_scroll.set_vexpand(True)
        tab_rot_scroll.set_overlay_scrolling(False)
        self.rot_tab = ShapeRotationSelector(self.cfg, on_change_callback=self._on_subwidget_changed)
        self.rot_tab.set_margin_top(8)
        self.rot_tab.set_margin_bottom(16)
        self.rot_tab.set_margin_start(8)
        self.rot_tab.set_margin_end(8)
        tab_rot_scroll.add(self.rot_tab)
        _cover_scroll(tab_rot_scroll, self.rot_tab)
        self.notebook.append_page(tab_rot_scroll, Gtk.Label(label=t('tab_rotation')))
        tab_light_scroll = Gtk.ScrolledWindow()
        tab_light_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.lighting_tab = LightingAndEffectsTab(self.cfg, on_change_callback=self._on_subwidget_changed)
        self.lighting_tab.set_margin_top(8)
        self.lighting_tab.set_margin_start(8)
        self.lighting_tab.set_margin_end(8)
        tab_light_scroll.add(self.lighting_tab)
        self.notebook.append_page(tab_light_scroll, Gtk.Label(label=t('tab_lighting')))
        tab_exp_scroll = Gtk.ScrolledWindow()
        tab_exp_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        if expert_box is not None:
            expert_box.set_margin_top(8)
            expert_box.set_margin_bottom(8)
            expert_box.set_margin_start(8)
            expert_box.set_margin_end(8)
            tab_exp_scroll.add(expert_box)
        self.notebook.append_page(tab_exp_scroll, Gtk.Label(label=t('tab_textures')))
        main_vbox.pack_start(self.notebook, True, True, 0)
        content_area.pack_start(main_vbox, True, True, 0)
        from gui.session_report import ScopeCopyButton
        scope_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        scope_row.pack_start(ScopeCopyButton(self._session_markdown), False, False, 0)
        main_vbox.pack_end(scope_row, False, False, 0)
        dialog.show_all()
        self._wire_reset_buttons(dialog)
        self.swatch_gallery._sync_color_selector_visibility()
        if self.mode_ctrl is not None:
            self.mode_ctrl._sync_corner_visibility()
        if self.geom_panel is not None and hasattr(self.geom_panel, 'rad_frame'):
            self.geom_panel.rad_frame.set_visible(get_active_shape_mode() == 'rectangular')
        dialog.set_modal(False)
        run_ok = _wait_nonmodal(dialog)
        self.preview_ctrl.cleanup_before_close()
        dialog.destroy()
        return bool(run_ok)

    def _session_markdown(self) -> str:
        from gui.session_report import build_session_markdown
        return build_session_markdown(self.procedure, self.cfg, self.notebook, getattr(self, '_initial_values', {}), _factory_values(self.procedure))
