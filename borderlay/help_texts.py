# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from locales.i18n import get_all_help_topics, t, t_help
HELP_TOPICS = get_all_help_topics()

def create_help_button(topic_key: str) -> Gtk.Button:
    spec = t_help(topic_key)
    btn = Gtk.Button(label='?')
    btn.set_relief(Gtk.ReliefStyle.NONE)
    btn.set_focus_on_click(False)
    btn.set_tooltip_text(f"{spec['title']}:\n{spec['short']} ({t('help_click_hint')})")

    def _on_clicked(widget):
        cur_spec = t_help(topic_key)
        pop = Gtk.Popover.new(widget)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.set_margin_top(10)
        vbox.set_margin_bottom(10)
        vbox.set_margin_start(12)
        vbox.set_margin_end(12)
        title_lbl = Gtk.Label(xalign=0)
        title_lbl.set_markup(f"<b>{cur_spec['title']}</b>")
        vbox.pack_start(title_lbl, False, False, 0)
        body_lbl = Gtk.Label(label=cur_spec['detail'], xalign=0)
        body_lbl.set_line_wrap(True)
        body_lbl.set_max_width_chars(52)
        vbox.pack_start(body_lbl, False, False, 0)
        pop.add(vbox)
        pop.show_all()
        pop.popup()
    btn.connect('clicked', _on_clicked)
    return btn
