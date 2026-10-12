"""Build live Icechunk stores from real Rosalia RINEX v3.04 raw data.

demo/11_icechunk_store.py and demo/13_workflow_store_operations.py both
need a populated MyIcechunkStore to render their read-only demo cells
(branches, groups, commit history, metadata ledger, root attrs). No
pre-built store fixture is published: canvodpy-test-data commit 7da92ea
accidentally gitignored the store fixture's chunk/manifest/snapshot data,
so both the tracked repo and its Zenodo archive contain only an empty
first-commit snapshot (unrecoverable).

This module runs the real `canvodpy` CLI once, at notebook-run time,
against the real raw RINEX under `_paths.ROSALIA` -- never against
`_paths.STORES_DIR`, which is read-only test data -- writing into a fresh
scratch Icechunk repository. Uses the CLI (not the Python Site/Pipeline API
directly) per this project's own documented "Running-the-pipeline rule",
via `sys.executable -m canvodpy.cli.app run --config-dir <dir>` so it runs
in the same interpreter/venv this notebook's own PEP 723 deps already
resolved -- no dependency on `canvodpy`'s console-script entry point being
on PATH.

The run reads only a settings file written into its own scratch directory
(`--config-dir`), so it needs no canvodpy checkout and no settings of the
machine: it runs the same in a standalone clone, on molab, from the Zenodo
download and inside the canvodpy monorepo.

`--no-vod` defaults to False and the recipe defines `vod_analyses`, so a
single CLI run produces *both* a GNSS store and a VOD store
(sibling directories under the same scratch `stores_root_dir`) -- no
separate VOD computation step needed. `_run_pipeline()` runs the CLI once
and is shared/cached by both accessors below, so calling both
`build_rosalia_store()` and `build_rosalia_vod_store()` in the same kernel
session only invokes the pipeline once.

Usage in a notebook cell::

    from _live_store import (
        build_rosalia_store, build_rosalia_vod_store,
        get_pipeline_command, get_pipeline_output,
    )
    store, store_path = build_rosalia_store()
    vod_store, vod_store_path = build_rosalia_vod_store()
    mo.md(f"```bash\\n{get_pipeline_command()}\\n```")
    mo.md(f"```text\\n{get_pipeline_output()}\\n```")
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import yaml

import _paths

if TYPE_CHECKING:
    from canvod.store import MyIcechunkStore

_RECIPE_PATH = Path(__file__).resolve().parent / "_rosalia_v3_04_recipe.yaml"
_SITE_NAME = "rosalia_v3_04"
_DATE = "2025001"  # the only DOY the test-data fixture ships

_cached: tuple["MyIcechunkStore", Path, "MyIcechunkStore", Path] | None = None
_last_cmd: list[str] | None = None
_last_stdout: str | None = None
_last_stderr: str | None = None


def _seed_aux_cache(scratch_aux_dir: Path) -> None:
    """Copy real SP3/CLK products into a writable scratch dir.

    The pipeline reads raw products from `aux_data_dir/01_SP3` and
    `.../02_CLK` but also *writes* its Hermite-interpolated cache back into
    the same `aux_data_dir` tree (`00_aux_zarr/`) -- confirmed via direct
    read of canvodpy/orchestrator/processor.py's
    `_ensure_aux_data_preprocessed`. So `aux_data_dir` can never be
    `_paths.AUX_DATA_DIR` directly (that's the read-only submodule); copy
    the real products into a scratch dir instead. A local-file hit means
    `download_aux_file()` is never called (it only fetches
    `if not file_path.exists()`), so this seed step means zero network
    calls. The fixture holds the orbits and clocks of 2024-366, 2025-001
    and 2025-002: a run joins the previous and the next day to the
    processed one, so the first and last epochs are interpolated, not
    extrapolated.
    """
    shutil.copytree(_paths.SP3_DIR, scratch_aux_dir / "01_SP3")
    shutil.copytree(_paths.CLK_DIR, scratch_aux_dir / "02_CLK")


def _write_settings(scratch_dir: Path) -> Path:
    """Write the run's settings file: the tracked recipe plus this run's paths.

    The tracked recipe (_rosalia_v3_04_recipe.yaml) deliberately omits
    `gnss_site_data_root`, the storage paths and the log folder -- those are real absolute
    paths that vary by machine/CI runner, injected here instead. The result
    is the complete `canvod-settings.yaml` of a configuration directory of
    its own, returned for `--config-dir`.
    """
    recipe = yaml.safe_load(_RECIPE_PATH.read_text())
    recipe["sites"][_SITE_NAME]["gnss_site_data_root"] = str(_paths.ROSALIA)
    recipe.setdefault("processing", {}).setdefault("storage", {}).update(
        {
            "stores_root_dir": str(scratch_dir / "stores"),
            "aux_data_dir": str(scratch_dir / "aux"),
            "shared_aux_cache_dir": None,
        }
    )
    # A run needs a log folder (processing.logging.log_dir).
    recipe["processing"].setdefault("logging", {})["log_dir"] = str(
        scratch_dir / "logs"
    )
    config_dir = scratch_dir / "config"
    config_dir.mkdir()
    (config_dir / "canvod-settings.yaml").write_text(
        yaml.safe_dump(recipe, sort_keys=False)
    )
    return config_dir


def _run_pipeline(n_workers: int | None = 2) -> tuple["MyIcechunkStore", Path, "MyIcechunkStore", Path]:
    """Run the real ingest+VOD pipeline once and return both populated stores.

    A single `canvodpy run` produces a GNSS store *and* a VOD
    store (`--no-vod` defaults to False, and the recipe defines
    `vod_analyses`) -- both are scratch Icechunk repositories under a
    freshly created `tempfile.mkdtemp()` directory, never inside the
    read-only `_paths.STORES_DIR` tree. Not cleaned up automatically (same
    trade-off `03_convenience_speedrun.py` and `19_workflow_single_day.py`
    already make re-decoding RINEX from scratch on every run: consistency
    over caching across kernel restarts). Cached for the remainder of this
    kernel session so re-importing/re-calling within one run doesn't
    rebuild, and so `build_rosalia_store()` + `build_rosalia_vod_store()`
    together only invoke the CLI once.
    """
    global _cached, _last_cmd, _last_stdout, _last_stderr
    if _cached is not None:
        return _cached

    _paths.ensure_data()  # no-op if an earlier cell already resolved it

    scratch_dir = Path(tempfile.mkdtemp(prefix="canvodpy_demo_rosalia_store_"))
    _seed_aux_cache(scratch_dir / "aux")
    config_dir = _write_settings(scratch_dir)

    cmd = [
        sys.executable,
        "-m",
        "canvodpy.cli.app",
        "run",
        "--site",
        _SITE_NAME,
        "--start",
        _DATE,
        "--end",
        _DATE,
        "--config-dir",
        str(config_dir),
    ]
    if n_workers is not None:
        cmd += ["--workers", str(n_workers)]
    _last_cmd = cmd

    # cwd=scratch_dir: the run must not depend on where marimo was started.
    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=scratch_dir
    )
    _last_stdout = result.stdout
    _last_stderr = result.stderr
    if result.returncode != 0:
        raise RuntimeError(
            "canvodpy run failed while building the demo stores "
            f"(exit {result.returncode}):\n"
            f"--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}"
        )

    from canvod.config import load_config
    from canvod.store import MyIcechunkStore

    # Resolve the store paths from the settings the run used rather than
    # guessing directory names.
    settings = load_config(config_dir=config_dir)
    store_path = settings.processing.storage.get_gnss_store_path(_SITE_NAME)
    vod_store_path = settings.processing.storage.get_vod_store_path(_SITE_NAME)
    store = MyIcechunkStore(store_path=store_path, config=settings)
    vod_store = MyIcechunkStore(
        store_path=vod_store_path, store_type="vod_store", config=settings
    )
    _cached = (store, store_path, vod_store, vod_store_path)
    return _cached


def build_rosalia_store(n_workers: int | None = 2) -> tuple["MyIcechunkStore", Path]:
    """Return (store, store_path) for the GNSS store."""
    store, store_path, _vod_store, _vod_store_path = _run_pipeline(n_workers)
    return store, store_path


def build_rosalia_vod_store(n_workers: int | None = 2) -> tuple["MyIcechunkStore", Path]:
    """Return (vod_store, vod_store_path) for the VOD store."""
    _store, _store_path, vod_store, vod_store_path = _run_pipeline(n_workers)
    return vod_store, vod_store_path


def get_pipeline_command() -> str:
    """Return the exact `canvodpy run` command last executed, shell-quoted.

    marimo notebooks can't run shell commands directly (there's no cell
    type for it), but the CLI invocation is real and worth showing --
    render this string in a markdown code fence rather than leaving the
    subprocess call as an invisible implementation detail. Call after
    build_rosalia_store()/build_rosalia_vod_store() in the same cell (or a
    later one -- _run_pipeline() is cached, so the command persists for the
    rest of the kernel session).
    """
    if _last_cmd is None:
        return "# not yet run -- call build_rosalia_store() or build_rosalia_vod_store() first"
    import shlex

    return " ".join(shlex.quote(part) for part in _last_cmd)


def get_pipeline_output() -> str:
    """Return the captured stdout+stderr of the last `canvodpy run` invocation.

    subprocess.run(..., capture_output=True) buffers everything and only
    returns once the process exits -- there's no way to stream a live,
    in-place-updating progress bar into a marimo cell this way, so this is
    the full transcript *after* the run finished, not a live view. Still
    real and worth showing: the CLI prints a run banner, ephemeris/aux
    status, and per-date progress that would otherwise be silently
    discarded (subprocess.run's captured output was previously only
    surfaced on failure).
    """
    if _last_stdout is None:
        return "# not yet run -- call build_rosalia_store() or build_rosalia_vod_store() first"
    combined = _last_stdout
    if _last_stderr:
        combined += f"\n--- stderr ---\n{_last_stderr}"
    return combined
