from ninja import Schema  # type: ignore
from typing import Optional

class FaqSchema(Schema):
    id: int
    question: str
    answer: str

class FaqPaginatedSchema(Schema):
    total: int
    offset: int
    limit: int
    faqs: list[FaqSchema]

class FaqCreationSchema(Schema):
    question: str
    answer: str

class FaqUpdateSchema(Schema):
    question: Optional[str] = None
    answer: Optional[str] = None

class FaqDeleteSchema(Schema):
    is_deleted: bool
    