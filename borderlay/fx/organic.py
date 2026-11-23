# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
from __future__ import annotations
import math
_m0005 = ('feather', 'fur', 'scales')

def _m0231(kind: str, _m0281: float, _m0503: float) -> float:
    g = max(0.0, min(1.0, float(_m0281) / 100.0))
    rim = max(24.0, float(_m0503))
    if kind == 'feather':
        return 16.0 + g * 72.0
    if kind == 'fur':
        _m0203 = 9.5 - g * 5.5
        return max(5.0, rim / max(1.8, _m0203))
    return 14.0 + g * 58.0

def _m0066(value: float, _m0436: float) -> float:
    if _m0436 <= 0.0:
        return 0.0
    return value - math.floor(value / _m0436) * _m0436

def _m0096(_m0208: float, _m0209: float, value: float) -> float:
    if _m0208 == _m0209:
        return 0.0 if value < _m0208 else 1.0
    t = max(0.0, min(1.0, (value - _m0208) / (_m0209 - _m0208)))
    return t * t * (3.0 - 2.0 * t)

def _m0050(ix: int, iy: int) -> float:
    n = ix * 374761393 + iy * 668265263 & 4294967295
    n = (n ^ n >> 13) * 1274126177 & 4294967295
    return (n & 65535) / 65535.0

def _m0036(value: float) -> float:
    return 0.0 if value < 0.0 else 1.0 if value > 1.0 else value

def _m0046(_m0365: float, _m0366: float, _m0347: float, width: float):
    if _m0365 < 0.0 or _m0365 > _m0347:
        return None
    t = _m0365 / _m0347
    if t < 0.16:
        _m0456 = 0.28 + t / 0.16 * 0.72
    else:
        _m0456 = math.sin((1.0 - t) * math.pi * 0.5) ** 0.42
    _m0292 = width * 0.5 * _m0456
    _m0106 = abs(_m0366)
    if _m0106 > _m0292:
        return None
    _m0536 = max(0.8, min(width * 0.08, _m0347 * 0.04))
    _m0535 = 1.0 - _m0096(_m0536 * 0.15, _m0536 * 1.05, _m0106)
    gap = max(2.0, _m0347 * 0.07)
    _m0439 = _m0066(_m0365 - _m0106 * 0.55, gap)
    _m0202 = min(_m0439, gap - _m0439)
    _m0118 = 1.0 - _m0096(0.3, gap * 0.34, _m0202)
    _m0207 = _m0096(_m0292 * 0.72, _m0292, _m0106)
    value = 0.8 - _m0535 * 0.55 - _m0207 * 0.52 - _m0118 * (1.0 - _m0207) * 0.1
    return _m0036(value)

def _m0059(_m0435: float) -> float:
    return 0.55 + 0.74 * (max(0.0, min(100.0, float(_m0435))) / 100.0)

def _m0047(_m0196: float) -> float:
    _m0435 = max(0.0, min(100.0, float(_m0196)))
    return 1.0 + (72.0 - _m0435) * 3.0 / 140.0

def _m0093(u: float, v: float, _m0567: float, _m0568: float, cols: int, rows: int, _m0136: float, _m0137: float) -> float:
    _m0437 = _m0567 * cols
    _m0438 = _m0568 * rows
    _m0592 = _m0066(u, _m0437)
    _m0600 = _m0066(v, _m0438)
    _m0341 = int(math.floor(_m0592 / _m0567)) % cols
    _m0342 = int(math.floor(_m0600 / _m0568)) % rows
    _m0128 = None
    _m0129 = 1000000000.0
    for oy in range(-2, 3):
        for ox in range(-2, 3):
            ix = (_m0341 + ox) % cols
            iy = (_m0342 + oy) % rows
            _m0347 = min(_m0136 * 0.92, _m0136 * (0.62 + 0.28 * _m0050(ix, iy)))
            width = _m0137 * (0.55 + 0.42 * _m0050(ix + 11, iy - 4))
            ang = (_m0050(ix - 2, iy + 6) - 0.5) * 0.16
            _m0343 = (_m0050(ix, iy + 3) - 0.5) * _m0567 * 0.22
            _m0344 = (_m0050(ix + 8, iy) - 0.5) * _m0568 * 0.18
            shift = _m0567 * 0.46 if iy & 1 else 0.0
            _m0510 = _m0066(ix * _m0567 + shift + _m0343, _m0437)
            _m0511 = _m0066(iy * _m0568 + _m0568 * 0.35 + _m0344, _m0438)
            dx = _m0103(_m0592 - _m0510, _m0437)
            dy = _m0103(_m0600 - _m0511, _m0438)
            _m0157 = math.cos(ang)
            _m0517 = math.sin(ang)
            _m0365 = dx * _m0157 + dy * _m0517
            _m0366 = -dx * _m0517 + dy * _m0157
            value = _m0046(_m0365, _m0366, _m0347, width)
            if value is None or _m0365 >= _m0129:
                continue
            _m0129 = _m0365
            _m0128 = value
    return 0.5 if _m0128 is None else _m0128

def _m0103(_m0195: float, _m0436: float) -> float:
    _m0292 = _m0436 * 0.5
    if _m0195 > _m0292:
        return _m0195 - _m0436
    if _m0195 < -_m0292:
        return _m0195 + _m0436
    return _m0195
_m0019: dict = {}

def _m0048(feature: float, _m0436: float, _m0196: float=72.0, _m0347: float=61.0) -> tuple:
    key = (round(feature, 2), round(_m0436, 2), int(_m0196), int(_m0347))
    cached = _m0019.get(key)
    if cached is not None:
        return cached
    d = max(0.0, min(1.0, float(_m0196) / 100.0))
    _m0220 = max(0.0, min(1.0, float(_m0347) / 100.0))
    _m0111 = max(12.0, feature * (0.85 + 0.7 * _m0220))
    _m0107 = max(0.06, 1.02 - 1.04 * d)
    _m0108 = max(1.6, feature * _m0107)
    cols = max(3, int(round(_m0436 / _m0111)))
    rows = max(4, int(round(_m0436 / _m0108)))
    _m0111 = _m0436 / float(cols)
    _m0108 = _m0436 / float(rows)
    _m0244 = 0.34 + 0.28 * _m0220
    _m0245 = 0.18 + 0.22 * _m0220
    _m0291 = []
    for iy in range(rows):
        _m0563 = _m0111 * 0.5 if iy & 1 else 0.0
        for ix in range(cols):
            _m0343 = (_m0050(ix + 2, iy) - 0.5) * _m0111 * 0.1
            _m0344 = (_m0050(ix, iy - 3) - 0.5) * _m0108 * 0.2
            _m0242 = (_m0050(ix - 3, iy + 8) - 0.5) * 0.4
            frac = min(0.92, _m0244 + _m0245 * _m0050(ix, iy))
            _m0291.append((_m0066(ix * _m0111 + _m0563 + _m0343, _m0436), _m0066(iy * _m0108 + _m0108 * 0.5 + _m0344, _m0436), _m0111 * frac, 1.05 + 0.65 * _m0050(ix + 4, iy - 2), math.cos(_m0242), math.sin(_m0242), 0.46 + 0.1 * _m0050(ix - 1, iy + 5)))
    if len(_m0019) > 6:
        _m0019.clear()
    _m0419 = (_m0291, cols, rows, _m0111, _m0108)
    _m0019[key] = _m0419
    return _m0419

def _m0094(u: float, v: float, feature: float, _m0436: float, _m0196: float=72.0, _m0347: float=61.0) -> float:
    _m0291, cols, rows, _m0111, _m0108 = _m0048(feature, _m0436, _m0196, _m0347)
    _m0341 = int(math.floor(_m0066(u, _m0436) / _m0111))
    _m0342 = int(math.floor(_m0066(v, _m0436) / _m0108))
    _m0592 = _m0066(u, _m0436)
    _m0600 = _m0066(v, _m0436)
    _m0316 = 0.0
    for oy in range(-2, 3):
        for ox in range(-2, 2):
            ix = (_m0341 + ox) % cols
            iy = (_m0342 + oy) % rows
            _m0510, _m0511, _m0347, _m0509, _m0157, _m0517, weight = _m0291[iy * cols + ix]
            dx = _m0103(_m0592 - _m0510, _m0436)
            dy = _m0103(_m0600 - _m0511, _m0436)
            _m0110 = dx * _m0157 + dy * _m0517
            _m0106 = -dx * _m0517 + dy * _m0157
            if _m0110 < 0.0 or _m0110 > _m0347:
                continue
            _m0294 = _m0509 * (1.0 - _m0110 / _m0347) ** 0.45
            if _m0294 < 0.45 or abs(_m0106) > _m0294 * 1.25:
                continue
            _m0182 = 1.0 - abs(_m0106) / (_m0294 * 1.25)
            _m0547 = _m0096(0.05, 0.75, _m0106 / max(_m0294, 0.45))
            _m0316 = max(_m0316, _m0182 * weight * (1.0 - _m0547 * 0.35))
    return _m0036(0.5 - _m0316)

def _m0089(_m0435: float) -> float:
    p = max(0.0, min(100.0, float(_m0435)))
    if p >= 61.0:
        return 1.0 + (p - 61.0) * (0.9 / 39.0)
    return 0.38 + p / 61.0 * 0.62

def _m0090(lx: float, ly: float, _m0159: float, _m0158: float, grow: float=1.0, _m0113: float=1.0):
    cx = _m0159 * 0.5
    cy = _m0158 * 0.96
    rx = _m0159 * 0.58 * grow
    ry = _m0158 * 0.9 * grow * _m0113
    _m0406 = (lx - cx) / rx
    _m0407 = (ly - cy) / ry
    _m0202 = math.hypot(_m0406, _m0407)
    if _m0202 >= 1.0:
        return None
    _m0144 = math.sqrt(max(0.0, 1.0 - _m0202 * _m0202))
    rim = _m0096(0.78, 0.98, _m0202)
    light = _m0096(0.05, -0.55, _m0407)
    return _m0036(0.7 + _m0144 * 0.16 + light * 0.08 - rim * 0.62)

def _m0095(u: float, v: float, _m0159: float, _m0158: float, _m0113: float=1.0) -> float:
    row = math.floor(v / _m0158)
    _m0169 = _m0159 * 0.5 if int(row) & 1 else 0.0
    col = math.floor((u + _m0169) / _m0159)
    lx = _m0066(u + _m0169, _m0159)
    ly = _m0066(v, _m0158)
    grow = 0.62 + 0.78 * _m0050(int(col), int(row))
    _m0247 = _m0090(lx, ly, _m0159, _m0158, grow, _m0113)
    _m0454 = 0.0 if int(row) & 1 else _m0159 * 0.5
    _m0450 = math.floor((u + _m0454) / _m0159)
    _m0451 = 0.62 + 0.78 * _m0050(int(_m0450), int(row) - 1)
    _m0449 = _m0090(_m0066(u + _m0454, _m0159), ly + _m0158, _m0159, _m0158, _m0451, _m0113)
    if _m0247 is None:
        return 0.4 if _m0449 is None else _m0449
    if _m0449 is None:
        return _m0247
    return _m0247

def _m0097(_m0141: bytearray, _m0590: int, _m0576: int) -> None:
    src = bytes(_m0141)
    for y in range(_m0576):
        row = y * _m0590
        _m0605 = (y - 1) % _m0576 * _m0590
        _m0606 = (y + 1) % _m0576 * _m0590
        for x in range(_m0590):
            _m0603 = (x - 1) % _m0590
            _m0604 = (x + 1) % _m0590
            _m0105 = src[row + x] * 6 + src[row + _m0603] + src[row + _m0604] + src[_m0605 + x] + src[_m0606 + x]
            _m0141[row + x] = _m0105 // 10

def _m0143(kind: str, _m0281: float, _m0503: float, fur_density: float=72.0, fur_length: float=61.0) -> tuple[bytes, int, int]:
    feature = _m0231(kind, _m0281, _m0503)
    _m0159 = _m0158 = 1.0
    _m0567 = _m0568 = feature
    _m0229 = 4
    _m0230 = 4
    if kind == 'feather':
        _m0136 = max(32, int(round(feature * 2.7)))
        _m0137 = max(12, int(round(feature * 0.72)))
        _m0418 = _m0047(fur_density)
        _m0160 = max(6, int(round(_m0136 * _m0418)))
        _m0161 = max(4, int(round(_m0137 * _m0418)))
        _m0229 = 2
        _m0230 = 2
        _m0567 = float(_m0160)
        _m0568 = float(_m0161)
        _m0590 = _m0160 * _m0229
        _m0576 = _m0161 * _m0230
    elif kind == 'fur':
        _m0547 = max(96, min(200, int(round(feature * 11.0))))
        _m0590 = _m0576 = _m0547
    else:
        _m0159 = max(8.0, feature)
        _m0158 = max(6.0, feature * 0.68)
        _m0590 = max(12, int(round(_m0159)))
        _m0576 = max(16, int(round(_m0158 * 2.0)))
    cap = 200
    if kind != 'feather' and max(_m0590, _m0576) > cap:
        scale = cap / float(max(_m0590, _m0576))
        _m0590 = max(16, int(round(_m0590 * scale)))
        _m0576 = max(16, int(round(_m0576 * scale)))
    if kind == 'scales':
        _m0159 = float(_m0590)
        _m0158 = float(_m0576) / 2.0
    _m0141 = bytearray(_m0590 * _m0576)
    if kind == 'scales':
        for y in range(_m0576):
            row = y * _m0590
            for x in range(_m0590):
                shade = _m0095(x + 0.5, y + 0.5, _m0159, _m0158, _m0089(fur_length))
                _m0141[row + x] = int(shade * 255.0 + 0.5)
    elif kind == 'fur':
        for y in range(_m0576):
            row = y * _m0590
            for x in range(_m0590):
                shade = _m0094(x + 0.5, y + 0.5, feature, float(_m0590), fur_density, fur_length)
                _m0141[row + x] = int(shade * 255.0 + 0.5)
        _m0097(_m0141, _m0590, _m0576)
    else:
        for y in range(_m0576):
            row = y * _m0590
            for x in range(_m0590):
                shade = _m0093(x + 0.5, y + 0.5, _m0567, _m0568, _m0229, _m0230, float(_m0136), float(_m0137))
                _m0141[row + x] = int(shade * 255.0 + 0.5)
    return (bytes(_m0141), _m0590, _m0576)

def _m0067(kind: str, _m0281: float, _m0557: float, _m0580: int) -> float:
    g = max(0.0, min(1.0, float(_m0281) / 100.0))
    _m0557 = max(72.0, float(_m0557))
    _m0580 = max(1, int(_m0580))
    if kind == 'fur':
        _m0436 = max(float(_m0580), _m0557 * (0.14 + g * 0.08))
        return max(1.0, _m0436 / float(_m0580))
    return 1.0

def _m0484(kind: str, width: int, height: int, _m0281: float, _m0503: float, angle_deg: float, _m0411: float=0.0, _m0412: float=0.0, _m0382: int=900000, fur_density: float=72.0, fur_length: float=61.0) -> tuple[bytes, int]:
    _m0579, _m0590, _m0576 = _m0143(kind, _m0281, _m0503, fur_density, fur_length)
    width = max(1, int(width))
    height = max(1, int(height))
    _m0557 = max(float(_m0503), float(min(width, height)))
    _m0332 = 1.0 / _m0067(kind, _m0281, _m0557, _m0590)
    _m0131 = 1
    _m0518 = width * height
    while _m0518 > _m0382:
        _m0131 += 1
        _m0518 = width // _m0131 * (height // _m0131)
    sw = max(1, width // _m0131)
    sh = max(1, height // _m0131)
    rad = math.radians(float(angle_deg))
    _m0157 = math.cos(rad)
    _m0517 = math.sin(rad)
    cx = _m0411 + width * 0.5
    cy = _m0412 + height * 0.5
    _m0282 = bytearray(sw * sh)
    for y in range(sh):
        _m0248 = _m0412 + (y + 0.5) * _m0131 - cy
        row = y * sw
        for x in range(sw):
            fx = _m0411 + (x + 0.5) * _m0131 - cx
            u = fx * _m0157 + _m0248 * _m0517
            v = -fx * _m0517 + _m0248 * _m0157
            tx = int(math.floor(u * _m0332)) % _m0590
            ty = int(math.floor(v * _m0332)) % _m0576
            _m0282[row + x] = _m0579[ty * _m0590 + tx]
    if _m0131 == 1 and sw == width and (sh == height):
        out = bytearray(width * height * 4)
        for i, g in enumerate(_m0282):
            _m0408 = i * 4
            out[_m0408] = g
            out[_m0408 + 1] = g
            out[_m0408 + 2] = g
            out[_m0408 + 3] = 255
        return (bytes(out), _m0131)
    out = bytearray(width * height * 4)
    for y in range(height):
        sy = min(sh - 1, y // _m0131)
        src = sy * sw
        _m0198 = y * width
        for x in range(width):
            g = _m0282[src + min(sw - 1, x // _m0131)]
            _m0408 = (_m0198 + x) * 4
            out[_m0408] = g
            out[_m0408 + 1] = g
            out[_m0408 + 2] = g
            out[_m0408 + 3] = 255
    return (bytes(out), _m0131)
