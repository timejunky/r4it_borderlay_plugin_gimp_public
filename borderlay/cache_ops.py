# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import hashlib
import importlib
import os
import shutil
import sys
import time
from pathlib import Path

class CacheOperations:

    @staticmethod
    def module_file(directory: Path, mod_name: str) -> Path | None:
        parts = str(mod_name).split('.')
        direct = directory.joinpath(*parts).with_suffix('.py')
        packaged = directory.joinpath(*parts, '__init__.py')
        if direct.is_file():
            return direct
        if packaged.is_file():
            return packaged
        return None

    @staticmethod
    def compute_modules_hash(directory: Path, module_names: tuple) -> str:
        hasher = hashlib.sha256()
        for mod_name in sorted(module_names):
            py_file = CacheOperations.module_file(directory, mod_name)
            if py_file is not None:
                hasher.update(mod_name.encode('utf-8'))
                try:
                    hasher.update(py_file.read_bytes())
                except OSError:
                    pass
        return hasher.hexdigest()

    @staticmethod
    def purge_module_pyc(directory: Path, module_names: tuple) -> int:
        removed = 0
        for mod_name in module_names:
            py_file = CacheOperations.module_file(directory, mod_name)
            if py_file is None:
                continue
            cache_dir = py_file.parent / '__pycache__'
            if not cache_dir.is_dir():
                continue
            for pyc_file in cache_dir.glob(f'{py_file.stem}.*.pyc'):
                try:
                    pyc_file.unlink()
                    removed += 1
                except OSError:
                    pass
        return removed

    @staticmethod
    def sync_domain_files(src_dir: Path, dst_dir: Path, module_names: tuple, force: bool=False) -> list:
        synced = []
        if not src_dir.is_dir() or src_dir.resolve() == dst_dir.resolve():
            return synced
        dst_dir.mkdir(parents=True, exist_ok=True)
        for mod_name in module_names:
            src_file = CacheOperations.module_file(src_dir, mod_name)
            if src_file is None:
                continue
            dst_file = dst_dir / src_file.relative_to(src_dir)
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            need_copy = force or not dst_file.is_file()
            if not need_copy:
                try:
                    src_bytes = src_file.read_bytes()
                    dst_bytes = dst_file.read_bytes()
                    need_copy = src_bytes != dst_bytes
                except OSError:
                    need_copy = True
            if need_copy:
                shutil.copy2(src_file, dst_file)
                synced.append(mod_name)
        return synced

    @staticmethod
    def reload_in_memory_modules(module_names: tuple) -> list:
        reloaded = []
        importlib.invalidate_caches()
        for mod_name in module_names:
            if mod_name == 'borderlay':
                continue
            mod_obj = sys.modules.get(mod_name)
            if mod_obj is not None:
                try:
                    importlib.reload(mod_obj)
                    reloaded.append(mod_name)
                except Exception:
                    pass
        return reloaded

    @staticmethod
    def touch_pdb_entrypoint(directory: Path):
        entry = directory / 'borderlay.py'
        if entry.is_file():
            now = time.time() + 1.0
            try:
                os.utime(entry, (now, now))
            except OSError:
                pass

    @staticmethod
    def is_pluginrc_missing_materials(gimp_user_dir: Path, src_dir: Path) -> bool:
        pluginrc = gimp_user_dir / 'pluginrc'
        if not pluginrc.is_file():
            return False
        try:
            text = pluginrc.read_text(encoding='utf-8', errors='ignore')
            try:
                from community_beacon import COMMUNITY_EDITION
            except Exception:
                COMMUNITY_EDITION = False
            if COMMUNITY_EDITION:
                return 'python-fu-borderlay-settings' not in text or '<Image>/Filters/Borderlay Studio' in text
            from locales.i18n import t
            return 'cherry_wood' not in text or 'light_source' not in text or 'rot_fade_mode' not in text or ('rot_cycle_times' not in text) or ('python-fu-borderlay-shapes' not in text) or ('python-fu-borderlay-paths' not in text) or ('python-fu-borderlay-settings' not in text) or ('<Image>/Filters/Borderlay Studio' in text) or (t('menu_shapes') not in text)
        except OSError:
            return False
