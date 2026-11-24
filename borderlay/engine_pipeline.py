# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
from cache_guard import CacheGuard
from engine_params import EngineExecutionParams
from selection import SelectionManager

class EngineRenderPipeline:

    def __init__(self, image, group, params: EngineExecutionParams, pump_fn=None):
        self.image = image
        self.group = group
        self.p = params
        self._pump_fn = pump_fn

    def _pump(self):
        if callable(self._pump_fn):
            try:
                self._pump_fn()
            except Exception:
                pass

    def execute_all_stages(self, outer_box: tuple, inner_box: tuple, original_selection):
        if self.p.is_glass:
            self._render_glass_pipeline(outer_box, inner_box)
        else:
            self._render_metal_and_wood_pipeline(outer_box, inner_box)
        if self.p.glanz > 0:
            self._render_lighting_stage(outer_box, inner_box)
        if self.p.use_shimmer:
            self._render_shimmer_stage(outer_box, inner_box, original_selection)

    def _render_glass_pipeline(self, outer_box: tuple, inner_box: tuple):
        CacheGuard.trigger_domain('glass', reload_memory=True)
        from fx.glass import GlassFX
        GlassFX(self.image, self.group, self.p.angle, self.p.width, outer_box=outer_box, inner_box=inner_box, outer_radius=self.p.outer_r, inner_radius=self.p.inner_r, profile_preset=self.p.profile_preset, custom_dsl=self.p.custom_zones, glass_rgb=self._glass_body_rgb(), center_mode=self.p.center_mode, inner_transparency=self.p.inner_transparency, glanz=self.p.glanz, use_shimmer=self.p.use_shimmer).render()
        self._pump()
        if self.p.material == 'frosted_milk_glass' and self.p.patina > 0:
            self._render_textures_stage(outer_box)

    def _glass_body_rgb(self):
        fixed = {'frosted_milk_glass': (236, 240, 244), 'smoked_obsidian_glass': (18, 20, 24)}
        return fixed.get(self.p.material, self.p.inlay_rgb)

    def _render_metal_and_wood_pipeline(self, outer_box: tuple, inner_box: tuple):
        CacheGuard.trigger_domain('bevel', reload_memory=True)
        from fx.bevel import Bevel3D
        from fx.metal import BaseMetal
        metal_layer = BaseMetal(self.image, self.group, self.p.material, self.p.angle).render()
        self._pump()
        if self.p.relief > 0:
            CacheGuard.trigger_domain('zones', reload_memory=True)
            Bevel3D(self.image, self.group, self.p.material, self.p.relief, self.p.angle, self.p.width, self.p.fasenbreite, self.p.fasenkontrast, outer_box=outer_box, inner_box=inner_box, outer_radius=self.p.outer_r, inner_radius=self.p.inner_r, profile_preset=self.p.profile_preset, custom_dsl=self.p.custom_zones, inlay_rgb=self.p.inlay_rgb, center_mode=self.p.center_mode, inner_transparency=self.p.inner_transparency, profil_hoehe=self.p.profil_hoehe, profil_tiefe=self.p.profil_tiefe, gimp_gradient_name=self.p.gimp_gradient).render()
            self._pump()
        if self.p.use_brushed or self.p.scratches > 0 or self.p.patina > 0 or (self.p.surface_organic in ('feather', 'fur', 'scales')):
            self._render_textures_stage(outer_box)
        if self.p.luxus:
            CacheGuard.trigger_domain(['fx.bloom'], reload_memory=True)
            from fx.bloom import LuxusBloom
            LuxusBloom(self.image, self.group, round(self.p.glanz * 0.55), material=self.p.material).render(metal_layer)
            self._pump()

    def _render_textures_stage(self, outer_box: tuple):
        CacheGuard.trigger_domain('textures', reload_memory=True)
        from fx.texture import TextureFX
        saved_ring_sel = None
        if self.p.center_mode == 'plate' and 0 < self.p.inner_transparency <= 25:
            saved_ring_sel = Gimp.Selection.save(self.image)
            SelectionManager.select_full_box(self.image, outer_box, self.p.outer_r)
        try:
            textures = TextureFX(self.image, self.group, self.p.angle, brushed_granularity=self.p.brushed_granularity, brushed_angle=self.p.brushed_angle, fur_density=self.p.fur_density, fur_length=self.p.fur_length)
            if self.p.use_brushed:
                textures.render_brushed()
            if self.p.scratches > 0:
                textures.render_scratches(self.p.scratches)
            if self.p.patina > 0:
                textures.render_patina(self.p.patina, self.p.material)
            if self.p.surface_organic in ('feather', 'fur', 'scales'):
                textures.render_organic(self.p.surface_organic, self.p.width)
        finally:
            if saved_ring_sel is not None:
                self.image.select_item(Gimp.ChannelOps.REPLACE, saved_ring_sel)
                self.image.remove_channel(saved_ring_sel)
        self._pump()

    def _render_lighting_stage(self, outer_box: tuple, inner_box: tuple):
        CacheGuard.trigger_domain(['fx.light_shapes', 'fx.light_rims', 'fx.light'], reload_memory=True)
        from fx.light import GlobalLight
        GlobalLight(self.image, self.group, self.p.angle, material=self.p.material, glanz=self.p.glanz, outer_box=outer_box, inner_box=inner_box, border_width=self.p.width, outer_radius=self.p.outer_r, inner_radius=self.p.inner_r, profile_preset=self.p.profile_preset, luxus=self.p.luxus, center_mode=self.p.center_mode, inner_transparency=self.p.inner_transparency, use_shimmer=self.p.use_shimmer, shimmer_side=self.p.shimmer_side, light_source=self.p.light_source, light_spread=self.p.light_spread).render()
        self._pump()

    def _render_shimmer_stage(self, outer_box: tuple, inner_box: tuple, original_selection):
        CacheGuard.trigger_domain(['fx.shimmer'], reload_memory=True)
        from fx.shimmer import ShimmerFX
        ShimmerFX(self.image, self.group, self.p.material, self.p.width, self.p.glanz, self.p.position, self.p.shimmer_side, outer_box=outer_box, inner_box=inner_box, outer_radius=self.p.outer_r, inner_radius=self.p.inner_r, profile_preset=self.p.profile_preset, angle=self.p.angle, inner_transparency=self.p.inner_transparency).render(original_selection)
        self._pump()
