"""Web fetch tool — download a URL and return readable text.

Used by the agent's fetch node. Turns a web page into plain text so the
firewall can scan it (malicious instructions often hide in fetched pages).

No extra dependency: HTML is stripped with the stdlib HTMLParser.
"""

from __future__ import annotations

import re
from html.parser import HTMLParser
from urllib.parse import urlparse

import requests

from app.core.config import settings
from app.domain.agents.state import FetchedItem

# Very small browser-ish user agent (some sites reject the default).
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; PromptInjectionFirewall/1.0; +demo)"
    ),
    "Accept": "text/html,text/plain,*/*",
}

_SKIP_TAGS = {"script", "style", "noscript", "template", "svg"}


class FetchError(RuntimeError):
    """Raised when a URL cannot be fetched or is not allowed."""


class _TextExtractor(HTMLParser):
    """Collect visible text, skipping script/style/etc."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._skip_depth = 0
        self._parts: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:  # noqa: ANN001
        if tag in _SKIP_TAGS:
            self._skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in _SKIP_TAGS and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._skip_depth == 0:
            text = data.strip()
            if text:
                self._parts.append(text)

    @property
    def text(self) -> str:
        return " ".join(self._parts)


def html_to_text(html: str) -> str:
    """Strip HTML tags and collapse whitespace."""
    parser = _TextExtractor()
    parser.feed(html)
    return re.sub(r"\s+", " ", parser.text).strip()


def _check_url(url: str) -> str:
    """Only allow http/https URLs."""
    url = (url or "").strip()
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise FetchError(f"Unsupported or invalid URL: {url!r}")
    return url


def download(url: str) -> str:
    """Download a URL and return its text (HTML converted to plain text)."""
    url = _check_url(url)
    try:
        response = requests.get(
            url,
            headers=_HEADERS,
            timeout=settings.FETCH_TIMEOUT_SECONDS,
            stream=True,
        )
        response.raise_for_status()

        # Read at most FETCH_MAX_BYTES to avoid huge downloads.
        raw = response.raw.read(settings.FETCH_MAX_BYTES, decode_content=True)
        encoding = response.encoding or "utf-8"
        body = raw.decode(encoding, errors="replace")

        content_type = response.headers.get("Content-Type", "")
        text = html_to_text(body) if "html" in content_type else body.strip()
        return text
    except requests.RequestException as exc:
        raise FetchError(f"Could not fetch {url}: {exc}") from exc


def fetch_web(url: str) -> FetchedItem:
    """Fetch a URL and return it as a FetchedItem for the firewall to scan."""
    text = download(url)
    return {"source": "url", "label": url, "content": text}
