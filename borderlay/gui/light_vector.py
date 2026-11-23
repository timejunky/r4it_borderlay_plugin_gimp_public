# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class _Area:

    def queue_draw(self):
        return None

class LightVectorPad(Gtk.Box):

    def __init__(self, cfg, on_change_callback=None):
        super().__init__()
        self.cfg = cfg
        self.area = _Area()

    def _sync_points_from_config(self):
        return None

    def _update_info_label(self):
        return None

    def apply_material_defaults_if_auto(self):
        return None
