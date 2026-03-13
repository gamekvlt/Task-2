from __future__ import annotations

import uuid
from typing import Dict


def unique_user_payload() -> Dict[str, str]:
    u = uuid.uuid4().hex
    return {
        "email": f"autotest_{u}@example.com",
        "password": f"pass_{u}",
        "name": f"User_{u[:8]}",
    }
