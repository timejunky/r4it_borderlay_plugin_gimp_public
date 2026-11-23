# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
from __future__ import annotations
import time
from dataclasses import dataclass, field
from typing import Any, Callable
from license_product import BORDERLAY_PRODUCT_ID, DEVICE_LIMIT_TIERS, LICENSE_CONTACT_URL, TIER_DISPLAY_NAMES, TIER_ORDER, MIN_TIER_FOR_FEATURE, contracted_seats_and_activations, limits_for_payload, limits_for_tier, normalize_tier, user_status_message

@dataclass
class _m0006:
    status_code: str = 'missing'
    _m0565: str = ''
    tier: str = 'community'
    tier_display: str = 'Community'
    is_active: bool = False
    _m0340: bool = False
    _m0226: int | None = None
    _m0601: list[str] = field(default_factory=list)
    feature_limits: dict[str, Any] = field(default_factory=dict)

    @property
    def _m0227(self) -> str:
        if self._m0226 is None:
            return ''
        try:
            import datetime
            _m0206 = datetime.datetime.fromtimestamp(self._m0226)
            return _m0206.strftime('%Y-%m-%d')
        except Exception:
            return str(self._m0226)

class LicensingService:
    _m0054: 'LicensingService | None' = None
    _m0017 = 60
    _m0098: list[Callable[[], None]] = []

    def __init__(self) -> None:
        self._cached_info: _m0006 | None = None
        self._cache_ts: float = 0.0

    @classmethod
    def get_instance(cls) -> 'LicensingService':
        if cls._m0054 is None:
            cls._m0054 = cls()
        return cls._m0054

    def _m0038(self):
        try:
            from licensing_client_bootstrap import _m0270
            return _m0270()
        except Exception:
            return None

    def _m0271(self) -> str:
        from license_product import portal_device_hash
        return portal_device_hash()

    def get_device_hash(self) -> str:
        return self._m0271()

    def _m0035(self, payload, tier, is_active, code, _m0601, _m0565):
        _m0186 = self._m0271()
        _m0239 = payload.get('fingerprints') or []
        if not isinstance(_m0239, list):
            _m0239 = [_m0239]
        _m0239 = [str(fp) for fp in _m0239]
        seats, _m0380 = contracted_seats_and_activations(tier, payload)
        _m0334 = _m0186 in _m0239
        _m0588 = len(_m0239)
        if not _m0334:
            _m0588 += 1
        if _m0588 > _m0380:
            is_active = False
            code = 'device_limit_exceeded'
            _m0565 = f'Device limit exceeded. This license permits {_m0380} activation(s) for {seats} seat(s).'
            _m0601.append(_m0565)
        return (is_active, code, _m0565, _m0601)

    def _m0028(self, code, tier, _m0565, _m0601, payload):
        if code != 'product_mismatch':
            return (tier, TIER_DISPLAY_NAMES.get(tier, tier.title()), limits_for_payload(tier, payload), _m0601)
        if _m0565 not in _m0601:
            _m0601.append(_m0565)
        return ('community', TIER_DISPLAY_NAMES['community'], limits_for_tier('community'), _m0601)

    def _m0099(self, status) -> _m0006:
        code = status.code.value if hasattr(status.code, 'value') else str(status.code)
        is_active = code == 'ok'
        payload = status.payload or {}
        _m0476 = payload.get('tier') or payload.get('plan') or 'community'
        tier = normalize_tier(_m0476)
        _m0565 = user_status_message(code, status.message or '')
        _m0601 = list(getattr(status, 'warnings', None) or [])
        tier, tier_display, limits, _m0601 = self._m0028(code, tier, _m0565, _m0601, payload)
        if is_active and tier in DEVICE_LIMIT_TIERS:
            is_active, code, _m0565, _m0601 = self._m0035(payload, tier, is_active, code, _m0601, _m0565)
        return _m0006(status_code=code, _m0565=_m0565, tier=tier, tier_display=tier_display, is_active=is_active, _m0340=getattr(status, 'trial', False), _m0226=getattr(status, 'expires_at', None), _m0601=_m0601, feature_limits=limits)

    def _m0041(self) -> None:
        from pathlib import Path
        pending = Path.home() / '.borderlay' / 'pending_activation.txt'
        if not pending.is_file():
            return
        try:
            raw = pending.read_text(encoding='utf-8').strip()
        except Exception:
            raw = ''
        try:
            pending.unlink(missing_ok=True)
        except Exception:
            pass
        if raw:
            self.activate(raw)

    def _m0033(self) -> _m0006:
        self._m0041()
        client = self._m0038()
        if client is None:
            return _m0102('No Borderlay Studio license key. Community stays available.')
        try:
            return self._m0099(client.get_status())
        except Exception as exc:
            return _m0102(str(exc))

    def get_status_info(self, force: bool=False) -> _m0006:
        now = time.monotonic()
        if force or self._cached_info is None or now - self._cache_ts > self._m0017:
            self._cached_info = self._m0033()
            self._cache_ts = now
        return self._cached_info

    def activate(self, _m0585: str) -> tuple[bool, str]:
        from license_activation_input import parse_activation_input
        self._cached_info = None
        client = self._m0038()
        if client is None:
            from licensing_client_bootstrap import _m0349
            return (False, _m0349())
        try:
            _m0329, payload = parse_activation_input(_m0585)
            if _m0329 == 'activation':
                status = client.store_activation(payload)
            else:
                if not payload:
                    return (False, 'Please enter a license key or activation JSON.')
                status = client.store_token(str(payload).strip())
            return self._m0055(status)
        except Exception as exc:
            return (False, f'Activation error: {exc}')

    def _m0032(self) -> tuple[bool, str]:
        from locales.i18n import t
        info = self.get_status_info(force=True)
        tier = normalize_tier(info.tier)
        if not info.is_active or tier not in DEVICE_LIMIT_TIERS:
            return (False, t('license_bind_failed', tier=info.tier_display, code=info.status_code))
        limits = info.feature_limits or limits_for_tier(tier)
        light = t('license_yes') if limits.get('light_pad') else t('license_no')
        zones = t('license_yes') if limits.get('zone_editor') else t('license_no')
        return (True, t('license_bound', tier=info.tier_display, light=light, zones=zones))

    def _m0055(self, status) -> tuple[bool, str]:
        code = status.code.value if hasattr(status.code, 'value') else str(status.code)
        message = status.message or ''
        stored = code == 'ok' or code in ('renewal_blocked', 'RENEWAL_BLOCKED') or 'Duplicate token' in message
        if stored:
            return self._m0032()
        return (False, user_status_message(code, message) or 'Activation failed.')

    def deactivate(self) -> tuple[bool, str]:
        self._cached_info = None
        client = self._m0038()
        if client is None:
            return (False, 'Borderlay Studio licensing client not available.')
        try:
            getattr(client, 'deactivate')()
            return (True, 'License deactivated.')
        except Exception as exc:
            return (False, f'Deactivation error: {exc}')

    def _m0030(self, limits: dict, feature: str) -> bool | None:
        if feature not in limits or not isinstance(limits[feature], bool):
            return None
        return bool(limits[feature])

    def _m0101(self, tier: str, feature: str) -> bool | None:
        _m0488 = MIN_TIER_FOR_FEATURE.get(feature)
        if not _m0488:
            return None
        try:
            _m0185 = TIER_ORDER.index(normalize_tier(tier))
            _m0487 = TIER_ORDER.index(normalize_tier(_m0488))
            return _m0185 >= _m0487
        except ValueError:
            return False

    def _m0297(self, feature: str) -> bool:
        info = self.get_status_info()
        if not info.is_active:
            _m0109 = self._m0030(limits_for_tier('community'), feature)
            return bool(_m0109) if _m0109 is not None else False
        limits = info.feature_limits or limits_for_tier(info.tier)
        _m0109 = self._m0030(limits, feature)
        if _m0109 is not None:
            return _m0109
        _m0109 = self._m0101(info.tier, feature)
        if _m0109 is not None:
            return _m0109
        client = self._m0038()
        if client is None:
            return False
        try:
            val = getattr(client, 'has_feature')(feature)
            if type(val).__name__ == 'MagicMock':
                return False
            return bool(val)
        except Exception:
            return False

    def _m0273(self) -> str:
        return self.get_status_info().tier

    def _m0490(self) -> None:
        self._cached_info = None

def _m0102(message: str) -> _m0006:
    return _m0006(status_code='missing', _m0565=message, feature_limits=limits_for_tier('community'))

def _m0564() -> str:
    info = LicensingService.get_instance().get_status_info(force=True)
    _m0455 = BORDERLAY_PRODUCT_ID
    active = 'yes' if info.is_active else 'no'
    return f'{_m0455}: {info.tier_display} ({info.status_code}, active {active}). {LICENSE_CONTACT_URL}'
