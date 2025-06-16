from typing import Optional, Union
from ninja import Router,Form
from blog_api.schemas.faq import FaqSchema,FaqCreationSchema,FaqDeleteSchema,FaqPaginatedSchema,FaqUpdateSchema
from blog_api.services.faq import faq_service


router = Router(
    tags=['FAQ']
)

@router.get('/faqs/',response=FaqPaginatedSchema)
def get_faqs(request,token:str,limit: int = 5, offset: int = 0):
    return faq_service.get_faqs(token=token,limit=limit,offset=offset)

@router.post('/faqs/',response=FaqSchema)
def create_faq(request,token:str, faq_data: Form[FaqCreationSchema]):
    return faq_service.create_faq(token=token,faq_data=faq_data)

@router.patch('/faqs/{faq_id}/update/',response=FaqSchema)
def update_faq_item(request,token:str, faq_id: int, data: Form[FaqUpdateSchema]):
    return faq_service.update_faq_item(token=token,faq_id=faq_id,data=data)

@router.get('/faqs/{faq_id}', response=FaqSchema)
def get_faq_by_id(request, token:str,faq_id: int):
    return faq_service.get_faq_by_id(token=token,faq_id=faq_id)

@router.delete('/faqs/{faq_id}/', response=Union[FaqDeleteSchema, dict[str, str]])
def delete_faq(request,token:str, faq_id: int):
    return faq_service.delete_faq(token=token,faq_id=faq_id)