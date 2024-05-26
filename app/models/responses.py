from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class RecommendationResponse(BaseModel):
    artist_name: str
    song_name: str


class Page(Generic[T]):
    def __init__(self, items: list[T], page_number: int, page_size: int, total_items: int) -> None:
        self.items = items
        self.page_number = page_number
        self.page_size = page_size
        self.total_items = total_items

    def total_pages(self) -> int:
        return (self.total_items + self.page_size - 1) // self.page_size

    def has_next_page(self) -> bool:
        return self.page_number < self.total_pages()

    def has_previous_page(self) -> bool:
        return self.page_number > 1
