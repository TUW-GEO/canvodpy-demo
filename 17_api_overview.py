# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "canvod-auxiliary",
#   "canvod-config",
#   "canvod-grids",
#   "canvod-ops",
#   "canvod-preflight",
#   "canvod-readers",
#   "canvod-store",
#   "canvod-store-metadata",
#   "canvod-utils",
#   "canvod-viz",
#   "canvod-vod",
#   "canvodpy",
#   "marimo>=0.21.1",
# ]
#
# [tool.uv.sources]
# canvod-auxiliary = { git = "https://github.com/TUW-GEO/canvodpy.git", subdirectory = "packages/canvod-auxiliary", rev = "0ad152a240120d81929da5f2fa0e6c6c3cb9f25a" }
# canvod-config = { git = "https://github.com/TUW-GEO/canvodpy.git", subdirectory = "packages/canvod-config", rev = "0ad152a240120d81929da5f2fa0e6c6c3cb9f25a" }
# canvod-grids = { git = "https://github.com/TUW-GEO/canvodpy.git", subdirectory = "packages/canvod-grids", rev = "0ad152a240120d81929da5f2fa0e6c6c3cb9f25a" }
# canvod-ops = { git = "https://github.com/TUW-GEO/canvodpy.git", subdirectory = "packages/canvod-ops", rev = "0ad152a240120d81929da5f2fa0e6c6c3cb9f25a" }
# canvod-preflight = { git = "https://github.com/TUW-GEO/canvodpy.git", subdirectory = "packages/canvod-preflight", rev = "0ad152a240120d81929da5f2fa0e6c6c3cb9f25a" }
# canvod-readers = { git = "https://github.com/TUW-GEO/canvodpy.git", subdirectory = "packages/canvod-readers", rev = "0ad152a240120d81929da5f2fa0e6c6c3cb9f25a" }
# canvod-store = { git = "https://github.com/TUW-GEO/canvodpy.git", subdirectory = "packages/canvod-store", rev = "0ad152a240120d81929da5f2fa0e6c6c3cb9f25a" }
# canvod-store-metadata = { git = "https://github.com/TUW-GEO/canvodpy.git", subdirectory = "packages/canvod-store-metadata", rev = "0ad152a240120d81929da5f2fa0e6c6c3cb9f25a" }
# canvod-utils = { git = "https://github.com/TUW-GEO/canvodpy.git", subdirectory = "packages/canvod-utils", rev = "0ad152a240120d81929da5f2fa0e6c6c3cb9f25a" }
# canvod-viz = { git = "https://github.com/TUW-GEO/canvodpy.git", subdirectory = "packages/canvod-viz", rev = "0ad152a240120d81929da5f2fa0e6c6c3cb9f25a" }
# canvod-vod = { git = "https://github.com/TUW-GEO/canvodpy.git", subdirectory = "packages/canvod-vod", rev = "0ad152a240120d81929da5f2fa0e6c6c3cb9f25a" }
# canvodpy = { git = "https://github.com/TUW-GEO/canvodpy.git", subdirectory = "canvodpy", rev = "0ad152a240120d81929da5f2fa0e6c6c3cb9f25a" }
#
# [tool.marimo.opengraph]
# title = "17 · API Overview"
# description = "Survey canVODpy's supported surfaces: the canvodpy run CLI for production use and Site.pipeline(), the Python entry point it wraps."
# ///

import marimo

__generated_with = "0.21.1"
app = marimo.App(
    width="medium", app_title="API Overview", css_file="canvod_nordic.css",
    html_head_file="canvod_head.html"
)


@app.cell
def _():
    import marimo as mo

    mo.md(
        r"""
    <p align="center" class="canvod-logo">
      <img class="canvod-logo-light" src="https://raw.githubusercontent.com/TUW-GEO/canvodpy/main/docs/assets/logo/canvodpy_logo_bright_mode.svg" alt="canVODpy logo" width="280">
      <img class="canvod-logo-dark" src="https://raw.githubusercontent.com/TUW-GEO/canvodpy/main/docs/assets/logo/canvodpy_logo_dark_mode.svg" alt="canVODpy logo" width="280">
    </p>

    # canvodpy API Overview

    [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/TUW-GEO/canvodpy-demo/blob/main/17_api_overview.py)

    canvodpy has **two supported ways to run or script the pipeline**.
    Both produce the same scientific results (the same VOD values from
    the same input data) but differ in where you invoke them from.

    | Surface | Style | Entry point | Use case |
    |---------|-------|-------------|----------|
    | **CLI** | Command-line | `canvodpy run --site ...` | Running production ingestion (recommended) |
    | **Site pipeline** | Python, object-oriented | `Site(...).pipeline()` | Python-native scripting; what the CLI wraps internally |

    Earlier versions of canvodpy exposed four numbered "API levels"
    (L1 convenience one-liners, L2 fluent method chaining, L3 site
    pipelines, L4 functional). L1 and L2 are now deprecated: L1 was a
    thin wrapper around exactly what `Site.pipeline()` already does, and
    L2's fluent chain was superfluous alongside it. L4,
    `canvodpy.functional`, is no longer maintained and gives different
    results than `canvodpy run`. All three are deprecated: they still work
    (with a `FutureWarning`) until the next major version, but are no
    longer documented or taught. This notebook covers what replaced them.

    ---

    """
    )

    return (mo,)


# ---------------------------------------------------------------------------
# Section: CLI
# ---------------------------------------------------------------------------


@app.cell
def _(mo):
    mo.md(
        r"""
    ## CLI: running the pipeline

    The recommended way to run canvodpy in production: a single command,
    no Python required. Each run processes one site and needs either a
    start date or `--update-to-latest`.

    ```bash
    # Process a range
    uv run canvodpy run --site Rosalia --start 2025001 --end 2025007

    # Add every file not yet stored, up to the latest day with files
    uv run canvodpy run --site Rosalia --update-to-latest

    # Several sites: one run per site, in a shell loop
    for site in Rosalia OtherSite; do
        uv run canvodpy run --site "$site" --update-to-latest
    done

    # Preview without executing
    uv run canvodpy run --site Rosalia --update-to-latest --dry-run
    ```

    `--update-to-latest` starts on the earliest last stored day among the
    receivers that have files not yet stored, so files that arrive late for
    a day already stored are still processed. It prints the dates it chose.
    On an empty store it stops and asks for `--start`.

    The CLI is a thin wrapper around `Site(...).pipeline().process_range()`,
    with the same code path and the same guarantees. It adds a live
    progress display and a few production-oriented flags
    (`--ephemeris-source`, `--vod-calculator`, `--workers`).

    See [01 · Running the Pipeline (CLI)](./01_cli_pipeline.py) for a full
    walkthrough of the flags.
    """
    )

    return


# ---------------------------------------------------------------------------
# Section: Site pipeline
# ---------------------------------------------------------------------------


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Site pipeline: Python-native scripting

    `Site(...).pipeline()` is what the CLI calls internally. Use it
    directly when you need scripted control from Python: looping over
    sites, embedding a run inside a notebook, or customising resources
    per invocation.

    ```python
    from canvodpy import Site

    site = Site("my_site")

    with site.pipeline(n_workers=4) as pipe:
        for date_key, datasets in pipe.process_range("2025001", "2025010"):
            print(f"{date_key}: {list(datasets)}")
    ```

    Once data is ingested, `site.vod` (a `VodComputer`) gives finer control
    over VOD computation as a separate stage, useful for production
    deployments that ingest nightly and recompute VOD on a different
    schedule.

    See [18 · Site Pipeline](./18_site_pipeline.py) for the full walkthrough.
    """
    )

    return


# ---------------------------------------------------------------------------
# Section: factory system
# ---------------------------------------------------------------------------


@app.cell
def _(mo):
    from canvodpy.factories import GridFactory, ReaderFactory, VODFactory

    _readers = ReaderFactory.list_available()
    _grids = GridFactory.list_available()
    _vods = VODFactory.list_available()

    mo.md(
        f"""
    ## Factory system

    All pipeline components are registered in factory classes, enabling
    extensibility without modifying core code:

    ```python
    from canvodpy.factories import ReaderFactory, GridFactory, VODFactory

    # List available components
    ReaderFactory.list_available()   # {_readers}
    GridFactory.list_available()     # {_grids}
    VODFactory.list_available()      # {_vods}

    # Register a custom component
    from my_package import MyCustomCalculator
    VODFactory.register("my_calculator", MyCustomCalculator)
    ```

    | Factory | Registered components |
    |---------|-----------------------|
    | `ReaderFactory` | {", ".join(f"`{r}`" for r in _readers)} |
    | `GridFactory` | {", ".join(f"`{g}`" for g in _grids)} |
    | `VODFactory` | {", ".join(f"`{v}`" for v in _vods)} |

    Custom components must implement the corresponding abstract base
    class (`GNSSDataReader`, `BaseGridBuilder`, or `VODCalculator`). A
    component registered here exists in this Python session only;
    `canvodpy run` starts its own. Readers and VOD calculators reach
    `canvodpy run` as a plugin: a package of your own that declares them
    as entry points (`canvodpy.readers`, `canvodpy.vod_calculators`).
    Installed plugins are registered when canvodpy is imported, so they
    appear in the table above and in `canvodpy run --vod-calculator`.
    [21 · Your Own VOD Calculator](./21_plugins.py) shows both ways.
    """
    )

    return GridFactory, ReaderFactory, VODFactory


# ---------------------------------------------------------------------------
# Section: choosing a surface
# ---------------------------------------------------------------------------


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Choosing a surface

    | If you want to... | Use |
    |-------------------|-----|
    | Run production ingestion from a shell/cron, `--update-to-latest` | CLI: `canvodpy run` |
    | Script a run in Python: loop over sites, embed in a notebook | `Site(...).pipeline()` |
    | Recompute VOD separately from ingestion | `Site(...).vod` (`VodComputer`) |
    | Orchestrate with Airflow | The optional `canvod-airflow` extension (`canvodpy.workflows.tasks`) |
    | Inspect or modify an intermediate step for research | The `canvod-*` packages directly, see [19 · Single-Day Workflow](./19_workflow_single_day.py) |
    | Extend with a custom reader/grid/calculator | Factories: `VODFactory.register()` (this session) |
    | Use your own reader or VOD calculator in `canvodpy run` | A plugin package (entry points), see [21 · Your Own VOD Calculator](./21_plugins.py) |

    The CLI and `Site(...).pipeline()` share the same implementation, so you
    can mix them freely. A common pattern: use the CLI for scheduled
    production runs, and `Site(...)` in an analysis notebook to open the
    stores the CLI wrote.

    ---

    The following notebooks demonstrate each surface in detail:

    - [01 · Running the Pipeline (CLI)](./01_cli_pipeline.py)
    - [18 · Site Pipeline](./18_site_pipeline.py)
    """
    )

    return


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------


@app.cell
def _(mo):
    mo.md(
        r"""
    ---

    **Previous**: [16 · 3D Grid Gallery](./16_grid_3d_gallery.py)
    | **Next**: [18 · Site Pipeline](./18_site_pipeline.py)

    *canVODpy · Apache 2.0*
    """
    )

    return


if __name__ == "__main__":
    app.run()
