# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
from __future__ import annotations
from pathlib import Path
from typing import Any
BORDERLAY_PRODUCT_ID = 'borderlay'
BORDERLAY_PRODUCT_ALIASES = frozenset({'borderlay', 'borderlay-studio', 'r4it-borderlay'})
LICENSE_CONTACT_URL = 'https://www.ready-4-it.com/contact'
MG_PRODUCT_IDS = frozenset({'manifestguard-python', 'manifestguard-py', 'mgpy'})
PIXEL_FORGE_PRODUCT_IDS = frozenset({'pixel-forge', 'pixelforge', 'r4it-pixel-forge'})
TIER_DISPLAY_NAMES: dict[str, str] = {'community': 'Community', 'look': 'Look', 'atelier': 'Atelier', 'team': 'Team'}
TIER_ALIASES: dict[str, str] = {'free': 'community', 'basic': 'community', 'standard': 'look', 'pro': 'atelier', 'premium': 'atelier', 'enterprise': 'team'}
TIER_ORDER = ['community', 'look', 'atelier', 'team']
MIN_TIER_FOR_FEATURE: dict[str, str] = {'rectangular_border': 'community', 'free_materials': 'community', 'auto_light': 'community', 'simple_profile': 'community', 'corners': 'community', 'shape_rotation': 'community', 'plate': 'look', 'wider_materials': 'look', 'named_presets': 'look', 'shape_arrays': 'look', 'support': 'look', 'light_pad': 'atelier', 'zone_editor': 'atelier', 'glass_gems': 'atelier', 'saved_presets': 'atelier', 'commercial_use': 'atelier', 'curved_shapes': 'look', 'shape_toolbox': 'look', 'shape_toolbox_pro': 'atelier', 'path_toolbox': 'atelier'}
FEATURE_DISPLAY: dict[str, str] = {'rectangular_border': 'Rectangular border', 'free_materials': 'Free materials', 'plate': 'Plate', 'wider_materials': 'Wider materials', 'corners': 'Miters and radii', 'named_presets': 'Named presets', 'shape_rotation': 'Shape rotation', 'shape_arrays': 'Shape arrays', 'support': 'Support', 'light_pad': 'Light pad', 'zone_editor': 'Zone editor', 'glass_gems': 'Glass and gems', 'saved_presets': 'Saved presets', 'commercial_use': 'Commercial use', 'curved_shapes': 'Circle, ellipse, leaf, freeform', 'shape_toolbox': 'Shape toolbox', 'shape_toolbox_pro': 'Pro shape toolbox', 'path_toolbox': 'Path toolbox', 'max_seats': 'Seats', 'max_devices': 'Activations'}
TEAM_MIN_SEATS = 2
TEAM_MAX_SEATS = 5
SEAT_FIELDS = ('seats', 'max_seats', 'maxSeats')
ACTIVATION_FIELDS = ('maxActivations', 'max_activations', 'max_devices')
TEAM_TIERS = frozenset({'team'})
DEVICE_LIMIT_TIERS = frozenset({'look', 'atelier', 'team'})
TIER_SEAT_FLOOR = {'community': 1, 'look': 2, 'atelier': 2, 'team': TEAM_MIN_SEATS}
TIER_ACTIVATION_FLOOR = {'community': 1, 'look': 2, 'atelier': 2, 'team': TEAM_MIN_SEATS}
TIER_SEAT_CAP = {'community': 1, 'look': 2, 'atelier': 2, 'team': TEAM_MAX_SEATS}
COMMUNITY_PROFILE = 'stamped_plate'
COMMUNITY_OUTER_RADIUS = 84
COMMUNITY_INNER_RADIUS = 38
_COMMUNITY_LIMITS: dict[str, Any] = {'rectangular_border': True, 'free_materials': True, 'auto_light': True, 'simple_profile': True, 'plate': False, 'wider_materials': False, 'corners': True, 'named_presets': False, 'shape_rotation': True, 'shape_arrays': False, 'support': False, 'light_pad': False, 'zone_editor': False, 'glass_gems': False, 'saved_presets': False, 'commercial_use': False, 'curved_shapes': False, 'shape_toolbox': False, 'shape_toolbox_pro': False, 'path_toolbox': False, 'max_seats': 1, 'max_devices': 1}
_LOOK_LIMITS: dict[str, Any] = {**_COMMUNITY_LIMITS, 'plate': True, 'wider_materials': True, 'corners': True, 'named_presets': True, 'shape_rotation': True, 'shape_arrays': True, 'support': True, 'curved_shapes': True, 'shape_toolbox': True, 'shape_toolbox_pro': False, 'path_toolbox': False, 'max_seats': 2, 'max_devices': 2}
_ATELIER_LIMITS: dict[str, Any] = {**_LOOK_LIMITS, 'light_pad': True, 'zone_editor': True, 'glass_gems': True, 'saved_presets': True, 'commercial_use': True, 'curved_shapes': True, 'shape_toolbox_pro': True, 'path_toolbox': True}
FEATURE_LIMITS: dict[str, dict[str, Any]] = {'community': dict(_COMMUNITY_LIMITS), 'look': dict(_LOOK_LIMITS), 'atelier': dict(_ATELIER_LIMITS), 'team': {**_ATELIER_LIMITS, 'max_seats': TEAM_MAX_SEATS, 'max_devices': TEAM_MAX_SEATS}}

def normalize_tier(raw: Any) -> str:
    tier = str(raw or 'community').strip().lower()
    return TIER_ALIASES.get(tier, tier)

def license_scope_root() -> Path:
    return Path.home() / '.borderlay'

def portal_device_hash() -> str:
    import hashlib
    import os
    import socket
    try:
        name = os.environ.get('COMPUTERNAME') or os.environ.get('HOSTNAME') or socket.gethostname()
        if not name:
            import uuid
            name = str(uuid.getnode())
        return hashlib.sha256(name.encode('utf-8')).hexdigest()
    except Exception:
        return 'unknown_device'

def accepted_product_ids() -> set[str]:
    return set(BORDERLAY_PRODUCT_ALIASES)

def configure_borderlay_licensing_client(client: Any) -> None:
    client.product_id = BORDERLAY_PRODUCT_ID
    client.app_name = 'borderlay'
    client.scope_root = license_scope_root()
    client._accepted_product_ids = accepted_product_ids
    client.get_device_hash = portal_device_hash

def limits_for_tier(tier: str) -> dict[str, Any]:
    key = normalize_tier(tier)
    return dict(FEATURE_LIMITS.get(key) or FEATURE_LIMITS['community'])

def _positive_int(raw: Any) -> int | None:
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return None
    return value if value >= 1 else None

def _payload_int(payload: dict[str, Any], keys: tuple[str, ...]) -> int | None:
    for key in keys:
        value = _positive_int(payload.get(key))
        if value is not None:
            return value
    return None

def _paired_seat_activation(seats: int | None, activations: int | None, floor: int) -> tuple[int, int]:
    if seats is None and activations is None:
        return (floor, floor)
    if seats is None:
        count = max(activations or floor, floor)
        return (count, count)
    if activations is None:
        count = max(seats, floor)
        return (count, count)
    count = max(min(seats, activations), floor)
    return (count, count)

def contracted_seats_and_activations(tier: str, payload: dict[str, Any] | None=None) -> tuple[int, int]:
    key = normalize_tier(tier)
    seat_floor = TIER_SEAT_FLOOR.get(key, 1)
    act_floor = TIER_ACTIVATION_FLOOR.get(key, 1)
    data = payload or {}
    seats = _payload_int(data, SEAT_FIELDS)
    activations = _payload_int(data, ACTIVATION_FIELDS)
    if key in TEAM_TIERS:
        seats, activations = _paired_seat_activation(seats, activations, seat_floor)
    else:
        seats = max(seats or seat_floor, seat_floor)
        activations = max(activations or act_floor, act_floor)
    cap = TIER_SEAT_CAP.get(key, 1)
    return (min(seats, cap), min(activations, cap))

def limits_for_payload(tier: str, payload: dict[str, Any] | None=None) -> dict[str, Any]:
    limits = limits_for_tier(tier)
    seats, activations = contracted_seats_and_activations(tier, payload)
    limits['max_seats'] = seats
    limits['max_devices'] = activations
    return limits

def user_status_message(code: str, message: str) -> str:
    if code == 'product_mismatch':
        return f'This key is not a Borderlay Studio license. Use a {BORDERLAY_PRODUCT_ID} token. Contact: {LICENSE_CONTACT_URL}'
    return message or ''

def active_limits() -> dict[str, Any]:
    import os
    try:
        from community_beacon import COMMUNITY_EDITION
        if COMMUNITY_EDITION:
            return limits_for_tier('community')
    except Exception:
        pass
    if os.environ.get('R4IT_BORDERLAY_DEV_UNLOCK') == '1':
        return limits_for_tier('team')
    try:
        from licensing_service import LicensingService
        info = LicensingService.get_instance().get_status_info()
        if info.is_active:
            tier = normalize_tier(info.tier)
            if tier in {'look', 'atelier', 'team'}:
                return dict(info.feature_limits or limits_for_tier(tier))
    except Exception:
        pass
    return limits_for_tier('community')

def paid_license_is_active() -> bool:
    try:
        from community_beacon import COMMUNITY_EDITION
        if COMMUNITY_EDITION:
            return True
    except Exception:
        pass
    try:
        from licensing_service import LicensingService
        info = LicensingService.get_instance().get_status_info(force=True)
        return bool(info.is_active and normalize_tier(info.tier) in {'look', 'atelier', 'team'})
    except Exception:
        return False

def require_paid_license() -> bool:
    if paid_license_is_active():
        return True
    try:
        from gui.studio_dialogs import StudioInfoDialogs
        StudioInfoDialogs.show_license_dialog()
    except Exception:
        return False
    return paid_license_is_active()

def edition_label(limits: dict[str, Any] | None=None) -> str:
    data = active_limits() if limits is None else limits
    if not data:
        return ''
    seats = int(data.get('max_seats') or 1)
    if data.get('glass_gems') and seats >= TEAM_MIN_SEATS:
        return TIER_DISPLAY_NAMES['team']
    if data.get('glass_gems'):
        return TIER_DISPLAY_NAMES['atelier']
    if data.get('plate'):
        return TIER_DISPLAY_NAMES['look']
    return TIER_DISPLAY_NAMES['community']

def preset_allowed(preset: str, limits: dict[str, Any] | None=None) -> bool:
    import config
    data = limits if limits is not None else active_limits()
    key = (preset or COMMUNITY_PROFILE).strip() or COMMUNITY_PROFILE
    if key == COMMUNITY_PROFILE:
        return True
    if key == 'custom':
        return bool(data.get('zone_editor'))
    if key in config.PROFILE_LABELS:
        return bool(data.get('named_presets'))
    return bool(data.get('saved_presets'))

def _cfg_get(cfg: Any, name: str, default: Any) -> Any:
    try:
        value = cfg.get_property(name)
    except Exception:
        return default
    return default if value is None else value

def _cfg_set(cfg: Any, name: str, value: Any) -> bool:
    try:
        current = cfg.get_property(name)
    except Exception:
        current = None
    if current == value:
        return False
    try:
        cfg.set_property(name, value)
    except Exception:
        return False
    return True

def _pull_config(cfg: Any, changed: list[str], name: str, value: Any, feature: str) -> None:
    if _cfg_set(cfg, name, value) and feature not in changed:
        changed.append(feature)

def _clamp_material_and_profile(cfg: Any, limits: dict[str, Any], changed: list[str]) -> str:
    import config
    material = str(_cfg_get(cfg, 'material', 'gold') or 'gold')
    if not config.material_allowed(material, wider=bool(limits.get('wider_materials')), glass=bool(limits.get('glass_gems'))):
        _pull_config(cfg, changed, 'material', 'gold', 'wider_materials')
    if not limits.get('plate'):
        center = str(_cfg_get(cfg, 'innen_modus', 'transparent') or 'transparent')
        if center in ('plate', 'inlay_well'):
            _pull_config(cfg, changed, 'innen_modus', 'transparent', 'plate')
    preset = str(_cfg_get(cfg, 'profil_preset', COMMUNITY_PROFILE) or COMMUNITY_PROFILE)
    if not preset_allowed(preset, limits):
        _pull_config(cfg, changed, 'profil_preset', COMMUNITY_PROFILE, 'named_presets')
        preset = COMMUNITY_PROFILE
    if not limits.get('corners'):
        _pull_config(cfg, changed, 'eckenradius_aussen', COMMUNITY_OUTER_RADIUS, 'corners')
        _pull_config(cfg, changed, 'eckenradius_innen', COMMUNITY_INNER_RADIUS, 'corners')
    return preset

def _clamp_zone_editor(cfg: Any, limits: dict[str, Any], changed: list[str], preset: str) -> None:
    import config
    if limits.get('zone_editor'):
        return
    builtin = config.BUILTIN_PATTERNS.get(preset, '') or config.DEFAULT_CUSTOM_DSL
    custom = str(_cfg_get(cfg, 'custom_zones', '') or '')
    if preset == 'custom' or (custom and custom != builtin):
        _pull_config(cfg, changed, 'custom_zones', builtin, 'zone_editor')
        if preset == 'custom':
            _pull_config(cfg, changed, 'profil_preset', COMMUNITY_PROFILE, 'zone_editor')

def _clamp_saved_light_and_arrays(cfg: Any, limits: dict[str, Any], changed: list[str]) -> None:
    if not limits.get('saved_presets'):
        if str(_cfg_get(cfg, 'preset_save_name', '') or '').strip():
            _pull_config(cfg, changed, 'preset_save_name', '', 'saved_presets')
    if not limits.get('shape_rotation'):
        if int(_cfg_get(cfg, 'shape_rotation', 0) or 0) != 0:
            _pull_config(cfg, changed, 'shape_rotation', 0, 'shape_rotation')
        if str(_cfg_get(cfg, 'shape_pivot', 'center') or 'center') != 'center':
            _pull_config(cfg, changed, 'shape_pivot', 'center', 'shape_rotation')
    if not limits.get('shape_arrays') and bool(_cfg_get(cfg, 'rot_repeat', False)):
        _pull_config(cfg, changed, 'rot_repeat', False, 'shape_arrays')
    if not limits.get('light_pad'):
        source = str(_cfg_get(cfg, 'light_source', 'auto') or 'auto')
        if source != 'auto':
            _pull_config(cfg, changed, 'light_source', 'auto', 'light_pad')

def clamp_procedure_config(cfg: Any, limits: dict[str, Any] | None=None) -> list[str]:
    limits = limits_for_tier('community')
    if not limits:
        return []
    changed: list[str] = []
    preset = _clamp_material_and_profile(cfg, limits, changed)
    _clamp_zone_editor(cfg, limits, changed, preset)
    _clamp_saved_light_and_arrays(cfg, limits, changed)
    return changed

def paid_materials_unlocked() -> bool:
    try:
        from licensing_service import LicensingService
        service = LicensingService.get_instance()
        info = service.get_status_info()
        if not info.is_active:
            return False
        return normalize_tier(info.tier) in {'look', 'atelier', 'team'}
    except Exception:
        return False
