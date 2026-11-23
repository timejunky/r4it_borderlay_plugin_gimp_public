# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
from config.catalog_metals import GRADMAP_7STOP_PART1, LABELS_METALS_GEMS, METALS_5STOP_PART1
from config.catalog_organic import GRADMAP_7STOP_PART2, LABELS_ORGANIC_SYNTH, METALS_5STOP_PART2
from config.catalog_atelier import GRADMAP_ATELIER, LABELS_ATELIER, METALS_ATELIER, RECIPES_ATELIER
METAL_LABELS = {**LABELS_METALS_GEMS, **LABELS_ORGANIC_SYNTH, **LABELS_ATELIER}
METALS = {**METALS_5STOP_PART1, **METALS_5STOP_PART2, **METALS_ATELIER}
GRADMAP_METALS = {**GRADMAP_7STOP_PART1, **GRADMAP_7STOP_PART2, **GRADMAP_ATELIER}
GRADMAP_POSITIONS = (0.16, 0.34, 0.52, 0.7, 0.86, 1.0)

def sample_grad_stops(stops, count=7):
    src = [tuple(s[:3]) for s in stops] if stops else [(0, 0, 0)]
    if count <= 1:
        return [src[0]]
    if len(src) == count:
        return src
    last = len(src) - 1
    scale255 = max((abs(c) for row in src for c in row)) > 1.5
    out = []
    for i in range(count):
        pos = i / (count - 1) * last
        i0 = int(pos)
        i1 = min(last, i0 + 1)
        frac = pos - i0
        mixed = tuple((src[i0][k] + (src[i1][k] - src[i0][k]) * frac for k in range(3)))
        if scale255:
            mixed = tuple((int(round(c)) for c in mixed))
        out.append(mixed)
    return out

def gradmap_positions(stops):
    n = len(stops)
    if n == 7:
        return GRADMAP_POSITIONS
    segs = max(1, n - 1)
    return tuple((1.0 if i == segs - 1 else round((i + 1) / float(segs), 4) for i in range(segs)))
BUILTIN_GIMP_GRADIENTS = ('none', 'Golden', 'Incandescent', 'Metallic Something', 'Rounded edge', 'Crown molding', 'Browns', 'Copper')
_RECIPE_TABLE = {'gold': ('cone', 48, 84, 84, False, 25, 0, 0, True), 'bronze': ('cone', 44, 82, 86, False, 30, 52, 3, True), 'messing': ('cone', 46, 88, 86, True, 24, 0, 2, True), 'aluminium': ('cone', 58, 64, 76, True, 28, 14, 0, False), 'silber': ('beam', 40, 96, 90, False, 18, 0, 0, True), 'oak_rustic': ('cone', 56, 68, 86, True, 88, 64, 18, False), 'plastic_gloss_red': ('beam', 34, 98, 90, False, 12, 0, 0, True)}
_RECIPE_TABLE.update(RECIPES_ATELIER)
MATERIAL_LIGHT_DEFAULTS = {k: {'light_source': v[0], 'light_spread': v[1], 'glanz': v[2], 'fasenkontrast': v[3], 'angle': 135, 'brushed': v[4], 'brushed_granularity': v[5], 'patina': v[6], 'scratches': v[7], 'luxus': v[8]} for k, v in _RECIPE_TABLE.items()}
MATERIAL_TIERS_ORDER = ('free', 'look', 'atelier')
FREE_MATERIAL_KEYS = ('gold', 'silber', 'aluminium', 'bronze', 'messing', 'oak_rustic', 'plastic_gloss_red')
MATERIAL_DISPLAY_ORDER = tuple(METAL_LABELS.keys())

def _material_group(title, keys):
    keys = tuple(keys)
    return (f'{title} ({len(keys)})', keys)
MATERIAL_CATEGORY_GROUPS = {'all': _material_group('Alle', MATERIAL_DISPLAY_ORDER), 'metals': _material_group('Gold & Kupfer', ('gold', 'bronze', 'messing')), 'chrome': _material_group('Chrom & Stahl', ('aluminium', 'silber')), 'gems': _material_group('Diamant & Juwel', ()), 'woods': _material_group('Holz & Kohle', ('oak_rustic',)), 'leather': _material_group('Leder & Falten', ()), 'stone': _material_group('Stein & Goldadern', ()), 'glass_synth': _material_group('Glas & Plastik', ('plastic_gloss_red',))}
ATELIER_MATERIAL_KEYS = frozenset(MATERIAL_CATEGORY_GROUPS['gems'][1]) | frozenset((key for key in MATERIAL_CATEGORY_GROUPS['glass_synth'][1] if 'glass' in key))
MATERIAL_TIERS = {key: 'free' if key in FREE_MATERIAL_KEYS else 'atelier' if key in ATELIER_MATERIAL_KEYS else 'look' for key in MATERIAL_DISPLAY_ORDER}

def material_allowed(key: str, *, wider: bool, glass: bool) -> bool:
    tier = MATERIAL_TIERS.get(key, 'atelier')
    if tier == 'free':
        return True
    if tier == 'look':
        return bool(wider)
    return bool(glass)
_COMMUNITY_KEYS = tuple(FREE_MATERIAL_KEYS)
MATERIAL_DISPLAY_ORDER = _COMMUNITY_KEYS
MATERIAL_CATEGORY_GROUPS = {'all': (f'Alle ({len(_COMMUNITY_KEYS)})', _COMMUNITY_KEYS)}
METAL_LABELS = {key: METAL_LABELS[key] for key in _COMMUNITY_KEYS if key in METAL_LABELS}
MATERIAL_LIGHT_DEFAULTS = {key: MATERIAL_LIGHT_DEFAULTS[key] for key in _COMMUNITY_KEYS if key in MATERIAL_LIGHT_DEFAULTS}
MATERIAL_TIERS = {key: 'free' for key in _COMMUNITY_KEYS}
