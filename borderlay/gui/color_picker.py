# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk, Gtk
QUICK_GLASS_COLORS = (('#7B1FA2', 'Amethyst-Violett'), ('#0088FF', 'Saphirblau'), ('#00BFA5', 'Türkis / Aquamarin'), ('#2E7D32', 'Smaragdgrün'), ('#C62828', 'Rubinrot'), ('#FF8F00', 'Bernstein-Gold'), ('#37474F', 'Rauchglas-Anthrazit'), ('#8EC5FC', 'Eis-Cyan / Milchglas'))

class ColorSwatchSelector(Gtk.Box):

    def __init__(self, cfg, on_change_callback=None, compact=False):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.cfg = cfg
        self.on_change_callback = on_change_callback
        self._updating = False
        top_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        lbl = Gtk.Label(label='Glas- / Inlay-Farbe:' if not compact else 'Farbe:')
        top_hbox.pack_start(lbl, False, False, 0)
        self.color_btn = Gtk.ColorButton()
        self.color_btn.set_title('Glas- oder Inlay-Farbe wählen (inkl. Pipette)')
        self.color_btn.set_tooltip_text('Öffnet den Farbwähler mit Farbrad und Bildschirm-Pipette für Kristallglas & Inlays.')
        self._sync_button_from_cfg()
        self.color_btn.connect('color-set', self._on_color_button_set)
        top_hbox.pack_start(self.color_btn, True, True, 0)
        self.pack_start(top_hbox, False, False, 0)
        palette_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        for hex_code, tip_name in QUICK_GLASS_COLORS:
            btn = Gtk.Button()
            btn.set_size_request(22, 20)
            btn.set_tooltip_text(f'{tip_name} ({hex_code})')
            rgba = Gdk.RGBA()
            rgba.parse(hex_code)
            btn.override_background_color(Gtk.StateFlags.NORMAL, rgba)
            btn.connect('clicked', self._on_quick_color_clicked, hex_code)
            palette_hbox.pack_start(btn, True, True, 0)
        self.pack_start(palette_hbox, False, False, 0)

    def _get_hex(self):
        try:
            val = str(self.cfg.get_property('inlay_hex') or '#7B1FA2').strip()
            return val if val.startswith('#') and len(val) == 7 else '#7B1FA2'
        except Exception:
            return '#7B1FA2'

    def _set_hex(self, hex_str):
        try:
            self.cfg.set_property('inlay_hex', hex_str.upper())
        except Exception:
            pass

    def _sync_button_from_cfg(self):
        self._updating = True
        rgba = Gdk.RGBA()
        if not rgba.parse(self._get_hex()):
            rgba.parse('#7B1FA2')
        self.color_btn.set_rgba(rgba)
        self._updating = False

    def _on_color_button_set(self, btn):
        if self._updating:
            return
        rgba = btn.get_rgba()
        r = max(0, min(255, round(rgba.red * 255.0)))
        g = max(0, min(255, round(rgba.green * 255.0)))
        b = max(0, min(255, round(rgba.blue * 255.0)))
        hex_str = f'#{r:02X}{g:02X}{b:02X}'
        self._set_hex(hex_str)
        if callable(self.on_change_callback):
            self.on_change_callback()

    def _on_quick_color_clicked(self, _btn, hex_str):
        self._set_hex(hex_str)
        self._sync_button_from_cfg()
        if callable(self.on_change_callback):
            self.on_change_callback()
