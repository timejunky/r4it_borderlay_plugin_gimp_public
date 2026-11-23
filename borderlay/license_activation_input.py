# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

def _read_if_path(value: str) -> str:
    candidate = Path(value)
    if not candidate.is_file():
        return value
    try:
        return candidate.read_text(encoding='utf-8').strip()
    except Exception:
        return value

def _looks_like_activation(data: dict[str, Any]) -> bool:
    return bool(data.get('activation_key') or data.get('token') or data.get('updateEntitlementUntil') or data.get('licenseId'))

def parse_activation_input(raw: str) -> tuple[str, str | dict[str, Any]]:
    value = str(raw or '').strip()
    if not value:
        return ('token', '')
    value = _read_if_path(value)
    if not value.startswith('{'):
        return ('token', value)
    try:
        data = json.loads(value)
    except Exception:
        return ('token', value)
    if isinstance(data, dict) and _looks_like_activation(data):
        return ('activation', data)
    return ('token', value)
