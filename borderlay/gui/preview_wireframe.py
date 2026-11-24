# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
from selection import SelectionManager
from shapes import FreeformSelectionHelper, set_active_rotation

class SelectionWireframePreviewer:

    @staticmethod
    def _get_prop(cfg, name: str, default):
        try:
            return cfg.get_property(name)
        except Exception:
            return default

    @classmethod
    def render_wireframe(cls, image, cfg, saved_selection, preview_group=None):
        if image is None or not image.is_valid():
            return
        try:
            if preview_group is not None and preview_group.is_valid():
                preview_group.set_visible(False)
            if saved_selection is not None and saved_selection.is_valid():
                image.select_item(Gimp.ChannelOps.REPLACE, saved_selection)
            else:
                Gimp.Selection.all(image)
            width = max(1, int(cls._get_prop(cfg, 'randbreite', 80)))
            position = str(cls._get_prop(cfg, 'position', 'aussen') or 'aussen')
            profile_preset = str(cls._get_prop(cfg, 'profil_preset', 'stamped_plate') or 'stamped_plate')
            outer_r = max(0, int(cls._get_prop(cfg, 'eckenradius_aussen', 64)))
            inner_r = max(0, int(cls._get_prop(cfg, 'eckenradius_innen', 0)))
            if profile_preset == 'logo_classic':
                outer_r = 0
                inner_r = 0
            elif profile_preset == 'atelier_look':
                inner_r = 0
            eff_rot = int(cls._get_prop(cfg, 'shape_rotation', 0))
            shape_pivot = str(cls._get_prop(cfg, 'shape_pivot', 'center') or 'center')
            SelectionManager.create_border(image, width, position, outer_radius=outer_r, inner_radius=inner_r, center_mode='transparent', inner_transparency=100, shape_rotation=eff_rot, shape_pivot=shape_pivot)
            FreeformSelectionHelper.clear_state(image)
            set_active_rotation(0, 'center')
            Gimp.displays_flush()
        except Exception:
            pass
