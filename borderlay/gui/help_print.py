# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
from __future__ import annotations
import html
import re
from pathlib import Path
import cairo
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gdk, GdkPixbuf, Gtk, Pango
from config import COPYRIGHT_YEAR, PLUGIN_VERSION
from locales.i18n import get_all_help_topics, t
_BRAND = Path(__file__).resolve().parents[1] / 'assets' / 'brand'
_PRINT_HEADER_PT = 68.0
_PRINT_LOGO_PT = 46.0
_PRINT_FOOTER_PT = 24.0
PRODUCT_PAGE_URL = 'https://www.ready-4-it.com/borderlay-studio'
WEBSITE_URL = 'https://www.ready-4-it.com'
_QR_ITEMS = (('Borderlay Studio', PRODUCT_PAGE_URL, ('https://www.ready-4-it.com/', 'borderlay-studio')), ('ready-4-it.com', WEBSITE_URL, ('https://www.ready-4-it.com',)))
_QR_SPECS = ((1, 16, 1, 10, ()), (2, 28, 1, 16, (18,)), (3, 44, 1, 26, (22,)), (4, 64, 2, 18, (26,)))
_QR_CACHE: dict[str, list[list[int]]] = {}

def _gf_tables() -> tuple[list[int], list[int]]:
    exp = [0] * 512
    log = [0] * 256
    val = 1
    for idx in range(255):
        exp[idx] = val
        log[val] = idx
        val <<= 1
        if val & 256:
            val ^= 285
    for idx in range(255, 512):
        exp[idx] = exp[idx - 255]
    return (exp, log)
_GF_EXP, _GF_LOG = _gf_tables()

def _gf_mul(left: int, right: int) -> int:
    if left == 0 or right == 0:
        return 0
    return _GF_EXP[_GF_LOG[left] + _GF_LOG[right]]

def _rs_generator(ec_len: int) -> list[int]:
    poly = [1]
    for idx in range(ec_len):
        factor = [1, _GF_EXP[idx]]
        nxt = [0] * (len(poly) + 1)
        for pi, pv in enumerate(poly):
            for fi, fv in enumerate(factor):
                nxt[pi + fi] ^= _gf_mul(pv, fv)
        poly = nxt
    return poly

def _rs_remainder(data: list[int], ec_len: int) -> list[int]:
    gen = _rs_generator(ec_len)
    reg = [0] * ec_len
    for byte in data:
        lead = byte ^ reg[0]
        reg = reg[1:] + [0]
        if lead:
            for idx in range(ec_len):
                reg[idx] ^= _gf_mul(gen[idx + 1], lead)
    return reg

def _qr_data_bytes(payload: bytes, data_cw: int) -> list[int]:
    bits = [0, 1, 0, 0] + [len(payload) >> s & 1 for s in range(7, -1, -1)]
    for byte in payload:
        bits.extend((byte >> s & 1 for s in range(7, -1, -1)))
    bits.extend([0] * min(4, data_cw * 8 - len(bits)))
    bits.extend([0] * (-len(bits) % 8))
    data = [sum((bits[pos + off] << 7 - off for off in range(8))) for pos in range(0, len(bits), 8)]
    pads = (236, 17)
    while len(data) < data_cw:
        data.append(pads[len(data) - len(bits) // 8 & 1])
    return data

def _qr_codewords(payload: bytes) -> tuple[int, tuple[int, ...], list[int]]:
    spec = next((row for row in _QR_SPECS if len(payload) <= row[1] - 2), None)
    if spec is None:
        raise ValueError('QR payload exceeds version 4 capacity')
    ver, data_cw, blocks, ec_len, align = spec
    data = _qr_data_bytes(payload, data_cw)
    chunk = data_cw // blocks
    d_blocks = [data[i * chunk:(i + 1) * chunk] for i in range(blocks)]
    e_blocks = [_rs_remainder(blk, ec_len) for blk in d_blocks]
    out = [blk[pos] for pos in range(chunk) for blk in d_blocks]
    out.extend((blk[pos] for pos in range(ec_len) for blk in e_blocks))
    return (ver, align, out)

def _place_finder(grid: list[list[int]], fixed: list[list[bool]], r0: int, c0: int) -> None:
    size = len(grid)
    for dr in range(-1, 8):
        for dc in range(-1, 8):
            rr, cc = (r0 + dr, c0 + dc)
            if not (0 <= rr < size and 0 <= cc < size):
                continue
            on_border = dr in (0, 6) and 0 <= dc <= 6 or (dc in (0, 6) and 0 <= dr <= 6)
            in_core = 2 <= dr <= 4 and 2 <= dc <= 4
            grid[rr][cc] = 1 if on_border or in_core else 0
            fixed[rr][cc] = True

def _place_alignment(grid: list[list[int]], fixed: list[list[bool]], cr: int, cc: int) -> None:
    for dr in range(-2, 3):
        for dc in range(-2, 3):
            dark = max(abs(dr), abs(dc)) != 1
            grid[cr + dr][cc + dc] = 1 if dark else 0
            fixed[cr + dr][cc + dc] = True

def _place_functions(ver: int, align: tuple[int, ...]) -> tuple[list[list[int]], list[list[bool]]]:
    size = 17 + 4 * ver
    grid = [[0] * size for _ in range(size)]
    fixed = [[False] * size for _ in range(size)]
    for r0, c0 in ((0, 0), (0, size - 7), (size - 7, 0)):
        _place_finder(grid, fixed, r0, c0)
    for idx in range(8, size - 8):
        bit = 1 if idx % 2 == 0 else 0
        grid[6][idx] = bit
        fixed[6][idx] = True
        grid[idx][6] = bit
        fixed[idx][6] = True
    for pos in align:
        _place_alignment(grid, fixed, pos, pos)
    grid[size - 8][8] = 1
    fixed[size - 8][8] = True
    for idx in range(9):
        fixed[8][idx] = True
        fixed[idx][8] = True
    for idx in range(size - 8, size):
        fixed[8][idx] = True
        fixed[idx][8] = True
    return (grid, fixed)

def _fill_data_bits(grid: list[list[int]], fixed: list[list[bool]], codewords: list[int]) -> None:
    size = len(grid)
    stream = [cw >> shift & 1 for cw in codewords for shift in range(7, -1, -1)]
    bit_i = 0
    col = size - 1
    upward = True
    while col > 0:
        if col == 6:
            col -= 1
        rows = range(size - 1, -1, -1) if upward else range(size)
        for row in rows:
            for dc in (0, -1):
                cc = col + dc
                if not fixed[row][cc]:
                    grid[row][cc] = stream[bit_i] if bit_i < len(stream) else 0
                    bit_i += 1
        upward = not upward
        col -= 2

def _mask_bit(mask_id: int, r: int, c: int) -> bool:
    if mask_id == 0:
        return (r + c) % 2 == 0
    if mask_id == 1:
        return r % 2 == 0
    if mask_id == 2:
        return c % 3 == 0
    if mask_id == 3:
        return (r + c) % 3 == 0
    if mask_id == 4:
        return (r // 2 + c // 3) % 2 == 0
    if mask_id == 5:
        return r * c % 2 + r * c % 3 == 0
    if mask_id == 6:
        return (r * c % 2 + r * c % 3) % 2 == 0
    return ((r + c) % 2 + r * c % 3) % 2 == 0

def _format_bits_m(mask_id: int) -> int:
    data = mask_id & 7
    rem = data << 10
    for shift in range(4, -1, -1):
        if rem & 1 << shift + 10:
            rem ^= 1335 << shift
    return (data << 10 | rem) ^ 21522

def _write_format(grid: list[list[int]], fmt: int) -> None:
    size = len(grid)
    bits = [fmt >> shift & 1 for shift in range(14, -1, -1)]
    c1 = [(8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 7), (8, 8), (7, 8), (5, 8), (4, 8), (3, 8), (2, 8), (1, 8), (0, 8)]
    c2 = [(size - 1, 8), (size - 2, 8), (size - 3, 8), (size - 4, 8), (size - 5, 8), (size - 6, 8), (size - 7, 8), (8, size - 8), (8, size - 7), (8, size - 6), (8, size - 5), (8, size - 4), (8, size - 3), (8, size - 2), (8, size - 1)]
    for idx, bit in enumerate(bits):
        r1, x1 = c1[idx]
        r2, x2 = c2[idx]
        grid[r1][x1] = bit
        grid[r2][x2] = bit

def _line_penalty(line: list[int]) -> int:
    pen = 0
    run = 1
    for idx in range(1, len(line)):
        if line[idx] == line[idx - 1]:
            run += 1
        else:
            if run >= 5:
                pen += 3 + (run - 5)
            run = 1
    if run >= 5:
        pen += 3 + (run - 5)
    return pen

def _penalty(grid: list[list[int]]) -> int:
    size = len(grid)
    score = sum((_line_penalty(row) for row in grid))
    score += sum((_line_penalty([grid[r][c] for r in range(size)]) for c in range(size)))
    for r in range(size - 1):
        for c in range(size - 1):
            v = grid[r][c]
            if v == grid[r][c + 1] == grid[r + 1][c] == grid[r + 1][c + 1]:
                score += 3
    dark = sum((sum(row) for row in grid))
    ratio = abs(dark * 100 // (size * size) - 50)
    return score + ratio // 5 * 10

def encode_qr_matrix(text: str) -> list[list[int]]:
    cached = _QR_CACHE.get(text)
    if cached is not None:
        return cached
    ver, align, codewords = _qr_codewords(text.encode('utf-8'))
    base, fixed = _place_functions(ver, align)
    _fill_data_bits(base, fixed, codewords)
    size = len(base)
    best_grid = None
    best_score = 10 ** 9
    for mask_id in range(8):
        cand = [row[:] for row in base]
        for r in range(size):
            for c in range(size):
                if not fixed[r][c] and _mask_bit(mask_id, r, c):
                    cand[r][c] ^= 1
        _write_format(cand, _format_bits_m(mask_id))
        score = _penalty(cand)
        if score < best_score:
            best_score = score
            best_grid = cand
    assert best_grid is not None
    _QR_CACHE[text] = best_grid
    return best_grid

def _plain(markup: str) -> str:
    text = re.sub('<[^>]+>', '', markup or '')
    return html.unescape(text).strip()

def _filled(key: str) -> str:
    return t(key).format(version=PLUGIN_VERSION, year=COPYRIGHT_YEAR)

def _help_blocks() -> list:
    from gui.help_visuals import help_visual_height_pt
    blocks = [('h1', t('help_window_title')), ('visual', 'overview'), ('p', _plain(t('help_intro_markup'))), ('gap', '')]
    for key, spec in get_all_help_topics().items():
        title = str(spec.get('title') or '').strip()
        detail = _plain(str(spec.get('detail') or ''))
        if title:
            blocks.append(('h2', title))
        if help_visual_height_pt(key) > 0:
            blocks.append(('visual', key))
        if detail:
            blocks.append(('p', detail))
        blocks.append(('gap', ''))
    blocks.append(('qr_links', ''))
    return blocks

def _print_scale(context) -> float:
    width = float(context.get_width() or 0.0)
    if width <= 2500.0:
        return 1.0
    dpi = 0.0
    try:
        dpi = float(context.get_dpi_y() or 0.0)
    except Exception:
        dpi = 0.0
    if dpi >= 72.0 and width / (dpi / 72.0) < 1400.0:
        return dpi / 72.0
    return width / 612.0

def _parse_print_font(font_name: str):
    desc = Pango.FontDescription.from_string(font_name or 'Sans 12')
    family = desc.get_family() or 'Sans'
    raw_size = desc.get_size()
    body_pt = raw_size / float(Pango.SCALE) if raw_size else 12.0
    body_pt = max(8.0, min(48.0, float(body_pt)))
    style = desc.get_style()
    if style == Pango.Style.ITALIC:
        slant = cairo.FONT_SLANT_ITALIC
    elif style == Pango.Style.OBLIQUE:
        slant = cairo.FONT_SLANT_OBLIQUE
    else:
        slant = cairo.FONT_SLANT_NORMAL
    bold = int(desc.get_weight()) >= int(Pango.Weight.BOLD)
    return (family, body_pt, slant, bold)

def _cairo_font(cr, size: float, family: str, slant, bold: bool=False) -> None:
    weight = cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL
    cr.select_font_face(family or 'Sans', slant, weight)
    cr.set_font_size(size)

def _wrap_lines(cr, text: str, width: float) -> list[str]:
    lines = []
    for paragraph in (text or '').split('\n'):
        if not paragraph.strip():
            lines.append('')
            continue
        current = ''
        for word in paragraph.split(' '):
            trial = word if not current else f'{current} {word}'
            if cr.text_extents(trial).x_advance <= width or not current:
                current = trial
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines

def _qr_block_height_pt() -> float:
    return 118.0

def _draw_qr_matrix(cr, matrix: list[list[int]], x: float, y: float, box_size: float) -> None:
    modules = len(matrix)
    quiet = 4
    cell = box_size / float(modules + 2 * quiet)
    cr.save()
    cr.set_source_rgb(1.0, 1.0, 1.0)
    cr.rectangle(x, y, box_size, box_size)
    cr.fill()
    cr.set_source_rgb(0.84, 0.84, 0.84)
    cr.set_line_width(max(0.5, box_size / 140.0))
    cr.rectangle(x, y, box_size, box_size)
    cr.stroke()
    cr.set_source_rgb(0.0, 0.0, 0.0)
    ox = x + quiet * cell
    oy = y + quiet * cell
    for r, row in enumerate(matrix):
        for c, bit in enumerate(row):
            if bit:
                cr.rectangle(ox + c * cell, oy + r * cell, cell + 0.02, cell + 0.02)
    cr.fill()
    cr.restore()

def _tag_link_begin(cr, url: str) -> bool:
    tag_fn = getattr(cr, 'tag_begin', None)
    tag_name = getattr(cairo, 'TAG_LINK', None)
    if tag_fn is None or tag_name is None:
        return False
    try:
        tag_fn(tag_name, f"uri='{url}'")
        return True
    except Exception:
        return False

def _tag_link_end(cr, active: bool) -> None:
    if not active:
        return
    try:
        cr.tag_end(cairo.TAG_LINK)
    except Exception:
        pass

def _draw_qr_links_block(cr, y: float, page_w: float, scale: float, face) -> None:
    family, _body_pt, slant, _bold = face
    cr.save()
    cr.set_source_rgb(0.78, 0.78, 0.78)
    cr.set_line_width(0.7 * scale)
    cr.move_to(0.0, y)
    cr.line_to(page_w, y)
    cr.stroke()
    qr_size = 74.0 * scale
    gap = 18.0 * scale
    col_w = max(qr_size + 90.0 * scale, (page_w - gap) / 2.0)
    top_y = y + 14.0 * scale
    for idx, (label, url, url_lines) in enumerate(_QR_ITEMS):
        cx = idx * (col_w + gap)
        linked = _tag_link_begin(cr, url)
        _draw_qr_matrix(cr, encode_qr_matrix(url), cx, top_y, qr_size)
        tx = cx + qr_size + 10.0 * scale
        cr.set_source_rgb(0.08, 0.08, 0.08)
        _cairo_font(cr, 10.0 * scale, family, slant, True)
        cr.move_to(tx, top_y + 26.0 * scale)
        cr.show_text(label)
        cr.set_source_rgb(0.12, 0.34, 0.62)
        _cairo_font(cr, 8.2 * scale, family, slant, False)
        for line_i, line in enumerate(url_lines):
            cr.move_to(tx, top_y + (42.0 + line_i * 12.0) * scale)
            cr.show_text(line)
        _tag_link_end(cr, linked)
    cr.restore()

def _layout_text_block(cr, pages, y: float, top_y: float, bottom: float, width: float, size: float, bold: bool, text: str, family: str, slant) -> float:
    leading = size * 1.38
    _cairo_font(cr, size, family, slant, bold)
    for line in _wrap_lines(cr, text, width):
        if y + leading > bottom and pages[-1]:
            pages.append([])
            y = top_y
            _cairo_font(cr, size, family, slant, bold)
        pages[-1].append(('text', line, size, bold, y))
        y += leading
    return y

def _place_block_item(pages: list, tag: str, key: str, box_h: float, y: float, top_y: float, bottom: float, after_pad: float) -> float:
    if y + box_h > bottom and pages[-1]:
        pages.append([])
        y = top_y
    pages[-1].append((tag, key, box_h, y))
    return y + box_h + after_pad

def _layout_print_pages(cr, context, scale: float, face) -> list:
    from gui.help_visuals import help_visual_height_pt
    family, body_pt, slant, body_bold = face
    width = max(1.0, float(context.get_width()))
    height = max(1.0, float(context.get_height()))
    top_start = max(_PRINT_HEADER_PT, 20.0 + body_pt * 2.6) * scale + 8.0 * scale
    bottom = height - max(_PRINT_FOOTER_PT, body_pt + 10.0) * scale
    pages: list = [[]]
    y = top_start
    sizes = {'h1': body_pt * 1.45, 'h2': body_pt * 1.2, 'p': body_pt}
    for kind, text in _help_blocks():
        if kind == 'gap':
            y += body_pt * 0.45 * scale
            if y > bottom and pages[-1]:
                pages.append([])
                y = top_start
        elif kind == 'visual':
            vis_h = help_visual_height_pt(text) * scale
            if vis_h > 0:
                y = _place_block_item(pages, 'visual', text, vis_h, y - body_pt * 0.45 * scale, top_start, bottom, body_pt * 1.15 * scale)
        elif kind == 'qr_links':
            y = _place_block_item(pages, 'qr_links', '', _qr_block_height_pt() * scale, y, top_start, bottom, 0.0)
        else:
            y = _layout_text_block(cr, pages, y, top_start, bottom, width, sizes[kind] * scale, kind != 'p' or body_bold, text, family, slant)
    return [page for page in pages if page] or [[]]

def _print_header(context, scale: float, face) -> None:
    cr = context.get_cairo_context()
    logo_px = max(1, int(round(_PRINT_LOGO_PT * scale)))
    logo_path = _BRAND / 'about.png'
    text_x = 0.0
    if logo_path.is_file():
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(str(logo_path), logo_px, logo_px, True)
        Gdk.cairo_set_source_pixbuf(cr, pixbuf, 0, 4 * scale)
        cr.paint()
        text_x = logo_px + 12.0 * scale
    family, body_pt, slant, _body_bold = face
    cr.set_source_rgb(0, 0, 0)
    _cairo_font(cr, body_pt * 1.15 * scale, family, slant, True)
    cr.move_to(text_x, max(26.0, body_pt * 1.3) * scale)
    cr.show_text(t('help_print_product'))
    _cairo_font(cr, body_pt * 0.9 * scale, family, slant, False)
    cr.move_to(text_x, max(46.0, body_pt * 2.3) * scale)
    cr.show_text(_filled('help_print_version'))

def _print_footer(context, scale: float, face, page_nr: int, total_pages: int) -> None:
    cr = context.get_cairo_context()
    family, body_pt, slant, _body_bold = face
    page_w = float(context.get_width())
    page_h = float(context.get_height())
    font_sz = max(8.5, body_pt * 0.72) * scale
    line_y = page_h - max(19.0, body_pt * 1.25) * scale
    text_y = page_h - max(8.0, body_pt * 0.5) * scale
    cr.save()
    cr.set_source_rgb(0.78, 0.78, 0.78)
    cr.set_line_width(0.6 * scale)
    cr.move_to(0.0, line_y)
    cr.line_to(page_w, line_y)
    cr.stroke()
    _cairo_font(cr, font_sz, family, slant, False)
    left_meta = f"{t('help_print_product')} · {_filled('help_print_version')} · "
    cr.set_source_rgb(0.28, 0.28, 0.28)
    cr.move_to(0.0, text_y)
    cr.show_text(left_meta)
    link_x = cr.text_extents(left_meta).x_advance
    linked = _tag_link_begin(cr, PRODUCT_PAGE_URL)
    cr.set_source_rgb(0.12, 0.34, 0.62)
    cr.move_to(link_x, text_y)
    cr.show_text('ready-4-it.com/borderlay-studio')
    _tag_link_end(cr, linked)
    marker = f'{page_nr + 1} / {max(1, total_pages)}'
    marker_w = cr.text_extents(marker).x_advance
    cr.set_source_rgb(0.28, 0.28, 0.28)
    cr.move_to(max(0.0, page_w - marker_w), text_y)
    cr.show_text(marker)
    cr.restore()

def print_help_document(parent, font_name: str) -> None:
    face = _parse_print_font(font_name)
    operation = Gtk.PrintOperation()
    operation.set_job_name(f'Borderlay Studio {PLUGIN_VERSION}')
    operation.set_embed_page_setup(True)
    pages = []

    def _begin(_op, context):
        cr = context.get_cairo_context()
        pages[:] = _layout_print_pages(cr, context, _print_scale(context), face)
        operation.set_n_pages(max(1, len(pages)))

    def _draw(_op, context, page_nr):
        from gui.help_visuals import draw_help_visual_print
        cr = context.get_cairo_context()
        scale = _print_scale(context)
        family, _body_pt, slant, _body_bold = face
        page_w = float(context.get_width())
        cr.set_source_rgb(0, 0, 0)
        chunk = pages[page_nr] if page_nr < len(pages) else []
        for item in chunk:
            tag = item[0]
            if tag == 'visual':
                _tag, topic_key, _vh, y = item
                draw_help_visual_print(cr, topic_key, 0.0, y, page_w, scale, family, slant)
                cr.set_source_rgb(0, 0, 0)
                continue
            if tag == 'qr_links':
                _tag, _unused, _qh, y = item
                _draw_qr_links_block(cr, y, page_w, scale, face)
                cr.set_source_rgb(0, 0, 0)
                continue
            _tag, line, size, bold, y = item
            if not line:
                continue
            _cairo_font(cr, size, family, slant, bold)
            cr.move_to(0, y)
            cr.show_text(line)
        _print_header(context, scale, face)
        _print_footer(context, scale, face, page_nr, len(pages))
    operation.connect('begin-print', _begin)
    operation.connect('draw-page', _draw)
    try:
        operation.run(Gtk.PrintOperationAction.PRINT_DIALOG, parent)
    except Exception:
        pass
