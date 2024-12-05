# SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
# SPDX-License-Identifier: BSD-2-Clause
"""Make sure that `venv-retarget run` starts up at least."""

from __future__ import annotations

import dataclasses
import functools
import json
import os
import pathlib
import subprocess  # noqa: S404
import sys
import tempfile
import typing

import pytest

from venv_retarget import defs
from venv_retarget import detect
from venv_retarget import impl
from venv_retarget import util


if typing.TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Final


@functools.lru_cache
def get_venv_python() -> str:
    """Either use the specified Python implementation or the current interpreter."""
    return os.environ.get("VENV_PYTHON", sys.executable)


@functools.lru_cache
def get_venv_python_version_info() -> tuple[int, int]:
    """Get the first two components of the `sys.version_info` tuple."""
    py: Final = get_venv_python()
    lines: Final = subprocess.check_output(  # noqa: S603
        [py, "-c", "import sys; print(sys.version_info[0]); print(sys.version_info[1]);"],
        encoding="UTF-8",
    ).splitlines()
    match lines:
        case [major, minor]:
            return int(major), int(minor)

        case _:
            raise RuntimeError(repr(lines))


def test_detect() -> None:
    """Create the simplest venv, make sure `detect_path()` works on it."""
    cfg: Final = defs.Config(log=util.build_logger(verbose=True), verbose=True)
    with tempfile.TemporaryDirectory(prefix="venv-retarget-test.") as tempd_obj:
        tempd: Final = pathlib.Path(tempd_obj)
        print(f"\nUsing {tempd} as a temporary directory")

        venvdir: Final = tempd / "harumph"
        subprocess.check_call([get_venv_python(), "-m", "venv", "--", venvdir])  # noqa: S603

        detected: Final = detect.detect_path(cfg, venvdir, use_prefix=True)
        assert detected.path == venvdir
        assert detected.cache_path == venvdir
        assert detected.prefix_path == venvdir

        if get_venv_python_version_info() >= (3, 11):
            assert detected.cfg_path == venvdir
        else:
            assert detected.cfg_path is None

        venvnew: Final = tempd / "hooray"
        venvdir.rename(venvnew)

        detected_new: Final = detect.detect_path(cfg, venvnew)
        assert detected_new == dataclasses.replace(detected, prefix_path=None)


def test_run_detect() -> None:
    """Create the simplest venv, run `venv-retarget detect` on it."""
    with tempfile.TemporaryDirectory(prefix="venv-retarget-test.") as tempd_obj:
        tempd: Final = pathlib.Path(tempd_obj)
        print(f"\nUsing {tempd} as a temporary directory")

        venvdir: Final = tempd / "trinket"
        subprocess.check_call([get_venv_python(), "-m", "venv", "--", venvdir])  # noqa: S603

        raw: Final = subprocess.check_output(  # noqa: S603
            [sys.executable, "-m", "venv_retarget", "detect", "--", venvdir],
            encoding="UTF-8",
        )
        print(f"{raw=!r}")
        decoded: Final = json.loads(raw)
        print(f"{decoded=!r}")
        assert decoded["path"] == str(venvdir)
        assert sorted(decoded.keys()) == sorted(
            field.name for field in dataclasses.fields(detect.Detected)
        )


def do_test_retarget(
    cb_retarget: Callable[[defs.Config, pathlib.Path, pathlib.Path | None], None],
    *,
    before: bool,
) -> None:
    """Create a venv, move it, make sure `.detect_path()` works on the new venv."""
    cfg: Final = defs.Config(log=util.build_logger(verbose=True), verbose=True)
    with tempfile.TemporaryDirectory(prefix="venv-retarget-test.") as tempd_obj:
        tempd: Final = pathlib.Path(tempd_obj)
        print(f"\nUsing {tempd} as a temporary directory")

        venvdir: Final = tempd / "this"
        subprocess.check_call([get_venv_python(), "-m", "venv", "--", venvdir])  # noqa: S603
        assert os.access(venvdir / "pyvenv.cfg", os.R_OK)
        assert os.access(venvdir / "bin" / "pip", os.X_OK)

        detected: Final = detect.detect_path(cfg, venvdir, use_prefix=True)
        assert detected.path == venvdir
        assert detected.cache_path == venvdir
        assert detected.prefix_path == venvdir

        if get_venv_python_version_info() >= (3, 11):
            assert detected.cfg_path == venvdir
        else:
            assert detected.cfg_path is None

        venvnew: Final = tempd / "that"

        if before:
            cb_retarget(cfg, venvdir, venvnew)
            assert os.access(venvdir / "pyvenv.cfg", os.R_OK)
            assert os.access(venvdir / "bin" / "pip", os.X_OK)

            detected_before: Final = detect.detect_path(cfg, venvdir)
            assert detected_before.path == venvnew
            assert detected_before.cache_path == venvnew
            assert detected_before.prefix_path is None

            if get_venv_python_version_info() >= (3, 11):
                assert detected_before.cfg_path == venvnew
            else:
                assert detected_before.cfg_path is None

        venvdir.rename(venvnew)

        if before:
            detected_after = detect.detect_path(cfg, venvnew, use_prefix=True)
            assert detected_after == dataclasses.replace(detected_before, prefix_path=venvnew)
        else:
            cb_retarget(cfg, venvnew, None)
            assert os.access(venvnew / "pyvenv.cfg", os.R_OK)
            assert os.access(venvnew / "bin" / "pip", os.X_OK)

            detected_after = detect.detect_path(cfg, venvnew, use_prefix=True)
            assert detected_after.path == venvnew
            assert detected_after.cache_path == venvnew
            assert detected_after.prefix_path == venvnew

            if get_venv_python_version_info() >= (3, 11):
                assert detected_after.cfg_path == venvnew
            else:
                assert detected_after.cfg_path is None


@pytest.mark.parametrize("before", [False, True])
def test_retarget(*, before: bool) -> None:
    """Create a venv, move it, make sure `.detect_path()` works on the new venv."""

    def retarget_call_func(
        cfg: defs.Config,
        venvdir: pathlib.Path,
        venvnew: pathlib.Path | None,
    ) -> None:
        """Invoke the function directly."""
        impl.retarget(cfg, venvdir, venvdst=venvnew)

    do_test_retarget(retarget_call_func, before=before)


@pytest.mark.parametrize("before", [False, True])
def test_run_retarget(*, before: bool) -> None:
    """Create a venv, move it, make sure `.detect_path()` works on the new venv."""

    def retarget_spawn(
        _cfg: defs.Config,
        venvdir: pathlib.Path,
        venvnew: pathlib.Path | None,
    ) -> None:
        """Spawn the command-line tool to retarget the venv."""
        vnewopts: Final[list[str | pathlib.Path]] = ["-d", venvnew] if venvnew is not None else []
        subprocess.check_call(  # noqa: S603
            [sys.executable, "-m", "venv_retarget", "-v", "retarget", *vnewopts, "--", venvdir],
        )

    do_test_retarget(retarget_spawn, before=before)
