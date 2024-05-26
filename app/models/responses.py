from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class RecommendationResponse(BaseModel):
    artist_name: str
    song_name: str


class Page(BaseModel, Generic[T]):
    items: list[T]
    page_number: int
    page_size: int
    total_items: int

    def total_pages(self) -> int:
        return (self.total_items + self.page_size - 1) // self.page_size

    def has_next_page(self) -> bool:
        return self.page_number < self.total_pages()

    def has_previous_page(self) -> bool:
        return self.page_number > 1
