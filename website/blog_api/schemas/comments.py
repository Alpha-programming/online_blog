from datetime import datetime
from typing import Optional
from ninja import Schema 
from .auth import UserSchema

class ArticleCommentSchema(Schema):
    id: int
    author: UserSchema
    text: str
    created_at: datetime

class CommentShortSchema(Schema):
    id: int
    text: str
    article_id: int
    author_id: int
    created_at: datetime

class CommentPaginatedSchema(Schema):
    total: int
    offset: int
    limit: int
    comments: list[CommentShortSchema]

class DeleteCommentSchema(Schema):
    is_deleted: bool

class CreationCommentSchema(Schema):
    article_id: int
    text: str

class CreationCommentSchema(Schema):
    article_id: Optional[int] = None
    text: Optional[str] = None
