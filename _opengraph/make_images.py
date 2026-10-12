"""Make the link-preview image (OpenGraph) of every notebook.

marimo shows `__marimo__/assets/<notebook>/opengraph.png` when a notebook
link is shared and on the notebook's card in a gallery. This script opens
template.html in headless Chrome once per notebook, with the number and
title from the notebook's `# title = "..."` header line, and saves a
1200 x 630 px screenshot there.

    uv run python _opengraph/make_images.py [--chrome PATH]

Run it again after a title changes or after background.png changes.
"""

import argparse
import http.server
import re
import subprocess
import threading
from functools import partial
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
MAC_CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TITLE = re.compile(r'^# title = "(\d\d) · (.+)"$', re.M)


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass  # Chrome's requests are not worth a line each


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--chrome", default=MAC_CHROME, help="Chrome or Chromium executable")
    args = parser.parse_args()

    handler = partial(QuietHandler, directory=str(HERE))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    port = server.server_address[1]
    try:
        for notebook in sorted(REPO.glob("[0-9][0-9]_*.py")):
            match = TITLE.search(notebook.read_text())
            if match is None:
                raise SystemExit(f"{notebook.name}: no '# title = \"NN · ...\"' header line")
            out = REPO / "__marimo__" / "assets" / notebook.stem / "opengraph.png"
            out.parent.mkdir(parents=True, exist_ok=True)
            url = f"http://127.0.0.1:{port}/template.html#{quote(match[1] + '|' + match[2])}"
            subprocess.run(
                [args.chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                 "--virtual-time-budget=5000", "--window-size=1200,630",
                 f"--screenshot={out}", url],
                check=True, capture_output=True,
            )
            print(f"{out.relative_to(REPO)}")
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()
