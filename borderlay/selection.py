# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import math
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
from shapes import CircularSelectionHelper, FreeformSelectionHelper, ShapeTransformHelper, get_active_shape_mode, is_circular_mode, is_curved_or_freeform_mode, is_forced_circle_1_1, is_freeform_mode, is_leaf_mode, set_active_rotation
from shapes.leaf_outline import leaf_polygon

class SelectionManager:

    @staticmethod
    def get_selection_box(image, channel=None):
        if channel is not None:
            if not image.select_item(Gimp.ChannelOps.REPLACE, channel):
                raise RuntimeError('Der Auswahlkanal konnte zur Box-Berechnung nicht geladen werden.')
        bounds = Gimp.Selection.bounds(image)
        has_selection = bounds[1] if len(bounds) == 6 else bounds[0]
        x1, y1, x2, y2 = bounds[-4:]
        if not has_selection:
            raise RuntimeError('Die Auswahl enthält keine gültigen Grenzen.')
        return (int(x1), int(y1), int(x2), int(y2))

    @staticmethod
    def select_rect_with_radius(image, op, x1, y1, x2, y2, radius):
        if is_freeform_mode():
            FreeformSelectionHelper.select_contour_box(image, op, x1, y1, x2, y2)
            return
        if is_circular_mode():
            CircularSelectionHelper.select_ellipse_box(image, op, x1, y1, x2, y2, force_circle=is_forced_circle_1_1())
            return
        w = max(1.0, float(x2 - x1))
        h = max(1.0, float(y2 - y1))
        r = max(0.0, min(float(radius), min(w, h) / 2.0))
        if r <= 0.5:
            if not image.select_rectangle(op, float(x1), float(y1), w, h):
                raise RuntimeError('Die rechteckige Auswahl konnte nicht erstellt werden.')
        elif not image.select_round_rectangle(op, float(x1), float(y1), w, h, r, r):
            raise RuntimeError('Die abgerundete Auswahl konnte nicht erstellt werden.')

    @staticmethod
    def select_full_box(image, box, radius):
        ox1, oy1, ox2, oy2 = box
        SelectionManager.select_rect_with_radius(image, Gimp.ChannelOps.REPLACE, ox1, oy1, ox2, oy2, radius)

    @staticmethod
    def select_zone_ring(image, outer_box, inner_box, r_out, r_in):
        ox1, oy1, ox2, oy2 = outer_box
        ix1, iy1, ix2, iy2 = inner_box
        SelectionManager.select_rect_with_radius(image, Gimp.ChannelOps.REPLACE, ox1, oy1, ox2, oy2, r_out)
        if ix2 > ix1 and iy2 > iy1:
            SelectionManager.select_rect_with_radius(image, Gimp.ChannelOps.SUBTRACT, ix1, iy1, ix2, iy2, r_in)

    @staticmethod
    def clip_source_drawable_corners(image, source_layer, outer_box, outer_radius):
        if source_layer is None or source_layer.is_group():
            return
        if is_curved_or_freeform_mode() or outer_radius <= 1.0:
            return
        ox1, oy1, ox2, oy2 = outer_box
        box_w = ox2 - ox1
        box_h = oy2 - oy1
        lw = source_layer.get_width()
        lh = source_layer.get_height()
        try:
            offs = source_layer.get_offsets()
            lx = int(offs[-2])
            ly = int(offs[-1])
        except Exception:
            lx, ly = (0, 0)
        is_full_layer_frame = ox1 <= lx + 4 and oy1 <= ly + 4 and (ox2 >= lx + lw - 4) and (oy2 >= ly + lh - 4)
        if not is_full_layer_frame:
            return
        saved_sel = Gimp.Selection.save(image)
        try:
            if not source_layer.has_alpha():
                source_layer.add_alpha()
            image.select_rectangle(Gimp.ChannelOps.REPLACE, float(ox1), float(oy1), float(max(1, box_w)), float(max(1, box_h)))
            SelectionManager.select_rect_with_radius(image, Gimp.ChannelOps.SUBTRACT, ox1, oy1, ox2, oy2, outer_radius)
            if not Gimp.Selection.is_empty(image):
                source_layer.edit_clear()
        except Exception:
            pass
        finally:
            Gimp.Selection.none(image)
            if saved_sel is not None:
                image.select_item(Gimp.ChannelOps.REPLACE, saved_sel)
                image.remove_channel(saved_sel)

    @staticmethod
    def select_inward_band(image, original_selection, width):
        if width <= 0:
            raise ValueError('Die Breite des Innenschimmers muss größer als null sein.')
        if not image.select_item(Gimp.ChannelOps.REPLACE, original_selection):
            raise RuntimeError('Die ursprüngliche Bildauswahl konnte nicht wiederhergestellt werden.')
        inner_selection = None
        completed = False
        try:
            if not Gimp.Selection.shrink(image, int(width)):
                raise RuntimeError('Die Bildauswahl konnte für den Innenschimmer nicht verkleinert werden.')
            inner_is_empty = Gimp.Selection.is_empty(image)
            if not inner_is_empty:
                inner_selection = Gimp.Selection.save(image)
                if inner_selection is None:
                    raise RuntimeError('Die innere Auswahl für den Schimmer konnte nicht gespeichert werden.')
            Gimp.Selection.none(image)
            if not image.select_item(Gimp.ChannelOps.REPLACE, original_selection):
                raise RuntimeError('Die Bildauswahl konnte für den Innenschimmer nicht wiederhergestellt werden.')
            if inner_selection is not None:
                if not image.select_item(Gimp.ChannelOps.SUBTRACT, inner_selection):
                    raise RuntimeError('Der Innenschimmer konnte nicht auf die innere Bildkante begrenzt werden.')
            completed = True
        finally:
            if inner_selection is not None:
                image.remove_channel(inner_selection)
            if not completed:
                Gimp.Selection.none(image)
                image.select_item(Gimp.ChannelOps.REPLACE, original_selection)

    @staticmethod
    def select_outward_band(image, original_selection, width):
        if width <= 0:
            raise ValueError('Die Breite des Außenschimmers muss größer als null sein.')
        if not image.select_item(Gimp.ChannelOps.REPLACE, original_selection):
            raise RuntimeError('Die Basisauswahl für den Außenschimmer konnte nicht geladen werden.')
        if not Gimp.Selection.grow(image, int(width)):
            raise RuntimeError('Die Auswahl konnte für den Außenschimmer nicht erweitert werden.')
        expanded_selection = Gimp.Selection.save(image)
        if expanded_selection is None:
            raise RuntimeError('Die erweiterte Auswahl für den Außenschimmer konnte nicht gespeichert werden.')
        try:
            Gimp.Selection.none(image)
            if not image.select_item(Gimp.ChannelOps.REPLACE, expanded_selection):
                raise RuntimeError('Die erweiterte Auswahl konnte nicht wiederhergestellt werden.')
            if not image.select_item(Gimp.ChannelOps.SUBTRACT, original_selection):
                raise RuntimeError('Der Außenschimmer konnte nicht auf die Auswahlkante begrenzt werden.')
        finally:
            image.remove_channel(expanded_selection)

    @staticmethod
    def _ensure_canvas_margin(image, orig_sel, needed_outward_px):
        if needed_outward_px <= 0:
            return
        x1, y1, x2, y2 = SelectionManager.get_selection_box(image, orig_sel)
        img_w = image.get_width()
        img_h = image.get_height()
        pad_left = max(0, needed_outward_px - x1)
        pad_top = max(0, needed_outward_px - y1)
        pad_right = max(0, x2 + needed_outward_px - img_w)
        pad_bottom = max(0, y2 + needed_outward_px - img_h)
        if pad_left > 0 or pad_top > 0 or pad_right > 0 or (pad_bottom > 0):
            new_w = img_w + pad_left + pad_right
            new_h = img_h + pad_top + pad_bottom
            if not image.resize(new_w, new_h, pad_left, pad_top):
                raise RuntimeError('Die Bildleinwand konnte nicht für den Außenrahmen erweitert werden.')

    @staticmethod
    def compute_frame_boxes(image, orig_sel, width, position):
        width = max(1, int(width))
        if position == 'aussen':
            SelectionManager._ensure_canvas_margin(image, orig_sel, width)
            ix1, iy1, ix2, iy2 = SelectionManager.get_selection_box(image, orig_sel)
            outer_box = (ix1 - width, iy1 - width, ix2 + width, iy2 + width)
            inner_box = (ix1, iy1, ix2, iy2)
        elif position == 'innen':
            ox1, oy1, ox2, oy2 = SelectionManager.get_selection_box(image, orig_sel)
            outer_box = (ox1, oy1, ox2, oy2)
            inner_box = (ox1 + width, oy1 + width, ox2 - width, oy2 - width)
        elif position in ('zentriert', 'mitte'):
            w_out = int(math.ceil(float(width) / 2.0))
            w_in = int(math.floor(float(width) / 2.0))
            if w_out > 0:
                SelectionManager._ensure_canvas_margin(image, orig_sel, w_out)
            bx1, by1, bx2, by2 = SelectionManager.get_selection_box(image, orig_sel)
            outer_box = (bx1 - w_out, by1 - w_out, bx2 + w_out, by2 + w_out)
            inner_box = (bx1 + w_in, by1 + w_in, bx2 - w_in, by2 - w_in)
        else:
            raise ValueError(f'Unbekannte Rahmenposition: {position}')
        if is_forced_circle_1_1():
            ox, oy, ow, oh = CircularSelectionHelper.normalize_box(*outer_box, force_circle=True)
            outer_box = (int(round(ox)), int(round(oy)), int(round(ox + ow)), int(round(oy + oh)))
            inner_box = (outer_box[0] + width, outer_box[1] + width, outer_box[2] - width, outer_box[3] - width)
        return (outer_box, inner_box)

    @staticmethod
    def _rotate_border_selection(image, outer_box, inner_box, shape_rotation: int, shape_pivot: str):
        pad_l, pad_t = ShapeTransformHelper.ensure_canvas_for_rotated_box(image, outer_box, float(shape_rotation), str(shape_pivot), extra_margin=4)
        shifted_outer = (outer_box[0] + pad_l, outer_box[1] + pad_t, outer_box[2] + pad_l, outer_box[3] + pad_t)
        shifted_inner = (inner_box[0] + pad_l, inner_box[1] + pad_t, inner_box[2] + pad_l, inner_box[3] + pad_t)
        ShapeTransformHelper.rotate_current_selection(image, float(shape_rotation), pivot_mode=str(shape_pivot), ref_box=shifted_outer)
        return (shifted_outer, shifted_inner)

    @staticmethod
    def _drop_temp_channel(image, channel) -> None:
        if channel is None:
            return
        if channel.is_valid():
            image.remove_channel(channel)

    @staticmethod
    def _leaf_base_selection(image, orig_sel):
        bx1, by1, bx2, by2 = SelectionManager.get_selection_box(image, orig_sel)
        image.select_polygon(Gimp.ChannelOps.REPLACE, leaf_polygon(bx1, by1, bx2, by2))
        return Gimp.Selection.save(image)

    @staticmethod
    def _active_base_selection(image, orig_sel):
        if not is_leaf_mode():
            return (orig_sel, None)
        leaf = SelectionManager._leaf_base_selection(image, orig_sel)
        if leaf is None:
            return (orig_sel, None)
        return (leaf, leaf)

    @staticmethod
    def _frame_inner_radius(inner_radius, outer_radius, width) -> float:
        eff_r_in = float(inner_radius)
        if outer_radius <= 1:
            return eff_r_in
        if eff_r_in > 0:
            return eff_r_in
        return max(28.0, float(outer_radius) - float(width) * 0.46)

    @staticmethod
    def _select_created_border(image, center_mode, inner_transparency, outer_box, inner_box, outer_radius, eff_r_in) -> None:
        SelectionManager.select_zone_ring(image, outer_box, inner_box, outer_radius, eff_r_in)

    @staticmethod
    def _restore_original_selection(image, orig_sel) -> None:
        Gimp.Selection.none(image)
        image.select_item(Gimp.ChannelOps.REPLACE, orig_sel)

    @staticmethod
    def create_border(image, width, position, outer_radius=64, inner_radius=0, center_mode='transparent', inner_transparency=100, shape_rotation=0, shape_pivot='center'):
        rot_deg = int(round(float(shape_rotation or 0)))
        set_active_rotation(0, shape_pivot)
        orig_sel = Gimp.Selection.save(image)
        if orig_sel is None:
            raise RuntimeError('Die Ausgangsauswahl konnte nicht gespeichert werden.')
        leaf_sel = None
        completed = False
        try:
            active_sel, leaf_sel = SelectionManager._active_base_selection(image, orig_sel)
            outer_box, inner_box = SelectionManager.compute_frame_boxes(image, active_sel, width, position)
            if is_freeform_mode():
                FreeformSelectionHelper.init_contour(image, active_sel, width, position, outer_box, inner_box)
            eff_r_in = SelectionManager._frame_inner_radius(inner_radius, outer_radius, width)
            SelectionManager._select_created_border(image, center_mode, inner_transparency, outer_box, inner_box, outer_radius, eff_r_in)
            if abs(rot_deg) > 0:
                outer_box, inner_box = SelectionManager._rotate_border_selection(image, outer_box, inner_box, rot_deg, str(shape_pivot))
                set_active_rotation(rot_deg, shape_pivot)
            if Gimp.Selection.is_empty(image):
                raise RuntimeError('Die erzeugte Rahmenauswahl ist leer.')
            completed = True
            return (outer_box, inner_box)
        finally:
            SelectionManager._drop_temp_channel(image, leaf_sel)
            if not completed:
                SelectionManager._restore_original_selection(image, orig_sel)
            image.remove_channel(orig_sel)
