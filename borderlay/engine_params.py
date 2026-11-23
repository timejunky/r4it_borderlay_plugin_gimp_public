# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import config
from community_material_seal import apply_community_materials, community_material_key
from cache_guard import CacheGuard
from shapes.common.shape_transform import ShapeTransformHelper

class EngineExecutionParams:

    def __init__(self, cfg, border_width_override=None, scale_factor: float=1.0):
        self.cfg = cfg
        self.scale_factor = float(scale_factor)
        raw_width = border_width_override if border_width_override is not None and int(border_width_override) > 0 else self._get_prop('randbreite', 80)
        self.width = max(1, int(raw_width))
        apply_community_materials()
        raw_mat = self._text_prop('material', 'gold')
        self.material = community_material_key(raw_mat)
        self.is_glass = self.material in ('colored_glass', 'frosted_milk_glass', 'smoked_obsidian_glass')
        self.gimp_gradient = self._text_prop('gimp_gradient', 'none')
        self.angle = int(self._get_prop('angle', 135))
        self.raw_glanz = int(self._get_prop('glanz', 84))
        self.raw_light_source = self._text_prop('light_source', 'auto')
        self.raw_light_spread = int(self._get_prop('light_spread', 45))
        CacheGuard.trigger_domain(['fx.light_shapes'], reload_memory=True)
        from fx.light_shapes import LightSourceShapes
        self.light_source, self.light_spread, self.glanz = LightSourceShapes.resolve_material_lighting(self.material, light_source=self.raw_light_source, light_spread=self.raw_light_spread, glanz=self.raw_glanz)
        self.relief = int(self._get_prop('relief', 95))
        self.fasenbreite = int(self._get_prop('fasenbreite', 34))
        self.fasenkontrast = int(self._get_prop('fasenkontrast', 85))
        self.position = self._text_prop('position', 'aussen')
        self.profile_preset = self._text_prop('profil_preset', 'stamped_plate')
        self.center_mode = self._text_prop('innen_modus', 'transparent')
        self.inner_transparency = int(self._get_prop('innen_transparenz', 100))
        self.profil_hoehe = int(self._get_prop('profil_hoehe', 88))
        self.profil_tiefe = int(self._get_prop('profil_tiefe', 88))
        self.custom_zones = str(self._get_prop('custom_zones', config.DEFAULT_CUSTOM_DSL) or '')
        self.save_name = self._text_prop('preset_save_name', '').strip()
        self.inlay_rgb = self.parse_hex_rgb(self._get_prop('inlay_hex', '#241134'))
        self.luxus = bool(self._get_prop('luxus', True))
        self.use_brushed = bool(self._get_prop('brushed', False))
        self.brushed_granularity = int(self._get_prop('brushed_granularity', 38))
        self.brushed_angle = int(self._get_prop('brushed_angle', -1))
        self.fur_density = max(1, min(100, int(self._get_prop('fur_density', 72))))
        self.fur_length = max(1, min(100, int(self._get_prop('fur_length', 61))))
        self.scratches = int(self._get_prop('scratches', 0))
        self.patina = int(self._get_prop('patina', 0))
        raw_organic = self._text_prop('surface_organic', '').strip().lower()
        self.surface_organic = raw_organic if raw_organic in ('feather', 'fur', 'scales') else ''
        self.use_shimmer = bool(self._get_prop('innen_schimmer', False))
        self.shimmer_side = self._text_prop('schimmer_seite', 'auto')
        self.shape_rotation = int(self._get_prop('shape_rotation', 0))
        self.shape_pivot = self._text_prop('shape_pivot', 'center')
        self.rot_repeat = bool(self._get_prop('rot_repeat', False))
        self.rot_angle_start = int(self._get_prop('rot_angle_start', 0))
        self.rot_angle_end = int(self._get_prop('rot_angle_end', 45))
        self.rot_angle_step = int(self._get_prop('rot_angle_step', 15))
        raw_fmode = self._get_prop('rot_fade_mode', '')
        self.rot_fade_steps = int(self._get_prop('rot_fade_steps', 20))
        self.rot_cycle_times = int(self._get_prop('rot_cycle_times', 1))
        self.rot_cycle_until = int(self._get_prop('rot_cycle_until', 0))
        kind, fade_mode, cycle_times = ShapeTransformHelper.parse_rotation_mode(raw_fmode, self.rot_cycle_times, self.rot_cycle_until)
        self.rot_array_kind = kind
        self.rot_fade_mode = fade_mode
        if kind in ('cycle', 'offset'):
            self.rot_cycle_times = cycle_times
        ShapeTransformHelper.set_active_fade_mode(fade_mode)
        self.rotation_schedule = ShapeTransformHelper.compute_rotation_series(repeat_enabled=self.rot_repeat, single_angle=self.shape_rotation, angle_start=self.rot_angle_start, angle_end=self.rot_angle_end, angle_step=self.rot_angle_step, fade_pct=self.rot_fade_steps, fade_mode=self.rot_fade_mode, cycle_times=self.rot_cycle_times, cycle_until=self.rot_cycle_until, array_kind=self.rot_array_kind)
        if self.save_name and self.custom_zones:
            config.save_user_preset(self.save_name, self.custom_zones)
        outer_r = max(0, round(self._get_prop('eckenradius_aussen', 64) * self.scale_factor))
        inner_r = max(0, round(self._get_prop('eckenradius_innen', 0) * self.scale_factor))
        if self.profile_preset == 'logo_classic':
            outer_r = 0
            inner_r = 0
        elif self.profile_preset == 'atelier_look':
            inner_r = 0
        self.outer_r = int(outer_r)
        self.inner_r = int(inner_r)

    def _text_prop(self, name: str, default: str) -> str:
        return str(self._get_prop(name, default) or default)

    def _get_prop(self, name: str, default):
        try:
            return self.cfg.get_property(name)
        except Exception:
            return default

    @staticmethod
    def parse_hex_rgb(hex_str: str, fallback=(36, 17, 52)) -> tuple:
        s = (hex_str or '').strip().lstrip('#')
        if len(s) == 6:
            try:
                return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))
            except ValueError:
                pass
        return fallback
