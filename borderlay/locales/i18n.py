# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
from __future__ import annotations
import importlib
import json
import os
from pathlib import Path
from locales import de, en
SUPPORTED_LANGUAGES: tuple[tuple[str, str], ...] = (('de', 'DE — Deutsch'), ('en', 'EN — English'), ('fr', 'FR — Français'), ('lb', 'LB — Lëtzebuergesch'), ('es', 'ES — Español'), ('it', 'IT — Italiano'), ('pt', 'PT — Português'), ('tr', 'TR — Türkçe'), ('ja', 'JA — 日本語'))
_LANG_CODES = {code for code, _label in SUPPORTED_LANGUAGES}
_LANG_STATE = Path.home() / '.borderlay' / 'language.json'
_MODULES: dict[str, object] = {'de': de, 'en': en}

def normalize_lang(code: str | None) -> str:
    raw = str(code or '').strip().lower().replace('-', '_')
    if not raw:
        return ''
    short = raw.split('_')[0].split('.')[0]
    if short in _LANG_CODES:
        return short
    return ''

def _load_saved_lang() -> str:
    try:
        data = json.loads(_LANG_STATE.read_text(encoding='utf-8'))
        if isinstance(data, dict):
            return normalize_lang(data.get('language'))
    except Exception:
        pass
    return ''

def _save_lang(code: str) -> None:
    try:
        _LANG_STATE.parent.mkdir(parents=True, exist_ok=True)
        _LANG_STATE.write_text(json.dumps({'language': code}), encoding='utf-8')
    except Exception:
        pass

def _detect_initial_lang() -> str:
    saved = _load_saved_lang()
    if saved:
        return saved
    for var in ('BORDERLAY_LANG', 'LANGUAGE', 'LC_ALL', 'LANG'):
        norm = normalize_lang(os.environ.get(var))
        if norm:
            return norm
    return 'de'
_ACTIVE_LANG = _detect_initial_lang()

def _lang_module(lang_code: str):
    code = normalize_lang(lang_code) or 'de'
    if code in _MODULES:
        return _MODULES[code]
    try:
        mod = importlib.import_module(f'locales.{code}')
        _MODULES[code] = mod
        return mod
    except Exception:
        return de

def set_language(lang_code: str, persist: bool=True):
    global _ACTIVE_LANG
    _ACTIVE_LANG = normalize_lang(lang_code) or 'de'
    if persist:
        _save_lang(_ACTIVE_LANG)

def get_language() -> str:
    return _ACTIVE_LANG

def t(key: str, default: str='', **kwargs) -> str:
    mod = _lang_module(_ACTIVE_LANG)
    table = getattr(mod, 'STRINGS', de.STRINGS)
    val = table.get(key)
    if val is None:
        val = en.STRINGS.get(key, de.STRINGS.get(key, default or key))
    if kwargs:
        try:
            return val.format(**kwargs)
        except Exception:
            return val
    return val

def t_help(topic_key: str) -> dict:
    mod = _lang_module(_ACTIVE_LANG)
    table = getattr(mod, 'HELP_TOPICS', de.HELP_TOPICS)
    fallback = {'title': 'Information', 'short': t('help_click_hint'), 'detail': ''}
    return table.get(topic_key, en.HELP_TOPICS.get(topic_key, de.HELP_TOPICS.get(topic_key, fallback)))

def get_all_help_topics() -> dict:
    mod = _lang_module(_ACTIVE_LANG)
    return getattr(mod, 'HELP_TOPICS', de.HELP_TOPICS)
