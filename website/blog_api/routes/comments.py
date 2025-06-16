from ninja import Router,Form
from blog_api.schemas.comments import CommentPaginatedSchema,CommentShortSchema,CreationCommentSchema,DeleteCommentSchema
from typing import Union
from blog_api.services.comments import comment_service


router = Router(
    tags=['Comments']
)

@router.get('/comments/', response=CommentPaginatedSchema)
def get_comments(request,token:str, limit: int = 5, offset: int = 0):
    return  comment_service.get_comments(limit=limit,offset=offset,token=token)

@router.get('/comments/{id}/', response=CommentShortSchema)
def get_comment_detail(request, token: str,id: int):
    return comment_service.get_comment_by_id(id=id,token=token)


@router.post('/comments/', response=CommentShortSchema)
def create_comment(request,token:str, comment_data: Form[CreationCommentSchema]):
    return comment_service.create_comment(comment_data=comment_data,token=token)

@router.put('/comments/{id}/update/',response=CommentShortSchema)
def update_comment(request, token:str, id:int, comment_data: Form[CreationCommentSchema]):
    return comment_service.update_comment(id=id, comment_data=comment_data,token=token)

@router.delete('/comments/{id}/', response=Union[DeleteCommentSchema,dict[str,str]])
def delete_comment(request,token:str, id:int):
    return comment_service.delete_comment(id=id,token=token)