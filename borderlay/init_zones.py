# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import json
import os
USER_PRESETS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_presets.json')
VALID_SHAPES = ('bevel_out', 'groove', 'flat', 'step', 'bevel_in', 'pipe')
SHAPE_ALIASES = {'slope_up': 'bevel_out', 'valley': 'groove', 'plateau': 'flat', 'terrace': 'step', 'slope_down': 'bevel_in', 'torus': 'pipe'}
DEFAULT_Z_VALUES = {'bevel_out': 64.0, 'groove': 12.0, 'flat': 100.0, 'step': 78.0, 'bevel_in': 26.0, 'pipe': 96.0}
BUILTIN_PATTERNS = {'stamped_plate': '19:bevel_out:64:main:round;5.5:groove:12:shadow:round;32.5:flat:100:main:round;5.5:groove:10:shadow:round;21:step:82:main:round;16.5:bevel_in:26:main:round'}
DEFAULT_CUSTOM_DSL = BUILTIN_PATTERNS['stamped_plate']
PROFILE_LABELS = {'stamped_plate': 'a) Geprägte Stempelplatte (Weiche Radien)'}
CENTER_MODES = {'transparent': 'Freies Bildfeld (Border)', 'plate': 'Durchgehende Metall-/Glasplatte (Plate)', 'inlay_well': 'Eingelassenes Inlay-Farbfeld (Inlay Well)'}

def load_user_presets() -> dict:
    if not os.path.isfile(USER_PRESETS_FILE):
        return {}
    try:
        with open(USER_PRESETS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict):
                return {str(k): str(v) for k, v in data.items() if isinstance(k, str) and isinstance(v, str)}
    except Exception:
        pass
    return {}

def save_user_preset(name: str, _m0184: str):
    _m0149 = (name or '').strip()
    if not _m0149 or not _m0184:
        return
    _m0413 = load_user_presets()
    _m0413[_m0149] = _m0184.strip()
    try:
        with open(USER_PRESETS_FILE, 'w', encoding='utf-8') as f:
            json.dump(_m0413, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def build_zone_token(_m0496, kind, z=None, mat='main', _m0158='auto') -> str:
    _m0148 = SHAPE_ALIASES.get(str(kind).strip().lower(), str(kind).strip().lower())
    if _m0148 not in VALID_SHAPES:
        _m0148 = 'flat'
    _m0197 = DEFAULT_Z_VALUES[_m0148] if z is None else float(z)
    _m0197 = max(0.0, min(100.0, _m0197))
    _m0194 = max(0.5, float(_m0496))
    return f"{_m0194:.1f}:{_m0148}:{_m0197:.0f}:{str(mat or 'main').strip().lower()}:{str(_m0158 or 'auto').strip().lower()}"

def build_dsl_from_specs(_m0570: list) -> str:
    _m0542 = []
    for sp in _m0570:
        if not isinstance(sp, dict):
            continue
        _m0542.append(build_zone_token(sp.get('share', 20.0), sp.get('kind', 'flat'), sp.get('z', None), sp.get('mat', 'main'), sp.get('corner', 'auto')))
    return ';'.join(_m0542) if _m0542 else DEFAULT_CUSTOM_DSL

def create_parametric_profile(_m0378=20.0, _m0408=40.0, _m0297=20.0, _m0288=20.0, _m0556=True) -> str:
    if not _m0556:
        return build_dsl_from_specs([{'share': _m0378, 'kind': 'bevel_out'}, {'share': _m0408 + _m0297, 'kind': 'flat'}, {'share': _m0288, 'kind': 'bevel_in'}])
    return build_dsl_from_specs([{'share': _m0378, 'kind': 'bevel_out'}, {'share': 5.5, 'kind': 'groove', 'mat': 'shadow'}, {'share': _m0408, 'kind': 'flat'}, {'share': 5.5, 'kind': 'groove', 'mat': 'shadow'}, {'share': _m0297, 'kind': 'step'}, {'share': _m0288, 'kind': 'bevel_in'}])

def _m0069(_m0412: str, custom_dsl: str) -> str:
    p_key = (_m0412 or 'stamped_plate').strip()
    _m0546 = load_user_presets()
    if p_key == 'custom' and (custom_dsl or '').strip():
        return custom_dsl.strip()
    if p_key in BUILTIN_PATTERNS:
        return BUILTIN_PATTERNS[p_key]
    if p_key in _m0546:
        return _m0546[p_key]
    if (custom_dsl or '').strip():
        return custom_dsl.strip()
    return BUILTIN_PATTERNS['stamped_plate']

def _m0087(_m0541: str):
    if not _m0541:
        return None
    fields = [f.strip() for f in _m0541.split(':')]
    if len(fields) < 2:
        return None
    try:
        _m0497 = max(0.5, float(fields[0]))
    except ValueError:
        _m0497 = 15.0
    _m0438 = fields[1].lower()
    kind = SHAPE_ALIASES.get(_m0438, _m0438)
    if kind not in VALID_SHAPES:
        kind = 'flat'
    try:
        _m0564 = float(fields[2]) if len(fields) >= 3 and fields[2] else DEFAULT_Z_VALUES[kind]
    except ValueError:
        _m0564 = DEFAULT_Z_VALUES[kind]
    _m0344 = fields[3].lower() if len(fields) >= 4 and fields[3] else 'main'
    _m0160 = fields[4].lower() if len(fields) >= 5 and fields[4] else 'auto'
    return {'share': _m0497, 'kind': kind, 'z': max(0.0, min(100.0, _m0564)), 'mat': _m0344, 'corner': _m0160}

def _m0056(zones: list) -> None:
    total = sum((z['share'] for z in zones))
    if total > 0:
        for zone in zones:
            zone['share'] = zone['share'] / total

def parse_profile_zones(_m0412: str, custom_dsl: str='', normalize_shares: bool=True) -> list:
    zones = []
    for part in _m0069(_m0412, custom_dsl).split(';'):
        zone = _m0087(part.strip())
        if zone is None:
            continue
        zones.append(zone)
    if not zones:
        return parse_profile_zones('stamped_plate', '', normalize_shares=normalize_shares)
    if normalize_shares:
        _m0056(zones)
    return zones
