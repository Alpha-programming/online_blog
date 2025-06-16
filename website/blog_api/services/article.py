import os
from typing import Optional
import uuid
from django.shortcuts import get_object_or_404
from slugify import slugify
from blog_api.schemas.articles import ArticleCreateSchema, ArticlesPaginatedSchema,ArticleUpdateSchema
from blog_app.models import Article, ArticleImage, Category, UserProfile
from ninja.files import UploadedFile 
from website.settings import BASE_DIR
from .auth import check_token

class ArticleService:
    def __save_photo(self, file: UploadedFile, folder_path: str):
        os.makedirs(os.path.dirname(folder_path), exist_ok=True)
        with open(folder_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

    def create_new_article(self,token: str,data: ArticleCreateSchema, preview: Optional[UploadedFile], gallery: Optional[list[UploadedFile]]):
        check_token(token=token)
        user_profile = UserProfile.objects.get(api_token=token)
        user = user_profile.user
        author = user

        _data = data.dict()
        title = _data.get('title')
        slug = slugify(title)
        if Article.objects.filter(slug=slug).exists():
            slug = f"{slug}-{uuid.uuid4().hex[:6]}"
            

        category = get_object_or_404(Category, pk=_data.pop('category'))
        
        article = Article.objects.create(**_data, category=category, author=author,slug=slug)


        if preview is not None:
            preview_path = f'{BASE_DIR}/media/articles/previews/{preview.name}'
            self.__save_photo(preview,preview_path)
            article.preview = f'articles/previews/{preview.name}'
            article.save()

        if gallery is not None:
            for item in gallery:
                item_path = f'{BASE_DIR}/media/articles/gallery/{item.name}'
                self.__save_photo(item, item_path)
                obj = ArticleImage.objects.create(
                    article=article,
                    photo = f'articles/gallery/{item.name}'
                )
        return article

    def get_paginated_articles(self,token: str, limit: int=5, offset: int=0) -> ArticlesPaginatedSchema:
        check_token(token=token)
        articles = Article.objects.all()
        total = articles.count()

        articles = articles[offset:limit]

        return ArticlesPaginatedSchema(
            total=total,
            offset=offset,
            limit=limit,
            articles=articles
        )
    
    def get_article_detail(self,token: str, id:int) -> Article:
        check_token(token=token)
        articles = get_object_or_404(Article, pk=id)
        return articles
    
    def delete_article(self,token: str, id:int) -> dict:
        check_token(token=token)
        article = get_object_or_404(Article,pk=id)
        article.delete()
        return{'is_deleted': True}
    
    def update_article(self, id:int,token:str, data: ArticleUpdateSchema,preview: Optional[UploadedFile],gallery: Optional[list[UploadedFile]]) -> Article:
        check_token(token=token)
        
        article = get_object_or_404(Article,pk=id)
        _data = data.dict()

        title = _data.get('title')
        if title:
            new_slug = slugify(title)
            if Article.objects.filter(slug=new_slug).exists():
                new_slug = f"{new_slug}-{uuid.uuid4().hex[:6]}"
            article.title = title
            article.slug = new_slug

        for key, value in _data.items():
            if not value: 
                current_value = getattr(article, key)
                setattr(article, key, current_value)
            else:
                if key == 'category':
                    category = get_object_or_404(Category, pk=value)
                    setattr(article, key, category)
                else:    
                    setattr(article, key, value)
        article.save()

        if preview is not None:
            if article.preview:
                image_path = os.path.join(BASE_DIR, 'media', str(article.preview))
                if os.path.exists(image_path):
                    os.remove(image_path)
            
            preview_dir = os.path.join(BASE_DIR, 'media', 'articles', 'previews')
            os.makedirs(preview_dir, exist_ok=True)

            ext = os.path.splitext(preview.name)[1]
            unique_name = f"{uuid.uuid4().hex}{ext}"
            preview_path = os.path.join(preview_dir, unique_name)
            self.__save_photo(preview, preview_path)

            article.preview = f'articles/previews/{unique_name}'
            article.save()

        if gallery is not None:
            for item in article.images.all():
                image_path = os.path.join(BASE_DIR, 'media', str(item.photo))
                if os.path.exists(image_path):
                    os.remove(image_path)
                item.delete()

            gallery_dir = os.path.join(BASE_DIR, 'media', 'articles', 'gallery')
            os.makedirs(gallery_dir, exist_ok=True)

            for item in gallery:
                ext = os.path.splitext(item.name)[1]
                unique_name = f"{uuid.uuid4().hex}{ext}"
                item_path = os.path.join(gallery_dir, unique_name)
                self.__save_photo(item, item_path)
                ArticleImage.objects.create(
                    article=article,
                    photo=f'articles/gallery/{unique_name}'
                )
        
        return article
    
article_service = ArticleService()