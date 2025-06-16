from django.http import HttpRequest
from ninja import Form, Router 
from blog_api.schemas.categories import CategorySchema,CategoryCreationSchema, CategoryDelete,CategoryPaginatedSchema
from typing import Union
from blog_api.services.categories import categories_service


router = Router(
    tags=['Categories']
)

@router.get('/categories/',response=CategoryPaginatedSchema)
def get_categories(request: HttpRequest, token: str,limit: int = 5, offset: int = 0):
    return categories_service.get_categories(token=token,limit=limit,offset=offset)

@router.post('/categories/',response=CategorySchema)
def create_category(request, token:str, category_data: Form[CategoryCreationSchema]):
    return categories_service.create_category(token=token, category_data=category_data)

@router.get('/categories/{category_id}', response=CategorySchema)
def get_categories_by_id(request,token: str, category_id: int):
    return categories_service.get_categories_by_id(token=token,category_id=category_id)

@router.patch('/categories/{category_id}', response=CategorySchema)
def update_category(request,token:str, category_id: int, data: Form[CategoryCreationSchema]):
    return categories_service.update_category(token=token,category_id=category_id,data=data)

@router.delete('/category/{category_id}/', response=Union[CategoryDelete, dict[str, str]])
def delete_category(request,token:str,  category_id: int):
    return categories_service.delete_category(token=token, category_id=category_id)
