from ninja import File, Form, Router, UploadedFile
from blog_api.schemas.articles import ArticlelistSchema,ArticlesPaginatedSchema,ArticlesDeleteSchema, ArticledetailSchema, ArticleCreateSchema, ArticleUpdateSchema
from typing import Union,Optional
from blog_api.services.article import article_service

router = Router(
    tags=['Articles']
)

@router.get('/articles/',response=ArticlesPaginatedSchema)
def get_articles(request,token:str,  offset: int = 0, limit: int = 5):
    return article_service.get_paginated_articles(token=token,limit=limit, offset=offset)

@router.get('/articles/{id}',response=ArticlelistSchema)
def get_article_detail(request,token: str,id: int):
    return article_service.get_article_detail(token=token,id=id)

@router.post('/articles/', response=ArticledetailSchema)
def create_new_article(request, token: str, data: Form[ArticleCreateSchema],
preview: Optional[UploadedFile] = File(None), gallery: Optional[list[UploadedFile]] = File(None)):
    return article_service.create_new_article(
        token=token,
        data=data,
        preview=preview,
        gallery=gallery
    )
     

@router.patch('/articles/{id}/update/',response=ArticledetailSchema)
def update_article(request,token:str,  id: int, data: Form[ArticleUpdateSchema],
                   preview: Optional[UploadedFile] = File(None), gallery: Optional[list[UploadedFile]] = File(None)):
    article_service.update_article(
        id=id,
        token=token,
        data=data,
        preview=preview,
        gallery=gallery
    )
    return article_service.update_article(token=token,id=id,data=data,preview=preview,gallery=gallery)

@router.delete('/articles/{id}/',response=Union[ArticlesDeleteSchema, dict[str, str]])
def delete_article(request, token:str, id:int):
    return article_service.delete_article(token=token,id=id)
