from django.shortcuts import get_object_or_404
from ninja import Router 
from blog_app.models import Comment,Article
from blog_app.models import UserProfile
from ninja.errors import HttpError
from typing import Union
from django.contrib.auth.models import User
from .auth import check_token
from blog_api.schemas import comments

class CommentService:
    def get_comments(self,token:str,limit: int=5, offset: int=0) -> comments.CommentPaginatedSchema:
        check_token(token=token)
        objects = Comment.objects.all()
        total_comments = objects.count()
        return comments.CommentPaginatedSchema(total=total_comments,
        offset=offset,
        limit=limit,
        comments=objects[offset:limit]                                    
        )
    
    def get_comment_by_id(self,token:str,  id: int) -> Comment:
        check_token(token=token)
        comment = get_object_or_404(Comment, pk=id)
        return comment
    
    def create_comment(self,token:str, comment_data: comments.CreationCommentSchema) -> Comment:
        check_token(token=token)
        _data = comment_data.dict()
        article = get_object_or_404(Article,pk=_data.pop('article_id'))
        user_profile = UserProfile.objects.get(api_token=token)
        user = user_profile.user
        author = user
        comment = Comment.objects.create(**_data,author=author,article=article)
        return comment
    
    def delete_comment(self, token:str, id: int) -> dict:
        check_token(token=token)
        comment = get_object_or_404(Comment,pk=id)
        comment.delete()
        return{'is_deleted': True}

    def update_comment(self, token:str,id: int, comment_data: comments.CreationCommentSchema) -> Comment:
        check_token(token=token)
        comment = get_object_or_404(Comment, id=id)
        for key, value in comment_data.dict().items():
            setattr(comment, key, value)
        comment.save()
        return comment

comment_service = CommentService()