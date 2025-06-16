from blog_app.models import UserProfile, User
from ninja.errors import HttpError
from typing import Union
from blog_api.schemas.auth import UserSchema,UserLoginSchema,UserTokenSchema
from ninja.errors import HttpError
from django.contrib.auth import authenticate

def check_token(token: str):
    try:
        user_profile = UserProfile.objects.get(api_token=token)
    except UserProfile.DoesNotExist:
        raise HttpError(401, "Invalid API Token")
    
class AuthService:
    def get_users(self,token: str, password: str) -> Union[list[UserSchema], str]:
        check_token(token=token)
        if password == 'alpha':
            users = User.objects.all()
            return users
        else:
            return "The password is incorrect. You don't have an access to this data"
    
    def get_token(self, data: UserLoginSchema) -> UserTokenSchema:
        data = data.dict()
        user = authenticate(username=data['username'], password=data['password'])

        if user is None:
            raise ValueError("Invalid credentials")

        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            raise ValueError("User token is not found")

        return UserTokenSchema(
            username=user.username,
            api_token=profile.api_token)

auth_service = AuthService()