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

def save_user_preset(name: str, _m0205: str):
    _m0168 = (name or '').strip()
    if not _m0168 or not _m0205:
        return
    _m0448 = load_user_presets()
    _m0448[_m0168] = _m0205.strip()
    try:
        with open(USER_PRESETS_FILE, 'w', encoding='utf-8') as f:
            json.dump(_m0448, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def build_zone_token(_m0537, kind, z=None, mat='main', _m0177='auto') -> str:
    _m0167 = SHAPE_ALIASES.get(str(kind).strip().lower(), str(kind).strip().lower())
    if _m0167 not in VALID_SHAPES:
        _m0167 = 'flat'
    _m0219 = DEFAULT_Z_VALUES[_m0167] if z is None else float(z)
    _m0219 = max(0.0, min(100.0, _m0219))
    _m0216 = max(0.5, float(_m0537))
    return f"{_m0216:.1f}:{_m0167}:{_m0219:.0f}:{str(mat or 'main').strip().lower()}:{str(_m0177 or 'auto').strip().lower()}"

def build_dsl_from_specs(_m0616: list) -> str:
    _m0586 = []
    for sp in _m0616:
        if not isinstance(sp, dict):
            continue
        _m0586.append(build_zone_token(sp.get('share', 20.0), sp.get('kind', 'flat'), sp.get('z', None), sp.get('mat', 'main'), sp.get('corner', 'auto')))
    return ';'.join(_m0586) if _m0586 else DEFAULT_CUSTOM_DSL

def create_parametric_profile(_m0413=20.0, _m0443=40.0, _m0327=20.0, _m0318=20.0, _m0602=True) -> str:
    if not _m0602:
        return build_dsl_from_specs([{'share': _m0413, 'kind': 'bevel_out'}, {'share': _m0443 + _m0327, 'kind': 'flat'}, {'share': _m0318, 'kind': 'bevel_in'}])
    return build_dsl_from_specs([{'share': _m0413, 'kind': 'bevel_out'}, {'share': 5.5, 'kind': 'groove', 'mat': 'shadow'}, {'share': _m0443, 'kind': 'flat'}, {'share': 5.5, 'kind': 'groove', 'mat': 'shadow'}, {'share': _m0327, 'kind': 'step'}, {'share': _m0318, 'kind': 'bevel_in'}])

def _m0081(_m0447: str, custom_dsl: str) -> str:
    p_key = (_m0447 or 'stamped_plate').strip()
    _m0591 = load_user_presets()
    if p_key == 'custom' and (custom_dsl or '').strip():
        return custom_dsl.strip()
    if p_key in BUILTIN_PATTERNS:
        return BUILTIN_PATTERNS[p_key]
    if p_key in _m0591:
        return _m0591[p_key]
    if (custom_dsl or '').strip():
        return custom_dsl.strip()
    return BUILTIN_PATTERNS['stamped_plate']

def _m0104(_m0585: str):
    if not _m0585:
        return None
    fields = [f.strip() for f in _m0585.split(':')]
    if len(fields) < 2:
        return None
    try:
        _m0538 = max(0.5, float(fields[0]))
    except ValueError:
        _m0538 = 15.0
    _m0474 = fields[1].lower()
    kind = SHAPE_ALIASES.get(_m0474, _m0474)
    if kind not in VALID_SHAPES:
        kind = 'flat'
    try:
        _m0610 = float(fields[2]) if len(fields) >= 3 and fields[2] else DEFAULT_Z_VALUES[kind]
    except ValueError:
        _m0610 = DEFAULT_Z_VALUES[kind]
    _m0378 = fields[3].lower() if len(fields) >= 4 and fields[3] else 'main'
    _m0179 = fields[4].lower() if len(fields) >= 5 and fields[4] else 'auto'
    return {'share': _m0538, 'kind': kind, 'z': max(0.0, min(100.0, _m0610)), 'mat': _m0378, 'corner': _m0179}

def _m0068(zones: list) -> None:
    total = sum((z['share'] for z in zones))
    if total > 0:
        for zone in zones:
            zone['share'] = zone['share'] / total

def parse_profile_zones(_m0447: str, custom_dsl: str='', normalize_shares: bool=True) -> list:
    zones = []
    for part in _m0081(_m0447, custom_dsl).split(';'):
        zone = _m0104(part.strip())
        if zone is None:
            continue
        zones.append(zone)
    if not zones:
        return parse_profile_zones('stamped_plate', '', normalize_shares=normalize_shares)
    if normalize_shares:
        _m0068(zones)
    return zones
