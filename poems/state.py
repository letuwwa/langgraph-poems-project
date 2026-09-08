from typing import Literal, TypedDict


class PoemState(TypedDict):
    topic: str
    tone: str
    form: Literal["poem", "haiku"]
    target_lines: int
    draft: str
    validation_errors: list[str]
    revision_count: int
