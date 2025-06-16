from typing import Optional
from ninja import Schema 
from pydantic import EmailStr

class UserSchema(Schema):
    id: int
    username: str
    first_name: Optional[str]

class UserLoginSchema(Schema):
    username: str
    password: str

class UserRegistrationSchema(Schema):
    first_name: str
    username: str
    email: EmailStr
    password1: str
    password2: str

class UserTokenSchema(Schema):
    username: str
    api_token : str