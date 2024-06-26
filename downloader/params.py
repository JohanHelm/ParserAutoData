from typing import Optional
from pydantic import BaseModel, Field


class RequestManagerParams(BaseModel):
    timeout: float = Field(default=5)
    headers: Optional[dict] = Field(default={
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"
})

