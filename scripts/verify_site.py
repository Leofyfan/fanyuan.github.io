#!/usr/bin/env python3
"""Verify the generated Fan Yuan academic site using only the standard library."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


BASE_PATH = "/fanyuan.github.io"
SUPPRESSED_TEXT_ELEMENTS = {"script", "style", "template"}

REQUIRED_ROUTES = {"/", "/publications/", "/404.html"}

PAPER_TITLES = (
    "GSM8K-V: Can Vision Language Models Solve Grade School Math Word Problems "
    "in Visual Contexts",
    "VidBot: Intelligent Video Learning Tool for Content Mining and Playback "
    "Traffic Statistics",
)

REQUIRED_TEXT = (
    "Fan Yuan",
    "Zhejiang University",
    "EMNLP 2026 Main Conference",
    "Best Demo Paper",
)

REQUIRED_IMAGE_PATHS = (
    "/images/profile.jpg",
    "/images/publications/gsm8k-v.png",
    "/images/publications/vidbot.png",
)

REQUIRED_LINKS = (
    "https://github.com/leofyfan",
    "mailto:yuanfan7777777@gmail.com",
    "https://arxiv.org/abs/2509.25160",
    "https://github.com/ZJU-REAL/GSM8K-V",
    "https://zju-real.github.io/GSM8K-V/",
    "https://huggingface.co/datasets/ZJU-REAL/GSM8K-V",
    "https://ieeexplore.ieee.org/document/10645449",
    "https://doi.org/10.1109/ICMEW63481.2024.10645449",
)

DEMO_STRINGS = (
    "Your Name",
    "Red Brick University",
    "Paper Title Number",
    "GitHub Journal of Bugs",
    "Teaching",
    "Portfolio",
    "Blog Posts",
    "Guide",
)

# CJK radicals, kana, bopomofo, Hangul, ideographs, and compatibility forms.
CJK_PATTERN = re.compile(
    r"[\u1100-\u11ff\u2e80-\u2fff\u3040-\u30ff\u3100-\u318f"
    r"\u31a0-\u31ff\u3200-\u33ff\u3400-\u4dbf\u4e00-\u9fff"
    r"\ua960-\ua97f\uac00-\ud7af\ud7b0-\ud7ff\uf900-\ufaff"
    r"\ufe30-\ufe4f\uff66-\uff9d\uffa1-\uffdc"
    r"\U0001aff0-\U0001afff\U0001b000-\U0001b16f"
    r"\U00020000-\U0002fa1f\U00030000-\U000323af]"
)


@dataclass(frozen=True)
class Reference:
    tag: str
    attribute: str
    value: str
    line: int


@dataclass(frozen=True)
class Image:
    source: str
    alt: str | None
    line: int


class SiteHTMLParser(HTMLParser):
    """Collect visible text, local-file references, images, and card counts."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.text_parts: list[str] = []
        self.references: list[Reference] = []
        self.images: list[Image] = []
        self.publication_cards = 0
        self.suppressed_element_depth = 0

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self._inspect_tag(tag, attrs)
        if tag.lower() in SUPPRESSED_TEXT_ELEMENTS:
            self.suppressed_element_depth += 1

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self._inspect_tag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        if (
            tag.lower() in SUPPRESSED_TEXT_ELEMENTS
            and self.suppressed_element_depth > 0
        ):
            self.suppressed_element_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.suppressed_element_depth == 0:
            self.text_parts.append(data)

    @property
    def visible_text(self) -> str:
        return re.sub(r"\s+", " ", "".join(self.text_parts)).strip()

    def _inspect_tag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        line, _ = self.getpos()
        attributes = {name.lower(): value for name, value in attrs}

        classes = (attributes.get("class") or "").split()
        if "publication-card" in classes:
            self.publication_cards += 1

        for attribute in ("href", "src"):
            value = attributes.get(attribute)
            if value is not None:
                self.references.append(
                    Reference(tag.lower(), attribute, value, line)
                )

        if tag.lower() == "img":
            self.images.append(
                Image(attributes.get("src") or "", attributes.get("alt"), line)
            )


def generated_route(site_root: Path, html_file: Path) -> str:
    relative = html_file.relative_to(site_root).as_posix()
    if relative == "index.html":
        return "/"
    if relative.endswith("/index.html"):
        return f"/{relative[:-len('index.html')]}"
    return f"/{relative}"


def read_utf8(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        errors.append(f"{path}: is not valid UTF-8 ({exc})")
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        errors.append(f"{path}: could not be read ({exc})")
        return ""


def strip_base_path(url_path: str) -> str:
    if url_path == BASE_PATH:
        return "/"
    if url_path.startswith(f"{BASE_PATH}/"):
        return url_path[len(BASE_PATH) :]
    return url_path


def local_target(
    site_root: Path, document: Path, value: str
) -> tuple[Path, str] | None:
    """Return a local reference's target and site-root-relative display path."""
    parsed = urlsplit(value.strip())
    if parsed.scheme or parsed.netloc:
        return None

    decoded_path = unquote(parsed.path)
    if not decoded_path:
        target = document
    elif decoded_path.startswith("/"):
        site_path = strip_base_path(decoded_path)
        target = site_root / site_path.lstrip("/")
    else:
        target = document.parent / decoded_path

    target = target.resolve()
    root = site_root.resolve()
    try:
        relative = target.relative_to(root)
    except ValueError:
        return target, f"outside generated site: {target}"

    normalized = f"/{relative.as_posix()}" if relative.as_posix() != "." else "/"
    if decoded_path.endswith("/"):
        normalized = f"{normalized.rstrip('/')}/"
    return target, normalized


def target_exists(target: Path, normalized_path: str) -> bool:
    if normalized_path.endswith("/"):
        return (target / "index.html").is_file()
    if target.is_file():
        return True
    if not Path(normalized_path).suffix:
        return (target / "index.html").is_file()
    return False


def verify_site(site_root: Path) -> list[str]:
    errors: list[str] = []
    if not site_root.is_dir():
        return [f"generated site directory does not exist: {site_root}"]

    html_files = sorted(site_root.rglob("*.html"))
    xml_files = sorted(site_root.rglob("*.xml"))
    route_files = {generated_route(site_root, path): path for path in html_files}

    for route in sorted(REQUIRED_ROUTES - route_files.keys()):
        errors.append(f"missing required HTML route: {route}")
    for route in sorted(route_files.keys() - REQUIRED_ROUTES):
        errors.append(f"unexpected generated HTML route: {route}")

    parsed_pages: dict[Path, SiteHTMLParser] = {}
    source_text: dict[Path, str] = {}
    for path in html_files:
        text = read_utf8(path, errors)
        source_text[path] = text
        parser = SiteHTMLParser()
        parser.feed(text)
        parser.close()
        parsed_pages[path] = parser

    for route in ("/", "/publications/"):
        path = route_files.get(route)
        if path is None:
            continue
        parser = parsed_pages[path]
        if parser.publication_cards != 2:
            errors.append(
                f"{route}: expected exactly 2 publication cards, "
                f"found {parser.publication_cards}"
            )
        for title in PAPER_TITLES:
            count = parser.visible_text.count(title)
            if count != 1:
                errors.append(
                    f"{route}: expected exactly one copy of {title!r}, found {count}"
                )

    visible_site_text = "\n".join(
        parser.visible_text for parser in parsed_pages.values()
    )
    for required in REQUIRED_TEXT:
        if required not in visible_site_text:
            errors.append(f"missing required visible text: {required!r}")

    all_anchor_hrefs: set[str] = set()
    all_image_src_targets: set[str] = set()
    for document, parser in parsed_pages.items():
        for image in parser.images:
            if image.alt is None or not image.alt.strip():
                errors.append(
                    f"{document.relative_to(site_root)}:{image.line}: "
                    f"image {image.source!r} has empty alternative text"
                )

        for reference in parser.references:
            value = reference.value.strip()
            if reference.tag == "a" and reference.attribute == "href":
                all_anchor_hrefs.add(value)

            location = f"{document.relative_to(site_root)}:{reference.line}"
            try:
                target_info = local_target(site_root, document, value)
            except ValueError as exc:
                errors.append(
                    f"{location}: invalid {reference.attribute} URL "
                    f"{value!r} ({exc})"
                )
                continue
            if target_info is None:
                continue
            target, normalized = target_info
            if reference.tag == "img" and reference.attribute == "src":
                all_image_src_targets.add(normalized)

            if normalized.startswith("outside generated site:"):
                errors.append(
                    f"{location}: local {reference.attribute} {value!r} "
                    f"resolves {normalized}"
                )
            elif not target_exists(target, normalized):
                errors.append(
                    f"{location}: local {reference.attribute} {value!r} "
                    f"does not resolve under {site_root}"
                )

    for image_path in REQUIRED_IMAGE_PATHS:
        if image_path not in all_image_src_targets:
            errors.append(f"missing required image source: {image_path!r}")

    for link in REQUIRED_LINKS:
        if link not in all_anchor_hrefs:
            errors.append(f"missing required exact link: {link!r}")

    generated_text = dict(source_text)
    for path in xml_files:
        generated_text[path] = read_utf8(path, errors)

    for path, text in generated_text.items():
        relative = path.relative_to(site_root)
        for demo_string in DEMO_STRINGS:
            if demo_string in text:
                errors.append(f"{relative}: contains demo string {demo_string!r}")
        cjk_match = CJK_PATTERN.search(text)
        if cjk_match is None:
            cjk_match = CJK_PATTERN.search(unescape(text))
        if cjk_match:
            errors.append(
                f"{relative}: contains CJK character {cjk_match.group()!r}"
            )

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "site_root",
        nargs="?",
        default="_site",
        type=Path,
        help="generated Jekyll site directory (default: _site)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = verify_site(args.site_root)
    if errors:
        print("Site verification failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Site verification passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
