import argparse
import hashlib
import os
import re
import sys
from collections import deque
from typing import Optional, Set
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup, Tag
from markdownify import markdownify as html_to_md


DEFAULT_START_URL = "https://mewe-ir.com/en/home/"  # Set a default starting URL here for local runs.


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Crawl a public site and export cleaned pages to Markdown."
    )
    parser.add_argument(
        "start_url",
        nargs="?",
        help="Starting URL for the crawl (optional, falls back to DEFAULT_START_URL)",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=50,
        help="Maximum number of pages to crawl (default: 50)",
    )
    parser.add_argument(
        "--output-dir",
        default="markdown_output",
        help="Directory to write Markdown files (default: markdown_output)",
    )
    return parser.parse_args()


def is_internal(url: str, domain: str) -> bool:
    parsed = urlparse(url)
    return parsed.netloc == "" or parsed.netloc == domain


def normalize_url(raw_url: str, base_url: str, domain: str) -> Optional[str]:
    """Resolve relative links, drop fragments/queries, enforce domain."""
    resolved = urljoin(base_url, raw_url)
    parsed = urlparse(resolved)
    if parsed.scheme not in ("http", "https"):
        return None
    if parsed.netloc != domain:
        return None
    cleaned = parsed._replace(fragment="", query="", params="")
    normalized = cleaned.geturl().rstrip("/")
    return normalized or None


def fetch_html(session: requests.Session, url: str) -> Optional[str]:
    try:
        resp = session.get(url, timeout=10)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding
        return resp.text
    except requests.RequestException:
        return None


def strip_noise(soup: BeautifulSoup) -> None:
    """Remove common non-content elements (headers, nav, footers, etc.)."""
    for tag_name in ["script", "style", "noscript", "header", "footer", "nav", "aside"]:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    # Drop elements that look like footers/headers/navigation based on class/id/role.
    noisy_tokens = ("footer", "foot", "header", "nav", "breadcrumb")
    for tag in soup.find_all(True):
        if not isinstance(tag, Tag):
            continue

        attrs = tag.attrs or {}
        classes_raw = attrs.get("class") or []
        classes = classes_raw if isinstance(classes_raw, list) else [classes_raw]

        haystack_parts = [
            " ".join(classes),
            str(attrs.get("id") or ""),
            str(attrs.get("role") or ""),
            str(attrs.get("aria-label") or ""),
        ]
        haystack = " ".join(haystack_parts).lower().strip()
        if haystack and any(token in haystack for token in noisy_tokens):
            tag.decompose()


def extract_content_html(soup: BeautifulSoup) -> str:
    """
    Keep only headings (h1-h3), paragraphs, and lists to preserve hierarchy,
    skipping nested duplicates to avoid repeated list items.
    """
    body = soup.body or soup
    allowed = {"h1", "h2", "h3", "p", "ul", "ol", "li"}
    new_soup = BeautifulSoup("<div></div>", "html.parser")
    container = new_soup.div

    for element in body.find_all(allowed, recursive=True):
        # Skip if an ancestor is also allowed to prevent duplication
        if any(parent.name in allowed for parent in element.parents if parent is not body):
            continue
        container.append(element)

    return str(container)


def slugify_url(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.strip("/") or "index"
    parts = [parsed.netloc] + [p for p in path.split("/") if p]
    slug = "-".join(parts)
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", slug).strip("-").lower() or "page"
    if parsed.query:
        digest = hashlib.md5(parsed.query.encode("utf-8")).hexdigest()[:8]
        slug = f"{slug}-{digest}"
    return slug[:200]


def ensure_unique_filename(slug: str, used: Set[str]) -> str:
    if slug not in used:
        used.add(slug)
        return slug
    counter = 2
    while True:
        candidate = f"{slug}-{counter}"
        if candidate not in used:
            used.add(candidate)
            return candidate
        counter += 1


def html_to_markdown(content_html: str) -> str:
    return html_to_md(
        content_html,
        heading_style="ATX",
        convert=["h1", "h2", "h3", "p", "ul", "ol", "li", "a"],
    ).strip()


def build_markdown_page(title: str, url: str, body_md: str) -> str:
    lines = [
        f"# {title or 'Untitled'}",
        f"Source: {url}",
        "",
        body_md,
    ]
    return "\n".join(lines).strip() + "\n"


def crawl(start_url: str, max_pages: int, output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)

    domain = urlparse(start_url).netloc
    visited: Set[str] = set()
    to_visit = deque([start_url.rstrip("/")])
    filenames_used: Set[str] = set()
    combined_pages: list[str] = []

    session = requests.Session()
    session.headers.update({"User-Agent": "MarkdownCrawler/1.0"})

    while to_visit and len(visited) < max_pages:
        url = to_visit.popleft()
        if url in visited:
            continue
        visited.add(url)

        html = fetch_html(session, url)
        if not html:
            continue

        soup = BeautifulSoup(html, "html.parser")

        # Collect links before stripping noise so nav/footers don't hide child pages.
        page_links = [a for a in soup.find_all("a", href=True) if isinstance(a, Tag)]

        strip_noise(soup)
        content_html = extract_content_html(soup)
        if not content_html.strip():
            continue

        page_title = (soup.title.string or "").strip() if soup.title else ""
        markdown_body = html_to_markdown(content_html)
        page_md = build_markdown_page(page_title, url, markdown_body)

        slug = ensure_unique_filename(slugify_url(url), filenames_used)
        filepath = os.path.join(output_dir, f"{slug}.md")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(page_md)

        combined_pages.append(page_md)

        for link in page_links:
            if not isinstance(link, Tag):
                continue

            attrs = link.attrs or {}
            href = attrs.get("href") or ""
            if not href:
                continue
            if not is_internal(href, domain):
                continue
            normalized = normalize_url(href, url, domain)
            if normalized and normalized not in visited:
                to_visit.append(normalized)

    combined_path = os.path.join(output_dir, "combined.md")
    with open(combined_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(combined_pages))


def main() -> None:
    args = parse_args()
    start_url = args.start_url or DEFAULT_START_URL
    if not start_url:
        sys.exit("Please set DEFAULT_START_URL or pass a start_url argument.")
    crawl(start_url, args.max_pages, args.output_dir)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Interrupted by user.")

