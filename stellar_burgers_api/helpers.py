from typing import Dict
def auth_header(access_token: str) -> Dict[str, str]:
    return {"Authorization": access_token}
