# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "marimo>=0.21.1",
# ]
#
# [tool.marimo.opengraph]
# title = "01 · Running the Pipeline (CLI)"
# description = "canvodpy run: the recommended command-line interface for production ingestion. Covers date ranges, --update-to-latest, several sites, dry-run previews, and the ephemeris-source/VOD-calculator flags."
# ///

import marimo

__generated_with = "0.21.1"
app = marimo.App(
    width="medium",
    app_title="Running the Pipeline (CLI)",
    css_file="canvod_nordic.css",
    html_head_file="canvod_head.html",
)


@app.cell
def _():
    import marimo as mo

    mo.md(
        r"""
    <p align="center" class="canvod-logo">
      <img class="canvod-logo-light" src="https://raw.githubusercontent.com/nfb2021/canvodpy/main/docs/assets/logo/canvodpy_logo_bright_mode.svg" alt="canVODpy logo" width="280">
      <img class="canvod-logo-dark" src="https://raw.githubusercontent.com/nfb2021/canvodpy/main/docs/assets/logo/canvodpy_logo_dark_mode.svg" alt="canVODpy logo" width="280">
    </p>

    # Running the Pipeline: the CLI

    [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/nfb2021/canvodpy-demo/blob/main/01_cli_pipeline.py?mode=edit)

    `canvodpy run` is the recommended way to run production ingestion. It
    wraps the exact same code path as `Site(...).pipeline().process_range()`
    (covered in [18 · Site Pipeline](./18_site_pipeline.py)), adding
    a live progress display on top.

    ```bash
    uv run canvodpy run --site Rosalia --start 2025001 --end 2025007
    ```

    ---

    """
    )

    return (mo,)


# ---------------------------------------------------------------------------
# Section: basic usage
# ---------------------------------------------------------------------------


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Basic usage

    ```bash
    # Process a specific range
    uv run canvodpy run --site Rosalia --start 2025001 --end 2025007

    # Add every file not yet stored, up to the latest day with files.
    # This is what you want in a cron job.
    uv run canvodpy run --site Rosalia --update-to-latest

    # Observation ingestion only, skip VOD calculation
    uv run canvodpy run --site Rosalia --start 2025001 --end 2025007 --no-vod

    # Preview what would be processed, without executing anything
    uv run canvodpy run --site Rosalia --update-to-latest --dry-run
    ```

    Every run needs either `--start` or `--update-to-latest`; a run with
    neither stops with an error, and so does `--update-to-latest`
    together with `--start` or `--end`.

    **`--update-to-latest`** finds the dates for you and prints them
    (`update: 2025001 to 2025007`). It starts on the earliest last stored
    day among the receivers that have files not yet stored, so files that
    arrive late for a day already stored are still processed. It ends on
    the latest day with files. If no receiver has new files, it says so
    and exits without error; on an empty store it stops and asks for
    `--start`. A daily cron entry needs no date-math:

    ```
    0 3 * * * cd /path/to/canvodpy && uv run canvodpy run --site Rosalia --update-to-latest
    ```

    In Python, `Site(...).pipeline().run(update_to_latest=True)` does the
    same.
    """
    )

    return


# ---------------------------------------------------------------------------
# Section: multiple sites
# ---------------------------------------------------------------------------


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Several sites

    Each run processes one site: sites can differ in their dates, data
    and settings. For several sites, run one after the other in a shell
    loop:

    ```bash
    for site in Rosalia OtherSite ThirdSite; do
        uv run canvodpy run --site "$site" --update-to-latest
    done
    ```

    Each site finds its own dates from its own store. More than one site
    in a run stops with an error.
    """
    )

    return


# ---------------------------------------------------------------------------
# Section: ephemeris source and VOD calculator
# ---------------------------------------------------------------------------


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Choosing ephemeris source and VOD calculator

    ```bash
    # Override the configured ephemeris source for this run
    uv run canvodpy run --site Rosalia --ephemeris-source broadcast --update-to-latest

    # Choose a VOD calculator (choices come from VODFactory.list_available())
    uv run canvodpy run --site Rosalia --vod-calculator tau_omega --update-to-latest
    ```

    | Flag | Choices | Default |
    |------|---------|---------|
    | `--ephemeris-source` | `final` (agency SP3/CLK), `broadcast` (SBF SatVisibility) | from `canvod-settings.yaml` |
    | `--vod-calculator` | registered in `VODFactory` (currently `tau_omega`) | `tau_omega` |

    Both flags are one-off overrides for a single invocation; they don't
    modify `canvod-settings.yaml`. Bake in a value there once you've
    settled on it for a site.
    """
    )

    return


# ---------------------------------------------------------------------------
# Section: resources
# ---------------------------------------------------------------------------


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Workers

    ```bash
    uv run canvodpy run --site Rosalia --workers 8 --update-to-latest
    ```

    `--workers` sets the number of worker processes. Without it, the
    number comes from the resource settings in `canvod-settings.yaml`.
    The run sizes its units of days from the memory budget.
    """
    )

    return


# ---------------------------------------------------------------------------
# Section: config overlay
# ---------------------------------------------------------------------------


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Config overlay

    ```bash
    uv run canvodpy run --site Rosalia --config cluster-overlay.yaml --update-to-latest
    ```

    Applies an overlay YAML on top of the main `canvod-settings.yaml`:
    only the fields present in the overlay are changed, everything else
    is read from the main file. Useful on shared/HPC machines where
    resource limits vary per job but the base configuration is
    version-controlled.
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

    **Next**: [02 · Configuration](./02_configuration.py)

    *canVODpy · Apache 2.0*
    """
    )

    return


if __name__ == "__main__":
    app.run()
