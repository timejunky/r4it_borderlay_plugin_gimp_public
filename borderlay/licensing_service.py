# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
from __future__ import annotations

class _m0015:
    status_code = 'community'
    tier = 'community'
    tier_display = 'Community'
    is_active = False
    _m0205: dict = {}

class LicensingService:
    _m0044: 'LicensingService | None' = None

    @classmethod
    def get_instance(cls) -> 'LicensingService':
        if cls._m0044 is None:
            cls._m0044 = cls()
        return cls._m0044

    def get_status_info(self, force: bool=False) -> _m0015:
        return _m0015()

    def get_device_hash(self) -> str:
        return ''

    def activate(self, _m0048: str) -> tuple[bool, str]:
        return (False, 'The Community edition has no license key.')

    def deactivate(self) -> tuple[bool, str]:
        return (True, 'Community edition.')
