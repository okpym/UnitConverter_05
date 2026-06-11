import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

MANIFEST_PATH = Path(__file__).parent / "manifest.json"


def load_manifest():
    with MANIFEST_PATH.open(encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def manifest():
    return load_manifest()


def pytest_configure(config):
    config.addinivalue_line("markers", "p0: README P0 — 이번 Phase 우선")
    config.addinivalue_line("markers", "p1: 추가 요구 — 세션 3 범위 밖")
    config.addinivalue_line("markers", "conv: 변환 시나리오 (CONV-*)")
    config.addinivalue_line("markers", "val: 입력 검증 (VAL-*)")
    config.addinivalue_line("markers", "golden: Golden Master approval (VAL-*)")
