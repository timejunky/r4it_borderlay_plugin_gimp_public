# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
class _m0011:

    @staticmethod
    def _m0392(_m0112, _m0483, _m0562, material='gold', _m0305=True, _m0335=None, _m0337=None, _m0336=None, _m0338=None):
        ox1, oy1, ox2, oy2 = _m0562
        w = float(ox2 - ox1)
        h = float(oy2 - oy1)
        _m0257 = float(_m0335) if _m0335 is not None else float(ox1 + w * 0.14)
        _m0259 = float(_m0337) if _m0337 is not None else float(oy1)
        _m0258 = float(_m0336) if _m0336 is not None else float(ox2 - w * 0.08)
        _m0260 = float(_m0338) if _m0338 is not None else float(oy2)
        if material == 'chrom':
            _m0271 = 236 if _m0305 else 228
            _m0351 = 122 if _m0305 else 116
            _m0320 = 22 if _m0305 else 26
            _m0112._m0210(_m0483, (_m0271, _m0271, _m0271), (_m0351, _m0351, _m0351), (_m0320, _m0320, _m0320), _m0257, _m0259, _m0258, _m0260, _m0398=0.46)
            return
        if material in ('rosegold', 'kupfer'):
            _m0275 = 234 if _m0305 else 222
            _m0354 = 148 if _m0305 else 138
            _m0323 = 52 if _m0305 else 60
            _m0112._m0210(_m0483, (_m0275, _m0275, _m0275), (_m0354, _m0354, _m0354), (_m0323, _m0323, _m0323), _m0257, _m0259, _m0258, _m0260, _m0398=0.48)
            if hasattr(_m0112, 'fill_radial_lobe'):
                _m0112._m0213(_m0483, _m0144=float(ox1 + w * 0.42), _m0145=float(oy1 + h * 0.05), radius=w * 0.6, _m0291=244 if _m0305 else 232, _m0352=192, _m0379=_m0354)
            return
        if material == 'edelstahl':
            _m0276 = 232 if _m0305 else 220
            _m0356 = 136 if _m0305 else 126
            _m0324 = 38 if _m0305 else 46
            _m0112._m0210(_m0483, (_m0276, _m0276, _m0276), (_m0356, _m0356, _m0356), (_m0324, _m0324, _m0324), _m0257, _m0259, _m0258, _m0260, _m0398=0.46)
            if hasattr(_m0112, 'fill_radial_lobe'):
                _m0112._m0213(_m0483, _m0144=float(ox1 + w * 0.4), _m0145=float(oy1 + h * 0.05), radius=w * 0.56, _m0291=242 if _m0305 else 228, _m0352=178, _m0379=_m0356)
            return
        if material == 'aluminium':
            _m0270 = 216 if _m0305 else 204
            _m0349 = 158 if _m0305 else 148
            _m0319 = 94 if _m0305 else 102
            _m0112._m0210(_m0483, (_m0270, _m0270, _m0270), (_m0349, _m0349, _m0349), (_m0319, _m0319, _m0319), _m0257, _m0259, _m0258, _m0260, _m0398=0.5)
            if hasattr(_m0112, 'fill_radial_lobe'):
                _m0112._m0213(_m0483, _m0144=float(ox1 + w * 0.42), _m0145=float(oy1 + h * 0.05), radius=w * 0.5, _m0291=228, _m0352=184, _m0379=_m0349)
            return
        if material == 'titan':
            _m0278 = 226 if _m0305 else 212
            _m0357 = 118 if _m0305 else 108
            _m0325 = 30 if _m0305 else 38
            _m0112._m0210(_m0483, (_m0278, _m0278, _m0278), (_m0357, _m0357, _m0357), (_m0325, _m0325, _m0325), _m0257, _m0259, _m0258, _m0260, _m0398=0.46)
            if hasattr(_m0112, 'fill_radial_lobe'):
                _m0112._m0213(_m0483, _m0144=float(ox1 + w * 0.42), _m0145=float(oy1 + h * 0.05), radius=w * 0.52, _m0291=236 if _m0305 else 220, _m0352=162, _m0379=_m0357)
            return
        if material == 'platinum':
            _m0274 = 240 if _m0305 else 228
            _m0353 = 160 if _m0305 else 148
            _m0322 = 54 if _m0305 else 62
            _m0112._m0210(_m0483, (_m0274, _m0274, _m0274), (_m0353, _m0353, _m0353), (_m0322, _m0322, _m0322), _m0257, _m0259, _m0258, _m0260, _m0398=0.48)
            if hasattr(_m0112, 'fill_radial_lobe'):
                _m0112._m0213(_m0483, _m0144=float(ox1 + w * 0.42), _m0145=float(oy1 + h * 0.05), radius=w * 0.54, _m0291=248 if _m0305 else 236, _m0352=198, _m0379=_m0353)
            return
        _m0277 = 236 if _m0305 else 222
        _m0166 = 128 if _m0305 else 118
        _m0170 = 34 if _m0305 else 40
        _m0112._m0210(_m0483, (184, 184, 184), (_m0166, _m0166, _m0166), (_m0170, _m0170, _m0170), _m0257, _m0259, _m0258, _m0260, _m0398=0.46)
        if hasattr(_m0112, 'fill_radial_lobe'):
            _m0112._m0213(_m0483, _m0144=float(ox1 + w * 0.44), _m0145=float(oy1 + h * 0.04), radius=w * 0.56, _m0291=_m0277, _m0352=172, _m0379=_m0166)
