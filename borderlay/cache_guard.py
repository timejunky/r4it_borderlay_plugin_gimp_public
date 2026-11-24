#!/usr/bin/env python3
# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import argparse
import os
import time
from pathlib import Path
from cache_lock import AtomicStateStore, _DomainLock
from cache_ops import CacheOperations

class CacheGuard:
    DOMAINS = {'pdb_schema': ('config.catalog_metals', 'config.catalog_organic', 'config.catalog_atelier', 'config.materials', 'init_zones', 'config', 'pdb_schema', 'borderlay'), 'zones': ('fx.zones_lighting', 'fx.zones_slopes', 'fx.zones_miter', 'fx.zones'), 'bevel': ('fx.gradmap', 'fx.metal', 'fx.bevel_center', 'fx.bevel_seams', 'fx.bevel'), 'lighting': ('fx.light_shapes', 'fx.light_rims', 'fx.light', 'fx.bloom', 'fx.shimmer'), 'textures': ('fx.patina', 'fx.organic', 'fx.texture'), 'glass': ('fx.gradmap', 'fx.glass_facets', 'fx.glass_optics', 'fx.glass'), 'gui': ('help_texts', 'gui.help_visuals', 'gui.studio_dialogs', 'gui.preview_gtk', 'gui.preview_wireframe', 'gui.canvas_preview', 'gui.color_picker', 'gui.profile_plot', 'gui.profile_selector', 'gui.corner_radii', 'gui.shape_rotation', 'gui.geometry_panel', 'gui.swatch_renderer', 'gui.light_vector', 'gui.lighting_tab', 'gui.materials', 'gui.swatch_textures', 'gui.swatch_renderer', 'gui.swatch_hover', 'gui.light_vector', 'gui.swatches', 'license_product', 'licensing_service', 'community_beacon', 'gui.simple_finish', 'gui.simple_modes', 'gui')}

    @staticmethod
    def get_plugin_dir() -> Path:
        return Path(__file__).resolve().parent

    @staticmethod
    def get_gimp_user_dir() -> Path:
        import sys
        if sys.platform == 'win32':
            base = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming')) / 'GIMP'
        elif sys.platform == 'darwin':
            base = Path.home() / 'Library' / 'Application Support' / 'GIMP'
        else:
            xdg = os.environ.get('XDG_CONFIG_HOME')
            base = (Path(xdg) if xdg else Path.home() / '.config') / 'GIMP'
        for ver in ('3.2', '3.0'):
            candidate = base / ver
            if candidate.is_dir():
                return candidate
        return base / '3.2'

    @classmethod
    def get_installed_plugin_dir(cls) -> Path:
        return cls.get_gimp_user_dir() / 'plug-ins' / 'borderlay'

    @classmethod
    def _every_plugin_module(cls) -> tuple:
        seen = []
        for mods in cls.DOMAINS.values():
            for name in mods:
                if name not in seen:
                    seen.append(name)
        for core_mod in ('utils', 'selection', 'engine', 'engine_params', 'engine_pipeline', 'gui.light_vector', 'gui.materials', 'gui.swatches', 'gui.simple_modes', 'gui', 'cache_lock', 'cache_ops', 'cache_guard'):
            if core_mod not in seen:
                seen.append(core_mod)
        plugin = cls.get_plugin_dir()
        for py_path in sorted(plugin.rglob('*.py')):
            rel = py_path.relative_to(plugin)
            if any((part.startswith(('.', '__')) for part in rel.parts)):
                continue
            if py_path.name == '__init__.py':
                name = '.'.join(rel.parts[:-1])
            else:
                name = '.'.join(rel.with_suffix('').parts)
            if name and name not in seen and (not name.startswith('_')):
                seen.append(name)
        return tuple(seen)

    @classmethod
    def _modules_from_names(cls, domain_or_modules) -> tuple:
        resolved = []
        for item in domain_or_modules:
            name = str(item).strip()
            if name in cls.DOMAINS:
                for module_name in cls.DOMAINS[name]:
                    if module_name not in resolved:
                        resolved.append(module_name)
            else:
                clean = name.removesuffix('.py')
                if clean not in resolved:
                    resolved.append(clean)
        return tuple(resolved)

    @classmethod
    def _resolve_modules(cls, domain_or_modules) -> tuple:
        if isinstance(domain_or_modules, str):
            key = domain_or_modules.strip().lower()
            if key == 'all':
                return cls._every_plugin_module()
            if key in cls.DOMAINS:
                return cls.DOMAINS[key]
            return (key.removesuffix('.py'),)
        return cls._modules_from_names(domain_or_modules)

    @classmethod
    def _changed_modules_in_dir(cls, directory, modules, force, pluginrc_incomplete, domain_tag) -> list:
        state_file = directory / '.borderlay_domain_hashes.json'
        state = AtomicStateStore.read_state(state_file)
        mod_hashes = state.get('module_hashes', {})
        changed_in_dir = []
        for mod_name in modules:
            cur_h = CacheOperations.compute_modules_hash(directory, (mod_name,))
            old_h = mod_hashes.get(mod_name, '')
            needs_pdb_touch = mod_name == 'borderlay' and pluginrc_incomplete
            if force or cur_h != old_h or needs_pdb_touch:
                changed_in_dir.append(mod_name)
                mod_hashes[mod_name] = cur_h
        if not changed_in_dir:
            return []
        CacheOperations.purge_module_pyc(directory, tuple(changed_in_dir))
        if 'borderlay' in changed_in_dir or 'config.materials' in changed_in_dir or 'init_zones' in changed_in_dir:
            CacheOperations.touch_pdb_entrypoint(directory)
            mod_hashes['borderlay'] = CacheOperations.compute_modules_hash(directory, ('borderlay',))
        state['module_hashes'] = mod_hashes
        state['last_domain'] = domain_tag
        state['updated_at'] = time.time()
        AtomicStateStore.write_state_atomic(state_file, state)
        return changed_in_dir

    @classmethod
    def trigger_domain(cls, domain_or_modules, sync_files: bool=False, reload_memory: bool=True, force: bool=False) -> list:
        modules = cls._resolve_modules(domain_or_modules)
        if not modules:
            return []
        domain_tag = domain_or_modules if isinstance(domain_or_modules, str) else '_'.join(modules[:2])
        src_dir = cls.get_plugin_dir()
        inst_dir = cls.get_installed_plugin_dir()
        lock_dir = inst_dir if inst_dir.exists() else src_dir
        lock_file = lock_dir / f'.cache_lock_{domain_tag}.lock'
        invalidated_modules = []
        with _DomainLock(lock_file) as acquired:
            if not acquired:
                return []
            if sync_files:
                CacheOperations.sync_domain_files(src_dir, inst_dir, modules, force=force)
            target_dirs = [src_dir]
            if inst_dir.is_dir() and inst_dir != src_dir:
                target_dirs.append(inst_dir)
            is_pdb_domain = 'borderlay' in modules or 'config.materials' in modules
            pluginrc_incomplete = CacheOperations.is_pluginrc_missing_materials(cls.get_gimp_user_dir(), src_dir) if is_pdb_domain else False
            for directory in target_dirs:
                changed_in_dir = cls._changed_modules_in_dir(directory, modules, force, pluginrc_incomplete, domain_tag)
                for module_name in changed_in_dir:
                    if module_name not in invalidated_modules:
                        invalidated_modules.append(module_name)
            if reload_memory and invalidated_modules:
                CacheOperations.reload_in_memory_modules(tuple(invalidated_modules))
        return invalidated_modules

def main():
    parser = argparse.ArgumentParser(description='Borderlay Partial Domain CacheGuard')
    parser.add_argument('--domain', default='all', help="Domäne ('pdb_schema', 'zones', 'bevel', 'lighting', 'textures', 'glass', 'gui', 'all') oder Modulname")
    parser.add_argument('--sync', action='store_true', help='Synchronisiert die Domänen-Dateien nach %APPDATA%')
    parser.add_argument('--force', action='store_true', help='Erzwingt die Invalidierung der gewählten Domäne')
    args = parser.parse_args()
    updated = CacheGuard.trigger_domain(args.domain, sync_files=args.sync, reload_memory=False, force=args.force)
    if updated:
        print(f"CacheGuard [{args.domain}]: Partiell invalidiert -> {', '.join(updated)}")
if __name__ == '__main__':
    main()
