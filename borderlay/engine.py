# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
import config
from cache_guard import CacheGuard
from engine_params import EngineExecutionParams
from engine_pipeline import EngineRenderPipeline
from locales.i18n import t
from selection import SelectionManager
from shapes import FreeformSelectionHelper, ShapeTransformHelper, set_active_rotation

class BorderlayEngine:

    def __init__(self, image, drawables, cfg, ui_pump_callback=None, apply_metadata=True):
        self.image = image
        self.drawables = drawables
        self.cfg = cfg
        self.ui_pump_callback = ui_pump_callback
        self.apply_metadata = bool(apply_metadata)

    def _pump_ui(self):
        if callable(self.ui_pump_callback):
            try:
                self.ui_pump_callback()
            except Exception:
                pass

    def _get_prop(self, name, default):
        try:
            return self.cfg.get_property(name)
        except Exception:
            return default

    @staticmethod
    def _parse_hex_rgb(hex_str, fallback=(36, 17, 52)):
        return EngineExecutionParams.parse_hex_rgb(hex_str, fallback=fallback)

    def _resolve_source_layer(self):
        if self.drawables:
            for d in self.drawables:
                if d is not None and d.is_valid() and (not d.is_group()):
                    return d
            if self.drawables[0] is not None and self.drawables[0].is_valid():
                return self.drawables[0]
        img_layers = self.image.get_layers()
        for lyr in img_layers:
            if lyr is not None and lyr.is_valid() and (not lyr.is_group()):
                return lyr
        return img_layers[0] if img_layers else None

    def _finish_run(self, selection_was_empty, original_selection, source_layer, undo_group_started):
        FreeformSelectionHelper.clear_state(self.image)
        set_active_rotation(0, 'center')
        if selection_was_empty:
            Gimp.Selection.none(self.image)
        elif original_selection is not None:
            self.image.select_item(Gimp.ChannelOps.REPLACE, original_selection)
        if original_selection is not None:
            self.image.remove_channel(original_selection)
        if source_layer is not None and source_layer.is_valid():
            try:
                self.image.set_selected_layers([source_layer])
            except Exception:
                pass
        if undo_group_started:
            self.image.undo_group_end()
        Gimp.context_pop()
        self._pump_ui()

    def run(self, border_width_override=None, scale_factor=1.0):
        CacheGuard.trigger_domain(['pdb_schema', 'engine_params', 'engine_pipeline'], reload_memory=True)
        self._pump_ui()
        params = EngineExecutionParams(self.cfg, border_width_override=border_width_override, scale_factor=scale_factor)
        selection_was_empty = Gimp.Selection.is_empty(self.image)
        Gimp.context_push()
        undo_group_started = False
        original_selection = None
        source_layer = None
        group = None
        try:
            self.image.undo_group_start()
            undo_group_started = True
            if selection_was_empty and (not Gimp.Selection.all(self.image)):
                raise RuntimeError(t('err_selection_invalid'))
            original_selection = Gimp.Selection.save(self.image)
            if original_selection is None:
                raise RuntimeError(t('err_selection_save_failed'))
            outer_box, inner_box = SelectionManager.create_border(self.image, params.width, params.position, outer_radius=params.outer_r, inner_radius=params.inner_r, center_mode=params.center_mode, inner_transparency=params.inner_transparency, shape_rotation=0, shape_pivot=params.shape_pivot)
            self._pump_ui()
            schedule = params.rotation_schedule
            has_rotation = any((abs(int(ang)) > 0 for ang, _op in schedule))
            source_layer = self._resolve_source_layer()
            if not has_rotation and len(schedule) == 1:
                SelectionManager.clip_source_drawable_corners(self.image, source_layer, outer_box, params.outer_r)
            parent = source_layer.get_parent() if source_layer else None
            layer_pos = self.image.get_item_position(source_layer) if source_layer else 0
            group_title = f'Borderlay: {config.METAL_LABELS[params.material]}'
            group = Gimp.GroupLayer.new(self.image, group_title)
            self.image.insert_layer(group, parent, layer_pos)
            self._pump_ui()
            pipeline = EngineRenderPipeline(self.image, group, params, pump_fn=self._pump_ui)
            pipeline.execute_all_stages(outer_box, inner_box, original_selection)
            FreeformSelectionHelper.clear_state(self.image)
            if has_rotation or len(schedule) > 1:
                ShapeTransformHelper.apply_post_render_rotation(self.image, group, outer_box, schedule, pivot_mode=params.shape_pivot, pump_fn=self._pump_ui)
            if self.apply_metadata:
                try:
                    from image_metadata import apply_image_metadata
                    apply_image_metadata(self.image)
                except Exception:
                    pass
            Gimp.displays_flush()
            return group
        finally:
            self._finish_run(selection_was_empty, original_selection, source_layer, undo_group_started)
