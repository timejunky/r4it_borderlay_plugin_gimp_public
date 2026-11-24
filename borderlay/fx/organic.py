# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
from __future__ import annotations
import math
_m0005 = ('feather', 'fur', 'scales')

def _m0206(kind: str, _m0252: float, _m0463: float) -> float:
    g = max(0.0, min(1.0, float(_m0252) / 100.0))
    rim = max(24.0, float(_m0463))
    if kind == 'feather':
        return 16.0 + g * 72.0
    if kind == 'fur':
        _m0182 = 9.5 - g * 5.5
        return max(5.0, rim / max(1.8, _m0182))
    return 14.0 + g * 58.0

def _m0054(value: float, _m0401: float) -> float:
    if _m0401 <= 0.0:
        return 0.0
    return value - math.floor(value / _m0401) * _m0401

def _m0083(_m0186: float, _m0187: float, value: float) -> float:
    if _m0186 == _m0187:
        return 0.0 if value < _m0186 else 1.0
    t = max(0.0, min(1.0, (value - _m0186) / (_m0187 - _m0186)))
    return t * t * (3.0 - 2.0 * t)

def _m0040(ix: int, iy: int) -> float:
    n = ix * 374761393 + iy * 668265263 & 4294967295
    n = (n ^ n >> 13) * 1274126177 & 4294967295
    return (n & 65535) / 65535.0

def _m0028(value: float) -> float:
    return 0.0 if value < 0.0 else 1.0 if value > 1.0 else value

def _m0036(_m0331: float, _m0332: float, _m0314: float, width: float):
    if _m0331 < 0.0 or _m0331 > _m0314:
        return None
    t = _m0331 / _m0314
    if t < 0.16:
        _m0420 = 0.28 + t / 0.16 * 0.72
    else:
        _m0420 = math.sin((1.0 - t) * math.pi * 0.5) ** 0.42
    _m0263 = width * 0.5 * _m0420
    _m0089 = abs(_m0332)
    if _m0089 > _m0263:
        return None
    _m0495 = max(0.8, min(width * 0.08, _m0314 * 0.04))
    _m0494 = 1.0 - _m0083(_m0495 * 0.15, _m0495 * 1.05, _m0089)
    gap = max(2.0, _m0314 * 0.07)
    _m0404 = _m0054(_m0331 - _m0089 * 0.55, gap)
    _m0181 = min(_m0404, gap - _m0404)
    _m0100 = 1.0 - _m0083(0.3, gap * 0.34, _m0181)
    _m0185 = _m0083(_m0263 * 0.72, _m0263, _m0089)
    value = 0.8 - _m0494 * 0.55 - _m0185 * 0.52 - _m0100 * (1.0 - _m0185) * 0.1
    return _m0028(value)

def _m0049(_m0400: float) -> float:
    return 0.55 + 0.74 * (max(0.0, min(100.0, float(_m0400))) / 100.0)

def _m0037(_m0175: float) -> float:
    _m0400 = max(0.0, min(100.0, float(_m0175)))
    return 1.0 + (72.0 - _m0400) * 3.0 / 140.0

def _m0080(u: float, v: float, _m0523: float, _m0524: float, cols: int, rows: int, _m0118: float, _m0119: float) -> float:
    _m0402 = _m0523 * cols
    _m0403 = _m0524 * rows
    _m0547 = _m0054(u, _m0402)
    _m0555 = _m0054(v, _m0403)
    _m0308 = int(math.floor(_m0547 / _m0523)) % cols
    _m0309 = int(math.floor(_m0555 / _m0524)) % rows
    _m0110 = None
    _m0111 = 1000000000.0
    for oy in range(-2, 3):
        for ox in range(-2, 3):
            ix = (_m0308 + ox) % cols
            iy = (_m0309 + oy) % rows
            _m0314 = min(_m0118 * 0.92, _m0118 * (0.62 + 0.28 * _m0040(ix, iy)))
            width = _m0119 * (0.55 + 0.42 * _m0040(ix + 11, iy - 4))
            ang = (_m0040(ix - 2, iy + 6) - 0.5) * 0.16
            _m0310 = (_m0040(ix, iy + 3) - 0.5) * _m0523 * 0.22
            _m0311 = (_m0040(ix + 8, iy) - 0.5) * _m0524 * 0.18
            shift = _m0523 * 0.46 if iy & 1 else 0.0
            _m0470 = _m0054(ix * _m0523 + shift + _m0310, _m0402)
            _m0471 = _m0054(iy * _m0524 + _m0524 * 0.35 + _m0311, _m0403)
            dx = _m0086(_m0547 - _m0470, _m0402)
            dy = _m0086(_m0555 - _m0471, _m0403)
            _m0138 = math.cos(ang)
            _m0476 = math.sin(ang)
            _m0331 = dx * _m0138 + dy * _m0476
            _m0332 = -dx * _m0476 + dy * _m0138
            value = _m0036(_m0331, _m0332, _m0314, width)
            if value is None or _m0331 >= _m0111:
                continue
            _m0111 = _m0331
            _m0110 = value
    return 0.5 if _m0110 is None else _m0110

def _m0086(_m0174: float, _m0401: float) -> float:
    _m0263 = _m0401 * 0.5
    if _m0174 > _m0263:
        return _m0174 - _m0401
    if _m0174 < -_m0263:
        return _m0174 + _m0401
    return _m0174
_m0016: dict = {}

def _m0038(feature: float, _m0401: float, _m0175: float=72.0, _m0314: float=61.0) -> tuple:
    key = (round(feature, 2), round(_m0401, 2), int(_m0175), int(_m0314))
    cached = _m0016.get(key)
    if cached is not None:
        return cached
    d = max(0.0, min(1.0, float(_m0175) / 100.0))
    _m0198 = max(0.0, min(1.0, float(_m0314) / 100.0))
    _m0093 = max(12.0, feature * (0.85 + 0.7 * _m0198))
    _m0090 = max(0.06, 1.02 - 1.04 * d)
    _m0091 = max(1.6, feature * _m0090)
    cols = max(3, int(round(_m0401 / _m0093)))
    rows = max(4, int(round(_m0401 / _m0091)))
    _m0093 = _m0401 / float(cols)
    _m0091 = _m0401 / float(rows)
    _m0218 = 0.34 + 0.28 * _m0198
    _m0219 = 0.18 + 0.22 * _m0198
    _m0262 = []
    for iy in range(rows):
        _m0521 = _m0093 * 0.5 if iy & 1 else 0.0
        for ix in range(cols):
            _m0310 = (_m0040(ix + 2, iy) - 0.5) * _m0093 * 0.1
            _m0311 = (_m0040(ix, iy - 3) - 0.5) * _m0091 * 0.2
            _m0216 = (_m0040(ix - 3, iy + 8) - 0.5) * 0.4
            frac = min(0.92, _m0218 + _m0219 * _m0040(ix, iy))
            _m0262.append((_m0054(ix * _m0093 + _m0521 + _m0310, _m0401), _m0054(iy * _m0091 + _m0091 * 0.5 + _m0311, _m0401), _m0093 * frac, 1.05 + 0.65 * _m0040(ix + 4, iy - 2), math.cos(_m0216), math.sin(_m0216), 0.46 + 0.1 * _m0040(ix - 1, iy + 5)))
    if len(_m0016) > 6:
        _m0016.clear()
    _m0384 = (_m0262, cols, rows, _m0093, _m0091)
    _m0016[key] = _m0384
    return _m0384

def _m0081(u: float, v: float, feature: float, _m0401: float, _m0175: float=72.0, _m0314: float=61.0) -> float:
    _m0262, cols, rows, _m0093, _m0091 = _m0038(feature, _m0401, _m0175, _m0314)
    _m0308 = int(math.floor(_m0054(u, _m0401) / _m0093))
    _m0309 = int(math.floor(_m0054(v, _m0401) / _m0091))
    _m0547 = _m0054(u, _m0401)
    _m0555 = _m0054(v, _m0401)
    _m0286 = 0.0
    for oy in range(-2, 3):
        for ox in range(-2, 2):
            ix = (_m0308 + ox) % cols
            iy = (_m0309 + oy) % rows
            _m0470, _m0471, _m0314, _m0469, _m0138, _m0476, weight = _m0262[iy * cols + ix]
            dx = _m0086(_m0547 - _m0470, _m0401)
            dy = _m0086(_m0555 - _m0471, _m0401)
            _m0092 = dx * _m0138 + dy * _m0476
            _m0089 = -dx * _m0476 + dy * _m0138
            if _m0092 < 0.0 or _m0092 > _m0314:
                continue
            _m0265 = _m0469 * (1.0 - _m0092 / _m0314) ** 0.45
            if _m0265 < 0.45 or abs(_m0089) > _m0265 * 1.25:
                continue
            _m0163 = 1.0 - abs(_m0089) / (_m0265 * 1.25)
            _m0506 = _m0083(0.05, 0.75, _m0089 / max(_m0265, 0.45))
            _m0286 = max(_m0286, _m0163 * weight * (1.0 - _m0506 * 0.35))
    return _m0028(0.5 - _m0286)

def _m0076(_m0400: float) -> float:
    p = max(0.0, min(100.0, float(_m0400)))
    if p >= 61.0:
        return 1.0 + (p - 61.0) * (0.9 / 39.0)
    return 0.38 + p / 61.0 * 0.62

def _m0077(lx: float, ly: float, _m0140: float, _m0139: float, grow: float=1.0, _m0095: float=1.0):
    cx = _m0140 * 0.5
    cy = _m0139 * 0.96
    rx = _m0140 * 0.58 * grow
    ry = _m0139 * 0.9 * grow * _m0095
    _m0371 = (lx - cx) / rx
    _m0372 = (ly - cy) / ry
    _m0181 = math.hypot(_m0371, _m0372)
    if _m0181 >= 1.0:
        return None
    _m0126 = math.sqrt(max(0.0, 1.0 - _m0181 * _m0181))
    rim = _m0083(0.78, 0.98, _m0181)
    light = _m0083(0.05, -0.55, _m0372)
    return _m0028(0.7 + _m0126 * 0.16 + light * 0.08 - rim * 0.62)

def _m0082(u: float, v: float, _m0140: float, _m0139: float, _m0095: float=1.0) -> float:
    row = math.floor(v / _m0139)
    _m0150 = _m0140 * 0.5 if int(row) & 1 else 0.0
    col = math.floor((u + _m0150) / _m0140)
    lx = _m0054(u + _m0150, _m0140)
    ly = _m0054(v, _m0139)
    grow = 0.62 + 0.78 * _m0040(int(col), int(row))
    _m0221 = _m0077(lx, ly, _m0140, _m0139, grow, _m0095)
    _m0419 = 0.0 if int(row) & 1 else _m0140 * 0.5
    _m0415 = math.floor((u + _m0419) / _m0140)
    _m0416 = 0.62 + 0.78 * _m0040(int(_m0415), int(row) - 1)
    _m0414 = _m0077(_m0054(u + _m0419, _m0140), ly + _m0139, _m0140, _m0139, _m0416, _m0095)
    if _m0221 is None:
        return 0.4 if _m0414 is None else _m0414
    if _m0414 is None:
        return _m0221
    return _m0221

def _m0084(_m0123: bytearray, _m0545: int, _m0532: int) -> None:
    src = bytes(_m0123)
    for y in range(_m0532):
        row = y * _m0545
        _m0559 = (y - 1) % _m0532 * _m0545
        _m0560 = (y + 1) % _m0532 * _m0545
        for x in range(_m0545):
            _m0557 = (x - 1) % _m0545
            _m0558 = (x + 1) % _m0545
            _m0088 = src[row + x] * 6 + src[row + _m0557] + src[row + _m0558] + src[_m0559 + x] + src[_m0560 + x]
            _m0123[row + x] = _m0088 // 10

def _m0125(kind: str, _m0252: float, _m0463: float, fur_density: float=72.0, fur_length: float=61.0) -> tuple[bytes, int, int]:
    feature = _m0206(kind, _m0252, _m0463)
    _m0140 = _m0139 = 1.0
    _m0523 = _m0524 = feature
    _m0203 = 4
    _m0204 = 4
    if kind == 'feather':
        _m0118 = max(32, int(round(feature * 2.7)))
        _m0119 = max(12, int(round(feature * 0.72)))
        _m0383 = _m0037(fur_density)
        _m0141 = max(6, int(round(_m0118 * _m0383)))
        _m0142 = max(4, int(round(_m0119 * _m0383)))
        _m0203 = 2
        _m0204 = 2
        _m0523 = float(_m0141)
        _m0524 = float(_m0142)
        _m0545 = _m0141 * _m0203
        _m0532 = _m0142 * _m0204
    elif kind == 'fur':
        _m0506 = max(96, min(200, int(round(feature * 11.0))))
        _m0545 = _m0532 = _m0506
    else:
        _m0140 = max(8.0, feature)
        _m0139 = max(6.0, feature * 0.68)
        _m0545 = max(12, int(round(_m0140)))
        _m0532 = max(16, int(round(_m0139 * 2.0)))
    cap = 200
    if kind != 'feather' and max(_m0545, _m0532) > cap:
        scale = cap / float(max(_m0545, _m0532))
        _m0545 = max(16, int(round(_m0545 * scale)))
        _m0532 = max(16, int(round(_m0532 * scale)))
    if kind == 'scales':
        _m0140 = float(_m0545)
        _m0139 = float(_m0532) / 2.0
    _m0123 = bytearray(_m0545 * _m0532)
    if kind == 'scales':
        for y in range(_m0532):
            row = y * _m0545
            for x in range(_m0545):
                shade = _m0082(x + 0.5, y + 0.5, _m0140, _m0139, _m0076(fur_length))
                _m0123[row + x] = int(shade * 255.0 + 0.5)
    elif kind == 'fur':
        for y in range(_m0532):
            row = y * _m0545
            for x in range(_m0545):
                shade = _m0081(x + 0.5, y + 0.5, feature, float(_m0545), fur_density, fur_length)
                _m0123[row + x] = int(shade * 255.0 + 0.5)
        _m0084(_m0123, _m0545, _m0532)
    else:
        for y in range(_m0532):
            row = y * _m0545
            for x in range(_m0545):
                shade = _m0080(x + 0.5, y + 0.5, _m0523, _m0524, _m0203, _m0204, float(_m0118), float(_m0119))
                _m0123[row + x] = int(shade * 255.0 + 0.5)
    return (bytes(_m0123), _m0545, _m0532)

def _m0055(kind: str, _m0252: float, _m0516: float, _m0536: int) -> float:
    g = max(0.0, min(1.0, float(_m0252) / 100.0))
    _m0516 = max(72.0, float(_m0516))
    _m0536 = max(1, int(_m0536))
    if kind == 'fur':
        _m0401 = max(float(_m0536), _m0516 * (0.14 + g * 0.08))
        return max(1.0, _m0401 / float(_m0536))
    return 1.0

def _m0447(kind: str, width: int, height: int, _m0252: float, _m0463: float, angle_deg: float, _m0376: float=0.0, _m0377: float=0.0, _m0347: int=900000, fur_density: float=72.0, fur_length: float=61.0) -> tuple[bytes, int]:
    _m0535, _m0545, _m0532 = _m0125(kind, _m0252, _m0463, fur_density, fur_length)
    width = max(1, int(width))
    height = max(1, int(height))
    _m0516 = max(float(_m0463), float(min(width, height)))
    _m0301 = 1.0 / _m0055(kind, _m0252, _m0516, _m0545)
    _m0113 = 1
    _m0477 = width * height
    while _m0477 > _m0347:
        _m0113 += 1
        _m0477 = width // _m0113 * (height // _m0113)
    sw = max(1, width // _m0113)
    sh = max(1, height // _m0113)
    rad = math.radians(float(angle_deg))
    _m0138 = math.cos(rad)
    _m0476 = math.sin(rad)
    cx = _m0376 + width * 0.5
    cy = _m0377 + height * 0.5
    _m0253 = bytearray(sw * sh)
    for y in range(sh):
        _m0222 = _m0377 + (y + 0.5) * _m0113 - cy
        row = y * sw
        for x in range(sw):
            fx = _m0376 + (x + 0.5) * _m0113 - cx
            u = fx * _m0138 + _m0222 * _m0476
            v = -fx * _m0476 + _m0222 * _m0138
            tx = int(math.floor(u * _m0301)) % _m0545
            ty = int(math.floor(v * _m0301)) % _m0532
            _m0253[row + x] = _m0535[ty * _m0545 + tx]
    if _m0113 == 1 and sw == width and (sh == height):
        out = bytearray(width * height * 4)
        for i, g in enumerate(_m0253):
            _m0373 = i * 4
            out[_m0373] = g
            out[_m0373 + 1] = g
            out[_m0373 + 2] = g
            out[_m0373 + 3] = 255
        return (bytes(out), _m0113)
    out = bytearray(width * height * 4)
    for y in range(height):
        sy = min(sh - 1, y // _m0113)
        src = sy * sw
        _m0177 = y * width
        for x in range(width):
            g = _m0253[src + min(sw - 1, x // _m0113)]
            _m0373 = (_m0177 + x) * 4
            out[_m0373] = g
            out[_m0373 + 1] = g
            out[_m0373 + 2] = g
            out[_m0373 + 3] = 255
    return (bytes(out), _m0113)
