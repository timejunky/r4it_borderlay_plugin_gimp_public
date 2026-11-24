# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp, GLib
from engine import BorderlayEngine
from gui.preview_gtk import GtkWindowEventHelper
from gui.preview_wireframe import SelectionWireframePreviewer

class CanvasPreviewController:
    PREVIEW_GROUP_PREFIX = 'Borderlay [Vorschau]:'
    BACKUP_LAYER_NAME = '__borderlay_source_backup__'

    def __init__(self, image, drawables, cfg):
        self.image = image
        self.drawables = list(drawables) if drawables else []
        self.cfg = cfg
        self.auto_enabled = False
        self.dialog = None
        self.apply_btn = None
        self._debounce_timer_id = None
        self._wireframe_timer_id = None
        self._preview_applied = False
        self._is_rendering = False
        self._preview_groups = []
        self._saved_selection = None
        self._source_backup = None
        self._orig_w = 0
        self._orig_h = 0
        self._source_layer = None
        self._orig_off_x = 0
        self._orig_off_y = 0
        if self._is_image_valid():
            self._orig_w = self.image.get_width()
            self._orig_h = self.image.get_height()
            self._source_layer = self._resolve_source_layer()
            if self._is_item_valid(self._source_layer):
                try:
                    offs = self._source_layer.get_offsets()
                    self._orig_off_x = int(offs[-2])
                    self._orig_off_y = int(offs[-1])
                except Exception:
                    pass
            if not Gimp.Selection.is_empty(self.image):
                self._saved_selection = Gimp.Selection.save(self.image)
                if self._is_item_valid(self._source_layer):
                    try:
                        self.image.set_selected_layers([self._source_layer])
                    except Exception:
                        pass

    def attach_dialog_widgets(self, dialog, apply_btn=None):
        self.dialog = dialog
        self.apply_btn = apply_btn

    @staticmethod
    def pump_gtk_events():
        GtkWindowEventHelper.pump_gtk_events()

    def _is_image_valid(self) -> bool:
        try:
            return self.image is not None and bool(self.image.is_valid())
        except Exception:
            return False

    @staticmethod
    def _is_item_valid(item) -> bool:
        try:
            return item is not None and bool(item.is_valid())
        except Exception:
            return False

    def _is_live_source(self, item) -> bool:
        if not self._is_item_valid(item) or item.is_group():
            return False
        name = item.get_name() or ''
        return not name.startswith(self.PREVIEW_GROUP_PREFIX) and (not name.startswith('Borderlay:')) and (name != self.BACKUP_LAYER_NAME)

    def _resolve_source_layer(self):
        if not self._is_image_valid():
            return None
        for drawable in self.drawables:
            if self._is_live_source(drawable):
                return drawable
        try:
            layers = self.image.get_layers()
        except Exception:
            return None
        for layer in layers:
            if self._is_live_source(layer):
                return layer
        return None

    def _ensure_source_backup(self):
        if self._is_item_valid(self._source_backup):
            return
        if not self._is_item_valid(self._source_layer) or self._source_layer.is_group():
            return
        try:
            backup = self._source_layer.copy()
            if backup is not None:
                backup.set_name(self.BACKUP_LAYER_NAME)
                backup.set_visible(False)
                parent = self._source_layer.get_parent()
                pos = self.image.get_item_position(self._source_layer) + 1
                self.image.insert_layer(backup, parent, pos)
                self._source_backup = backup
                self._source_layer.set_visible(True)
                self.image.set_selected_layers([self._source_layer])
        except Exception:
            self._source_backup = None

    def _restore_source_layer_from_backup(self):
        if not self._is_item_valid(self._source_backup):
            return
        try:
            restored = self._source_backup.copy()
            if restored is None:
                return
            orig_name = self._source_layer.get_name() if self._is_item_valid(self._source_layer) else 'Hintergrund'
            restored.set_name(orig_name)
            restored.set_visible(True)
            parent = self._source_backup.get_parent()
            pos = self.image.get_item_position(self._source_backup)
            self.image.insert_layer(restored, parent, pos)
            restored.set_offsets(self._orig_off_x, self._orig_off_y)
            if self._is_item_valid(self._source_layer):
                self.image.remove_layer(self._source_layer)
            self._source_layer = restored
            self.drawables = [restored]
            self.image.set_selected_layers([restored])
        except Exception:
            pass

    def _reset_canvas_size_if_expanded(self):
        if not self._is_image_valid() or not self._is_item_valid(self._source_layer):
            return
        try:
            cur_w = self.image.get_width()
            cur_h = self.image.get_height()
            if (cur_w != self._orig_w or cur_h != self._orig_h) and self._orig_w > 0 and (self._orig_h > 0):
                offs = self._source_layer.get_offsets()
                cur_ox = int(offs[-2])
                cur_oy = int(offs[-1])
                dx = self._orig_off_x - cur_ox
                dy = self._orig_off_y - cur_oy
                self.image.resize(self._orig_w, self._orig_h, dx, dy)
        except Exception:
            pass

    def remove_preview_layers(self):
        if not self._preview_applied or not self._is_image_valid():
            self._preview_applied = False
            self._preview_groups.clear()
            return
        try:
            for grp in list(self._preview_groups):
                if self._is_item_valid(grp):
                    self.image.remove_layer(grp)
            for layer in list(self.image.get_layers()):
                if self._is_item_valid(layer):
                    name = layer.get_name() or ''
                    if name.startswith(self.PREVIEW_GROUP_PREFIX):
                        self.image.remove_layer(layer)
            self._reset_canvas_size_if_expanded()
            self._restore_source_layer_from_backup()
            if self._is_item_valid(self._saved_selection):
                self.image.select_item(Gimp.ChannelOps.REPLACE, self._saved_selection)
            else:
                Gimp.Selection.none(self.image)
            Gimp.displays_flush()
        except Exception:
            pass
        finally:
            self._preview_applied = False
            self._preview_groups.clear()

    def render_selection_wireframe_now(self):
        self._wireframe_timer_id = None
        if self._is_rendering or not self._is_image_valid():
            return False
        for grp in self._preview_groups:
            if self._is_item_valid(grp):
                grp.set_visible(False)
        self._reset_canvas_size_if_expanded()
        SelectionWireframePreviewer.render_wireframe(self.image, self.cfg, self._saved_selection)
        if self._is_item_valid(self._source_layer):
            try:
                self.image.set_selected_layers([self._source_layer])
            except Exception:
                pass
        return False

    def schedule_selection_wireframe(self):
        if self._wireframe_timer_id is not None:
            GLib.source_remove(self._wireframe_timer_id)
            self._wireframe_timer_id = None
        if not self._is_rendering and self._is_image_valid():
            self._wireframe_timer_id = GLib.timeout_add(60, self.render_selection_wireframe_now)

    def render_now(self, _button=None):
        self._debounce_timer_id = None
        if self._wireframe_timer_id is not None:
            GLib.source_remove(self._wireframe_timer_id)
            self._wireframe_timer_id = None
        if self._is_rendering or not self._is_image_valid():
            return False
        self._is_rendering = True
        GtkWindowEventHelper.set_dialog_busy(self.dialog, self.apply_btn, True)
        try:
            self.remove_preview_layers()
            self._reset_canvas_size_if_expanded()
            self.pump_gtk_events()
            self._ensure_source_backup()
            if self._is_item_valid(self._saved_selection):
                self.image.select_item(Gimp.ChannelOps.REPLACE, self._saved_selection)
            else:
                Gimp.Selection.none(self.image)
            src = self._resolve_source_layer()
            active_drawables = [src] if self._is_item_valid(src) else []
            engine = BorderlayEngine(self.image, active_drawables, self.cfg, ui_pump_callback=self.pump_gtk_events, apply_metadata=False)
            created_group = engine.run()
            self._preview_groups.clear()
            if self._is_item_valid(created_group):
                nm = created_group.get_name() or 'Borderlay:'
                created_group.set_name(nm.replace('Borderlay:', self.PREVIEW_GROUP_PREFIX, 1))
                self._preview_groups.append(created_group)
            else:
                for layer in self.image.get_layers():
                    if self._is_item_valid(layer):
                        nm = layer.get_name() or ''
                        if nm.startswith('Borderlay:'):
                            layer.set_name(nm.replace('Borderlay:', self.PREVIEW_GROUP_PREFIX, 1))
                            self._preview_groups.append(layer)
            if self._is_item_valid(src):
                self.image.set_selected_layers([src])
            self._preview_applied = True
            Gimp.displays_flush()
        except Exception as exc:
            Gimp.message(f'Live-Vorschau-Hinweis: {exc}')
        finally:
            self._is_rendering = False
            GtkWindowEventHelper.set_dialog_busy(self.dialog, self.apply_btn, False)
            GtkWindowEventHelper.force_window_repaint(self.dialog)
            GLib.timeout_add(40, lambda: (GtkWindowEventHelper.force_window_repaint(self.dialog), False)[1])
        return False

    def schedule_update(self):
        self.schedule_selection_wireframe()
        if self._debounce_timer_id is not None:
            GLib.source_remove(self._debounce_timer_id)
            self._debounce_timer_id = None
        if self.auto_enabled and (not self._is_rendering) and self._is_image_valid():
            self._debounce_timer_id = GLib.timeout_add(350, self.render_now)

    def cleanup_before_close(self):
        for tid_attr in ('_wireframe_timer_id', '_debounce_timer_id'):
            tid = getattr(self, tid_attr, None)
            if tid is not None:
                GLib.source_remove(tid)
                setattr(self, tid_attr, None)
        if not self._is_image_valid():
            self._preview_applied = False
            self._preview_groups.clear()
            self._saved_selection = None
            self._source_backup = None
            return
        self.remove_preview_layers()
        self._reset_canvas_size_if_expanded()
        if self._is_item_valid(self._source_backup):
            try:
                self.image.remove_layer(self._source_backup)
            except Exception:
                pass
        self._source_backup = None
        if self._is_item_valid(self._saved_selection):
            try:
                self.image.select_item(Gimp.ChannelOps.REPLACE, self._saved_selection)
                self.image.remove_channel(self._saved_selection)
            except Exception:
                pass
        else:
            try:
                Gimp.Selection.none(self.image)
            except Exception:
                pass
        self._saved_selection = None
        if self._is_item_valid(self._source_layer):
            try:
                self.image.set_selected_layers([self._source_layer])
            except Exception:
                pass
        Gimp.displays_flush()
