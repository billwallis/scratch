import pathlib
import subprocess
import sys
import textwrap
from collections.abc import Iterable, Generator

HOME = pathlib.Path.home()
SKIP = (
    ".DS_Store",
    "__pycache__",
    ".venv",
)


def get_jetbrains_path(platform: str) -> pathlib.Path:
    if platform == "win32":
        jetbrains_path = HOME / "AppData/Roaming/JetBrains"
    else:
        jetbrains_path = HOME / "Library/Application Support/JetBrains"

    assert jetbrains_path.exists()  # noqa: S101
    return jetbrains_path


def run_cmd(
    cmds: Iterable[str],
    print_cmd: bool = False,
) -> Generator[str]:
    if print_cmd:
        print(" ".join(cmds))

    # https://stackoverflow.com/a/4417735
    popen = subprocess.Popen(
        args=cmds,
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )
    if popen.stdout:
        for line in popen.stdout:
            yield line.rstrip("\n")
    if popen.stderr:
        for line in popen.stderr:
            yield line.rstrip("\n")

    popen.wait()
    if popen.returncode != 0:
        raise RuntimeError()


def print_repo_contents(repo: pathlib.Path) -> None:
    scratch = repo / ".scratch"
    envrc = repo / ".envrc"
    poe_tasks = repo / "poe_tasks.toml"
    if not (scratch.exists() or poe_tasks.exists() or envrc.exists()):
        return

    print(repo)
    if scratch.exists():
        print(f"\t{scratch.name}/")
        for file in walk(scratch):
            print(f"\t\t{file.name}")
    if envrc.exists():
        print(f"\t{envrc.name}")
    if poe_tasks.exists():
        print(f"\t{poe_tasks.name}")


def walk(path: pathlib.Path) -> Generator[pathlib.Path]:
    assert path.is_dir(), f"'{path}' is not a directory"
    for child in path.iterdir():
        if child.name not in SKIP:
            yield child


def walk_and_print(directory: pathlib.Path) -> None:
    assert directory.is_dir(), f"'{directory}' is not a directory"
    print(directory)

    def _walk_and_print(path: pathlib.Path, depth: int) -> None:
        assert path.is_dir(), f"'{path}' is not a directory"
        children = sorted(walk(path), key=lambda f: f.is_dir())
        for child in children:
            if child.is_dir():
                print(textwrap.indent(child.name + "/", "\t" * depth))
                _walk_and_print(child, depth=depth + 1)
            else:
                print(textwrap.indent(child.name, "\t" * depth))

    _walk_and_print(directory, 1)


def main() -> int:
    print("-------------------------")
    print("Repositories to deal with")
    # Exploit the fact that I maintain a strict folder hierarchy
    for remote in walk(HOME / "repos"):
        for repo in walk(remote):
            print_repo_contents(repo)

    print("-----------------------")
    print("Other shit to deal with")
    walk_and_print(HOME / "bin")
    jetbrains_path = get_jetbrains_path(sys.platform)
    walk_and_print(jetbrains_path / "PyCharm2026.2/scratches")
    walk_and_print(jetbrains_path / "PyCharm2026.2/consoles/db")

    print("--------------------")
    print("Outstanding git work")
    all(run_cmd(("git", "meta", "update", str(HOME / "repos"))))
    for line in run_cmd(
        cmds=(
            "git",
            "meta",
            "report",
            str(HOME / "repos"),
            "--exclude",
            ".*/daily-tracker",
        ),
        print_cmd=True,
    ):
        print(line)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())  # pragma: no cover
