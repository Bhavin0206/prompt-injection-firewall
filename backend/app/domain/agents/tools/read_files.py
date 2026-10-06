"""Folder / email tool — read text and email files from a folder.

Used by the agent's fetch node to simulate a "source" without a real inbox:
point it at a folder of .txt / .eml files and it returns one FetchedItem
per file, ready for the firewall to scan.
"""

from __future__ import annotations

import email
from email import policy
from pathlib import Path

from app.domain.agents.state import FetchedItem
from app.domain.agents.tools.fetch_web import html_to_text

# File types we know how to read.
SUPPORTED_SUFFIXES = {
    ".txt", ".md", ".log", ".csv", ".json",
    ".html", ".htm", ".eml",
    # source code (the PDF lists "Source code" as an input source)
    ".py", ".js", ".ts", ".java", ".sh", ".sql",
    ".yml", ".yaml", ".xml",
}

# Safety caps so one huge folder cannot stall a run.
MAX_FILES = 50
MAX_FILE_BYTES = 1_000_000  # 1 MB per file


class ReadError(RuntimeError):
    """Raised when a folder/file cannot be read."""


def _email_body(message: email.message.Message) -> str:
    """Extract the readable body from an email message."""
    if message.is_multipart():
        # prefer a plain-text part
        for part in message.walk():
            if part.get_content_type() == "text/plain" and not part.get_filename():
                return part.get_content()
        # otherwise the HTML part
        for part in message.walk():
            if part.get_content_type() == "text/html" and not part.get_filename():
                return html_to_text(part.get_content())
        return ""

    content = message.get_content()
    if message.get_content_type() == "text/html":
        return html_to_text(content)
    return content


def read_file(path: str | Path) -> FetchedItem:
    """Read one file and return it as a FetchedItem."""
    file_path = Path(path)
    if not file_path.is_file():
        raise ReadError(f"Not a file: {file_path}")

    if file_path.stat().st_size > MAX_FILE_BYTES:
        raise ReadError(f"File too large: {file_path.name}")

    if file_path.suffix.lower() == ".eml":
        with file_path.open("rb") as handle:
            message = email.message_from_binary_file(handle, policy=policy.default)
        subject = message.get("Subject", "")
        body = _email_body(message)
        content = f"Subject: {subject}\n\n{body}".strip()
    else:
        text = file_path.read_text(encoding="utf-8", errors="replace")
        content = html_to_text(text) if file_path.suffix.lower() in {".html", ".htm"} else text

    return {"source": "folder", "label": file_path.name, "content": content}


def read_folder(folder: str | Path) -> list[FetchedItem]:
    """Read every supported file in a folder (sorted, capped at MAX_FILES)."""
    folder_path = Path(folder)
    if not folder_path.is_dir():
        raise ReadError(f"Not a folder: {folder_path}")

    files = sorted(
        p
        for p in folder_path.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED_SUFFIXES
    )[:MAX_FILES]

    items: list[FetchedItem] = []
    for file_path in files:
        try:
            items.append(read_file(file_path))
        except ReadError:
            # skip unreadable files; the caller can still scan the rest
            continue
    return items
