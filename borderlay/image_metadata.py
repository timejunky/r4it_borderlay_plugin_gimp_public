# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
from __future__ import annotations
import json
from pathlib import Path
from typing import Any
import config
_SETTINGS_PATH = Path.home() / '.borderlay' / 'metadata_settings.json'
_DEFAULTS: dict[str, Any] = {'apply_defaults': True, 'preserve_existing': True, 'copyright': '', 'author': '', 'website': '', 'description': '', 'keywords': ''}

def load_metadata_settings() -> dict[str, Any]:
    data = dict(_DEFAULTS)
    try:
        loaded = json.loads(_SETTINGS_PATH.read_text(encoding='utf-8'))
        if isinstance(loaded, dict):
            for key in _DEFAULTS:
                if key in loaded:
                    if isinstance(_DEFAULTS[key], bool):
                        data[key] = bool(loaded[key])
                    else:
                        data[key] = str(loaded[key] or '')
    except Exception:
        pass
    return data

def save_metadata_settings(settings: dict[str, Any]) -> None:
    clean = dict(_DEFAULTS)
    for key in _DEFAULTS:
        if key in settings:
            if isinstance(_DEFAULTS[key], bool):
                clean[key] = bool(settings[key])
            else:
                clean[key] = str(settings[key] or '').strip()
    _SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    _SETTINGS_PATH.write_text(json.dumps(clean, ensure_ascii=False, indent=2), encoding='utf-8')

def active_tier_name() -> str:
    try:
        from community_beacon import COMMUNITY_EDITION
        if COMMUNITY_EDITION:
            return 'Community'
    except Exception:
        pass
    try:
        from license_product import active_limits, edition_label
        limits = active_limits()
        if limits:
            label = edition_label(limits)
            if label:
                return label
    except Exception:
        pass
    try:
        from licensing_service import LicensingService
        info = LicensingService.get_instance().get_status_info()
        if info.is_active and info.tier_display:
            return str(info.tier_display)
    except Exception:
        pass
    return 'Studio'

def product_meta_stamp() -> str:
    return f'Borderlay Studio {config.PLUGIN_VERSION} ({active_tier_name()})'

def _get_tag(meta: Any, tag: str) -> str:
    try:
        if hasattr(meta, 'try_get_tag_string'):
            val = meta.try_get_tag_string(tag)
        else:
            val = meta.get_tag_string(tag)
        return str(val or '').strip()
    except Exception:
        return ''

def _set_tag(meta: Any, tag: str, value: str, *, preserve: bool) -> None:
    text = str(value or '').strip()
    if not text:
        return
    if preserve and _get_tag(meta, tag):
        return
    try:
        if hasattr(meta, 'try_set_tag_string'):
            meta.try_set_tag_string(tag, text)
        else:
            meta.set_tag_string(tag, text)
    except Exception:
        pass

def _set_keywords(meta: Any, raw_keywords: str, *, preserve: bool) -> None:
    items = [part.strip() for part in str(raw_keywords or '').split(',') if part.strip()]
    if not items:
        return
    for tag in ('Xmp.dc.subject', 'Iptc.Application2.Keywords'):
        try:
            if preserve:
                existing = meta.try_get_tag_multiple(tag) if hasattr(meta, 'try_get_tag_multiple') else meta.get_tag_multiple(tag)
                if existing:
                    continue
            if hasattr(meta, 'try_set_tag_multiple'):
                meta.try_set_tag_multiple(tag, items)
            else:
                meta.set_tag_multiple(tag, items)
        except Exception:
            _set_tag(meta, tag, ', '.join(items), preserve=preserve)

def apply_image_metadata(image: Any) -> bool:
    if image is None:
        return False
    import gi
    gi.require_version('Gimp', '3.0')
    from gi.repository import Gimp
    meta = None
    try:
        meta = image.get_metadata()
    except Exception:
        meta = None
    if meta is None:
        meta = Gimp.Metadata.new()
    if meta is None:
        return False
    stamp = product_meta_stamp()
    _set_tag(meta, 'Exif.Image.Software', stamp, preserve=False)
    _set_tag(meta, 'Xmp.xmp.CreatorTool', stamp, preserve=False)
    settings = load_metadata_settings()
    if settings.get('apply_defaults', True):
        preserve = bool(settings.get('preserve_existing', True))
        c_text = str(settings.get('copyright') or '').strip()
        a_text = str(settings.get('author') or '').strip()
        w_text = str(settings.get('website') or '').strip()
        d_text = str(settings.get('description') or '').strip()
        k_text = str(settings.get('keywords') or '').strip()
        for tag in ('Exif.Image.Copyright', 'Xmp.dc.rights', 'Iptc.Application2.Copyright'):
            _set_tag(meta, tag, c_text, preserve=preserve)
        for tag in ('Exif.Image.Artist', 'Xmp.dc.creator', 'Iptc.Application2.Byline'):
            _set_tag(meta, tag, a_text, preserve=preserve)
        for tag in ('Xmp.xmpRights.WebStatement', 'Xmp.dc.source'):
            _set_tag(meta, tag, w_text, preserve=preserve)
        for tag in ('Exif.Image.ImageDescription', 'Xmp.dc.description', 'Iptc.Application2.Caption'):
            _set_tag(meta, tag, d_text, preserve=preserve)
        _set_keywords(meta, k_text, preserve=preserve)
    image.set_metadata(meta)
    _set_export_comment(image, _export_comment(settings, stamp), preserve=bool(settings.get('preserve_existing', True)))
    return True
_GIMP_STOCK_COMMENTS = {'', 'created with gimp', 'erstellt mit gimp', 'créé avec gimp', 'creado con gimp', 'criado com o gimp', 'creato con gimp', 'gimp ile oluşturuldu', 'gimp で作成'}

def _export_comment(settings: dict[str, Any], stamp: str) -> str:
    lines = [stamp]
    if settings.get('apply_defaults', True):
        for key in ('copyright', 'author', 'website', 'description', 'keywords'):
            text = str(settings.get(key) or '').strip()
            if text:
                lines.append(text)
    return '\n'.join(lines)

def _read_comment(image: Any) -> str:
    try:
        parasite = image.get_parasite('gimp-comment')
    except Exception:
        return ''
    if parasite is None:
        return ''
    try:
        data = parasite.get_data()
    except Exception:
        return ''
    if isinstance(data, (bytes, bytearray)):
        return bytes(data).decode('utf-8', errors='replace').strip('\x00').strip()
    return str(data or '').strip('\x00').strip()

def _set_export_comment(image: Any, text: str, *, preserve: bool) -> None:
    existing = _read_comment(image)
    stock = existing.strip().lower() in _GIMP_STOCK_COMMENTS
    ours = existing.startswith('Borderlay Studio ')
    if preserve and existing and (not stock) and (not ours):
        return
    import gi
    gi.require_version('Gimp', '3.0')
    from gi.repository import Gimp
    flags_enum = getattr(Gimp, 'ParasiteFlags', None)
    flags = int(getattr(flags_enum, 'PERSISTENT', 1) if flags_enum is not None else 1)
    for payload in (text.encode('utf-8'), text):
        try:
            image.attach_parasite(Gimp.Parasite.new('gimp-comment', flags, payload))
            return
        except Exception:
            continue
