# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
from __future__ import annotations
import json
import os
import platform
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any, Callable
COMMUNITY_EDITION = True
APP_ID = 'alv_prd_borderlay_public'
TRACK_URL = 'https://login.alveos.eu/api/v1/track'
SKIP_ENV = 'BORDERLAY_SKIP_ALVEOS_BEACON'
ACCEPT_ENV = 'BORDERLAY_BEACON_ACCEPT'
CONSENT_DEFAULT_ACCEPT = True

def _home(home: Path | None) -> Path:
    return home if home is not None else Path.home()

def _stamp_path(home: Path) -> Path:
    return home / '.borderlay' / 'community-beacon.json'

def _read_stamp(home: Path) -> dict[str, Any]:
    path = _stamp_path(home)
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}

def _write_stamp(home: Path, stamp: dict[str, Any]) -> None:
    path = _stamp_path(home)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(stamp, indent=2) + '\n', encoding='utf-8')

def _truthy(name: str) -> bool:
    return str(os.environ.get(name) or '').strip().lower() in {'1', 'true', 'yes'}

def _ask_beacon_consent() -> bool:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    try:
        gi.require_version('GimpUi', '3.0')
        from gi.repository import GimpUi
        GimpUi.init('borderlay')
    except (ValueError, ImportError):
        pass
    from locales.i18n import t
    dialog = Gtk.MessageDialog(modal=True, message_type=Gtk.MessageType.QUESTION, buttons=Gtk.ButtonsType.NONE, text=t('beacon_consent_title'))
    dialog.format_secondary_text(t('beacon_consent_body'))
    dialog.add_button(t('beacon_consent_no'), Gtk.ResponseType.CANCEL)
    dialog.add_button(t('beacon_consent_yes'), Gtk.ResponseType.OK)
    dialog.set_default_response(Gtk.ResponseType.OK if CONSENT_DEFAULT_ACCEPT else Gtk.ResponseType.CANCEL)
    try:
        response = dialog.run()
    finally:
        dialog.destroy()
    return response == Gtk.ResponseType.OK

def _store_consent(root: Path, stamp: dict[str, Any], agreed: bool) -> bool:
    stamp['consented'] = agreed
    try:
        _write_stamp(root, stamp)
    except OSError:
        return False
    return True

def _resolve_consent(root: Path, stamp: dict[str, Any], *, interactive: bool, ask: Callable[[], bool] | None) -> dict[str, Any] | None:
    if _truthy(ACCEPT_ENV):
        if not _store_consent(root, stamp, True):
            return {'ok': True, 'skipped': True, 'reason': 'no_consent'}
        return None
    if stamp.get('consented') is True:
        return None
    if stamp.get('consented') is False:
        return {'ok': True, 'skipped': True, 'reason': 'refused'}
    if not interactive:
        return {'ok': True, 'skipped': True, 'reason': 'no_consent'}
    prompter = ask if ask is not None else _ask_beacon_consent
    try:
        agreed = bool(prompter())
    except Exception:
        return {'ok': True, 'skipped': True, 'reason': 'no_consent'}
    if not _store_consent(root, stamp, agreed):
        return {'ok': True, 'skipped': True, 'reason': 'refused' if not agreed else 'no_consent'}
    if not agreed:
        return {'ok': True, 'skipped': True, 'reason': 'refused'}
    return None

def report_community_download(*, version: str='1.2.3', home: Path | None=None, opener: Any=None, timeout_sec: float=1.5, interactive: bool=False, ask: Callable[[], bool] | None=None) -> dict[str, Any]:
    if not COMMUNITY_EDITION:
        return {'ok': True, 'skipped': True, 'reason': 'private_tree'}
    if _truthy(SKIP_ENV):
        return {'ok': True, 'skipped': True, 'reason': 'skip'}
    root = _home(home)
    stamp = _read_stamp(root)
    skipped = _resolve_consent(root, stamp, interactive=interactive, ask=ask)
    if skipped is not None:
        return skipped
    if stamp.get('install_reported') and stamp.get('version') == version:
        return {'ok': True, 'skipped': True, 'reason': 'already_reported'}
    instance = str(stamp.get('instance_id') or '')
    if len(instance) < 32:
        instance = uuid.uuid4().hex
    event = 'update' if stamp.get('install_reported') else 'install'
    body = {'app_id': APP_ID, 'instance_id': instance, 'event': event, 'version': version, 'client_type': 'gimp', 'platform': platform.system().lower()}
    payload = json.dumps(body).encode('utf-8')
    request = urllib.request.Request(TRACK_URL, data=payload, method='POST', headers={'Content-Type': 'application/json', 'Accept': 'application/json', 'User-Agent': f'BorderlayBeacon/{version}'})
    fetch = opener if opener is not None else urllib.request.urlopen
    try:
        with fetch(request, timeout=timeout_sec) as response:
            status = int(getattr(response, 'status', 200) or 200)
    except (urllib.error.URLError, OSError, TimeoutError):
        return {'ok': True, 'skipped': True, 'reason': 'fail_open', 'event': event}
    if status not in {200, 202}:
        return {'ok': True, 'skipped': True, 'reason': 'fail_open', 'status': status}
    stamp.update({'instance_id': instance, 'install_reported': True, 'version': version})
    try:
        _write_stamp(root, stamp)
    except OSError:
        pass
    return {'ok': True, 'skipped': False, 'event': event, 'status': status}

def report_community_uninstall(*, version: str='', home: Path | None=None, opener: Any=None, timeout_sec: float=1.5) -> dict[str, Any]:
    if not COMMUNITY_EDITION:
        return {'ok': True, 'skipped': True, 'reason': 'private_tree'}
    if _truthy(SKIP_ENV):
        return {'ok': True, 'skipped': True, 'reason': 'skip'}
    root = _home(home)
    stamp = _read_stamp(root)
    if stamp.get('consented') is not True:
        reason = 'refused' if stamp.get('consented') is False else 'no_consent'
        return {'ok': True, 'skipped': True, 'reason': reason}
    if stamp.get('uninstall_reported'):
        return {'ok': True, 'skipped': True, 'reason': 'already_reported'}
    instance = str(stamp.get('instance_id') or '')
    if len(instance) < 32:
        return {'ok': True, 'skipped': True, 'reason': 'no_instance'}
    current = version or str(stamp.get('version') or '1.2.3')
    body = {'app_id': APP_ID, 'instance_id': instance, 'event': 'uninstall', 'version': current, 'client_type': 'gimp', 'platform': platform.system().lower()}
    payload = json.dumps(body).encode('utf-8')
    request = urllib.request.Request(TRACK_URL, data=payload, method='POST', headers={'Content-Type': 'application/json', 'Accept': 'application/json', 'User-Agent': f'BorderlayBeacon/{current}'})
    fetch = opener if opener is not None else urllib.request.urlopen
    try:
        with fetch(request, timeout=timeout_sec) as response:
            status = int(getattr(response, 'status', 200) or 200)
    except (urllib.error.URLError, OSError, TimeoutError):
        return {'ok': True, 'skipped': True, 'reason': 'fail_open', 'event': 'uninstall'}
    if status not in {200, 202}:
        return {'ok': True, 'skipped': True, 'reason': 'fail_open', 'status': status}
    stamp['uninstall_reported'] = True
    stamp['install_reported'] = False
    try:
        _write_stamp(root, stamp)
    except OSError:
        pass
    return {'ok': True, 'skipped': False, 'event': 'uninstall', 'status': status}
