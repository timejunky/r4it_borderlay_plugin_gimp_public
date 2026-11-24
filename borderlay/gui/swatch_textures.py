# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import math
import cairo

class SwatchTextureArtist:

    @staticmethod
    def rounded_top_left_path(cr, x: float, y: float, sz: int, r: float):
        eff_r = max(0.0, min(float(r), float(sz - x - 1), float(sz - y - 1)))
        if eff_r <= 0.5:
            cr.rectangle(x, y, sz - x, sz - y)
            return
        cr.new_sub_path()
        cr.arc(x + eff_r, y + eff_r, eff_r, math.pi, 1.5 * math.pi)
        cr.line_to(sz, y)
        cr.line_to(sz, sz)
        cr.line_to(x, sz)
        cr.close_path()

    @classmethod
    def draw_characteristic_texture(cls, cr, mat_key: str, sz: int, ox: float, oy: float, thick: float):
        if mat_key in ('zebra_wood', 'wenge_wood'):
            dark = (0.12, 0.06, 0.02, 0.72) if mat_key == 'wenge_wood' else (0.16, 0.08, 0.03, 0.78)
            light = (0.85, 0.72, 0.48, 0.45) if mat_key == 'zebra_wood' else (0.45, 0.32, 0.18, 0.35)
            for i, gy in enumerate(range(int(oy), sz, 4)):
                cr.set_source_rgba(*(dark if i % 2 == 0 else light))
                cr.rectangle(ox, gy, sz - ox, 2.2)
                cr.fill()
            return
        if mat_key in ('shagreen', 'ostrich_leather', 'python_leather', 'croc_emboss'):
            cr.set_source_rgba(0.05, 0.05, 0.04, 0.55)
            step = 5 if mat_key != 'shagreen' else 4
            radius = 1.6 if mat_key == 'ostrich_leather' else 1.0
            for py in range(int(oy) + 3, sz, step):
                shift = 2 if py // step % 2 == 0 else 0
                for px in range(int(ox) + 3, sz, step):
                    cr.arc(px + shift, py, radius, 0, 2.0 * math.pi)
                    cr.fill()
            return
        if mat_key in ('opal_white', 'abalone', 'labradorite', 'moonstone'):
            flecks = ((1.0, 0.45, 0.7, 0.55), (0.35, 0.85, 0.75, 0.5), (0.45, 0.55, 1.0, 0.45))
            for i, (px, py) in enumerate(((ox + 10, oy + 12), (ox + 24, oy + 18), (ox + 16, oy + 30))):
                cr.set_source_rgba(*flecks[i % 3])
                cr.arc(px, py, 4.5, 0, 2.0 * math.pi)
                cr.fill()
            return
        if mat_key in ('urushi_black', 'urushi_green', 'urushi_red', 'pearl_lacquer', 'onyx_black'):
            cr.set_source_rgba(1.0, 1.0, 1.0, 0.82)
            cr.move_to(ox + 2, oy + 16)
            cr.line_to(ox + 30, oy + 2)
            cr.line_to(ox + 36, oy + 2)
            cr.line_to(ox + 2, oy + 22)
            cr.close_path()
            cr.fill()
            return
        if mat_key == 'ebony_gold':
            cr.set_source_rgba(0.98, 0.78, 0.22, 0.95)
            cr.set_line_width(1.15)
            for px, py, w in ((ox + 8, oy + 18, 10), (ox + 22, oy + 11, 7), (ox + 16, oy + 30, 12), (ox + 34, oy + 22, 8)):
                cr.move_to(px, py)
                cr.line_to(px + w, py - 3)
                cr.stroke()
            return
        if mat_key == 'leather_nappa_black':
            cr.set_source_rgba(0.75, 0.84, 0.96, 0.35)
            for py in range(int(oy) + 4, sz - 2, 3):
                for px in range(int(ox) + 4, sz - 2, 3):
                    cr.arc(px, py, 0.7, 0, 2.0 * math.pi)
                    cr.fill()
            cr.set_source_rgba(0.92, 0.96, 1.0, 0.55)
            cr.set_line_width(1.6)
            cr.move_to(ox + 2, oy + 14)
            cr.line_to(ox + 28, oy + 4)
            cr.stroke()
            return
        if mat_key == 'malachite':
            for i, gy in enumerate(range(int(oy), sz, 5)):
                cr.set_source_rgba(0.05, 0.28, 0.16, 0.55 if i % 2 == 0 else 0.28)
                cr.rectangle(ox, gy, sz - ox, 2.4)
                cr.fill()
            return
        if mat_key == 'teak_wood':
            cr.set_line_width(1.1)
            for i, gy in enumerate(range(int(oy) + 3, sz, 4)):
                cr.set_source_rgba(0.28, 0.12, 0.02, 0.55 if i % 2 == 0 else 0.22)
                cr.move_to(ox, gy)
                cr.line_to(sz, gy + 1)
                cr.stroke()
            return
        if mat_key == 'jade_stone':
            cr.set_source_rgba(0.72, 0.95, 0.78, 0.35)
            cr.arc(ox + 16, oy + 18, 9, 0, 2.0 * math.pi)
            cr.fill()
            cr.arc(ox + 30, oy + 12, 6, 0, 2.0 * math.pi)
            cr.fill()
            return
        if mat_key == 'blued_steel':
            cr.set_source_rgba(0.15, 0.35, 0.72, 0.45)
            cr.rectangle(ox, oy, sz - ox, sz - oy)
            cr.fill()
            cr.set_source_rgba(0.75, 0.88, 1.0, 0.7)
            cr.move_to(ox, oy + 20)
            cr.line_to(ox + 36, oy + 2)
            cr.line_to(ox + 40, oy + 2)
            cr.line_to(ox, oy + 24)
            cr.close_path()
            cr.fill()
            return
        if mat_key == 'pewter':
            cr.set_source_rgba(0.25, 0.28, 0.24, 0.45)
            for py in range(int(oy) + 3, sz, 4):
                for px in range(int(ox) + 3, sz, 4):
                    if (px + py) % 8 == 0:
                        cr.arc(px, py, 1.1, 0, 2.0 * math.pi)
                        cr.fill()
            return
        if mat_key in ('marble_portoro_gold', 'lapis_gold_veins', 'slate_kintsugi', 'leather_vintage_gold', 'venetian_gold_glass', 'gold_veined'):
            cr.set_source_rgba(1.0, 0.84, 0.28, 0.88)
            cr.set_line_width(1.35)
            cr.move_to(ox + 4, oy + 28)
            cr.curve_to(ox + 16, oy + 22, ox + 20, oy + 14, ox + 36, oy + 6)
            cr.stroke()
            cr.set_line_width(0.85)
            cr.move_to(ox + 18, oy + 20)
            cr.line_to(ox + 28, oy + 26)
            cr.stroke()
            if mat_key not in ('ebony_gold', 'leather_vintage_gold'):
                return
        if mat_key in ('diamond_white', 'diamond_black', 'emerald_cut', 'ruby_star', 'sapphire_cut', 'amethyst_cut', 'carnelian'):
            cr.set_source_rgba(1.0, 1.0, 1.0, 0.55)
            wedges = ((ox + 4, oy + 28, ox + 22, oy + 6, ox + 8, oy + 8), (ox + 18, oy + 8, ox + 40, oy + 4, ox + 34, oy + 22), (ox + 10, oy + 34, ox + 28, oy + 18, ox + 36, oy + 36))
            for ax, ay, bx, by, cx, cy in wedges:
                cr.move_to(ax, ay)
                cr.line_to(bx, by)
                cr.line_to(cx, cy)
                cr.close_path()
                cr.fill()
            sparks = {'diamond_white': ((0.25, 0.95, 1.0, 0.9), (1.0, 0.25, 0.7, 0.9)), 'emerald_cut': ((0.95, 0.78, 0.22, 0.9), (0.55, 1.0, 0.75, 0.7)), 'ruby_star': ((1.0, 1.0, 1.0, 0.95), (1.0, 0.7, 0.75, 0.5)), 'sapphire_cut': ((0.55, 0.75, 1.0, 0.9), (1.0, 1.0, 1.0, 0.85)), 'amethyst_cut': ((0.85, 0.6, 1.0, 0.85), (1.0, 1.0, 1.0, 0.8)), 'carnelian': ((1.0, 0.55, 0.2, 0.85), (1.0, 0.85, 0.6, 0.55))}.get(mat_key, ((1.0, 1.0, 1.0, 0.9), (0.9, 0.95, 1.0, 0.6)))
            for rgba, px, py, radius in ((sparks[0], ox + 14, oy + 14, 1.7), (sparks[1], ox + 27, oy + 20, 1.3), (sparks[0], ox + 20, oy + 31, 1.1)):
                cr.set_source_rgba(*rgba)
                cr.arc(px, py, radius, 0, 2.0 * math.pi)
                cr.fill()
            if mat_key == 'ruby_star':
                cr.set_source_rgba(1.0, 1.0, 1.0, 0.85)
                cr.set_line_width(1.1)
                cr.move_to(ox + 6, oy + 30)
                cr.line_to(ox + 34, oy + 8)
                cr.move_to(ox + 8, oy + 10)
                cr.line_to(ox + 32, oy + 32)
                cr.stroke()
            return
        if mat_key in ('charcoal_matte', 'charcoal_ember'):
            cr.set_line_width(1.2)
            if mat_key == 'charcoal_ember':
                cr.set_source_rgba(1.0, 0.38, 0.05, 0.92)
            else:
                cr.set_source_rgba(0.02, 0.02, 0.03, 0.78)
            for step in range(10, 46, 9):
                cr.move_to(ox + 3, oy + step)
                cr.line_to(ox + step + 4, oy + 3)
                cr.stroke()
            return
        if mat_key == 'carbon_fiber':
            for py in range(int(oy), sz, 4):
                for px in range(int(ox), sz, 4):
                    if (px + py) // 4 % 2 == 0:
                        cr.set_source_rgba(0.04, 0.05, 0.07, 0.58)
                    else:
                        cr.set_source_rgba(0.65, 0.72, 0.82, 0.3)
                    cr.rectangle(px, py, 3.6, 1.8)
                    cr.fill()
            return
        if mat_key == 'chrom':
            cr.set_source_rgba(0.02, 0.04, 0.09, 0.78)
            cr.move_to(ox, oy + 16)
            cr.line_to(ox + 26, oy)
            cr.line_to(ox + 40, oy)
            cr.line_to(ox, oy + 30)
            cr.close_path()
            cr.fill()
            cr.set_source_rgba(0.88, 0.96, 1.0, 0.92)
            cr.move_to(ox, oy + 31)
            cr.line_to(ox + 41, oy)
            cr.line_to(ox + 49, oy)
            cr.line_to(ox, oy + 39)
            cr.close_path()
            cr.fill()
            return
        if mat_key == 'schwarzchrom':
            cr.set_source_rgba(0.02, 0.03, 0.05, 0.62)
            cr.rectangle(ox, oy, sz - ox, sz - oy)
            cr.fill()
            cr.set_source_rgba(0.82, 0.9, 1.0, 0.75)
            cr.move_to(ox, oy + 24)
            cr.line_to(ox + 34, oy)
            cr.line_to(ox + 39, oy)
            cr.line_to(ox, oy + 29)
            cr.close_path()
            cr.fill()
            return
        if mat_key in ('edelstahl', 'damast_steel'):
            cr.set_line_width(1.1 if mat_key == 'damast_steel' else 0.9)
            for i in range(-14, sz, 2 if mat_key == 'edelstahl' else 3):
                if i % 4 == 0:
                    cr.set_source_rgba(1.0, 1.0, 1.0, 0.36)
                else:
                    cr.set_source_rgba(0.06, 0.08, 0.11, 0.32)
                cr.move_to(ox, oy + i)
                cr.line_to(ox + i + 30, oy)
                cr.stroke()
            return
        if mat_key == 'titan':
            cr.set_source_rgba(0.06, 0.09, 0.16, 0.34)
            cr.rectangle(ox, oy, sz - ox, sz - oy)
            cr.fill()
            cr.set_line_width(0.75)
            for i in range(int(oy) + 2, sz, 3):
                cr.set_source_rgba(0.78, 0.86, 1.0, 0.22 if i % 2 == 0 else 0.08)
                cr.move_to(ox, i)
                cr.line_to(sz, i)
                cr.stroke()
            return
        if mat_key == 'aluminium':
            cr.set_source_rgba(0.82, 0.85, 0.9, 0.24)
            cr.rectangle(ox, oy, sz - ox, sz - oy)
            cr.fill()
            for py in range(int(oy) + 2, sz, 3):
                for px in range(int(ox) + 2, sz, 3):
                    cr.set_source_rgba(0.25, 0.28, 0.32, 0.14 if (px + py) % 2 == 0 else 0.05)
                    cr.rectangle(px, py, 1.2, 1.2)
                    cr.fill()
            return
        if mat_key in ('platinum', 'champagne_gold'):
            cr.set_source_rgba(1.0, 0.94, 0.82, 0.22)
            cr.rectangle(ox, oy, sz - ox, sz - oy)
            cr.fill()
            return
        if mat_key == 'silber':
            rad = cairo.RadialGradient(ox + 14, oy + 14, 1.5, ox + 16, oy + 16, 26.0)
            rad.add_color_stop_rgba(0.0, 1.0, 1.0, 1.0, 0.85)
            rad.add_color_stop_rgba(0.5, 0.92, 0.95, 1.0, 0.3)
            rad.add_color_stop_rgba(1.0, 0.8, 0.84, 0.9, 0.0)
            cr.set_source(rad)
            cr.rectangle(ox, oy, sz - ox, sz - oy)
            cr.fill()
            return
        if mat_key in ('cherry_wood', 'oak_rustic', 'mahogany_royal', 'bamboo_zen', 'driftwood_ash'):
            cr.set_line_width(1.35)
            for r_step in range(8, 62, 5):
                cr.set_source_rgba(0.18, 0.04, 0.02, 0.46 if r_step % 10 == 3 else 0.24)
                cr.arc(ox + 54, oy + 54, float(r_step), math.pi, 1.52 * math.pi)
                cr.stroke()
            return
        if mat_key in ('walnut_burl', 'olive_wood'):
            cr.set_source_rgba(0.16, 0.08, 0.02, 0.28)
            cr.rectangle(ox, oy, sz - ox, sz - oy)
            cr.fill()
            burl_knots = ((ox + 14, oy + 13, 6.0), (ox + 34, oy + 11, 4.8), (ox + 12, oy + 33, 5.2), (ox + 25, oy + 23, 4.0), (ox + 44, oy + 16, 4.5))
            for kx, ky, kr in burl_knots:
                rad = cairo.RadialGradient(kx, ky, 0.7, kx, ky, kr)
                if mat_key == 'walnut_burl':
                    rad.add_color_stop_rgba(0.0, 0.18, 0.02, 0.06, 0.88)
                    rad.add_color_stop_rgba(0.55, 0.32, 0.08, 0.12, 0.46)
                else:
                    rad.add_color_stop_rgba(0.0, 0.05, 0.16, 0.02, 0.82)
                    rad.add_color_stop_rgba(0.55, 0.2, 0.28, 0.06, 0.48)
                rad.add_color_stop_rgba(1.0, 0.45, 0.24, 0.1, 0.0)
                cr.set_source(rad)
                cr.arc(kx, ky, kr, 0, 2.0 * math.pi)
                cr.fill()
            return
        if mat_key in ('saddle_leather', 'leather_creased', 'leather_vintage_gold', 'leather_oxblood', 'leather_suede', 'leather_cognac'):
            cr.set_source_rgba(0.12, 0.04, 0.01, 0.42)
            for py in range(int(oy) + 3, sz - 2, 4):
                for px in range(int(ox) + 3, sz - 2, 4):
                    shift = 2 if py % 8 == 0 else 0
                    cr.arc(px + shift, py, 1.05, 0, 2.0 * math.pi)
                    cr.fill()
            if mat_key in ('leather_creased', 'leather_cognac', 'leather_oxblood'):
                cr.set_source_rgba(0.04, 0.02, 0.01, 0.48)
                cr.set_line_width(1.4)
                for f_off in (16, 28, 40):
                    cr.move_to(ox + 2, oy + f_off)
                    cr.curve_to(ox + f_off * 0.5, oy + f_off * 0.6, ox + f_off * 0.7, oy + f_off * 0.3, ox + f_off, oy + 2)
                    cr.stroke()
            cr.set_source_rgba(0.98, 0.86, 0.66, 0.88)
            cr.set_line_width(1.35)
            cr.set_dash([3.2, 2.4])
            cls.rounded_top_left_path(cr, ox + thick * 0.46, oy + thick * 0.46, sz, 11.0)
            cr.stroke()
            cr.set_dash([])
            return
        if mat_key in ('bronze', 'kupfer_patina', 'granite_obsidian'):
            cr.set_source_rgba(0.09, 0.05, 0.01, 0.4)
            for py in range(int(oy) + 2, sz, 3):
                for px in range(int(ox) + 2, sz, 3):
                    if (px * 3 + py) % 4 == 0:
                        cr.rectangle(px, py, 1.4, 1.4)
                        cr.fill()
            return
        if mat_key in ('colored_glass', 'frosted_milk_glass', 'smoked_obsidian_glass', 'plastic_gloss_red', 'plastic_cyber_cyan', 'amber_glass'):
            cr.set_source_rgba(1.0, 1.0, 1.0, 0.42 if mat_key == 'frosted_milk_glass' else 0.72)
            cr.move_to(ox + 3, oy + 24)
            cr.line_to(ox + 26, oy + 3)
            cr.line_to(ox + 35, oy + 3)
            cr.line_to(ox + 3, oy + 33)
            cr.close_path()
            cr.fill()
