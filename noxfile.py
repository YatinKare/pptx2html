# noxfile.py
from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, cast

from nox_uv import session as _session  # type: ignore

# Provide a typed alias for the decorator to keep mypy happy even without stubs
SessionDecorator = Callable[[Callable[..., Any]], Callable[..., Any]]
session: SessionDecorator = cast(SessionDecorator, _session)

ROOT = Path(__file__).parent


def _posarg(default: str, flag: str, posargs: list[str]) -> list[str]:
    """Extract a '--flag value' pair from posargs or use default."""
    if flag in posargs:
        i = posargs.index(flag)
        try:
            return [flag, posargs[i + 1]]
        except IndexError:
            pass
    return [flag, default]


@session  # clean, uv-managed venv each run
def user_editable(s: Any) -> None:
    """
    User-like run: editable install, then execute the example runner.
    Usage:
      nox -s user_editable -- --input /path/to.pptx --out out_dir --debug
    """
    s.run("uv", "pip", "install", "-e", ".")
    # pass-through args with sane defaults
    args = []
    args += _posarg("Galaxy presentation.pptx", "--input", s.posargs)
    args += _posarg("out_editable", "--out", s.posargs)
    if "--debug" in s.posargs:
        args += ["--debug"]
    s.run("python", str(ROOT / "examples" / "runner.py"), *args)


@session
def user_wheel(s: Any) -> None:
    """
    Real-user simulation: build wheel, install it into a fresh env, run example
    Usage:
      nox -s user_wheel -- --input /path/to.pptx --out out_dir --open
    """
    s.run("uv", "build")
    dist = ROOT / "dist"
    wheels = sorted(dist.glob("*.whl"))
    if not wheels:
        s.error("No wheel found in dist/")
    wheel = str(wheels[-1])
    s.run("uv", "pip", "install", wheel)

    args = []
    args += _posarg("Galaxy presentation.pptx", "--input", s.posargs)
    args += _posarg("out_wheel", "--out", s.posargs)
    if "--debug" in s.posargs:
        args += ["--debug"]
    s.run("python", str(ROOT / "examples" / "runner.py"), *args)
