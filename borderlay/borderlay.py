#!/usr/bin/env python3
# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import sys
import traceback
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import GLib, Gimp
import config
from locales.i18n import t
from pdb_schema import PdbSchemaRegistrar
from shapes import set_active_shape_mode
PROC_RECTANGULAR = config.PLUGIN_NAME
PROC_SHAPES = 'python-fu-borderlay-shapes'
PROC_PATHS = 'python-fu-borderlay-paths'
PROC_CIRCULAR = 'python-fu-borderlay-circular'
PROC_FREEFORM = 'python-fu-borderlay-freeform'
PROC_HELP = 'python-fu-borderlay-help'
PROC_LICENSE = 'python-fu-borderlay-license'
PROC_ABOUT = 'python-fu-borderlay-about'
PROC_SETTINGS = 'python-fu-borderlay-settings'
MENU_STUDIO_PATH = '<Image>/Borderlay Studio'

class BorderlayPlugin(Gimp.PlugIn):

    def do_query_procedures(self):
        return [PROC_RECTANGULAR, PROC_HELP, PROC_LICENSE, PROC_ABOUT, PROC_SETTINGS]

    def do_set_i18n(self, name):
        return False

    @staticmethod
    def _sanitize_interactive_config(cfg):
        try:
            if int(cfg.get_property('relief')) < 20:
                cfg.set_property('relief', 96)
            if int(cfg.get_property('fasenkontrast')) < 20:
                cfg.set_property('fasenkontrast', 84)
            if int(cfg.get_property('profil_hoehe')) < 20:
                cfg.set_property('profil_hoehe', 90)
            if int(cfg.get_property('profil_tiefe')) < 20:
                cfg.set_property('profil_tiefe', 92)
            shim_side = str(cfg.get_property('schimmer_seite') or 'auto')
            if shim_side in ('innen', 'aussen'):
                cfg.set_property('schimmer_seite', 'auto')
        except Exception:
            pass

    def do_create_procedure(self, name):
        if name in (PROC_HELP, PROC_LICENSE, PROC_ABOUT, PROC_SETTINGS):
            proc = Gimp.ImageProcedure.new(self, name, Gimp.PDBProcType.PLUGIN, self.run_info_dialog, name)
            proc.set_image_types('*')
            proc.set_sensitivity_mask(Gimp.ProcedureSensitivityMask.ALWAYS)
            if name == PROC_HELP:
                proc.set_menu_label(t('menu_help'))
                short_tip = t('doc_short_help')
            elif name == PROC_LICENSE:
                proc.set_menu_label(t('menu_license'))
                short_tip = t('doc_short_license')
            elif name == PROC_SETTINGS:
                proc.set_menu_label(t('menu_settings'))
                short_tip = t('doc_short_settings')
            else:
                proc.set_menu_label(t('menu_about'))
                short_tip = t('doc_short_about')
            proc.set_documentation(short_tip, None, None)
            proc.add_menu_path(MENU_STUDIO_PATH)
            proc.set_attribution(t('attr_author'), t('attr_copyright'), config.COPYRIGHT_YEAR)
            return proc
        procedure = Gimp.ImageProcedure.new(self, name, Gimp.PDBProcType.PLUGIN, self.run, name)
        procedure.set_image_types('RGB*')
        procedure.set_sensitivity_mask(Gimp.ProcedureSensitivityMask.DRAWABLE | Gimp.ProcedureSensitivityMask.DRAWABLES | Gimp.ProcedureSensitivityMask.NO_DRAWABLES)
        procedure.set_menu_label(t('menu_rect'))
        short_doc = t('doc_short_rect')
        procedure.add_menu_path(MENU_STUDIO_PATH)
        procedure.set_documentation(short_doc, None, None)
        procedure.set_attribution(t('attr_author'), t('attr_copyright'), config.COPYRIGHT_YEAR)
        PdbSchemaRegistrar.register_arguments(procedure)
        return procedure

    def run_info_dialog(self, procedure, run_mode, _image, _drawables, _config_obj, proc_name):
        if run_mode == Gimp.RunMode.INTERACTIVE:
            from gui.studio_dialogs import StudioInfoDialogs
            if proc_name == PROC_HELP:
                try:
                    self.persistent_enable()
                except Exception:
                    pass
                help_dlg = StudioInfoDialogs.show_help_dialog(self)
                context = GLib.MainContext.default()
                while help_dlg is not None:
                    try:
                        if not help_dlg.get_visible():
                            break
                    except Exception:
                        break
                    while context.pending():
                        context.iteration(False)
                    self.persistent_process(50)
            elif proc_name == PROC_LICENSE:
                StudioInfoDialogs.show_license_dialog()
            elif proc_name == PROC_SETTINGS:
                StudioInfoDialogs.show_metadata_settings_dialog()
            else:
                StudioInfoDialogs.show_about_dialog()
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, None)

    def run(self, procedure, run_mode, image, drawables, config_obj, proc_name):
        from cache_guard import CacheGuard
        from engine import BorderlayEngine
        try:
            from license_product import active_limits, clamp_procedure_config
            from locales.i18n import t
            try:
                from community_beacon import report_community_download
                from config import PLUGIN_VERSION
                report_community_download(version=PLUGIN_VERSION, interactive=run_mode == Gimp.RunMode.INTERACTIVE)
            except Exception:
                pass
            from community_material_seal import apply_community_materials
            apply_community_materials()
            CacheGuard.trigger_domain('pdb_schema', reload_memory=True)
            if run_mode == Gimp.RunMode.INTERACTIVE:
                from license_product import require_paid_license
                if not require_paid_license():
                    return procedure.new_return_values(Gimp.PDBStatusType.CANCEL, None)
            limits = active_limits()
            set_active_shape_mode('rectangular')
            clamp_procedure_config(config_obj)
            if run_mode == Gimp.RunMode.INTERACTIVE:
                self._sanitize_interactive_config(config_obj)
                from gui import BorderlayGUI
                gui = BorderlayGUI(procedure, image, drawables, config_obj)
                if not gui.show():
                    return procedure.new_return_values(Gimp.PDBStatusType.CANCEL, None)
                try:
                    current_selected = image.get_selected_layers()
                    if current_selected:
                        drawables = current_selected
                except Exception:
                    pass
            moved = clamp_procedure_config(config_obj)
            if moved and run_mode == Gimp.RunMode.INTERACTIVE:
                Gimp.message(t('license_preview_only'))
            engine = BorderlayEngine(image, drawables, config_obj)
            engine.run()
            return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, None)
        except Exception as exc:
            tb_str = traceback.format_exc()
            Gimp.message(f'Borderlay Ausführungsfehler: {exc}\n{tb_str}')
            return procedure.new_return_values(Gimp.PDBStatusType.CANCEL, None)
if __name__ == '__main__':
    Gimp.main(BorderlayPlugin.__gtype__, sys.argv)
