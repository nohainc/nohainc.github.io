from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


EXPECTED_VERSION = "1.0.0"
EXPECTED_BASE_URL = "https://nohainc.github.io"
EXPECTED_BASE_PATH = "/"
EXPECTED_IMPLEMENTATIONS_DESCRIPTION = (
    "Compare Nano Markup 1.0.0 for Python, Go, JavaScript, TypeScript, Dart, Java, and .NET."
)
EXPECTED_IMPLEMENTATION_LINKS = {
    "https://pypi.org/project/nanomarkup/",
    "https://github.com/nohainc/nanomarkup.python",
    "https://github.com/nohainc/nanomarkup.python/releases/tag/v1.0.0",
    "https://pkg.go.dev/github.com/nohainc/nanomarkup.go",
    "https://github.com/nohainc/nanomarkup.go",
    "https://github.com/nohainc/nanomarkup.go/releases/tag/v1.0.0",
    "https://www.npmjs.com/package/nanomarkup",
    "https://github.com/nohainc/nanomarkup.javascript",
    "https://github.com/nohainc/nanomarkup.javascript/releases/tag/v1.0.0",
    "https://pub.dev/packages/nanomarkup",
    "https://github.com/nohainc/nanomarkup.dart",
    "https://github.com/nohainc/nanomarkup.dart/releases/tag/v1.0.0",
    "https://github.com/nohainc/nanomarkup.java",
    "https://github.com/nohainc/nanomarkup.java/releases/tag/v1.0.0",
    "https://github.com/nohainc/nanomarkup.dotnet",
    "https://github.com/nohainc/nanomarkup.dotnet/releases/tag/v1.0.0",
    "https://github.com/nohainc/nanomarkup.c",
    "https://github.com/nohainc/nanomarkup.c/releases/tag/v1.0.0",
}
FORBIDDEN_LEGACY_TEXT = (
    "nanomarkup.github.com",
    "one tab",
    "implicit list",
    "description This is a multi-line value",
    "nanomarkup.delphi",
)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.navigation_links: list[str] = []
        self.stylesheets: list[str] = []
        self.canonical: list[str] = []
        self.descriptions: list[str] = []
        self.title_parts: list[str] = []
        self.title_count = 0
        self.in_navigation = False
        self.in_title = False

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        values = dict(attrs)
        if tag == "nav":
            self.in_navigation = True
        if tag == "a" and values.get("href"):
            self.links.append(values["href"] or "")
            if self.in_navigation:
                self.navigation_links.append(values["href"] or "")
        if tag == "link" and values.get("rel") == "canonical":
            self.canonical.append(values.get("href") or "")
        if tag == "link" and values.get("rel") == "stylesheet":
            href = values.get("href") or ""
            self.stylesheets.append(href)
            self.links.append(href)
        if tag == "meta" and values.get("name") == "description":
            self.descriptions.append(values.get("content") or "")
        if tag == "title":
            self.title_count += 1
            self.in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "nav":
            self.in_navigation = False
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)


def check_page(path: Path, site: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(text)

    relative = path.relative_to(site)
    if parser.title_count != 1:
        errors.append(
            f"{relative}: expected one title, found {parser.title_count}"
        )
    if len(parser.descriptions) != 1:
        errors.append(
            f"{relative}: expected one meta description, found {len(parser.descriptions)}"
        )
    if len(parser.canonical) != 1:
        errors.append(
            f"{relative}: expected one canonical URL, found {len(parser.canonical)}"
        )
    elif not parser.canonical[0].startswith(EXPECTED_BASE_URL):
        errors.append(f"{relative}: unexpected canonical URL {parser.canonical[0]!r}")

    if relative.name != "specification.html" and parser.stylesheets != [
        "/assets/css/style.css"
    ]:
        errors.append(
            f"{relative}: expected root stylesheet URL, found {parser.stylesheets!r}"
        )

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
        site / "implementations.html",
        site / "sitemap.xml",
        site / "robots.txt",
        site / "google34e3fed16101cfdb.html",
    )
    errors = [f"missing generated file: {path}" for path in required if not path.is_file()]

    for page in (
        site / "index.html",
        site / "404.html",
        site / "specification.html",
        site / "implementations.html",
    ):
        if page.is_file():
            errors.extend(check_page(page, site))

    index = site / "index.html"
    if index.is_file():
        index_text = index.read_text(encoding="utf-8")
        if EXPECTED_VERSION not in index_text:
            errors.append(f"index.html does not identify Nano Markup {EXPECTED_VERSION}")
        parser = PageParser()
        parser.feed(index_text)
        expected_canonical = f"{EXPECTED_BASE_URL}/"
        if parser.canonical != [expected_canonical]:
            errors.append(
                "index.html: canonical URL must be "
                f"{expected_canonical!r}, not the duplicate /index.html URL"
            )

    implementations = site / "implementations.html"
    if implementations.is_file():
        parser = PageParser()
        parser.feed(implementations.read_text(encoding="utf-8"))
        expected_canonical = f"{EXPECTED_BASE_URL}/implementations.html"
        if parser.canonical != [expected_canonical]:
            errors.append(
                "implementations.html: canonical URL must be "
                f"{expected_canonical!r}"
            )
        title = "".join(parser.title_parts).strip()
        if title != "Implementations — Nano Markup":
            errors.append(f"implementations.html: unexpected title {title!r}")
        if parser.descriptions != [EXPECTED_IMPLEMENTATIONS_DESCRIPTION]:
            errors.append("implementations.html: unexpected meta description")
        for navigation_link in (
            f"{EXPECTED_BASE_PATH}specification.html",
            f"{EXPECTED_BASE_PATH}implementations.html",
        ):
            if navigation_link not in parser.navigation_links:
                errors.append(
                    "implementations.html: missing primary navigation link "
                    f"{navigation_link!r}"
                )
        missing_links = EXPECTED_IMPLEMENTATION_LINKS.difference(parser.links)
        for link in sorted(missing_links):
            errors.append(f"implementations.html: missing implementation link {link!r}")
        text = implementations.read_text(encoding="utf-8")
        for required_text in (
            "Python 3.11+",
            "Go 1.24+",
            "Node.js 22+",
            "Dart 3.12+",
            "Java 17+",
            ".NET 8+",
            "C11 / C++17+",
            "npm install nanomarkup",
            "dart pub add nanomarkup",
            "Stable 1.0.0",
            "112-case shared conformance corpus",
        ):
            if required_text not in text:
                errors.append(
                    f"implementations.html: missing required text {required_text!r}"
                )

    sitemap = site / "sitemap.xml"
    if sitemap.is_file():
        sitemap_text = sitemap.read_text(encoding="utf-8")
        if EXPECTED_BASE_URL not in sitemap_text:
            errors.append("sitemap.xml does not use the canonical site URL")
        if f"{EXPECTED_BASE_URL}/implementations.html" not in sitemap_text:
            errors.append("sitemap.xml does not include implementations.html")

    if errors:
        print("Website validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Website validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
