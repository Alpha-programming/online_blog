from ninja import Schema  # type: ignore
from datetime import datetime

class CategorySchema(Schema):
    id: int
    name: str
    slug: str
    created_at: datetime

class CategoryPaginatedSchema(Schema):
    total: int
    offset: int
    limit: int
    categories: list[CategorySchema]
    

class CategoryCreationSchema(Schema):
    name: str

class CategoryDelete(Schema):
    is_deleted: bool
    