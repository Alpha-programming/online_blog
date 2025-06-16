import uuid
from ninja.errors import ValidationError
from blog_api.schemas.categories import CategorySchema,CategoryCreationSchema,CategoryPaginatedSchema
from blog_app.models import Category
from django.shortcuts import get_object_or_404
from slugify import slugify
from .auth import check_token

class CategoriesService:
    def get_categories(self, token: str,limit: int=5, offset: int=0) -> CategoryPaginatedSchema:
        check_token(token=token)
        categories = Category.objects.all()
        return CategoryPaginatedSchema(total=categories.count(),limit=limit, offset=offset, categories=categories[offset:limit])
    
    def create_category(self, token:str, category_data: CategoryCreationSchema) -> Category:
        check_token(token=token)
        category = Category.objects.create(
            name=category_data.name,
            slug=slugify(category_data.name)
        )
        return category

    def get_categories_by_id(self,token: str, category_id: int) -> Category:
        check_token(token=token)
        category = get_object_or_404(Category, pk=category_id)
        return category
    
    def update_category(self,token:str, category_id: int, data: CategoryCreationSchema) -> Category:
        check_token(token=token)
        category = get_object_or_404(Category, pk=category_id)
        
        if Category.objects.filter(name=data.name).exclude(id=category_id).exists():
            raise ValidationError("A category with this name already exists.")


        for key, value in data.dict().items():
            setattr(category, key, value)
            name = value
            new_slug = slugify(name)
            if Category.objects.filter(slug=new_slug).exists():
                new_slug = f"{new_slug}-{uuid.uuid4().hex[:6]}"
            category.name = name
            category.slug = new_slug

        category.save()
        return category
    
    def delete_category(self,token:str,  category_id: int) -> dict:
        check_token(token=token)
        category = get_object_or_404(Category, pk=category_id)
        category.delete()
        return{'is_deleted': True}

categories_service = CategoriesService()