from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


EXPECTED_VERSION = "1.0.0"
EXPECTED_BASE_URL = "https://nohainc.github.io/nanomarkup.github.com"
EXPECTED_BASE_PATH = "/nanomarkup.github.com/"
FORBIDDEN_LEGACY_TEXT = (
    "one tab",
    "implicit list",
    "description This is a multi-line value",
    "nanomarkup.delphi",
)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.canonical: list[str] = []
        self.descriptions = 0
        self.titles = 0

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        values = dict(attrs)
        if tag == "a" and values.get("href"):
            self.links.append(values["href"] or "")
        if tag == "link" and values.get("rel") == "canonical":
            self.canonical.append(values.get("href") or "")
        if tag == "meta" and values.get("name") == "description":
            self.descriptions += 1
        if tag == "title":
            self.titles += 1


def check_page(path: Path, site: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(text)

    relative = path.relative_to(site)
    if parser.titles != 1:
        errors.append(f"{relative}: expected one title, found {parser.titles}")
    if parser.descriptions != 1:
        errors.append(
            f"{relative}: expected one meta description, found {parser.descriptions}"
        )
    if len(parser.canonical) != 1:
        errors.append(
            f"{relative}: expected one canonical URL, found {len(parser.canonical)}"
        )
    elif not parser.canonical[0].startswith(EXPECTED_BASE_URL):
        errors.append(f"{relative}: unexpected canonical URL {parser.canonical[0]!r}")

    for href in parser.links:
        parsed = urlparse(href)
        if parsed.scheme or href.startswith(("mailto:", "#")):
            continue
        target = (path.parent / parsed.path).resolve()
        if parsed.path.startswith(EXPECTED_BASE_PATH):
            target = site / parsed.path.removeprefix(EXPECTED_BASE_PATH)
        if parsed.path.endswith("/"):
            target /= "index.html"
        if not target.exists():
            errors.append(f"{relative}: broken local link {href!r}")

    lowered = text.lower()
    for legacy in FORBIDDEN_LEGACY_TEXT:
        if legacy.lower() in lowered:
            errors.append(f"{relative}: contains legacy wording {legacy!r}")
    return errors


def main() -> int:
    site = Path(sys.argv[1] if len(sys.argv) > 1 else "_site").resolve()
    required = (
        site / "index.html",
        site / "specification.html",
        site / "sitemap.xml",
        site / "robots.txt",
        site / "google34e3fed16101cfdb.html",
    )
    errors = [f"missing generated file: {path}" for path in required if not path.is_file()]

    for page in (site / "index.html", site / "404.html", site / "specification.html"):
        if page.is_file():
            errors.extend(check_page(page, site))

    index = site / "index.html"
    if index.is_file() and EXPECTED_VERSION not in index.read_text(encoding="utf-8"):
        errors.append(f"index.html does not identify Nano Markup {EXPECTED_VERSION}")

    sitemap = site / "sitemap.xml"
    if sitemap.is_file() and EXPECTED_BASE_URL not in sitemap.read_text(encoding="utf-8"):
        errors.append("sitemap.xml does not use the canonical site URL")

    if errors:
        print("Website validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Website validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
