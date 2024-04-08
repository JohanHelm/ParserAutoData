from typing import Optional

from pydantic import BaseModel, Field

DEFAULT_REQUEST_PARAMS: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
}
DEFAULT_TO = 20.0


class RequestManagerParams(BaseModel):
    headers: Optional[dict] = Field(default=DEFAULT_REQUEST_PARAMS)

    timeout: float = Field(default=DEFAULT_TO)
