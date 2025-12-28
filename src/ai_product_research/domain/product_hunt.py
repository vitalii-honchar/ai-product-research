from pydantic import BaseModel
from typing import Optional


class ProductHuntPost(BaseModel):
    id: str
    name: str
    tagline: str
    description: str
    votesCount: int
    url: str
    website: str
    thumbnail_url: Optional[str] = None
    topics: list[str] = []