# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import json
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import config
MATERIAL_PRESETS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_material_presets.json')
MATERIAL_CATEGORIES = {'all': ('Alle Kategorien', tuple(config.METAL_LABELS.keys())), 'warm_metals': ('Edel- & Buntmetalle (Gold, Kupfer, Bronze)', ('gold', 'bronze', 'messing')), 'white_metals': ('Weißmetalle & Spiegelchrom', ('aluminium', 'silber')), 'wood_leather': ('Edelholz & Naturstoffe (Kirschbaum, Nussbaum, Leder)', ()), 'glass': ('Kristall- & Milchglas', ())}
BUILTIN_MATERIAL_TEMPLATES = {}

class MaterialBrowserPanel(Gtk.Box):

    def __init__(self, cfg, on_change_callback=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.cfg = cfg
        self.on_change_callback = on_change_callback
        self._updating = False
        frame = Gtk.Frame(label='Material-Kategorien, Vorlagen & Oberflächen-Finish')
        grid = Gtk.Grid(column_spacing=8, row_spacing=6)
        grid.set_margin_top(8)
        grid.set_margin_bottom(8)
        grid.set_margin_start(8)
        grid.set_margin_end(8)
        grid.attach(Gtk.Label(label='Kategorie:', xalign=0), 0, 0, 1, 1)
        self.cat_combo = Gtk.ComboBoxText()
        for c_key, (c_label, _) in MATERIAL_CATEGORIES.items():
            self.cat_combo.append(c_key, c_label)
        self.cat_combo.set_active_id('all')
        self.cat_combo.connect('changed', self._on_category_changed)
        grid.attach(self.cat_combo, 1, 0, 2, 1)
        grid.attach(Gtk.Label(label='Basis-Material:', xalign=0), 0, 1, 1, 1)
        self.mat_combo = Gtk.ComboBoxText()
        self._populate_materials('all')
        self.mat_combo.connect('changed', self._on_material_changed)
        grid.attach(self.mat_combo, 1, 1, 2, 1)
        grid.attach(Gtk.Label(label='Material-Vorlage:', xalign=0), 0, 2, 1, 1)
        self.tpl_combo = Gtk.ComboBoxText()
        self._populate_templates()
        self.tpl_combo.connect('changed', self._on_template_selected)
        grid.attach(self.tpl_combo, 1, 2, 2, 1)
        finish_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        btn_mirror = Gtk.Button(label='Spiegelnd')
        btn_mirror.set_tooltip_text('Maximiert Spiegelglanz & Kontrast, deaktiviert Rauheit')
        btn_mirror.connect('clicked', self._on_preset_mirror)
        btn_frosted = Gtk.Button(label='Milchig / Satin')
        btn_frosted.set_tooltip_text('Weiche, milchig-matte Lichtstreuung mit feiner Satin-Körnung')
        btn_frosted.connect('clicked', self._on_preset_frosted)
        btn_brushed = Gtk.Button(label='Gebürstet')
        btn_brushed.set_tooltip_text('Aktiviert gerichteten Metall-/Holz-Haarschliff')
        btn_brushed.connect('clicked', self._on_preset_brushed)
        btn_grained = Gtk.Button(label='Körnung / Guss')
        btn_grained.set_tooltip_text('Aktiviert feinporige Guss- und Strukturkörnung')
        btn_grained.connect('clicked', self._on_preset_grained)
        for b in (btn_mirror, btn_frosted, btn_brushed, btn_grained):
            finish_box.pack_start(b, True, True, 0)
        grid.attach(finish_box, 0, 3, 3, 1)
        grid.attach(Gtk.Label(label='Look speichern:', xalign=0), 0, 4, 1, 1)
        self.save_entry = Gtk.Entry()
        self.save_entry.set_placeholder_text('z.B. Kirschbaum Dunkel')
        grid.attach(self.save_entry, 1, 4, 1, 1)
        save_btn = Gtk.Button(label='Speichern')
        save_btn.connect('clicked', self._on_save_material_preset)
        grid.attach(save_btn, 2, 4, 1, 1)
        frame.add(grid)
        self.pack_start(frame, False, False, 0)

    def _populate_materials(self, cat_key):
        self._updating = True
        cur_mat = self._get_prop('material', 'gold')
        self.mat_combo.remove_all()
        _, allowed_keys = MATERIAL_CATEGORIES.get(cat_key, MATERIAL_CATEGORIES['all'])
        for k in allowed_keys:
            if k in config.METAL_LABELS:
                self.mat_combo.append(k, config.METAL_LABELS[k])
        if not self.mat_combo.set_active_id(cur_mat) and allowed_keys:
            self.mat_combo.set_active_id(allowed_keys[0])
        self._updating = False

    def _load_all_templates(self):
        templates = dict(BUILTIN_MATERIAL_TEMPLATES)
        if os.path.isfile(MATERIAL_PRESETS_FILE):
            try:
                with open(MATERIAL_PRESETS_FILE, 'r', encoding='utf-8') as f:
                    user_data = json.load(f)
                    if isinstance(user_data, dict):
                        templates.update(user_data)
            except Exception:
                pass
        return templates

    def _populate_templates(self):
        self._updating = True
        self.tpl_combo.remove_all()
        self.tpl_combo.append('none', '-- Vorlage wählen (z.B. Kirschbaum / Spiegelchrom) --')
        for t_key, t_spec in self._load_all_templates().items():
            self.tpl_combo.append(t_key, t_spec.get('label', t_key))
        self.tpl_combo.set_active_id('none')
        self._updating = False

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

    def _on_category_changed(self, combo):
        cat_key = combo.get_active_id() or 'all'
        self._populate_materials(cat_key)

    def _on_material_changed(self, combo):
        if self._updating:
            return
        mat_key = combo.get_active_id()
        if mat_key:
            self._set_prop('material', mat_key)
            if callable(self.on_change_callback):
                self.on_change_callback()

    def _on_template_selected(self, combo):
        if self._updating:
            return
        t_key = combo.get_active_id()
        if not t_key or t_key == 'none':
            return
        templates = self._load_all_templates()
        spec = templates.get(t_key)
        if not spec:
            return
        for prop_key, prop_val in spec.items():
            if prop_key != 'label':
                self._set_prop(prop_key, prop_val)
        self._set_prop('surface_organic', str(spec.get('surface_organic', '') or ''))
        self._populate_materials(self.cat_combo.get_active_id() or 'all')
        if callable(self.on_change_callback):
            self.on_change_callback()

    def _on_preset_mirror(self, _btn):
        self._set_prop('glanz', 100)
        self._set_prop('fasenkontrast', 96)
        self._set_prop('brushed', False)
        self._set_prop('patina', 0)
        self._set_prop('scratches', 0)
        self._set_prop('surface_organic', '')
        self._set_prop('luxus', True)
        if callable(self.on_change_callback):
            self.on_change_callback()

    def _on_preset_frosted(self, _btn):
        self._set_prop('glanz', 58)
        self._set_prop('fasenkontrast', 64)
        self._set_prop('fasenbreite', 52)
        self._set_prop('brushed', True)
        self._set_prop('brushed_granularity', 14)
        self._set_prop('patina', 16)
        self._set_prop('surface_organic', '')
        self._set_prop('luxus', False)
        if callable(self.on_change_callback):
            self.on_change_callback()

    def _on_preset_brushed(self, _btn):
        self._set_prop('brushed', True)
        self._set_prop('brushed_granularity', 42)
        self._set_prop('scratches', 3)
        self._set_prop('surface_organic', '')
        if callable(self.on_change_callback):
            self.on_change_callback()

    def _on_preset_grained(self, _btn):
        self._set_prop('brushed', False)
        self._set_prop('patina', 48)
        self._set_prop('scratches', 2)
        self._set_prop('surface_organic', '')
        if callable(self.on_change_callback):
            self.on_change_callback()

    def _on_save_material_preset(self, _btn):
        raw_name = (self.save_entry.get_text() or '').strip()
        if not raw_name:
            return
        key = raw_name.lower().replace(' ', '_')
        all_tpl = {}
        if os.path.isfile(MATERIAL_PRESETS_FILE):
            try:
                with open(MATERIAL_PRESETS_FILE, 'r', encoding='utf-8') as f:
                    all_tpl = json.load(f)
            except Exception:
                all_tpl = {}
        all_tpl[key] = {'label': f'User: {raw_name}', 'material': self._get_prop('material', 'gold'), 'glanz': self._get_prop('glanz', 85), 'fasenkontrast': self._get_prop('fasenkontrast', 85), 'brushed': self._get_prop('brushed', False), 'brushed_granularity': self._get_prop('brushed_granularity', 30), 'brushed_angle': self._get_prop('brushed_angle', -1), 'fur_density': self._get_prop('fur_density', 72), 'fur_length': self._get_prop('fur_length', 61), 'finish_mode': self._get_prop('finish_mode', ''), 'patina': self._get_prop('patina', 0), 'scratches': self._get_prop('scratches', 0), 'surface_organic': self._get_prop('surface_organic', ''), 'luxus': self._get_prop('luxus', True)}
        try:
            with open(MATERIAL_PRESETS_FILE, 'w', encoding='utf-8') as f:
                json.dump(all_tpl, f, indent=2, ensure_ascii=False)
            self.save_entry.set_text('')
            self._populate_templates()
            self.tpl_combo.set_active_id(key)
        except Exception:
            pass
