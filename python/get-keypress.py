#!/usr/bin/env python

import os
import string
import sys

GREEN = "\033[0;32m"
GREY = "\033[38;5;240m"
RESET = "\033[0m"

# Known keys
KEYS = {
    # Missing/named printables
    b" ": "space",
    b"\xc2\xac": "¬",
    b"\xc2\xa3": "£",
    # Command keys
    b"\x1b": "esc",
    b"\t": "tab",
    b"\x1b[Z": "shift+tab  (posix)",
    b"\r": "return  (windows)",
    b"\n": "return  (posix)",
    b"\x1b\n": "shift+return  (posix)",
    b"\x7f": "backspace  (posix)",
    b"\x1b\x7f": "ctrl+backspace  (posix)",
    b"\x1b[3~" : "delete  (posix)",
    b"\x1b[3;2~" : "shift+delete  (posix)",
    b"\x1b[3;9~" : "ctrl+delete  (posix)",
    b"\x1b[3;10~" : "ctrl+shift+delete  (posix)",
    b"\x1b[H" : "home  (posix)",
    b"\x1b[1;2H" : "shift+home  (posix)",
    b"\x1b\x1b[H" : "ctrl+shift+home  (posix)",
    b"\x1b[F" : "end  (posix)",
    b"\x1b[1;2F" : "shift+end  (posix)",
    b"\x1b\x1b[F" : "ctrl+shift+end  (posix)",
    b"\x1b[5~" : "page up  (posix)",
    b"\x1b[5;9~" : "ctrl+page up  (posix)",
    b"\x1b[5;10~" : "ctrl+shift+page up  (posix)",
    b"\x1b[6~" : "page down  (posix)",
    b"\x1b[6;9~" : "ctrl+page down  (posix)",
    b"\x1b[6;10~" : "ctrl+shift+page down  (posix)",
    # Arrow keys
    b"\xe0H": "up  (windows)",
    b"\x1b[A": "up  (posix)",
    b"\xe0P": "down  (windows)",
    b"\x1b[B": "down  (posix)",
    b"\xe0M": "right  (windows)",
    b"\x1b[C": "right  (posix)",
    b"\xe0K": "left  (windows)",
    b"\x1b[D": "left  (posix)",
    b"\x1b[1;2A": "shift+up  (posix)",
    b"\x1b[1;2B": "shift+down  (posix)",
    b"\x1b[1;2C": "shift+right  (posix)",
    b"\x1b[1;2D": "shift+left  (posix)",
    b"\x01": "ctrl+left  (posix)",
    b"\x05": "ctrl+right  (posix)",
    b"\x1b\x1b[A": "ctrl+shift+up  (posix)",
    b"\x1b\x1b[B": "ctrl+shift+down  (posix)",
    b"\x1b\x1b[C": "ctrl+shift+right  (posix)",
    b"\x1b\x1b[D": "ctrl+shift+left  (posix)",
    # Function keys
    b"\x1bOP": "F1  (posix)",
    b"\x1bOQ": "F2  (posix)",
    b"\x1bOR": "F3  (posix)",
    b"\x1bOS": "F4  (posix)",
    b"\x1b[15~": "F5  (posix)",
    b"\x1b[17~": "F6  (posix)",
    b"\x1b[18~": "F7  (posix)",
    b"\x1b[19~": "F8  (posix)",
    b"\x1b[20~": "F9  (posix)",
    b"\x1b[21~": "F10  (posix)",
    b"\x1b[24~": "F12  (posix)",
}


def _getch() -> bytes:
    """
    Prompt for single-key user input.

    Like `input()`, but returns immediately after one keypress.

    ---

    Source - https://stackoverflow.com/a/47197390
    Posted by neoDev, modified by community. See post 'Timeline' for change history
    Retrieved 2026-10-30, License - CC BY-SA 3.0
    """

    if sys.platform == "win32":
        import msvcrt

        key = msvcrt.getch()
        if key in (bytes([0]), bytes([224])):
            key = key + msvcrt.getch()

        return key
    else:
        import termios
        import tty

        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        try:
            return os.read(sys.stdin.fileno(), 32)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


def main() -> int:
    try:
        while True:
            key = _getch()
            name = "<unknown>"
            if key in KEYS:
                name = KEYS[key]
            elif key.decode() in string.printable:
                name = key.decode()
            print(f"{GREEN}{repr(key):<16}{RESET}  {GREY}{name}{RESET}")
    except BaseException:  # noqa
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
