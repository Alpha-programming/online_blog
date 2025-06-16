from typing import Union
from ninja import Form, Router 
from blog_api.schemas.auth import UserSchema, UserLoginSchema,UserTokenSchema, UserRegistrationSchema
from blog_api.services.auth import auth_service
from django.contrib.auth import authenticate, login, logout
from ninja.errors import ValidationError
from django.contrib.auth.models import User

router = Router(
    tags=['Auth']
)

@router.get('/auth/users/{password}', response=Union[list[UserSchema], str])
def get_users(request,token: str, password: str):
   return auth_service.get_user(token=token, password=password)


@router.post('/auth/login',response=UserSchema)
def login_user(request, login_data: UserLoginSchema):
    user = authenticate(
        username=login_data.username,
        password=login_data.password
    )
    if user is None:
        raise ValidationError('User not found')
    login(request, user)
    return user

@router.post('/auth/register/', response=UserSchema)
def register_user(request, register_data: UserRegistrationSchema):
    if User.objects.filter(username=register_data.username).exists():
        raise ValidationError('User with this username already registered')

    data = register_data.dict()
    password1 = data.pop('password1')
    password2 = data.pop('password2')
    if password1 != password2:
        raise ValidationError('passwords are not similiar')
    
    user = User.objects.create(**data)
    user.set_password(password1)
    user.save()
    return user

@router.post('/auth/logout/')
def user_logout(request):
    logout(request)
    return {'is_authenticated': request.user.is_authenticated}

@router.post('/auth/token/', response=UserTokenSchema)
def user_token(request, data: Form[UserLoginSchema]):
    return auth_service.get_token(data)
    