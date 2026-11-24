# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import GObject
import config
from locales.i18n import t

class PdbSchemaRegistrar:

    @staticmethod
    def register_arguments(procedure):
        procedure.add_int_argument('randbreite', t('pdb_randbreite_nick'), t('pdb_randbreite_blurb'), 1, 500, 96, GObject.ParamFlags.READWRITE)
        procedure.add_string_argument('position', t('pdb_position_nick'), t('pdb_position_blurb'), 'aussen', GObject.ParamFlags.READWRITE)
        procedure.add_string_argument('material', t('pdb_material_nick'), t('pdb_material_blurb'), 'gold', GObject.ParamFlags.READWRITE)
        procedure.add_string_argument('gimp_gradient', t('pdb_gimp_gradient_nick'), t('pdb_gimp_gradient_blurb'), 'none', GObject.ParamFlags.READWRITE)
        procedure.add_int_argument('eckenradius_aussen', t('pdb_r_out_nick'), t('pdb_r_out_blurb'), 0, 300, 84, GObject.ParamFlags.READWRITE)
        procedure.add_int_argument('eckenradius_innen', t('pdb_r_in_nick'), t('pdb_r_in_blurb'), 0, 300, 38, GObject.ParamFlags.READWRITE)
        procedure.add_string_argument('profil_preset', t('pdb_profil_preset_nick'), t('pdb_profil_preset_blurb'), 'stamped_plate', GObject.ParamFlags.READWRITE)
        procedure.add_string_argument('innen_modus', t('pdb_innen_modus_nick'), t('pdb_innen_modus_blurb'), 'transparent', GObject.ParamFlags.READWRITE)
        procedure.add_int_argument('innen_transparenz', t('pdb_innen_transp_nick'), t('pdb_innen_transp_blurb'), 0, 100, 100, GObject.ParamFlags.READWRITE)
        procedure.add_string_argument('inlay_hex', t('pdb_inlay_hex_nick'), t('pdb_inlay_hex_blurb'), '#7B1FA2', GObject.ParamFlags.READWRITE)
        procedure.add_int_argument('relief', t('pdb_relief_nick'), t('pdb_relief_blurb'), 0, 100, 96, GObject.ParamFlags.READWRITE)
        procedure.add_int_argument('profil_hoehe', t('pdb_profil_hoehe_nick'), t('pdb_profil_hoehe_blurb'), 0, 100, 90, GObject.ParamFlags.READWRITE)
        procedure.add_int_argument('profil_tiefe', t('pdb_profil_tiefe_nick'), t('pdb_profil_tiefe_blurb'), 0, 100, 92, GObject.ParamFlags.READWRITE)
        procedure.add_int_argument('fasenbreite', t('pdb_fasenbreite_nick'), t('pdb_fasenbreite_blurb'), 5, 100, 34, GObject.ParamFlags.READWRITE)
        procedure.add_int_argument('fasenkontrast', t('pdb_fasenkontrast_nick'), t('pdb_fasenkontrast_blurb'), 0, 100, 84, GObject.ParamFlags.READWRITE)
        procedure.add_int_argument('angle', t('pdb_angle_nick'), t('pdb_angle_blurb'), 0, 360, 135, GObject.ParamFlags.READWRITE)
        procedure.add_int_argument('glanz', t('pdb_glanz_nick'), t('pdb_glanz_blurb'), 0, 100, 84, GObject.ParamFlags.READWRITE)
        procedure.add_string_argument('light_source', t('pdb_light_source_nick'), t('pdb_light_source_blurb'), 'auto', GObject.ParamFlags.READWRITE)
        procedure.add_int_argument('light_spread', t('pdb_light_spread_nick'), t('pdb_light_spread_blurb'), 5, 100, 45, GObject.ParamFlags.READWRITE)
        procedure.add_boolean_argument('luxus', t('pdb_luxus_nick'), t('pdb_luxus_blurb'), True, GObject.ParamFlags.READWRITE)
        procedure.add_boolean_argument('innen_schimmer', t('pdb_innen_schimmer_nick'), t('pdb_innen_schimmer_blurb'), False, GObject.ParamFlags.READWRITE)
        procedure.add_string_argument('schimmer_seite', t('pdb_schimmer_seite_nick'), t('pdb_schimmer_seite_blurb'), 'auto', GObject.ParamFlags.READWRITE)
        procedure.add_boolean_argument('brushed', t('pdb_brushed_nick'), t('pdb_brushed_blurb'), False, GObject.ParamFlags.READWRITE)
        procedure.add_int_argument('brushed_granularity', t('pdb_brushed_gran_nick'), t('pdb_brushed_gran_blurb'), 1, 100, 38, GObject.ParamFlags.READWRITE)
        procedure.add_int_argument('brushed_angle', t('pdb_brushed_angle_nick'), t('pdb_brushed_angle_blurb'), -1, 360, -1, GObject.ParamFlags.READWRITE)
        procedure.add_int_argument('scratches', t('pdb_scratches_nick'), t('pdb_scratches_blurb'), 0, 100, 0, GObject.ParamFlags.READWRITE)
        procedure.add_int_argument('patina', t('pdb_patina_nick'), t('pdb_patina_blurb'), 0, 100, 0, GObject.ParamFlags.READWRITE)
        procedure.add_string_argument('custom_zones', t('pdb_custom_zones_nick'), t('pdb_custom_zones_blurb'), config.DEFAULT_CUSTOM_DSL, GObject.ParamFlags.READWRITE)
        procedure.add_string_argument('preset_save_name', t('pdb_preset_save_nick'), t('pdb_preset_save_blurb'), '', GObject.ParamFlags.READWRITE)
        procedure.add_int_argument('shape_rotation', t('pdb_shape_rot_nick'), t('pdb_shape_rot_blurb'), -180, 180, 0, GObject.ParamFlags.READWRITE)
        procedure.add_string_argument('shape_pivot', t('pdb_shape_pivot_nick'), t('pdb_shape_pivot_blurb'), 'center', GObject.ParamFlags.READWRITE)
        procedure.add_boolean_argument('rot_repeat', t('pdb_rot_repeat_nick'), t('pdb_rot_repeat_blurb'), False, GObject.ParamFlags.READWRITE)
        procedure.add_int_argument('rot_angle_start', t('pdb_rot_a1_nick'), t('pdb_rot_a1_blurb'), -180, 180, 0, GObject.ParamFlags.READWRITE)
        procedure.add_int_argument('rot_angle_end', t('pdb_rot_a2_nick'), t('pdb_rot_a2_blurb'), -180, 180, 45, GObject.ParamFlags.READWRITE)
        procedure.add_int_argument('rot_angle_step', t('pdb_rot_step_nick'), t('pdb_rot_step_blurb'), 2, 180, 15, GObject.ParamFlags.READWRITE)
        procedure.add_int_argument('rot_cycle_times', t('pdb_rot_cycles_nick'), t('pdb_rot_cycles_blurb'), 1, 4, 1, GObject.ParamFlags.READWRITE)
        procedure.add_int_argument('rot_cycle_until', t('pdb_rot_until_nick'), t('pdb_rot_until_blurb'), -360, 360, 0, GObject.ParamFlags.READWRITE)
        procedure.add_string_argument('rot_fade_mode', t('pdb_rot_fmode_nick'), t('pdb_rot_fmode_blurb'), 'step', GObject.ParamFlags.READWRITE)
        procedure.add_int_argument('rot_fade_steps', t('pdb_rot_fade_nick'), t('pdb_rot_fade_blurb'), 0, 95, 20, GObject.ParamFlags.READWRITE)
        procedure.add_string_argument('surface_organic', t('pdb_surface_organic_nick'), t('pdb_surface_organic_blurb'), '', GObject.ParamFlags.READWRITE)
        procedure.add_int_argument('fur_density', t('pdb_fur_density_nick'), t('pdb_fur_density_blurb'), 1, 100, 72, GObject.ParamFlags.READWRITE)
        procedure.add_int_argument('fur_length', t('pdb_fur_length_nick'), t('pdb_fur_length_blurb'), 1, 100, 61, GObject.ParamFlags.READWRITE)
        procedure.add_string_argument('finish_mode', t('pdb_finish_mode_nick'), t('pdb_finish_mode_blurb'), '', GObject.ParamFlags.READWRITE)
