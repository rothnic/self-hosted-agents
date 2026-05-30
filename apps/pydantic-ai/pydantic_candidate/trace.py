from __future__ import annotations

import hashlib
import json
from typing import Any


def stable_id(prefix: str, value: Any, length: int = 16) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"{prefix}-{hashlib.sha256(encoded).hexdigest()[:length]}"
