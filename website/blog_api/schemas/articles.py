from datetime import datetime
from ninja import Field, Schema
from pydantic import validator
from blog_app.models import Article
from .categories import CategorySchema
from typing import Optional
from .auth import UserSchema
from .comments import ArticleCommentSchema

class ArticlelistSchema(Schema):
    id: int
    title: str
    slug: str
    short_description: str
    preview: Optional[str]
    views: int
    category: CategorySchema
    author: UserSchema
    created_at: datetime

class ArticlesPaginatedSchema(Schema):
    total: int
    offset: int
    limit: int 
    articles: list[ArticlelistSchema] 

class ArticleImageSchema(Schema):
    id: int
    photo: str

class ArticledetailSchema(Schema):
    id: int
    title: str
    slug: str
    short_description: str
    full_description: Optional[str]
    preview: Optional[str]
    views: int
    category: CategorySchema
    author: UserSchema
    comments: list[Optional[ArticleCommentSchema]]
    total_likes: int = 0
    total_dislikes: int = 0
    total_comments: int = 0
    created_at: datetime
    updated_at: datetime
    images: Optional[list[ArticleImageSchema]]

    @staticmethod
    def resolve_total_likes(obj: Article):
        return obj.likes.user.all().count()
    
    @staticmethod
    def resolve_total_dislikes(obj: Article):
        return obj.dislikes.user.all().count()
    
    @staticmethod
    def resolve_total_comments(obj: Article):
        return obj.comments.all().count()
      

class ArticleCreateSchema(Schema):
    title: str = Field(..., description="Enter the article title")
    short_description: str= Field(..., description="Write a short summary of the article")
    full_description: Optional[str] = Field(None, description="Write the full content of the article")
    category: int = Field(..., description='Write the category id')
    
class ArticlesDeleteSchema(Schema):
    is_deleted: bool

class ArticleUpdateSchema(Schema):
    title: Optional[str] = Field(None, description="Enter the article title")
    short_description: Optional[str] = Field(None, description="Write a short summary of the article")
    full_description: Optional[str] = Field(None, description="Write the full content of the article")
    category: Optional[int] = Field(None, description='Write the category id')
    
    @validator("category", pre=True)
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v