"""Golden Master approval helpers."""

import os
from pathlib import Path

GOLDEN_DIR = Path(__file__).parent / "golden"


def assert_matches_golden(actual: str, relative: str) -> None:
    """Compare actual vs tests/golden/{relative} (e.g. VAL-01.approved.txt)."""
    path = GOLDEN_DIR / relative
    normalized = actual.rstrip("\n") + "\n"

    if os.environ.get("UPDATE_GOLDEN") == "1":
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(normalized, encoding="utf-8")
        return

    if not path.is_file():
        raise AssertionError(f"Golden missing: {path} — run UPDATE_GOLDEN=1 pytest …")

    expected = path.read_text(encoding="utf-8")
    if normalized != expected:
        raise AssertionError(
            f"Golden mismatch: {path}\n--- expected\n{expected}--- actual\n{normalized}"
        )
