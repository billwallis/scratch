#!/usr/bin/env python

import os
import sys


# TODO: Add dictionary of "known" keys


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
            print(f"{_getch()!r}")
    except BaseException:  # noqa
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
