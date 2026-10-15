<!-- Python & Package Manager -->
[![Python](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![marimo](https://marimo.io/shield.svg)](https://canvodpy.eu/notebooks/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)

<!-- Identity -->
[![canVODpy](https://img.shields.io/badge/canVODpy-submodule-2d6a4f)](https://github.com/nfb2021/canvodpy)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![CLIMERS @ TU Wien](https://img.shields.io/badge/CLIMERS-TU_Wien-006699)](https://www.tuwien.at/en/mg/geo/climers)
[![VODnet](https://img.shields.io/badge/-VODnet-2d6a4f?labelColor=555555&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAAAXNSR0IArs4c6QAAAHhlWElmTU0AKgAAAAgABAEaAAUAAAABAAAAPgEbAAUAAAABAAAARgEoAAMAAAABAAIAAIdpAAQAAAABAAAATgAAAAAAAABIAAAAAQAAAEgAAAABAAOgAQADAAAAAQABAACgAgAEAAAAAQAAAA6gAwAEAAAAAQAAAA4AAAAAjn8NzQAAAAlwSFlzAAALEwAACxMBAJqcGAAAAflJREFUKBWtUEtoE1EUPe+9SczHiam/aixtqi1E7aai4kK0CAVBDFZwrQs3xp2KIriYtiKuav3QRVxYKIjFVihWrCBIaaWioKidQBsxi3SwYmMmkxidYWaemYEEKUgRPHDhXu4575x3gf+NKfVD3UQ2u/Zv7wrLF8mPfV2ZH1ZCNIM7xUCAHHjyfN6wQ8mZo3vvE4Av57tzOjfd/WZpivfJSW5wkzvomnzFe2SFTyyU+iFJtCpk1eaRfOIw84TuRsN7kEkVMDzyEjPvUtga2YiDTRFM5+m+F8XYHMZuzDqaWlQf8yVMpmJ0/DUu9g6hVNQAy8au3W04NHAV85oFRulZS+LDkIjtWmcyHT6vQHYoXwrouTWKkv4LLOAHE4N4K6dxZ2AISl4DpawVDVrYcXSFZtTPGSV8IatjUVErJ+Cwbdstx3Vw8CG+pmQIHg+HUVlWo7aSp/qz9Kn3W5p5S/x4DJ8/lfGt4kAow7bmBpQ9fuQ3RUFtM4Uz61Qk/vijbpLbgtc61n05zjQ1hCvXHmB9fT3OnT8NOWfi+uxP0IJxE4S4jrXzxrffm1xlb75Aud/cEFmD9vYW6KaNUoUmCpS3BblUPNk45sR0UBM6Qzx2qd9LVnfqujGS+64puaX8olEuj4uMHHnc2dTrcFZGtCOMxv11KxP/kfEbTTzNcyb5ar0AAAAASUVORK5CYII=&logoColor=white)](https://www.gfz.de/en/section/remote-sensing-and-geoinformatics/projects/vodnet)

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/nfb2021/canvodpy/main/docs/assets/logo/canvodpy_logo_dark_mode.svg">
    <img alt="canVODpy logo" src="https://raw.githubusercontent.com/nfb2021/canvodpy/main/docs/assets/logo/canvodpy_logo_bright_mode.svg" width="312">
  </picture>
</p>

# canVODpy Demo Notebooks

Interactive [marimo](https://marimo.io) notebooks for the [canVODpy](https://github.com/nfb2021/canvodpy) GNSS-Transmissometry (GNSS-T) VOD retrieval ecosystem. The notebooks cover the full pipeline, from raw GNSS file reading to vegetation optical depth retrieval, versioned storage, and visualisation.

---

## Look at the notebooks in your browser (no installation)

Each notebook in the [table below](#notebooks) has a molab link that opens
it in your browser in [marimo molab](https://molab.marimo.io/). The copies
on [canvodpy.eu/notebooks](https://canvodpy.eu/notebooks/) also show their
results: they were run on the test data when the site was built.

To run a notebook yourself, see the next section. Notebooks that read real
GNSS data download the test data on first use and cache it locally.

---

## Run locally: standalone

### Prerequisites

Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/):

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Way 1: in a clone

```bash
git clone https://github.com/nfb2021/canvodpy-demo.git
cd canvodpy-demo
```

Each notebook declares its own dependencies via a PEP 723 header, so `uv`
installs them automatically on first run. No `uv sync` or manual dependency
management is needed.

```bash
# Interactive editing
cd canvodpy-demo
uvx marimo edit --sandbox 10_vod_retrieval.py

# Read-only app
uvx marimo run --sandbox 10_vod_retrieval.py
```

`uvx` and `--sandbox` together mean this never touches (or requires) any
project-level virtual environment: the notebook's own PEP 723 header
declares everything it needs, installed into a throwaway venv.

### Way 2: as a single file

You do not need the repository at all. Give marimo the raw URL of one
notebook on GitHub, and `--sandbox` builds a throwaway environment from the
notebook's own PEP 723 header:

```bash
uvx marimo edit --sandbox https://raw.githubusercontent.com/nfb2021/canvodpy-demo/main/10_vod_retrieval.py
```

Every notebook is self-contained: it declares its `canvod*` dependencies and
their pinned revision, and it fetches its data with `canvodpy.demo_data()`.

### Way 3: on molab

Open a notebook from the [table](#notebooks) in molab, or browse the rendered
copies at [canvodpy.eu/notebooks](https://canvodpy.eu/notebooks/).

---

marimo notebooks also run in the [VS Code marimo extension](https://marimo.io/docs/installation) and
in containers; the sandbox image they use is documented in the
[marimo sandbox-image docs](https://marimohub.docs.marimo.io/sandbox-image).

---

## Run locally: inside the canvodpy monorepo

If you are working inside the canvodpy monorepo, the notebooks are available as the `demo/` submodule and share the monorepo's virtual environment and test data automatically.

```bash
git clone --recurse-submodules https://github.com/nfb2021/canvodpy.git
cd canvodpy
uv sync

# Interactive editing
uv run marimo edit demo/10_vod_retrieval.py

# Read-only app
uv run marimo run demo/10_vod_retrieval.py
```

---

## Notebooks

| # | Notebook | Topic | Open |
|---|---|---|---|
| 01 | `01_cli_pipeline.py` | `canvodpy run`: the production CLI | [![molab](https://marimo.io/shield.svg)](https://molab.marimo.io/github/nfb2021/canvodpy-demo/blob/main/01_cli_pipeline.py?mode=edit) |
| 02 | `02_configuration.py` | Pydantic configuration models | [![molab](https://marimo.io/shield.svg)](https://molab.marimo.io/github/nfb2021/canvodpy-demo/blob/main/02_configuration.py?mode=edit) |
| 03 | `03_convenience_speedrun.py` | Full pipeline in five cells | [![molab](https://marimo.io/shield.svg)](https://molab.marimo.io/github/nfb2021/canvodpy-demo/blob/main/03_convenience_speedrun.py?mode=edit) |
| 04 | `04_naming_convention.py` | GNSS filename convention parsing and validation | [![molab](https://marimo.io/shield.svg)](https://molab.marimo.io/github/nfb2021/canvodpy-demo/blob/main/04_naming_convention.py?mode=edit) |
| 05 | `05_rinex_reading.py` | RINEX v3.04 file reading → `xarray.Dataset` | [![molab](https://marimo.io/shield.svg)](https://molab.marimo.io/github/nfb2021/canvodpy-demo/blob/main/05_rinex_reading.py?mode=edit) |
| 06 | `06_sbf_reading.py` | SBF binary file reading | [![molab](https://marimo.io/shield.svg)](https://molab.marimo.io/github/nfb2021/canvodpy-demo/blob/main/06_sbf_reading.py?mode=edit) |
| 07 | `07_satellite_catalog.py` | IGS SatelliteCatalog: PRN metadata and lookup | [![molab](https://marimo.io/shield.svg)](https://molab.marimo.io/github/nfb2021/canvodpy-demo/blob/main/07_satellite_catalog.py?mode=edit) |
| 08 | `08_ephemeris_coordinates.py` | SP3/CLK augmentation and ECEF → spherical transforms | [![molab](https://marimo.io/shield.svg)](https://molab.marimo.io/github/nfb2021/canvodpy-demo/blob/main/08_ephemeris_coordinates.py?mode=edit) |
| 09 | `09_hemispheric_grids.py` | Equal-area, equal-angle, geodesic, Fibonacci grids | [![molab](https://marimo.io/shield.svg)](https://molab.marimo.io/github/nfb2021/canvodpy-demo/blob/main/09_hemispheric_grids.py?mode=edit) |
| 10 | `10_vod_retrieval.py` | Tau-Omega VOD retrieval algorithm | [![molab](https://marimo.io/shield.svg)](https://molab.marimo.io/github/nfb2021/canvodpy-demo/blob/main/10_vod_retrieval.py?mode=edit) |
| 11 | `11_icechunk_store.py` | Versioned Icechunk/Zarr storage | [![molab](https://marimo.io/shield.svg)](https://molab.marimo.io/github/nfb2021/canvodpy-demo/blob/main/11_icechunk_store.py?mode=edit) |
| 12 | `12_store_metadata.py` | DataCite/ACDD/STAC provenance metadata | [![molab](https://marimo.io/shield.svg)](https://molab.marimo.io/github/nfb2021/canvodpy-demo/blob/main/12_store_metadata.py?mode=edit) |
| 13 | `13_workflow_store_operations.py` | Store read/write/branch operations | [![molab](https://marimo.io/shield.svg)](https://molab.marimo.io/github/nfb2021/canvodpy-demo/blob/main/13_workflow_store_operations.py?mode=edit) |
| 14 | `14_visualization.py` | 2D/3D hemispheric visualisation | [![molab](https://marimo.io/shield.svg)](https://molab.marimo.io/github/nfb2021/canvodpy-demo/blob/main/14_visualization.py?mode=edit) |
| 15 | `15_grid_exploration.py` | Interactive hemispheric grid explorer | [![molab](https://marimo.io/shield.svg)](https://molab.marimo.io/github/nfb2021/canvodpy-demo/blob/main/15_grid_exploration.py?mode=edit) |
| 16 | `16_grid_3d_gallery.py` | 3D gallery comparing all hemispheric grid types | [![molab](https://marimo.io/shield.svg)](https://molab.marimo.io/github/nfb2021/canvodpy-demo/blob/main/16_grid_3d_gallery.py?mode=edit) |
| 17 | `17_api_overview.py` | API overview: CLI and Site pipeline | [![molab](https://marimo.io/shield.svg)](https://molab.marimo.io/github/nfb2021/canvodpy-demo/blob/main/17_api_overview.py?mode=edit) |
| 18 | `18_site_pipeline.py` | `Site().pipeline().process_range()` | [![molab](https://marimo.io/shield.svg)](https://molab.marimo.io/github/nfb2021/canvodpy-demo/blob/main/18_site_pipeline.py?mode=edit) |
| 19 | `19_workflow_single_day.py` | End-to-end single-day processing | [![molab](https://marimo.io/shield.svg)](https://molab.marimo.io/github/nfb2021/canvodpy-demo/blob/main/19_workflow_single_day.py?mode=edit) |
| 20 | `20_workflow_batch_processing.py` | Batch processing with Dask | [![molab](https://marimo.io/shield.svg)](https://molab.marimo.io/github/nfb2021/canvodpy-demo/blob/main/20_workflow_batch_processing.py?mode=edit) |
| 21 | `21_plugins.py` | Your own VOD calculator: register it, compare it, make it a plugin | [![molab](https://marimo.io/shield.svg)](https://molab.marimo.io/github/nfb2021/canvodpy-demo/blob/main/21_plugins.py?mode=edit) |

---

## Test data

Notebooks that read real GNSS data get it from `canvodpy.demo_data()`, which
downloads it on first use into your platform's cache folder (Linux
`~/.cache/canvodpy/demo`, macOS `~/Library/Caches/canvodpy/demo`, Windows
`%LOCALAPPDATA%\canvodpy\demo`). Subsequent runs reuse the cached copy.

The download is roughly 1 GB and contains, for the Rosalia, Austria site on
DOY 2025-001:

- **RINEX v3.04** observations (~350 MB): a full day per receiver, for both the
  reference and canopy receivers.
- **SBF** binary observations (~190 MB): the first two hours of the day.
- **Auxiliary data** (~350 MB): CODE final SP3 orbit and CLK clock files for
  the day and its neighboring days, plus the pre-computed auxiliary Zarr
  store.

`demo_data()` needs no manual download and no cloned test-data repository.

---

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](https://github.com/nfb2021/canvodpy/blob/main/CONTRIBUTING.md) in the canvodpy repository for guidelines.

---

## License

[Apache License 2.0](LICENSE)

---

## Affiliation

Founded by **Nicolas François Bader**

[Climate and Environmental Remote Sensing Research Unit (CLIMERS)](https://www.tuwien.at/en/mg/geo/climers)
Department of Geodesy and Geoinformation, TU Wien

Email: support@canvodpy.eu
