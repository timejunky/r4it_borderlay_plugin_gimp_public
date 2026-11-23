# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
_m0025 = ('gold', 'silber', 'aluminium', 'bronze', 'messing', 'oak_rustic', 'plastic_gloss_red')
_m0021 = frozenset(_m0025)
_m0022 = {'gold': 'Gold 24k (Warmes Feingold)', 'silber': 'Silber (925 Sterling)', 'aluminium': 'Aluminium (Eloxiert Matt)', 'bronze': 'Antik-Bronze (Guss-Patina)', 'messing': 'Messing (Polished Brass)', 'oak_rustic': 'Rustikale Alteiche (Tief gebürstet)', 'plastic_gloss_red': 'Hochglanz-ABS-Plastik (Signalrot)'}
_m0024 = {'gold': ((32, 18, 5), (98, 62, 18), (178, 128, 52), (236, 194, 108), (255, 248, 220)), 'silber': ((40, 48, 58), (96, 108, 122), (160, 174, 190), (214, 224, 234), (248, 252, 255)), 'aluminium': ((78, 82, 86), (132, 136, 140), (168, 172, 176), (196, 200, 204), (220, 224, 228)), 'bronze': ((26, 15, 6), (82, 50, 22), (152, 98, 46), (212, 156, 86), (250, 224, 168)), 'messing': ((30, 22, 4), (96, 74, 16), (178, 144, 42), (236, 208, 98), (255, 250, 218)), 'oak_rustic': ((42, 38, 28), (86, 78, 58), (128, 116, 88), (168, 156, 124), (206, 196, 168)), 'plastic_gloss_red': ((36, 4, 6), (108, 12, 16), (196, 24, 30), (244, 78, 82), (255, 238, 238))}
_m0020 = {'gold': ((28, 15, 4), (66, 40, 14), (128, 84, 34), (186, 138, 66), (228, 184, 100), (248, 224, 170), (255, 252, 238)), 'silber': ((36, 44, 56), (88, 102, 118), (150, 166, 184), (206, 218, 230), (246, 250, 255)), 'aluminium': ((72, 76, 80), (124, 128, 132), (164, 168, 172), (196, 200, 204), (224, 228, 232)), 'bronze': ((28, 17, 7), (72, 45, 20), (128, 84, 38), (178, 124, 62), (218, 164, 92), (242, 202, 138), (255, 240, 196)), 'messing': ((28, 20, 4), (78, 58, 12), (146, 114, 28), (202, 168, 58), (236, 208, 104), (250, 234, 168), (255, 252, 232)), 'oak_rustic': ((36, 32, 24), (78, 70, 52), (124, 112, 84), (170, 158, 126), (210, 200, 172)), 'plastic_gloss_red': ((28, 3, 4), (78, 8, 12), (148, 16, 22), (212, 28, 34), (242, 68, 72), (252, 158, 160), (255, 248, 248))}
_m0023 = {'gold': {'light_source': 'cone', 'light_spread': 48, 'glanz': 84, 'fasenkontrast': 84, 'angle': 135, 'brushed': False, 'brushed_granularity': 25, 'patina': 0, 'scratches': 0, 'luxus': True}, 'silber': {'light_source': 'beam', 'light_spread': 40, 'glanz': 96, 'fasenkontrast': 90, 'angle': 135, 'brushed': False, 'brushed_granularity': 18, 'patina': 0, 'scratches': 0, 'luxus': True}, 'aluminium': {'light_source': 'cone', 'light_spread': 58, 'glanz': 64, 'fasenkontrast': 76, 'angle': 135, 'brushed': True, 'brushed_granularity': 28, 'patina': 14, 'scratches': 0, 'luxus': False}, 'bronze': {'light_source': 'cone', 'light_spread': 44, 'glanz': 82, 'fasenkontrast': 86, 'angle': 135, 'brushed': False, 'brushed_granularity': 30, 'patina': 52, 'scratches': 3, 'luxus': True}, 'messing': {'light_source': 'cone', 'light_spread': 46, 'glanz': 88, 'fasenkontrast': 86, 'angle': 135, 'brushed': True, 'brushed_granularity': 24, 'patina': 0, 'scratches': 2, 'luxus': True}, 'oak_rustic': {'light_source': 'cone', 'light_spread': 56, 'glanz': 68, 'fasenkontrast': 86, 'angle': 135, 'brushed': True, 'brushed_granularity': 88, 'patina': 64, 'scratches': 18, 'luxus': False}, 'plastic_gloss_red': {'light_source': 'beam', 'light_spread': 34, 'glanz': 98, 'fasenkontrast': 90, 'angle': 135, 'brushed': False, 'brushed_granularity': 12, 'patina': 0, 'scratches': 0, 'luxus': True}}

def apply_community_materials():
    import config
    import config.materials
    labels = dict(_m0022)
    _m0383 = {key: tuple((tuple(channel) for channel in stops)) for key, stops in _m0024.items()}
    _m0278 = {key: tuple((tuple(channel) for channel in stops)) for key, stops in _m0020.items()}
    light = {key: dict(values) for key, values in _m0023.items()}
    _m0578 = {key: 'free' for key in _m0025}
    _m0285 = {'all': ('Alle (%d)' % len(_m0025), _m0025)}
    for module in (config, config.materials):
        module.METAL_LABELS = labels
        module.METALS = _m0383
        module.GRADMAP_METALS = _m0278
        module.MATERIAL_LIGHT_DEFAULTS = light
        module.MATERIAL_DISPLAY_ORDER = _m0025
        module.MATERIAL_TIERS = _m0578
        module.MATERIAL_CATEGORY_GROUPS = _m0285
        module.FREE_MATERIAL_KEYS = _m0025

    def _m0027(key, **_m0051):
        return str(key or '') in _m0021
    config.material_allowed = _m0027
    config.materials.material_allowed = _m0027

def community_material_key(key):
    apply_community_materials()
    text = str(key or 'gold')
    if text in _m0021:
        return text
    return 'gold'
