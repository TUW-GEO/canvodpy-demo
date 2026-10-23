# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "canvod-preflight",
#   "canvod-utils",
#   "canvodpy",
#   "marimo>=0.23.9",
# ]
#
# [tool.uv.sources]
# canvod-preflight = { git = "https://github.com/TUW-GEO/canvodpy.git", subdirectory = "packages/canvod-preflight", rev = "0ad152a240120d81929da5f2fa0e6c6c3cb9f25a" }
# canvod-utils = { git = "https://github.com/TUW-GEO/canvodpy.git", subdirectory = "packages/canvod-utils", rev = "0ad152a240120d81929da5f2fa0e6c6c3cb9f25a" }
# canvodpy = { git = "https://github.com/TUW-GEO/canvodpy.git", subdirectory = "canvodpy", rev = "0ad152a240120d81929da5f2fa0e6c6c3cb9f25a" }
#
# [tool.marimo.opengraph]
# title = "04 · Naming Convention & Validation"
# description = "Parse and validate GNSS filenames against the IGS/RINEX naming convention. Explore the structured metadata encoded in every canVODpy filename."
# ///

import marimo

__generated_with = "0.25.2"
app = marimo.App(
    width="medium",
    app_title="Naming Convention & Validation",
    css_file="canvod_nordic.css",
    html_head_file="canvod_head.html",
)


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    <p align="center" class="canvod-logo">
      <img class="canvod-logo-light" src="https://raw.githubusercontent.com/TUW-GEO/canvodpy/main/docs/assets/logo/canvodpy_logo_bright_mode.svg" alt="canVODpy logo" width="280">
      <img class="canvod-logo-dark" src="https://raw.githubusercontent.com/TUW-GEO/canvodpy/main/docs/assets/logo/canvodpy_logo_dark_mode.svg" alt="canVODpy logo" width="280">
    </p>

    # Naming Convention and File Validation

    [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/TUW-GEO/canvodpy-demo/blob/main/04_naming_convention.py)

    GNSS-Transmissometry campaigns generate thousands of files across
    multiple receivers, days, and sampling intervals.  Without a strict
    naming convention, duplicate or misattributed files can silently
    corrupt a dataset.

    The **canvod-preflight** package is the single source of truth for the
    canVOD filename convention.  Its **`CanVODFilename`** is a structured
    parser for the IGS-derived long-name convention.  `canvodpy run` uses it
    to find each receiver's files, and `canvodpy config validate` checks a
    site's files the same way before you process them.

    The naming convention encodes station identity, receiver role, time window,
    sampling rate, and file type into a single, self-describing filename.
    This eliminates ambiguity when ingesting data from multiple receivers
    and time periods.

    ---
    """)
    return


@app.cell
def _():
    from pathlib import Path

    from canvodpy import demo_data

    root = demo_data("rinex")
    canopy_dir = root / "rinex_v3_04" / "01_Rosalia" / "02_canopy" / "01_GNSS" / "01_raw"
    return (canopy_dir,)


@app.cell
def _(mo):
    mo.md(r"""
    ## The canVOD filename convention

    ```
    ROSA01TUW_R_20250010000_15M_05S_AA.rnx
    ^^^|^|^^^   ^^^^|^^^|^^^^ ^^^ ^^^ ^^
    SIT T NN AGC  YYYY DOY HHMM PER SMP PH  TYPE
    ```

    | Field | Chars | Description | Example |
    |-------|-------|-------------|---------|
    | **SIT** | 3 | Site identifier (uppercase) | `ROS` |
    | **T** | 1 | Receiver type: `R`=reference, `A`=active (canopy) | `A` |
    | **NN** | 2 | Receiver number (01--99) | `01` |
    | **AGC** | 3 | Operating agency (uppercase) | `TUW` |
    | `_R_` | 3 | Separator (RINEX convention) | |
    | **YYYY** | 4 | Year | `2025` |
    | **DOY** | 3 | Day of year (001--366) | `001` |
    | **HHMM** | 4 | Start hour and minute (GPS time) | `0000` |
    | **PER** | 3 | File duration (`15M`, `01H`, `01D`) | `15M` |
    | **SMP** | 3 | Sampling interval (`05S`, `01S`) | `05S` |
    | **PH** | 2 | Reserved; ignored during parsing | `AA` |
    | **TYPE** | 2-8 | File type (`rnx`, `sbf`, `nmea`, or a reader plugin's own) | `rnx` |

    This convention extends the
    [IGS long-name standard](http://acc.igs.org/misc/rinex304.pdf)
    (page 14f) with a receiver-type field (`T`) that distinguishes
    reference and canopy receivers at the same site.
    """)
    return


@app.cell
def _():
    from canvod.preflight import CanVODFilename

    return (CanVODFilename,)


@app.cell
def _(CanVODFilename, canopy_dir, mo):
    _file = sorted(canopy_dir.glob("25001/*.rnx"))[0]
    parsed = CanVODFilename.from_filename(_file.name)

    mo.md(f"""
    ## Parsing a filename

    ```python
    from canvod.preflight import CanVODFilename

    parsed = CanVODFilename.from_filename("{_file.name}")
    ```

    | Field | Value |
    |-------|-------|
    | **Site** | `{parsed.site}` |
    | **Receiver type** | `{parsed.receiver_type}` |
    | **Receiver number** | `{parsed.receiver_number}` |
    | **Agency** | `{parsed.agency}` |
    | **Year** | {parsed.year} |
    | **DOY** | {parsed.doy} |
    | **Hour:Minute** | {parsed.hour:02d}:{parsed.minute:02d} |
    | **Period** | `{parsed.period}` ({parsed.batch_duration}) |
    | **Sampling** | `{parsed.sampling}` ({parsed.sampling_interval}) |
    | **Content** | `{parsed.content}` |
    | **File type** | `{parsed.file_type}` |
    | **Reconstructed** | `{parsed.name}` |

    The model is frozen (immutable) and round-trips perfectly:
    `CanVODFilename.from_filename(parsed.name)` produces an identical object.
    """)
    return


@app.cell
def _(CanVODFilename, canopy_dir, mo):
    _files = sorted(canopy_dir.glob("25001/*.rnx"))

    _first_five = []
    for _f in _files[:5]:
        _p = CanVODFilename.from_filename(_f.name)
        _first_five.append(
            f"| `{_f.name}` | {_p.hour:02d}:{_p.minute:02d} | `{_p.period}` |"
        )

    _last = CanVODFilename.from_filename(_files[-1].name)

    mo.md(f"""
    ## Test data: one full day

    The canopy receiver directory contains **{len(_files)}** RINEX files
    covering DOY 2025-001 (1 January 2025).

    | File | Start (GPS time) | Period |
    |------|-------------|--------|
    {chr(10).join(_first_five)}
    | ... | | |
    | `{_files[-1].name}` | {_last.hour:02d}:{_last.minute:02d} | `{_last.period}` |

    The file period (`{_last.period}`) and total count are determined
    by the receiver configuration.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Which files a run processes

    `canvodpy run` scans each receiver's `directory` recursively, in any
    folder layout (all files in one folder, one folder per day, or deeper
    nesting).  A file's day comes from the date in its name, not from its
    folder.  Without a naming recipe, only files that follow the convention
    are processed; other files are passed over.  A run stops before reading
    any data if

    1. a directory holds files of more than one receiver,
    2. two files map to the same canonical name, or
    3. two files cover the same time, for example a daily file next to the
       15-minute files of the same day.

    Check a site before processing it.  The check finds the files exactly
    as a run does and also lists the files a run would pass over:

    ```bash
    canvodpy config validate --site <site>
    ```
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Files that don't follow the convention

    Sites that receive data from third-party operators often use their own
    naming schemes (RINEX v2 short names, Septentrio native names, etc.).
    The optional `canvod-filemap` package from
    [canvodpy-extensions](https://github.com/TUW-GEO/canvodpy-extensions)
    provides **naming recipes**: a recipe translates a receiver's physical
    filenames to canonical names, without renaming anything on disk.
    Create one per receiver and name it in the receiver's `recipe` setting:

    ```bash
    just naming-init <site> <recipe>
    ```

    Downstream code only sees canonical names, so processing behaves the
    same regardless of how files were originally named.

    A recipe can also live in a GitHub repository, so every computer that
    processes the site uses the same file. Give its raw URL, pinned to a
    commit or a tag:

    ```yaml
    recipe: https://raw.githubusercontent.com/<account>/<recipes-repo>/<commit>/recipes/<site>/<recipe>.yaml
    ```

    A recipe in a private repository needs a GitHub token in `GH_TOKEN` or
    `GITHUB_TOKEN`. The GNSS store records each receiver's recipe and the
    sha256 of its content, and a run stops if the settings give another
    recipe, since it would find other files than the days already stored.
    Record a recipe that changed on purpose, with a reason:

    ```bash
    canvodpy store amend <site> --update-recipe <receiver> --reason "..."
    ```
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    With canonical names, every file is unambiguously identified, and
    overlapping or misattributed files stop a run before any data is read.

    **Previous**: [03 · Speedrun: Full Pipeline](./03_convenience_speedrun.py)
    | **Next**: [05 · RINEX Reading](./05_rinex_reading.py)

    *canVODpy · Apache 2.0*
    """)
    return


if __name__ == "__main__":
    app.run()
