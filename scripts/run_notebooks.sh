#!/usr/bin/env bash
# Runs every notebook as a script (`uv run --script`), as CI does. A notebook
# that raises an error fails the run; the others still run.
#
#   scripts/run_notebooks.sh              # all notebooks
#   scripts/run_notebooks.sh 05 13        # only these
#
# Logs go to $LOG_DIR (default: logs/). Notebook 13 writes to a copy of a
# demo store and needs settings for it: they are made here, from the store,
# with `canvodpy config init --from-store`.
set -uo pipefail

cd "$(dirname "$0")/.."
LOG_DIR="${LOG_DIR:-logs}"
mkdir -p "$LOG_DIR"

if [ "$#" -gt 0 ]; then
    notebooks=()
    for n in "$@"; do notebooks+=("$n"_*.py); done
else
    notebooks=([0-9][0-9]_*.py)
fi

# A Python script with the dependencies of notebook 13, so it runs the same
# canvodpy version as the notebooks.
notebook_13_python() {
    local script="$LOG_DIR/settings_13.py"
    awk '{ print } /^# \/\/\/$/ && NR > 1 { exit }' 13_workflow_store_operations.py > "$script"
    cat >> "$script"
    uv run --script "$script" "$@"
}

# Settings for notebook 13, made from the reference store of the demo data
# with `canvodpy config init --from-store`. The values the store doesn't
# know get the test persona and folders under $LOG_DIR.
notebook_13_settings() {
    local config_dir="$LOG_DIR/settings_13"
    rm -rf "$config_dir"
    notebook_13_python "$config_dir" > "$LOG_DIR/13_settings.log" 2>&1 <<'PY' || return 1
import subprocess
import sys
from pathlib import Path

import yaml

import canvodpy

config_dir = Path(sys.argv[1]).resolve()
store = canvodpy.demo_data("stores") / "stores" / "rosalia_rinex_v3_04" / "gnss"
subprocess.run(
    [sys.executable, "-m", "canvodpy.cli.app", "config", "init", "--no-interactive",
     "--config-dir", str(config_dir), "--from-store", str(store)],
    check=True,
)
path = config_dir / "canvod-settings.yaml"
header = "".join(line for line in path.read_text().splitlines(True) if line.startswith("#"))
settings = yaml.safe_load(path.read_text())
persona = {
    "author": "J. R. R. Tolkien",
    "email": "j.r.r.tolkien@the.inklings.org",
    "institution": "Fangorn",
}
data = config_dir / "data"


def fill(node, key=None):
    if isinstance(node, dict):
        return {k: fill(v, k) for k, v in node.items()}
    if node == "TODO":
        return persona.get(key, str(data / key))
    return node


path.write_text(header + yaml.safe_dump(fill(settings), sort_keys=False))
print(f"settings: {path}")
PY
    echo "$config_dir"
}

failed=()
for nb in "${notebooks[@]}"; do
    name="${nb%.py}"
    start=$SECONDS
    if [[ "$nb" == 13_* ]]; then
        if ! config_dir="$(notebook_13_settings)"; then
            echo "FAIL $nb (settings, see $LOG_DIR/13_settings.log)"
            failed+=("$nb")
            continue
        fi
        CANVOD_CONFIG_DIR="$config_dir" uv run --script "$nb" > "$LOG_DIR/$name.log" 2>&1
    else
        uv run --script "$nb" > "$LOG_DIR/$name.log" 2>&1
    fi
    rc=$?
    if [ "$rc" -eq 0 ]; then
        echo "ok   $nb ($((SECONDS - start)) s)"
    else
        echo "FAIL $nb ($((SECONDS - start)) s, see $LOG_DIR/$name.log)"
        failed+=("$nb")
    fi
done

if [ "${#failed[@]}" -gt 0 ]; then
    echo "${#failed[@]} notebook(s) failed: ${failed[*]}"
    exit 1
fi
echo "All ${#notebooks[@]} notebooks ran."
