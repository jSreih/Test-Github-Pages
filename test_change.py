"""Fetch a random cat fact from a public API and inject it into index.html.

Uses the free, no-API-key Cat Facts API: https://catfact.ninja/fact
Run with: python3 test_change.py
"""

import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API_URL = "https://catfact.ninja/fact"
HTML_FILE = Path(__file__).parent / "index.html"

START_MARKER = "<!-- API_CONTENT_START -->"
END_MARKER = "<!-- API_CONTENT_END -->"


def fetch_fact() -> str:
    """Return a random cat fact from the public API."""
    request = urllib.request.Request(
        API_URL, headers={"User-Agent": "Mozilla/5.0 (test_change.py)"}
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))
    return data["fact"]


def build_block(fact: str) -> str:
    """Build the HTML block to insert between the markers."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    return (
        f"{START_MARKER}\n"
        f'    <section id="api-content">\n'
        f"      <h2>Random Cat Fact</h2>\n"
        f"      <p>{fact}</p>\n"
        f"      <small>Fetched from catfact.ninja at {timestamp}</small>\n"
        f"    </section>\n"
        f"    {END_MARKER}"
    )


def update_html(block: str) -> None:
    """Replace the existing marker block, or insert one before </body>."""
    html = HTML_FILE.read_text(encoding="utf-8")

    if START_MARKER in html and END_MARKER in html:
        before = html.split(START_MARKER)[0]
        after = html.split(END_MARKER)[1]
        html = before + block + after
    else:
        html = html.replace("</body>", f"    {block}\n  </body>")

    HTML_FILE.write_text(html, encoding="utf-8")


def main() -> None:
    fact = fetch_fact()
    print(f"Fetched fact: {fact}")
    update_html(build_block(fact))
    print(f"Updated {HTML_FILE}")


if __name__ == "__main__":
    main()
