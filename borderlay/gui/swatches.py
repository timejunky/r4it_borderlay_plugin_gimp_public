# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import config
from license_product import edition_label
from locales.i18n import t
from gui.color_picker import ColorSwatchSelector
from gui.swatch_hover import SwatchHoverPreviewController
from gui.swatch_renderer import SwatchThumbnailRenderer
from help_texts import create_help_button
MATERIAL_DEFAULT_INLAY_HEX = {'frosted_milk_glass': '#8EC5FC', 'smoked_obsidian_glass': '#37474F', 'venetian_gold_glass': '#FF8F00', 'emerald_cut': '#2E7D32', 'ruby_star': '#C62828', 'lapis_gold_veins': '#0088FF', 'plastic_cyber_cyan': '#00BFA5'}

class MaterialSwatchGallery(Gtk.Box):

    def __init__(self, cfg, license_limits=None, on_change_callback=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.cfg = cfg
        self.license_limits = license_limits if isinstance(license_limits, dict) else None
        self.on_change_callback = on_change_callback
        self._updating = False
        self._active_category = 'all'
        self._cat_buttons = {}
        self._swatch_buttons = {}
        self._swatch_images = {}
        hdr = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        title = Gtk.Label(xalign=0)
        n_mat = len(config.MATERIAL_DISPLAY_ORDER)
        title.set_markup(f'<b>Material-Auswahl ({n_mat} Studio-Materialien)</b>')
        hdr.pack_start(title, True, True, 0)
        edition = edition_label(self.license_limits) or t('license_edition_paid')
        self.edition_lbl = Gtk.Label(label=edition)
        self.edition_lbl.set_tooltip_text(t('license_pro_toggle'))
        hdr.pack_end(self.edition_lbl, False, False, 0)
        self.pack_start(hdr, False, False, 0)
        body_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        cat_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        for cat_key, (cat_label, _) in config.MATERIAL_CATEGORY_GROUPS.items():
            b = Gtk.ToggleButton(label=cat_label)
            b.set_size_request(128, 28)
            b.set_active(cat_key == 'all')
            b.connect('toggled', self._on_category_toggled, cat_key)
            cat_vbox.pack_start(b, False, False, 0)
            self._cat_buttons[cat_key] = b
        body_hbox.pack_start(cat_vbox, False, False, 0)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_min_content_width(292)
        scroll.set_min_content_height(340)
        scroll.set_hexpand(True)
        scroll.set_vexpand(True)
        self.grid = Gtk.Grid(column_spacing=6, row_spacing=6)
        self.grid.set_margin_top(4)
        self.grid.set_margin_bottom(4)
        self.grid.set_margin_start(4)
        self.grid.set_margin_end(4)
        scroll.add(self.grid)
        body_hbox.pack_start(scroll, True, True, 0)
        self.pack_start(body_hbox, True, True, 0)
        self.color_frame = Gtk.Frame()
        color_hdr = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        color_lbl = Gtk.Label()
        color_lbl.set_markup('<b>Glas- &amp; Inlay-Farbe</b>')
        color_hdr.pack_start(color_lbl, False, False, 4)
        color_hdr.pack_start(create_help_button('inlay_color'), False, False, 0)
        self.color_frame.set_label_widget(color_hdr)
        self.color_selector = ColorSwatchSelector(self.cfg, on_change_callback=self._on_glass_color_changed, compact=False)
        self.color_selector.set_margin_top(4)
        self.color_selector.set_margin_bottom(6)
        self.color_selector.set_margin_start(6)
        self.color_selector.set_margin_end(6)
        self.color_frame.add(self.color_selector)
        self.pack_start(self.color_frame, False, False, 0)
        cur_mat = self._get_prop('material', 'gold')
        self.active_lbl = Gtk.Label(xalign=0)
        self.active_lbl.set_markup(f"<span foreground='#58D68D'>✔ <b>Aktiv: {config.METAL_LABELS.get(cur_mat, cur_mat)}</b></span>")
        self.pack_start(self.active_lbl, False, False, 0)
        self.hover_preview = SwatchHoverPreviewController(self)
        self._rebuild_swatch_grid()
        self._sync_color_selector_visibility()

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

    def _current_swatch_state(self) -> tuple:
        r_out = int(self._get_prop('eckenradius_aussen', 84))
        preset = str(self._get_prop('profil_preset', 'stamped_plate') or 'stamped_plate')
        is_rounded = preset != 'logo_classic' and r_out > 4
        c_mode = str(self._get_prop('innen_modus', 'transparent') or 'transparent')
        in_transp = int(self._get_prop('innen_transparenz', 100))
        is_plate = c_mode in ('plate', 'inlay_well') or in_transp < 95
        glass_hex = str(self._get_prop('inlay_hex', '#7B1FA2') or '#7B1FA2')
        if preset in ('simple_bevel', 'slim_bevel'):
            prof_mode = 'simple'
        elif preset in ('pipe_torus', 'triple_wave_pipes', 'heavy_vault_rim', 'wave_profile'):
            prof_mode = 'pipe'
        else:
            prof_mode = 'grooved'
        return (is_rounded, is_plate, glass_hex, prof_mode)

    def _needs_inlay_color_picker(self) -> bool:
        mat = str(self._get_prop('material', 'gold') or 'gold')
        if mat in ('colored_glass', 'frosted_milk_glass', 'smoked_obsidian_glass', 'venetian_gold_glass'):
            return True
        c_mode = str(self._get_prop('innen_modus', 'transparent') or 'transparent')
        if c_mode == 'inlay_well':
            return True
        preset = str(self._get_prop('profil_preset', 'stamped_plate') or 'stamped_plate')
        dsl = str(self._get_prop('custom_zones', '') or '')
        zones = config.parse_profile_zones(preset, dsl)
        return any((z.get('mat') == 'inlay' for z in zones))

    def _sync_color_selector_visibility(self):
        show_picker = self._needs_inlay_color_picker()
        self.color_frame.set_no_show_all(not show_picker)
        if show_picker:
            self.color_frame.show_all()
        else:
            self.color_frame.hide()

    def _apply_material_standard_recipe(self, mat_key: str):
        recipe = config.MATERIAL_LIGHT_DEFAULTS.get(mat_key)
        self._set_prop('surface_organic', '')
        if isinstance(recipe, dict):
            cur_lsrc = str(self._get_prop('light_source', 'auto') or 'auto')
            if cur_lsrc != 'auto':
                self._set_prop('light_source', str(recipe.get('light_source', 'cone')))
            self._set_prop('light_spread', int(recipe.get('light_spread', 48)))
            self._set_prop('glanz', int(recipe.get('glanz', 84)))
            self._set_prop('fasenkontrast', int(recipe.get('fasenkontrast', 84)))
            self._set_prop('luxus', bool(recipe.get('luxus', True)))
            self._set_prop('brushed', bool(recipe.get('brushed', False)))
            self._set_prop('brushed_granularity', int(recipe.get('brushed_granularity', 38)))
            self._set_prop('patina', int(recipe.get('patina', 0)))
            self._set_prop('scratches', int(recipe.get('scratches', 0)))
            self._set_prop('surface_organic', '')
        if mat_key in MATERIAL_DEFAULT_INLAY_HEX:
            self._set_prop('inlay_hex', MATERIAL_DEFAULT_INLAY_HEX[mat_key])
            self.color_selector._sync_button_from_cfg()

    def _on_glass_color_changed(self):
        self.refresh_geometry_previews()
        if callable(self.on_change_callback):
            self.on_change_callback()

    def _on_category_toggled(self, btn, cat_key):
        if self._updating or not btn.get_active():
            return
        self._updating = True
        self._active_category = cat_key
        for k, other in self._cat_buttons.items():
            if k != cat_key and other.get_active():
                other.set_active(False)
        self._rebuild_swatch_grid()
        self._updating = False

    def _rebuild_swatch_grid(self):
        for child in list(self.grid.get_children()):
            self.grid.remove(child)
        self._swatch_buttons.clear()
        self._swatch_images.clear()
        cur_mat = self._get_prop('material', 'gold')
        is_rounded, is_plate, glass_hex, prof_mode = self._current_swatch_state()
        _, mat_keys = config.MATERIAL_CATEGORY_GROUPS.get(self._active_category, config.MATERIAL_CATEGORY_GROUPS['all'])
        cols = 3
        for idx, mat_key in enumerate(mat_keys):
            full_label = config.METAL_LABELS.get(mat_key, mat_key)
            tier = config.MATERIAL_TIERS.get(mat_key, 'atelier')
            is_paid = tier != 'free'
            unlocked = self._material_open(mat_key)
            btn = Gtk.ToggleButton()
            btn.set_active(mat_key == cur_mat)
            btn.set_sensitive(True)
            btn.set_has_tooltip(False)
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            pix = SwatchThumbnailRenderer.render_pixbuf(mat_key, is_paid, unlocked, is_rounded, is_plate, glass_hex, prof_mode, tier)
            img = Gtk.Image.new_from_pixbuf(pix)
            vbox.pack_start(img, False, False, 0)
            self._swatch_images[mat_key] = img
            short_title = full_label.split('(')[0].strip()
            lbl = Gtk.Label()
            lbl.set_markup(f'<small>{short_title[:13]}</small>')
            vbox.pack_start(lbl, False, False, 0)
            btn.add(vbox)
            btn.connect('toggled', self._on_swatch_clicked, mat_key)
            btn.connect('enter-notify-event', lambda b, _ev, mk=mat_key: (self.hover_preview.show_for_button(b, mk, is_rounded=self._current_swatch_state()[0]), False)[1])
            btn.connect('leave-notify-event', lambda _b, _ev: (self.hover_preview.hide(), False)[1])
            self.grid.attach(btn, idx % cols, idx // cols, 1, 1)
            self._swatch_buttons[mat_key] = btn
        self.grid.show_all()

    def refresh_geometry_previews(self):
        is_rounded, is_plate, glass_hex, prof_mode = self._current_swatch_state()
        for mat_key, img_widget in self._swatch_images.items():
            tier = config.MATERIAL_TIERS.get(mat_key, 'atelier')
            pix = SwatchThumbnailRenderer.render_pixbuf(mat_key, tier != 'free', self._material_open(mat_key), is_rounded, is_plate, glass_hex, prof_mode, tier)
            img_widget.set_from_pixbuf(pix)
        self._sync_color_selector_visibility()

    def _material_open(self, mat_key: str) -> bool:
        if not self.license_limits:
            return True
        return config.material_allowed(mat_key, wider=bool(self.license_limits.get('wider_materials')), glass=bool(self.license_limits.get('glass_gems')))

    def _on_swatch_clicked(self, btn, mat_key):
        if self._updating or not btn.get_active():
            return
        self._updating = True
        for k, other_btn in self._swatch_buttons.items():
            if k != mat_key and other_btn.get_active():
                other_btn.set_active(False)
        self._set_prop('material', mat_key)
        self._apply_material_standard_recipe(mat_key)
        self._sync_color_selector_visibility()
        self.active_lbl.set_markup(f"<span foreground='#58D68D'>✔ <b>Aktiv: {config.METAL_LABELS.get(mat_key, mat_key)}</b></span>")
        self._updating = False
        if callable(self.on_change_callback):
            self.on_change_callback()
