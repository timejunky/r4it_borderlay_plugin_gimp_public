# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
from __future__ import annotations
import logging
import os
import sys
from pathlib import Path
_m0062 = logging.getLogger(__name__)
_m0016 = False
_m0018 = None

def _m0084() -> Path:
    return Path(__file__).resolve().parents[1]

def _m0065() -> list[Path]:
    _m0225 = (os.environ.get('R4IT_MGPY_SRC') or '').strip()
    _m0145 = Path(__file__).resolve().parent / '_vendor'
    _m0512 = [_m0145, Path(_m0225) if _m0225 else None, _m0084().parent / 'r4it_manifest_guard_py' / 'src', _m0084().parent.parent / 'r4it_manifest_guard_py' / 'src']
    out: list[Path] = []
    for root in _m0512:
        if root is None:
            continue
        client = root / 'manifestguard' / 'licensing' / 'client.py'
        if client.is_file():
            out.append(root.resolve())
    return out

def _m0224() -> bool:
    global _m0016
    try:
        import manifestguard.licensing.client
        return True
    except ImportError:
        pass
    for src in _m0065():
        _m0562 = str(src)
        if _m0562 not in sys.path:
            sys.path.insert(0, _m0562)
        try:
            import importlib
            for mod in list(sys.modules):
                if mod == 'manifestguard' or mod.startswith('manifestguard.'):
                    del sys.modules[mod]
            importlib.import_module('manifestguard.licensing.client')
            _m0016 = True
            _m0062.debug('mgpy licensing loaded from %s', src)
            return True
        except ImportError as exc:
            _m0062.debug('mgpy licensing import failed for %s: %s', src, exc)
            continue
    return False

def _m0270():
    global _m0018
    if _m0018 is not None:
        return _m0018
    if not _m0224():
        return None
    try:
        from manifestguard.licensing.client import LicensingClient
        from license_product import configure_borderlay_licensing_client
        client = getattr(LicensingClient, 'get_instance')()
        configure_borderlay_licensing_client(client)
        _m0018 = client
        return client
    except Exception as exc:
        _m0062.debug('LicensingClient unavailable: %s', exc)
        return None

def _m0349() -> str:
    from locales.i18n import t
    return t('license_client_unavailable')
