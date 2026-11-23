# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import html
import re
from pathlib import Path
import gi
gi.require_version('Gimp', '3.0')
gi.require_version('GimpUi', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gdk, GdkPixbuf, GimpUi, Gtk, Pango
from config import COPYRIGHT_YEAR, PLUGIN_VERSION
from locales.i18n import get_all_help_topics, t
_BRAND = Path(__file__).resolve().parents[1] / 'assets' / 'brand'
_READABLE_FONTS = ('Segoe UI', 'Calibri', 'Georgia')
_HELP_DLG = None

def _plain(markup: str) -> str:
    text = re.sub('<[^>]+>', '', markup or '')
    return html.unescape(text).strip()

def _filled(key: str) -> str:
    return t(key).format(version=PLUGIN_VERSION, year=COPYRIGHT_YEAR)

def _community_edition() -> bool:
    try:
        from community_beacon import COMMUNITY_EDITION
    except Exception:
        return False
    return bool(COMMUNITY_EDITION)

def _short_hash(digest: str) -> str:
    clean = (digest or '').strip()
    if len(clean) <= 18:
        return clean
    return f'{clean[:8]}…{clean[-6:]}'

def _add_device_hash_row(container, service):
    device_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
    device = Gtk.Label(xalign=0)
    device.set_line_wrap(False)
    device.set_selectable(True)
    device_row.pack_start(device, True, True, 0)
    copy_hash = Gtk.Button(label=t('license_copy_hash'))

    def _copy_device_hash(_btn):
        digest = service.get_device_hash().strip()
        if not digest:
            return
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(digest, -1)
    copy_hash.connect('clicked', _copy_device_hash)
    device_row.pack_start(copy_hash, False, False, 0)
    container.pack_start(device_row, False, False, 0)
    full_digest = service.get_device_hash().strip()
    device.set_text(t('license_device_hash').format(digest=_short_hash(full_digest)))
    if full_digest:
        device.set_tooltip_text(full_digest)
    return device

def _add_community_purchase(vbox) -> None:
    from licensing_service import LicensingService
    frame = Gtk.Frame()
    frame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
    inner = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    inner.set_margin_top(8)
    inner.set_margin_bottom(8)
    inner.set_margin_start(10)
    inner.set_margin_end(10)
    note = Gtk.Label(xalign=0)
    note.set_line_wrap(True)
    note.set_markup(t('license_community_next'))
    inner.pack_start(note, False, False, 0)
    _add_device_hash_row(inner, LicensingService.get_instance())
    frame.add(inner)
    vbox.pack_start(frame, False, False, 0)

def _build_license_terms_scroll(terms_text: str):
    scroll = Gtk.ScrolledWindow()
    scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
    scroll.set_shadow_type(Gtk.ShadowType.IN)
    if hasattr(scroll, 'set_propagate_natural_height'):
        scroll.set_propagate_natural_height(False)
    scroll.set_min_content_height(150)
    if hasattr(scroll, 'set_max_content_height'):
        scroll.set_max_content_height(190)
    scroll.set_size_request(-1, 175)
    terms = Gtk.TextView()
    terms.set_editable(False)
    terms.set_cursor_visible(False)
    terms.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
    terms.set_left_margin(6)
    terms.set_right_margin(6)
    terms.get_buffer().set_text(terms_text)
    scroll.add(terms)
    return scroll

def _add_paid_activation(vbox) -> None:
    from licensing_service import LicensingService
    service = LicensingService.get_instance()
    status = Gtk.Label(xalign=0)
    status.set_line_wrap(True)
    vbox.pack_start(status, False, False, 0)
    device = _add_device_hash_row(vbox, service)
    key_hint = Gtk.Label(xalign=0)
    key_hint.set_line_wrap(True)
    key_hint.set_text(t('license_key_label'))
    vbox.pack_start(key_hint, False, False, 0)
    key_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
    entry = Gtk.Entry()
    entry.set_placeholder_text(t('license_key_placeholder'))
    entry.set_visibility(False)
    key_box.pack_start(entry, True, True, 0)
    reveal = Gtk.Button(label=t('license_key_show'))

    def _toggle_key(_btn):
        visible = not entry.get_visibility()
        entry.set_visibility(visible)
        reveal.set_label(t('license_key_hide') if visible else t('license_key_show'))
    reveal.connect('clicked', _toggle_key)
    key_box.pack_start(reveal, False, False, 0)
    vbox.pack_start(key_box, False, False, 0)
    result = Gtk.Label(xalign=0)
    result.set_line_wrap(True)
    vbox.pack_start(result, False, False, 0)
    buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
    activate_btn = Gtk.Button(label=t('license_activate'))
    deactivate_btn = Gtk.Button(label=t('license_deactivate'))
    buttons.pack_start(activate_btn, False, False, 0)
    buttons.pack_start(deactivate_btn, False, False, 0)
    vbox.pack_start(buttons, False, False, 0)

    def _paint_status():
        info = service.get_status_info(force=True)
        status.set_text(t('license_status_line').format(tier=info.tier_display, code=info.status_code, active=t('license_yes') if info.is_active else t('license_no')))
        full_digest = service.get_device_hash().strip()
        device.set_text(t('license_device_hash').format(digest=_short_hash(full_digest)))
        if full_digest:
            device.set_tooltip_text(full_digest)

    def _on_activate(_btn):
        ok, message = service.activate(entry.get_text())
        result.set_text(message)
        if ok:
            _paint_status()
        return ok

    def _on_deactivate(_btn):
        _ok, message = service.deactivate()
        result.set_text(message)
        entry.set_text('')
        _paint_status()
    activate_btn.connect('clicked', _on_activate)
    deactivate_btn.connect('clicked', _on_deactivate)
    _paint_status()
    entry.grab_focus()

def _linkify(text: str) -> str:
    escaped = html.escape(text or '')
    return re.sub('https://[^\\s<]+', lambda match: f"<a href='{match.group(0)}'>{match.group(0)}</a>", escaped)

def _intro_parts() -> tuple:
    plain = _plain(t('help_intro_markup'))
    heading, _, rest = plain.partition('\n')
    return (heading.strip(), rest.strip())

def _print_help(parent, font_name: str) -> None:
    from gui.help_print import print_help_document
    print_help_document(parent, font_name)

def apply_window_icon(window) -> None:
    icon = _BRAND / 'borderlay.ico'
    if icon.is_file():
        try:
            window.set_icon_from_file(str(icon))
        except Exception:
            pass

def _help_selected_face(font_combo, font_size, theme):
    chosen = font_combo.get_active_id() or 'standard'
    family = theme['family'] if chosen == 'standard' else chosen
    return (family, float(font_size.get_value()))

def _help_sync_wrap(title_lbl, short_lbl, body_lbl, _widget, allocation):
    target = max(180, int(allocation.width) - 28)
    title_lbl.set_size_request(target, -1)
    short_lbl.set_size_request(target, -1)
    body_lbl.set_size_request(target, -1)

def _help_restyle(font_combo, font_size, theme, labels):
    family, size = _help_selected_face(font_combo, font_size, theme)
    desc = Pango.FontDescription.from_string(f'{family} {size:g}')
    for label in labels:
        label.override_font(desc)

def _help_reset_scroll(article_scroll):
    adj = article_scroll.get_vadjustment()
    if adj is not None:
        adj.set_value(0)

def _help_show_topic(topic_key, spec, title_lbl, short_lbl, visual_box, body_lbl, article_scroll):
    from gui.help_visuals import populate_help_visuals
    if spec is None:
        heading, steps = _intro_parts()
        title_lbl.set_markup(f'<b>{html.escape(heading)}</b>')
        short_lbl.hide()
        populate_help_visuals(visual_box, 'overview')
        body_lbl.show()
        body_lbl.set_text(steps)
        _help_reset_scroll(article_scroll)
        return
    short_lbl.show()
    body_lbl.show()
    title_lbl.set_markup(f"<b>{html.escape(str(spec.get('title') or ''))}</b>")
    short_lbl.set_markup(f"<i>{html.escape(str(spec.get('short') or ''))}</i>")
    populate_help_visuals(visual_box, topic_key)
    detail = str(spec.get('detail') or '')
    if 'https://' in detail:
        body_lbl.set_markup(_linkify(detail))
    else:
        body_lbl.set_text(detail)
    _help_reset_scroll(article_scroll)

def _help_on_row(topics, title_lbl, short_lbl, visual_box, body_lbl, article_scroll, _box, row):
    if row is None:
        return
    topic_key, spec = topics[row.get_index()]
    _help_show_topic(topic_key, spec, title_lbl, short_lbl, visual_box, body_lbl, article_scroll)

def _help_forget(dlg, *_args):
    global _HELP_DLG
    if _HELP_DLG is dlg:
        _HELP_DLG = None

def _help_on_response(dlg, _dlg, response_id):
    closing = int(response_id) in (int(Gtk.ResponseType.CLOSE), int(Gtk.ResponseType.DELETE_EVENT), int(Gtk.ResponseType.CANCEL))
    if closing:
        dlg.destroy()

class StudioInfoDialogs:

    @staticmethod
    def show_about_dialog():
        GimpUi.init('borderlay')
        dlg = Gtk.Dialog(title=t('about_window_title'))
        dlg.add_button('_OK', Gtk.ResponseType.OK)
        dlg.set_default_size(460, 560)
        apply_window_icon(dlg)
        content = dlg.get_content_area()
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        vbox.set_margin_top(12)
        vbox.set_margin_bottom(12)
        vbox.set_margin_start(16)
        vbox.set_margin_end(16)
        logo_path = _BRAND / 'about.png'
        if logo_path.is_file():
            img = Gtk.Image.new_from_file(str(logo_path))
            img.set_halign(Gtk.Align.CENTER)
            vbox.pack_start(img, False, False, 0)
        headline = Gtk.Label(xalign=0)
        headline.set_markup(f"<b>{t('about_headline')}</b>")
        headline.set_line_wrap(True)
        vbox.pack_start(headline, False, False, 0)
        body = Gtk.Label(xalign=0)
        body.set_line_wrap(True)
        body.set_markup(_filled('about_markup'))
        vbox.pack_start(body, False, False, 0)
        content.pack_start(vbox, True, True, 0)
        dlg.show_all()
        dlg.run()
        dlg.destroy()

    @staticmethod
    def show_help_dialog(owner=None):
        global _HELP_DLG
        if _HELP_DLG is not None:
            try:
                _HELP_DLG.present()
                if owner is not None:
                    owner._help_window = _HELP_DLG
                return _HELP_DLG
            except Exception:
                _HELP_DLG = None
        GimpUi.init('borderlay')
        dlg = Gtk.Dialog(title=t('help_window_title'))
        dlg.add_button('_OK', Gtk.ResponseType.CLOSE)
        dlg.set_default_response(Gtk.ResponseType.NONE)
        dlg.set_default_size(920, 620)
        dlg.set_modal(False)
        dlg.set_destroy_with_parent(False)
        dlg.set_transient_for(None)
        apply_window_icon(dlg)
        _HELP_DLG = dlg
        if owner is not None:
            owner._help_window = dlg
        content = dlg.get_content_area()
        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        outer.set_margin_top(10)
        outer.set_margin_bottom(10)
        outer.set_margin_start(12)
        outer.set_margin_end(12)
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        nav_caption = Gtk.Label(xalign=0)
        nav_caption.set_markup(f"<b>{html.escape(t('help_nav_topics'))}</b>")
        toolbar.pack_start(nav_caption, False, False, 0)
        print_btn = Gtk.Button(label=t('help_print'))
        print_btn.set_halign(Gtk.Align.END)
        font_combo = Gtk.ComboBoxText()
        font_combo.append('standard', t('help_font_standard'))
        for family in _READABLE_FONTS:
            font_combo.append(family, family)
        font_combo.set_active_id('standard')
        font_size = Gtk.SpinButton.new_with_range(9, 18, 1)
        font_size.set_value(11)
        font_lbl = Gtk.Label(label=t('help_font'))
        size_lbl = Gtk.Label(label=t('help_font_size'))
        theme = {'family': 'Sans'}
        print_btn.connect('clicked', lambda _b: _print_help(dlg, '{0} {1:g}'.format(*_help_selected_face(font_combo, font_size, theme))))
        toolbar.pack_end(print_btn, False, False, 0)
        toolbar.pack_end(font_size, False, False, 0)
        toolbar.pack_end(size_lbl, False, False, 0)
        toolbar.pack_end(font_combo, False, False, 0)
        toolbar.pack_end(font_lbl, False, False, 0)
        outer.pack_start(toolbar, False, False, 0)
        topics = [('overview', None)] + list(get_all_help_topics().items())
        topic_list = Gtk.ListBox()
        topic_list.set_selection_mode(Gtk.SelectionMode.BROWSE)
        row_labels = []
        for key, spec in topics:
            row_label = Gtk.Label(xalign=0)
            row_label.set_line_wrap(False)
            row_label.set_ellipsize(Pango.EllipsizeMode.END)
            row_label.set_margin_top(3)
            row_label.set_margin_bottom(3)
            row_label.set_margin_start(10)
            row_label.set_margin_end(8)
            title = t('help_nav_overview') if spec is None else str(spec.get('title') or key)
            row_label.set_text(title)
            row_label.set_tooltip_text(title)
            row_labels.append(row_label)
            topic_list.add(row_label)
        nav_scroll = Gtk.ScrolledWindow()
        nav_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        nav_scroll.set_size_request(260, -1)
        nav_scroll.add(topic_list)
        title_lbl = Gtk.Label(xalign=0)
        title_lbl.set_line_wrap(True)
        title_lbl.set_selectable(True)
        short_lbl = Gtk.Label(xalign=0)
        short_lbl.set_line_wrap(True)
        short_lbl.set_selectable(True)
        body_lbl = Gtk.Label(xalign=0)
        body_lbl.set_line_wrap(True)
        body_lbl.set_selectable(True)
        article = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        article.set_valign(Gtk.Align.START)
        article.set_margin_top(8)
        article.set_margin_bottom(8)
        article.set_margin_start(12)
        article.set_margin_end(12)
        visual_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        article.pack_start(title_lbl, False, False, 0)
        article.pack_start(short_lbl, False, False, 0)
        article.pack_start(visual_box, False, False, 0)
        article.pack_start(body_lbl, False, False, 0)
        article_scroll = Gtk.ScrolledWindow()
        article_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        article_scroll.add(article)
        article_scroll.connect('size-allocate', lambda widget, allocation: _help_sync_wrap(title_lbl, short_lbl, body_lbl, widget, allocation))
        styled = [nav_caption, title_lbl, short_lbl, body_lbl]

        def _restyle(*_args):
            _help_restyle(font_combo, font_size, theme, row_labels + styled)
        font_combo.connect('changed', _restyle)
        font_size.connect('value-changed', _restyle)
        topic_list.connect('row-selected', lambda box, row: _help_on_row(topics, title_lbl, short_lbl, visual_box, body_lbl, article_scroll, box, row))
        paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        paned.pack1(nav_scroll, False, False)
        paned.pack2(article_scroll, True, False)
        paned.set_position(270)
        outer.pack_start(paned, True, True, 0)
        content.pack_start(outer, True, True, 0)
        dlg.connect('destroy', lambda *args: _help_forget(dlg, *args))
        dlg.connect('response', lambda widget, response_id: _help_on_response(dlg, widget, response_id))
        dlg.show_all()
        base = nav_caption.get_pango_context().get_font_description()
        if base is not None and base.get_family():
            theme['family'] = base.get_family()
        theme_size = base.get_size() / float(Pango.SCALE) if base is not None else 0
        if theme_size >= 8:
            font_size.set_value(theme_size)
        _help_restyle(font_combo, font_size, theme, row_labels + styled)
        first = topic_list.get_row_at_index(0)
        if first is not None:
            topic_list.select_row(first)
        _HELP_DLG = dlg
        dlg.present()
        return dlg

    @staticmethod
    def _license_terms_text() -> str:
        plugin_root = Path(__file__).resolve().parents[1]
        for path in (plugin_root / 'LICENSE.txt', plugin_root / 'LICENSE', plugin_root.parent / 'LICENSE'):
            if path.is_file():
                return path.read_text(encoding='utf-8-sig').strip()
        return ''

    @staticmethod
    def show_license_dialog():
        GimpUi.init('borderlay')
        is_community = _community_edition()
        title_key = 'license_window_title_community' if is_community else 'license_window_title'
        dlg = Gtk.Dialog(title=t(title_key))
        dlg.add_button('_OK', Gtk.ResponseType.OK)
        dlg.set_default_size(640, 560)
        dlg.set_resizable(True)
        apply_window_icon(dlg)
        content = dlg.get_content_area()
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        vbox.set_margin_top(12)
        vbox.set_margin_bottom(12)
        vbox.set_margin_start(16)
        vbox.set_margin_end(16)
        hdr = Gtk.Label(xalign=0)
        hdr.set_line_wrap(True)
        hdr_key = 'license_hdr_community_markup' if is_community else 'license_hdr_markup'
        hdr.set_markup(_filled(hdr_key))
        vbox.pack_start(hdr, False, False, 0)
        if is_community:
            _add_community_purchase(vbox)
        info = Gtk.Label(xalign=0)
        info.set_line_wrap(True)
        info.set_markup(t('license_body_markup'))
        vbox.pack_start(info, False, False, 0)
        terms_text = StudioInfoDialogs._license_terms_text()
        if terms_text:
            vbox.pack_start(_build_license_terms_scroll(terms_text), True, True, 0)
        if not is_community:
            _add_paid_activation(vbox)
        content.pack_start(vbox, True, True, 0)
        dlg.show_all()
        dlg.run()
        dlg.destroy()

    @staticmethod
    def show_metadata_settings_dialog():
        from image_metadata import load_metadata_settings, product_meta_stamp, save_metadata_settings
        from locales.i18n import SUPPORTED_LANGUAGES, get_language, set_language
        GimpUi.init('borderlay')
        dlg = Gtk.Dialog(title=t('meta_window_title'))
        dlg.add_button(t('meta_cancel'), Gtk.ResponseType.CANCEL)
        save_btn = dlg.add_button(t('meta_save'), Gtk.ResponseType.OK)
        save_btn.get_style_context().add_class('suggested-action')
        dlg.set_default_size(520, 380)
        apply_window_icon(dlg)
        content = dlg.get_content_area()
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_top(12)
        vbox.set_margin_bottom(12)
        vbox.set_margin_start(14)
        vbox.set_margin_end(14)
        lang_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        lang_row.pack_start(Gtk.Label(label='Language / Sprache:', xalign=0), False, False, 0)
        lang_combo = Gtk.ComboBoxText()
        for lang_code, lang_label in SUPPORTED_LANGUAGES:
            lang_combo.append(lang_code, lang_label)
        lang_combo.set_active_id(get_language())
        lang_row.pack_start(lang_combo, True, True, 0)
        vbox.pack_start(lang_row, False, False, 0)
        stamp_lbl = Gtk.Label(label=t('meta_product_line').format(stamp=product_meta_stamp()), xalign=0)
        stamp_lbl.set_line_wrap(True)
        vbox.pack_start(stamp_lbl, False, False, 0)
        hint_lbl = Gtk.Label(label=t('meta_hint'), xalign=0)
        hint_lbl.set_line_wrap(True)
        vbox.pack_start(hint_lbl, False, False, 0)
        settings = load_metadata_settings()
        apply_chk = Gtk.CheckButton(label=t('meta_apply_chk'))
        apply_chk.set_active(bool(settings.get('apply_defaults', True)))
        vbox.pack_start(apply_chk, False, False, 0)
        preserve_chk = Gtk.CheckButton(label=t('meta_preserve_chk'))
        preserve_chk.set_active(bool(settings.get('preserve_existing', True)))
        vbox.pack_start(preserve_chk, False, False, 0)
        grid = Gtk.Grid(column_spacing=8, row_spacing=6)
        fields = (('copyright', 'meta_copyright', '© 2026'), ('author', 'meta_author', ''), ('website', 'meta_website', 'https://'), ('description', 'meta_description', ''), ('keywords', 'meta_keywords', 'Borderlay, GIMP, 3D'))
        entries = {}
        for row_idx, (key, label_key, placeholder) in enumerate(fields):
            grid.attach(Gtk.Label(label=t(label_key), xalign=0), 0, row_idx, 1, 1)
            entry = Gtk.Entry()
            entry.set_hexpand(True)
            entry.set_text(str(settings.get(key) or ''))
            if placeholder:
                entry.set_placeholder_text(placeholder)
            grid.attach(entry, 1, row_idx, 1, 1)
            entries[key] = entry
        vbox.pack_start(grid, False, False, 0)
        content.pack_start(vbox, True, True, 0)
        dlg.show_all()
        response = dlg.run()
        if response == Gtk.ResponseType.OK:
            chosen_lang = lang_combo.get_active_id()
            if chosen_lang:
                set_language(chosen_lang)
            save_metadata_settings({'apply_defaults': apply_chk.get_active(), 'preserve_existing': preserve_chk.get_active(), **{key: entry.get_text() for key, entry in entries.items()}})
        dlg.destroy()
