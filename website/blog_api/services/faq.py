from blog_app.models import FAQ
from blog_api.schemas.faq import FaqSchema,FaqCreationSchema,FaqPaginatedSchema
from django.shortcuts import get_object_or_404
from .auth import check_token


class FaqService:
    def get_faqs(self,token:str,limit: int=5, offset: int=0) -> FaqPaginatedSchema:
        check_token(token=token)
        items = FAQ.objects.all()
        return FaqPaginatedSchema(total=items.count(),offset=offset,limit=limit,faqs=items[offset:limit])
    
    def create_faq(self,token:str, faq_data: FaqCreationSchema) -> FAQ:
        check_token(token=token)
        faq = FAQ.objects.create(**faq_data.dict())
        return faq
    
    def update_faq_item(self,token:str, faq_id: int, data: FaqCreationSchema) -> FAQ:
        check_token(token=token)
        faq = get_object_or_404(FAQ,pk=faq_id)

        for key, value in data.dict().items():
            if not value:
                current_value = getattr(faq, key)
                
                setattr(faq, key, current_value)
            else:
                setattr(faq, key, value)

        faq.save()
        return faq
    
    def get_faq_by_id(self, token:str,faq_id: int) -> FAQ:
        check_token(token=token)
        faq = get_object_or_404(FAQ, pk=faq_id)
        return faq
    
    def delete_faq(self,token:str, faq_id: int) -> dict:
        check_token(token=token)
        faq = get_object_or_404(FAQ,pk=faq_id)
        faq.delete()
        return{'is_deleted': True}
    
faq_service = FaqService()
