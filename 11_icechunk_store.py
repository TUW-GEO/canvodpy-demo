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
#   "pooch>=1.6",
#   "pyyaml>=6.0",
#   "marimo>=0.21.1",
# ]
#
# [tool.uv.sources]
# canvod-auxiliary = { git = "https://github.com/nfb2021/canvodpy.git", subdirectory = "packages/canvod-auxiliary", rev = "e6e90bedd25e7d42d240cbf3a6cb80edc811c97e" }
# canvod-config = { git = "https://github.com/nfb2021/canvodpy.git", subdirectory = "packages/canvod-config", rev = "e6e90bedd25e7d42d240cbf3a6cb80edc811c97e" }
# canvod-grids = { git = "https://github.com/nfb2021/canvodpy.git", subdirectory = "packages/canvod-grids", rev = "e6e90bedd25e7d42d240cbf3a6cb80edc811c97e" }
# canvod-ops = { git = "https://github.com/nfb2021/canvodpy.git", subdirectory = "packages/canvod-ops", rev = "e6e90bedd25e7d42d240cbf3a6cb80edc811c97e" }
# canvod-preflight = { git = "https://github.com/nfb2021/canvodpy.git", subdirectory = "packages/canvod-preflight", rev = "e6e90bedd25e7d42d240cbf3a6cb80edc811c97e" }
# canvod-readers = { git = "https://github.com/nfb2021/canvodpy.git", subdirectory = "packages/canvod-readers", rev = "e6e90bedd25e7d42d240cbf3a6cb80edc811c97e" }
# canvod-store = { git = "https://github.com/nfb2021/canvodpy.git", subdirectory = "packages/canvod-store", rev = "e6e90bedd25e7d42d240cbf3a6cb80edc811c97e" }
# canvod-store-metadata = { git = "https://github.com/nfb2021/canvodpy.git", subdirectory = "packages/canvod-store-metadata", rev = "e6e90bedd25e7d42d240cbf3a6cb80edc811c97e" }
# canvod-utils = { git = "https://github.com/nfb2021/canvodpy.git", subdirectory = "packages/canvod-utils", rev = "e6e90bedd25e7d42d240cbf3a6cb80edc811c97e" }
# canvod-viz = { git = "https://github.com/nfb2021/canvodpy.git", subdirectory = "packages/canvod-viz", rev = "e6e90bedd25e7d42d240cbf3a6cb80edc811c97e" }
# canvod-vod = { git = "https://github.com/nfb2021/canvodpy.git", subdirectory = "packages/canvod-vod", rev = "e6e90bedd25e7d42d240cbf3a6cb80edc811c97e" }
# canvodpy = { git = "https://github.com/nfb2021/canvodpy.git", subdirectory = "canvodpy", rev = "e6e90bedd25e7d42d240cbf3a6cb80edc811c97e" }
#
# [tool.marimo.opengraph]
# title = "11 · Icechunk Store"
# description = "Write, read, and version GNSS-T datasets in a cloud-native Icechunk/Zarr store. Explore branching, snapshots, and deduplication guardrails."
# ///

import marimo

__generated_with = "0.24.0"
app = marimo.App(
    width="medium",
    app_title="Icechunk Store",
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

    # Versioned GNSS Data Storage with Icechunk

    [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/nfb2021/canvodpy-demo/blob/main/11_icechunk_store.py?mode=edit)

    The **canvod-store** package provides a versioned, transactional storage
    layer built on **Icechunk**, a Git-like version control system for
    N-dimensional arrays (Zarr v3).

    Each observation dataset is stored as a Zarr group inside an Icechunk
    repository.  The store provides:

    - **Append-only ingestion** with three-layer deduplication
      (file hash, temporal overlap, intra-batch overlap)
    - **Branching and tagging** for experimental analyses
    - **Commit history** with full audit trail
    - **Session management** (read-only and writable contexts)
    - **Metadata ledger** tracking which files have been ingested

    ---

    **Test data**: the GNSS store and the VOD store that `canvodpy run`
    writes from the Rosalia RINEX v3.04 day, 2025-01-01 (canopy and
    reference receiver), downloaded with `canvodpy.demo_data("stores")`.
    They are canVODpy's published reference stores. How a run builds
    them is shown in [01 · CLI Pipeline](./01_cli_pipeline.py).

    """
    )
    return (mo,)


@app.cell
def _(mo):
    from canvod.store import open_gnss_store
    from canvodpy import demo_data

    stores_root = demo_data("stores") / "stores" / "rosalia_rinex_v3_04"
    store_path = stores_root / "gnss"
    store = open_gnss_store(store_path)

    _branches = store.get_branch_names()
    _groups = store.list_groups()

    mo.md(
        f"""
    ## Opening a store

    ```python
    from canvod.store import open_gnss_store
    from canvodpy import demo_data

    stores_root = demo_data("stores") / "stores" / "rosalia_rinex_v3_04"
    store = open_gnss_store(stores_root / "gnss")
    ```

    For your own site, give the path of its GNSS store, for example
    `open_gnss_store("/data/stores/my_site/gnss")`.

    | Property | Value |
    |----------|-------|
    | **Path** | `{store_path}` |
    | **Branches** | {", ".join(f"`{b}`" for b in _branches)} |
    | **Groups** | {", ".join(f"`{g}`" for g in _groups) if _groups else "(empty)"} |

    `demo_data("stores")` downloads the store once and returns the same
    folder on every later call. This notebook only reads it; copy a
    store before you write to it.
    """
    )
    return store, stores_root


@app.cell
def _(store):
    store
    return


@app.cell
def _(mo, stores_root):
    from canvod.store import open_vod_store

    vod_store_path = stores_root / "vod"
    vod_store = open_vod_store(vod_store_path)

    _vod_branches = vod_store.get_branch_names()
    _vod_groups = vod_store.list_groups()

    mo.md(
        f"""
    ## The VOD store

    VOD products live in a **separate** Icechunk store, sibling to the GNSS
    store above -- same `MyIcechunkStore` class, but groups are
    nested `{{calculator_name}}/{{analysis_name}}` rather than flat
    per-receiver names, since one VOD store can hold output from multiple
    retrieval algorithms.

    ```python
    vod_store = open_vod_store(stores_root / "vod")
    ```

    | Property | Value |
    |----------|-------|
    | **Path** | `{vod_store_path}` |
    | **Branches** | {", ".join(f"`{b}`" for b in _vod_branches)} |
    | **Groups** | {", ".join(f"`{g}`" for g in _vod_groups) if _vod_groups else "(empty)"} |

    A normal `canvodpy run` writes to both stores in the same pipeline pass
    whenever the site config defines `vod_analyses` -- no separate VOD
    computation step is needed.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Reading data

    The `readonly_session()` context manager opens a snapshot of the store
    at a specific branch.  Within the session, groups can be opened as
    lazy `xarray.Dataset` objects backed by Dask arrays.
    """)
    return


@app.cell
def _(mo, store):
    import xarray as xr

    _groups = store.list_groups()

    if _groups:
        with store.readonly_session(branch="main") as _session:
            _root = xr.open_zarr(_session.store, consolidated=False)
        _info = f"Root dataset: `{dict(_root.sizes)}`"
    else:
        _info = "Store has no groups yet."

    mo.md(
        f"""
    ### Read-only session

    ```python
    with store.readonly_session(branch="main") as session:
        ds = xr.open_zarr(session.store, group="canopy_01", consolidated=False)
    ```

    {_info}
    """
    )
    return


@app.cell
def _(mo, store):
    _history = store.get_history(branch="main", limit=5)

    if _history:
        _rows = []
        for _h in _history:
            _msg = _h.get("commit_msg", "---")[:60]
            _ts = str(_h.get("written_at", "---"))[:19]
            _rows.append(f"| `{_ts}` | {_msg} |")
        _table = f"""
    | Timestamp | Message |
    |-----------|---------|
    {chr(10).join(_rows)}
    """
    else:
        _table = "No commits found."

    mo.md(
        f"""
    ## Commit history

    Every write operation creates a commit with a message and timestamp.
    The history is navigable like Git:

    ```python
    history = store.get_history(branch="main", limit=10)
    ```

    {_table}
    """
    )
    return


@app.cell
def _(mo, store):
    _branches = store.get_branch_names()

    mo.md(
        f"""
    ## Branching

    Branches enable experimental analyses without affecting the main data:

    ```python
    # Create a branch from main
    with store.writable_session(branch="experiment_v1") as session:
        # Write experimental data ...
        session.commit("experimental VOD with different grid")
    ```

    **Current branches**: {", ".join(f"`{b}`" for b in _branches)}

    This is analogous to Git branching: the `main` branch contains the
    canonical dataset, while feature branches hold exploratory results.
    Branches can be merged or deleted without affecting `main`.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Three-layer deduplication

    The store prevents duplicate data from entering the repository through
    three independent checks:

    1. **File hash match**: the SHA-256 hash of each RINEX/SBF file is
       recorded in the metadata ledger.  If the same file is ingested
       again, it is skipped, and the ledger records the skip.

    2. **Temporal overlap**: the start and end timestamps of each ingested
       file are compared against the existing data.  Files that overlap
       with previously ingested data are rejected.

    3. **Intra-batch overlap**: within a single batch of files being
       ingested, overlapping files are detected before any writes occur.

    ```python
    # Check which files are already in the store
    existing = store.batch_check_existing(
        group_name="canopy_01",
        file_hashes=["abc123...", "def456...", "ghi789..."],
    )
    # Returns: {"abc123..."} (set of hashes already present)
    ```

    This design ensures that re-running the pipeline on the same data
    is safe and idempotent.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Creating a new store

    The `create_gnss_store()` and `create_vod_store()` factory functions
    initialise new Icechunk repositories with the appropriate configuration:

    ```python
    from canvod.store import create_gnss_store, create_vod_store

    # For raw observation data
    gnss_store = create_gnss_store(Path("/data/my_site/observations.icechunk"))

    # For VOD products
    vod_store = create_vod_store(Path("/data/my_site/vod.icechunk"))
    ```

    ### Writing data

    ```python
    with store.writable_session(branch="main") as session:
        # First write to a group
        store.write_initial_group(ds, group_name="canopy_01")

        # Subsequent writes append along the epoch dimension
        store.append_to_group(ds_new, group_name="canopy_01", append_dim="epoch")
    ```

    The `append_to_group()` method handles all deduplication, epoch
    alignment, and SID padding automatically.
    """)
    return


@app.cell
def _(mo, store):
    _attrs = store.get_root_attrs()

    _rows = []
    for _k, _v in list(_attrs.items())[:10]:
        _val = str(_v)[:80]
        _rows.append(f"| `{_k}` | `{_val}` |")

    _table = (
        f"""
    | Key | Value |
    |-----|-------|
    {chr(10).join(_rows)}
    """
        if _rows
        else "No root attributes set."
    )

    mo.md(
        f"""
    ## Root attributes

    Store-level metadata is stored in root Zarr attributes.  The
    `source_format` attribute indicates whether the data originated
    from RINEX or SBF files.

    ```python
    attrs = store.get_root_attrs()
    store.set_root_attrs({{"source_format": "rinex3"}})
    ```

    {_table}
    """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    **Previous**: [10 · VOD Retrieval](./10_vod_retrieval.py)
    | **Next**: [12 · Store Metadata](./12_store_metadata.py)

    *canVODpy · Apache 2.0*
    """)
    return


if __name__ == "__main__":
    app.run()
