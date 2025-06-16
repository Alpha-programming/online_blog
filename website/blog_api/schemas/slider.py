from ninja import Schema  # type: ignore
from typing import Optional

class SliderSchema(Schema):
    title: str
    description: str
    image: str

class SliderPaginatedSchema(Schema):
    total: int
    offset: int
    limit: int
    slides: list[SliderSchema]

class SliderCreationSchema(Schema):
    title: str
    description: str

class SliderUpdateSchema(Schema):
    title: Optional[str] = None
    description : Optional[str] = None
    

class SliderDeleteSchema(Schema):
    is_deleted: bool