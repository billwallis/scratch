"""
Dump console contents.
"""

from __future__ import annotations

import dataclasses
import logging
import pathlib
import re
import shutil
import sys
import uuid
from collections.abc import Generator

HERE = pathlib.Path(__file__).resolve().parent
TARGET_PATH = HERE / "consoles"

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
BLUE = "\033[0;34m"
MAGENTA = "\033[0;35m"
CYAN = "\033[0;36m"
GREY = "\033[38;5;240m"
BOLD = "\033[1m"
RESET = "\033[0m"

logger = logging.getLogger(__file__)
logging.basicConfig(
    level=logging.DEBUG,
    format=f"{GREY}%(asctime)s{RESET}  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def colour(text: str, colour_: str) -> str:
    return f"{colour_}{text}{RESET}"


@dataclasses.dataclass
class ConsolePath:
    path: pathlib.Path
    tool: str
    uuid: uuid.UUID

    @classmethod
    def from_path(cls, filepath: pathlib.Path, pattern: re.Pattern) -> ConsolePath:
        match = pattern.search(filepath.as_posix())
        if match is None:
            raise ValueError(f"unexpected filepath: '{filepath}'")
        return ConsolePath(
            path=filepath,
            tool=match.group("tool"),
            uuid=uuid.UUID(match.group("uuid")),
        )


def get_jetbrains_path(platform: str) -> pathlib.Path:
    if platform == "win32":
        jetbrains_path = pathlib.Path.home() / "AppData/Roaming/JetBrains"
    else:
        jetbrains_path = pathlib.Path.home() / "Library/Application Support/JetBrains"

    assert jetbrains_path.exists()  # noqa: S101
    return jetbrains_path


def get_console_pattern(jetbrains_path: pathlib.Path) -> re.Pattern:
    # <jetbrains path>/<versioned IDE>/consoles/db/<uuid>/console.sql
    return re.compile(
        rf"{jetbrains_path.as_posix()}/(?P<tool>[\w. ]+)/consoles/db/(?P<uuid>[0-9a-f-]{{36}})/console\.sql"
    )


def walk(path: pathlib.Path, pattern: re.Pattern) -> Generator[pathlib.Path]:
    # It's inefficient to only check the _files_ rather than immediately
    # omit entire directories, but alas, I cba to optimise this :shrug:
    for child in path.iterdir():
        if child.is_file():
            if pattern.match(child.as_posix()):
                yield child
        else:
            yield from walk(child, pattern)


def get_consoles(
    jetbrains_path: pathlib.Path,
    console_pattern: re.Pattern,
) -> Generator[ConsolePath]:
    logger.info(colour("parsing filepaths", BLUE))
    for filename in walk(jetbrains_path, pattern=console_pattern):
        yield ConsolePath.from_path(filepath=filename, pattern=console_pattern)


def write_console(
    source_console: ConsolePath,
    target_directory: pathlib.Path,
) -> None:
    target_console_path = (
        target_directory / source_console.tool / f"{source_console.uuid}.sql"
    )
    target_console_path.parent.mkdir(parents=True, exist_ok=True)
    logger.debug(
        colour(f"copying '{source_console.path}' to '{target_console_path}'", GREEN)
    )
    shutil.copy(
        src=source_console.path,
        dst=target_console_path,
    )


def main() -> int:
    jetbrains_path = get_jetbrains_path(platform=sys.platform)
    console_pattern = get_console_pattern(jetbrains_path=jetbrains_path)
    consoles = get_consoles(
        jetbrains_path=jetbrains_path,
        console_pattern=console_pattern,
    )
    logger.info(colour("copying consoles", BLUE))
    for console in consoles:
        write_console(
            source_console=console,
            target_directory=TARGET_PATH,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
