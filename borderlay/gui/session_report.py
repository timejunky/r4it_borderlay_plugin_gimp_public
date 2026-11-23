# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import ctypes
import platform
import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk, Gtk
from locales.i18n import t
_SKIP = {'procedure', 'run-mode', 'image', 'drawables', 'drawable'}

class ScopeCopyButton(Gtk.Button):

    def __init__(self, text_provider):
        super().__init__(label='⌖')
        self._provider = text_provider
        self._tip = t('scope_copy_tip')
        self.set_tooltip_text(self._tip)
        self.set_relief(Gtk.ReliefStyle.NONE)
        self.set_size_request(36, 28)
        self.connect('clicked', self._on_clicked)

    def _on_clicked(self, _button):
        try:
            text = str(self._provider() or '')
            clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
            clipboard.set_text(text, -1)
            clipboard.store()
            self.set_tooltip_text(t('scope_copied'))
        except Exception:
            self.set_tooltip_text(self._tip)
            return
        from gi.repository import GLib
        GLib.timeout_add(1600, self._restore_tip)

    def _restore_tip(self):
        self.set_tooltip_text(self._tip)
        return False

def attach_scope_button(dialog, text_provider) -> None:
    area = dialog.get_action_area()
    button = ScopeCopyButton(text_provider)
    area.pack_start(button, False, False, 0)
    if hasattr(area, 'set_child_secondary'):
        area.set_child_secondary(button, True)

def build_session_markdown(procedure, cfg, notebook, initial: dict, factory: dict) -> str:
    page = _current_tab(notebook)
    values = _current_values(procedure, cfg)
    lines = ['# Borderlay Studio', '', '## Umgebung', f'- OS: {_os_line()}', f'- RAM: {_ram_line()}', f'- GIMP: {_gimp_version()}', f'- Borderlay: {_plugin_version()}', '', '## Lizenz', f'- {_license_line()}', '', '## Reiter', f'- {page}', '', '## Einstellungen', '| Einstellung | Wert |', '| --- | --- |']
    for name, nick, value in values:
        lines.append(f'| {_cell(nick)} | {_cell(value)} |')
    lines.extend(['', '## Änderungen seit dem Öffnen'])
    lines.extend(_delta_lines(values, initial))
    lines.extend(['', '## Abweichung von den Vorgaben'])
    lines.extend(_delta_lines(values, factory))
    lines.extend(['', '## Lesart', _reading(cfg)])
    lines.append('')
    return '\n'.join(lines)

def _current_tab(notebook) -> str:
    try:
        index = int(notebook.get_current_page())
        page = notebook.get_nth_page(index)
        label = notebook.get_tab_label(page)
        if label is not None and hasattr(label, 'get_text'):
            text = str(label.get_text() or '').strip()
            if text:
                return text
    except Exception:
        pass
    return ''

def _current_values(procedure, cfg) -> list:
    rows = []
    try:
        arguments = procedure.get_arguments()
    except Exception:
        return rows
    for pspec in arguments:
        name = str(getattr(pspec, 'name', '') or '')
        if not name or name in _SKIP:
            continue
        try:
            value = cfg.get_property(name)
        except Exception:
            continue
        nick = name
        getter = getattr(pspec, 'get_nick', None)
        if getter is not None:
            try:
                nick = str(getter() or name)
            except Exception:
                nick = name
        rows.append((name, nick, _show(value)))
    return rows

def _delta_lines(rows, baseline: dict) -> list:
    if not baseline:
        return ['- keine']
    changes = []
    for name, nick, value in rows:
        if name not in baseline:
            continue
        previous = _show(baseline.get(name))
        if previous != value:
            changes.append(f'- {nick}: {previous} → {value}')
    return changes or ['- keine']

def _reading(cfg) -> str:
    try:
        from shapes.common.shape_transform import ShapeTransformHelper
        repeat = bool(cfg.get_property('rot_repeat'))
        if not repeat:
            angle = int(cfg.get_property('shape_rotation'))
            pivot = str(cfg.get_property('shape_pivot') or 'center')
            return f'Einfache Drehung, {angle}°, Achse {pivot}.'
        kind, fade, times = ShapeTransformHelper.parse_rotation_mode(cfg.get_property('rot_fade_mode'), int(cfg.get_property('rot_cycle_times')), int(cfg.get_property('rot_cycle_until')))
        start = int(cfg.get_property('rot_angle_start'))
        end = int(cfg.get_property('rot_angle_end'))
        step = int(cfg.get_property('rot_angle_step'))
        fade_pct = int(cfg.get_property('rot_fade_steps'))
        until = int(cfg.get_property('rot_cycle_until'))
        names = {'sweep': 'Von–bis', 'until': 'Bis Winkel', 'offset': 'Wiederholung', 'cycle': 'Fading-Zyklus'}
        fade_name = 'ohne Fading' if fade_pct <= 0 else 'End Transparency' if fade == 'end_target' else 'Fading Steps'
        text = f'{names.get(kind, kind)}, {fade_name}, {fade_pct} %. Start {start}°, Ende {end}°, Schritt {step}°.'
        if kind == 'until':
            text += f' Ziel {until}°.'
        elif kind == 'offset':
            text += f' Durchläufe {times}.'
        elif kind == 'cycle':
            text += f' Zyklen {times}, der letzte beginnt vor einer vollen Drehung.'
        return text
    except Exception:
        return 'Drehung konnte nicht gelesen werden.'

def _show(value) -> str:
    if isinstance(value, bool):
        return 'ja' if value else 'nein'
    text = str(value)
    if len(text) > 180:
        return text[:177] + '…'
    return text

def _cell(text) -> str:
    return str(text).replace('|', '/').replace('\n', ' ')

def _os_line() -> str:
    return platform.platform()

def _ram_line() -> str:
    if platform.system() != 'Windows':
        return ''

    class MemoryStatus(ctypes.Structure):
        _fields_ = [('dwLength', ctypes.c_ulong), ('dwMemoryLoad', ctypes.c_ulong), ('ullTotalPhys', ctypes.c_ulonglong), ('ullAvailPhys', ctypes.c_ulonglong), ('ullTotalPageFile', ctypes.c_ulonglong), ('ullAvailPageFile', ctypes.c_ulonglong), ('ullTotalVirtual', ctypes.c_ulonglong), ('ullAvailVirtual', ctypes.c_ulonglong), ('ullAvailExtendedVirtual', ctypes.c_ulonglong)]
    status = MemoryStatus()
    status.dwLength = ctypes.sizeof(status)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
        return ''
    total = status.ullTotalPhys / 1024 ** 3
    free = status.ullAvailPhys / 1024 ** 3
    return f'{total:.1f} GB gesamt, {free:.1f} GB frei'

def _gimp_version() -> str:
    try:
        gi.require_version('Gimp', '3.0')
        from gi.repository import Gimp
        version = Gimp.version()
        if isinstance(version, (tuple, list)):
            return '.'.join((str(part) for part in version[:3]))
        return str(version)
    except Exception:
        return ''

def _plugin_version() -> str:
    try:
        from config import PLUGIN_VERSION
        return str(PLUGIN_VERSION)
    except Exception:
        return ''

def _license_line() -> str:
    try:
        from image_metadata import active_tier_name
        return active_tier_name()
    except Exception:
        return ''
