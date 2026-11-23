# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk, Gtk
from locales.i18n import t

class GtkWindowEventHelper:

    @staticmethod
    def pump_gtk_events():
        try:
            max_iter = 40
            while Gtk.events_pending() and max_iter > 0:
                Gtk.main_iteration_do(False)
                max_iter -= 1
        except Exception:
            pass

    @classmethod
    def set_dialog_busy(cls, dialog, apply_btn, busy: bool):
        if dialog is None:
            return
        try:
            if apply_btn is not None:
                apply_btn.set_sensitive(not busy)
                apply_btn.set_label(t('live_preview_busy') if busy else t('live_preview_btn'))
            gdk_win = dialog.get_window()
            if gdk_win is not None:
                if busy:
                    display = gdk_win.get_display()
                    cursor = Gdk.Cursor.new_from_name(display, 'progress')
                    gdk_win.set_cursor(cursor)
                else:
                    gdk_win.set_cursor(None)
            cls.pump_gtk_events()
        except Exception:
            pass

    @classmethod
    def force_window_repaint(cls, dialog):
        if dialog is None:
            return
        try:
            cls.pump_gtk_events()
            gdk_win = dialog.get_window()
            if gdk_win is not None:
                gdk_win.invalidate_rect(None, True)
                gdk_win.process_updates(True)
            dialog.queue_draw()
            dialog.present()
            cls.pump_gtk_events()
        except Exception:
            pass
