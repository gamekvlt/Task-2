from __future__ import annotations

from typing import Callable, Dict, Generator, List, Optional

import pytest
import requests

from stellar_burgers_api.api_client import ApiClient
from stellar_burgers_api.config import BASE_URL
from stellar_burgers_api import endpoints as ep
from stellar_burgers_api.helpers import auth_header
from stellar_burgers_api.data import unique_user_payload


@pytest.fixture(scope="session")
def api() -> ApiClient:
    return ApiClient(BASE_URL)


@pytest.fixture
def user_cleanup(api: ApiClient) -> Generator[Callable[[Optional[str]], None], None, None]:
    tokens: List[str] = []

    def add(access_token: Optional[str]) -> None:
        if access_token:
            tokens.append(access_token)

    yield add

    for token in tokens:
        try:
            api.delete(ep.USER, headers=auth_header(token))
        except requests.exceptions.RequestException:
            pass


@pytest.fixture
def new_user_payload() -> Dict[str, str]:
    return unique_user_payload()
