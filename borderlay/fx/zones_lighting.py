# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
class _m0012:

    @staticmethod
    def _m0427(_m0130, _m0524, _m0608, material='gold', _m0337=True, _m0369=None, _m0371=None, _m0370=None, _m0372=None):
        ox1, oy1, ox2, oy2 = _m0608
        w = float(ox2 - ox1)
        h = float(oy2 - oy1)
        _m0286 = float(_m0369) if _m0369 is not None else float(ox1 + w * 0.14)
        _m0288 = float(_m0371) if _m0371 is not None else float(oy1)
        _m0287 = float(_m0370) if _m0370 is not None else float(ox2 - w * 0.08)
        _m0289 = float(_m0372) if _m0372 is not None else float(oy2)
        if material == 'chrom':
            _m0301 = 236 if _m0337 else 228
            _m0386 = 122 if _m0337 else 116
            _m0354 = 22 if _m0337 else 26
            _m0130._m0235(_m0524, (_m0301, _m0301, _m0301), (_m0386, _m0386, _m0386), (_m0354, _m0354, _m0354), _m0286, _m0288, _m0287, _m0289, _m0433=0.46)
            return
        if material in ('rosegold', 'kupfer'):
            _m0305 = 234 if _m0337 else 222
            _m0389 = 148 if _m0337 else 138
            _m0357 = 52 if _m0337 else 60
            _m0130._m0235(_m0524, (_m0305, _m0305, _m0305), (_m0389, _m0389, _m0389), (_m0357, _m0357, _m0357), _m0286, _m0288, _m0287, _m0289, _m0433=0.48)
            if hasattr(_m0130, 'fill_radial_lobe'):
                _m0130._m0238(_m0524, _m0163=float(ox1 + w * 0.42), _m0164=float(oy1 + h * 0.05), radius=w * 0.6, _m0321=244 if _m0337 else 232, _m0387=192, _m0414=_m0389)
            return
        if material == 'edelstahl':
            _m0306 = 232 if _m0337 else 220
            _m0391 = 136 if _m0337 else 126
            _m0358 = 38 if _m0337 else 46
            _m0130._m0235(_m0524, (_m0306, _m0306, _m0306), (_m0391, _m0391, _m0391), (_m0358, _m0358, _m0358), _m0286, _m0288, _m0287, _m0289, _m0433=0.46)
            if hasattr(_m0130, 'fill_radial_lobe'):
                _m0130._m0238(_m0524, _m0163=float(ox1 + w * 0.4), _m0164=float(oy1 + h * 0.05), radius=w * 0.56, _m0321=242 if _m0337 else 228, _m0387=178, _m0414=_m0391)
            return
        if material == 'aluminium':
            _m0300 = 216 if _m0337 else 204
            _m0384 = 158 if _m0337 else 148
            _m0353 = 94 if _m0337 else 102
            _m0130._m0235(_m0524, (_m0300, _m0300, _m0300), (_m0384, _m0384, _m0384), (_m0353, _m0353, _m0353), _m0286, _m0288, _m0287, _m0289, _m0433=0.5)
            if hasattr(_m0130, 'fill_radial_lobe'):
                _m0130._m0238(_m0524, _m0163=float(ox1 + w * 0.42), _m0164=float(oy1 + h * 0.05), radius=w * 0.5, _m0321=228, _m0387=184, _m0414=_m0384)
            return
        if material == 'titan':
            _m0308 = 226 if _m0337 else 212
            _m0392 = 118 if _m0337 else 108
            _m0359 = 30 if _m0337 else 38
            _m0130._m0235(_m0524, (_m0308, _m0308, _m0308), (_m0392, _m0392, _m0392), (_m0359, _m0359, _m0359), _m0286, _m0288, _m0287, _m0289, _m0433=0.46)
            if hasattr(_m0130, 'fill_radial_lobe'):
                _m0130._m0238(_m0524, _m0163=float(ox1 + w * 0.42), _m0164=float(oy1 + h * 0.05), radius=w * 0.52, _m0321=236 if _m0337 else 220, _m0387=162, _m0414=_m0392)
            return
        if material == 'platinum':
            _m0304 = 240 if _m0337 else 228
            _m0388 = 160 if _m0337 else 148
            _m0356 = 54 if _m0337 else 62
            _m0130._m0235(_m0524, (_m0304, _m0304, _m0304), (_m0388, _m0388, _m0388), (_m0356, _m0356, _m0356), _m0286, _m0288, _m0287, _m0289, _m0433=0.48)
            if hasattr(_m0130, 'fill_radial_lobe'):
                _m0130._m0238(_m0524, _m0163=float(ox1 + w * 0.42), _m0164=float(oy1 + h * 0.05), radius=w * 0.54, _m0321=248 if _m0337 else 236, _m0387=198, _m0414=_m0388)
            return
        _m0307 = 236 if _m0337 else 222
        _m0187 = 128 if _m0337 else 118
        _m0191 = 34 if _m0337 else 40
        _m0130._m0235(_m0524, (184, 184, 184), (_m0187, _m0187, _m0187), (_m0191, _m0191, _m0191), _m0286, _m0288, _m0287, _m0289, _m0433=0.46)
        if hasattr(_m0130, 'fill_radial_lobe'):
            _m0130._m0238(_m0524, _m0163=float(ox1 + w * 0.44), _m0164=float(oy1 + h * 0.04), radius=w * 0.56, _m0321=_m0307, _m0387=172, _m0414=_m0187)
