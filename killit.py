from __future__ import print_function
from datetime import datetime
import sys
import os

import urwid
import psutil

APP_BANNER = 'Kill it with fire!!!    [q]uit  [enter] kill it'

_proc = {}
_debugfile = None


def _close_debug(fo):
    fo.close()


def DEBUG(*obj):
    """Open a terminal emulator and write messages to it for debugging."""
    global _debugfile
    if _debugfile is None:
        import atexit
        masterfd, slavefd = os.openpty()
        pid = os.fork()
        if pid:
            os.close(masterfd)
            _debugfile = os.fdopen(slavefd, "w+", 0)
            atexit.register(_close_debug, _debugfile)
        else:
            os.close(slavefd)
            os.execlp("urxvt", "urxvt", "-pty-fd", str(masterfd))
    print(datetime.now(), ":", ", ".join(map(repr, obj)), file=_debugfile)


def get_processes_by_name(name):
    p = []
    for process in psutil.process_iter():
        cmdline = ' '.join(process.cmdline())
        if name in cmdline:
            if 'killit' not in cmdline:
                p.append(process)
    return p


def exit_program(button=None):
    raise urwid.ExitMainLoop()


def handle_keys(key):
    if key == 'q':
        exit_program()


class Menu(object):
    def __init__(self):
        self.listbox = None

    def menu(self, title, choices):
        body = [urwid.Text(title), urwid.Divider()]
        for c in choices:
            button = urwid.Button(c)
            urwid.connect_signal(button, 'click', self.item_chosen, c)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        listbox = urwid.ListBox(urwid.SimpleFocusListWalker(body))
        self.listbox = listbox
        return listbox

    def item_chosen(self, button, choice):
        pid = int(choice.split(':')[0])
        _proc[pid].kill()
        self._remove_item(button)

    def _remove_item(self, button):
        for item in self.listbox.body:
            try:
                if item.original_widget == button:
                    self.listbox.body.remove(item)
            except AttributeError:
                pass


def main():
    global proc
    name = ' '.join(sys.argv[1:])
    if not name:
        print("Usage: killit <search term>")
        sys.exit()

    processes = get_processes_by_name(name)

    for p in processes:
        _proc[p.pid] = p

    lines = ['%s: %s' % (pid, ' '.join(p.cmdline()))
             for (pid, p) in _proc.items()]

    menu = Menu()
    main = urwid.Padding(
        menu.menu(APP_BANNER, lines), left=2, right=2)
    top = urwid.Overlay(
        main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
        align='center', width=('relative', 80),
        valign='middle', height=('relative', 80),
        min_width=20, min_height=9)
    urwid.MainLoop(
        top,
        palette=[('reversed', 'standout', '')],
        unhandled_input=handle_keys).run()


if __name__ == "__main__":
    main()
