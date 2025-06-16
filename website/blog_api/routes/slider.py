from ninja import Form, Router,File,UploadedFile
from blog_api.schemas.slider import SliderSchema,SliderCreationSchema,SliderDeleteSchema,SliderUpdateSchema,SliderPaginatedSchema
from typing import Optional, Union
from blog_api.services.slider import slider_service

router = Router(
    tags=['Slider']
)

@router.get('/slider/',response=SliderPaginatedSchema)
def get_slider_item(request,token:str,limit: int = 5, offset: int = 0):
    return slider_service.get_sliders(token=token,limit=limit,offset=offset)

@router.post('/slider/',response=SliderSchema)
def create_slider(request,token:str, slider_data: Form[SliderCreationSchema],image: UploadedFile=File()):
    return slider_service.create_slider(token=token, slider_data=slider_data,image=image)

@router.patch('/slider/{slider_id}/update/',response=SliderSchema)
def update_slider(request,token:str, slider_id: int, data: Form[SliderUpdateSchema],image: Optional[UploadedFile]=File(None)):
    return slider_service.update_slider(token=token, slider_id=slider_id, data=data,image=image)

@router.get('/slider/{slider_id}', response=SliderSchema)
def get_slider_by_id(request,token:str, slider_id: int):
    return slider_service.get_slider_by_id(token=token,slider_id=slider_id)

@router.delete('/slider/{slider_id}/', response=Union[SliderDeleteSchema, dict[str, str]])
def delete_slider(request,token:str, slider_id: int):
    return slider_service.delete_slider(token=token, slider_id=slider_id)