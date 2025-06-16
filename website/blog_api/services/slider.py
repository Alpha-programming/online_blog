import os
from ninja import UploadedFile
from blog_api.schemas.slider import SliderCreationSchema,SliderPaginatedSchema,SliderUpdateSchema
from django.shortcuts import get_object_or_404
from blog_app.models import Slider
from .auth import check_token
from website.settings import BASE_DIR
from ninja.errors import ValidationError

class SliderService:
    def get_sliders(self,token: str,limit: int=5, offset: int=0) -> SliderPaginatedSchema:
        check_token(token=token)
        slides = Slider.objects.all()
        return SliderPaginatedSchema(total=slides.count(),offset=offset,limit=limit,slides=slides[offset:limit])
    
    def create_slider(self,token:str, slider_data: SliderCreationSchema,image: UploadedFile) -> Slider:
        check_token(token=token)
        
        if Slider.objects.filter(title=slider_data.title).exists():
            raise ValidationError("A slide with this title already exists.")
        slider = Slider.objects.create(**slider_data.dict())
        if image is not None:
            preview_path = f'{BASE_DIR}/media/slider/{image.name}'
            preview_bytes = image.read()
            with open(preview_path, mode='wb') as _file:
                _file.write(preview_bytes)
            slider.image = f'slider/{image.name}'

        slider.save()

        return slider
    
    def update_slider(self,token:str, slider_id: int, data: SliderUpdateSchema,image: UploadedFile) -> Slider:
        check_token(token=token)
        slider = get_object_or_404(Slider,pk=slider_id)
        if Slider.objects.filter(title=data.title).exists():
            raise ValidationError("A slide with this title already exists.")
        for key, value in data.dict().items():
            if not value:
                current_value = getattr(slider, key)
                setattr(slider, key, current_value)
            else:
                setattr(slider, key, value)

        if image is not None:
            if slider.image:
                image_path = os.path.join(BASE_DIR, 'media', str(slider.image))
                if os.path.exists(image_path):
                    os.remove(image_path)

            preview_path = f'{BASE_DIR}/media/slider/{image.name}'
            preview_bytes = image.read()
            with open(preview_path, mode='wb') as _file:
                _file.write(preview_bytes)
            slider.image = f'slider/{image.name}'

        slider.save()
        return slider
    
    def get_slider_by_id(self,token:str, slider_id: int) -> Slider:
        check_token(token=token)
        slider = get_object_or_404(Slider, pk=slider_id)
        return slider
    
    def delete_slider(self,token:str, slider_id: int) -> dict:
        check_token(token=token)
        slider = get_object_or_404(Slider, pk=slider_id)
        slider.delete()
        if slider.image:
                image_path = os.path.join(BASE_DIR, 'media', str(slider.image))
                if os.path.exists(image_path):
                    os.remove(image_path)
        return{'is_deleted': True}

slider_service = SliderService()