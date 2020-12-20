from pydantic import BaseModel, Field, EmailStr, UUID4
from typing import List
from typing import Optional
from .blog import Paginate


class VerificationCode(BaseModel):
    """
    ... 表示必填项
    """
    mobile: str = Field(..., min_length=11, max_length=11, description='手机号')
    type: str = Field(..., description='验证码类型')

    class Config:
        schema_extra = {
            "example": {
                "mobile": "18666666666",
                "type": "register",
            }
        }


class UserCreate(BaseModel):
    username: str = Field(..., min_length=6, max_length=32, description='用户名')
    email: Optional[EmailStr] = Field(None, description='电子邮箱')
    mobile: Optional[str] = Field(None, description='手机号码')
    password: str = Field(..., min_length=8, max_length=32, description='密码')

    class Config:
        schema_extra = {
            "example": {
                "username": "testuser01",
                "email": "testuser01@example.com",
                "mobile": "18666666666",
                "password": "testuser01password",
            }
        }


class UserDetail(BaseModel):
    uuid: UUID4 = Field(description='uuid,用户的主键')
    username: str = Field(description='用户名称')
    email: Optional[EmailStr] = Field(description='电子邮箱')
    mobile: Optional[str] = Field(description='手机号')

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "testuser01",
                "email": "testuser01@example.com",
                "mobile": "13888888888",
                "password": "testuser01password"
            }
        }


class UserLogin(BaseModel):
    username: Optional[str] = Field(None, min_length=6, max_length=32, description='用户名')
    email: Optional[EmailStr] = Field(None, description='电子邮箱')
    mobile: Optional[str] = Field(None, description='手机号码')
    password: str = Field(..., min_length=8, max_length=32, description='密码')

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "testuser01",
                "email": "testuser01@example.com",
                "mobile": "18666666666",
                "password": "testuser001password"
            }
        }


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, description='电子邮箱')
    mobile: Optional[str] = Field(None, description='手机号码')
    password: str = Field(..., min_length=8, max_length=32, description='密码')

    class Config:
        schema_extra = {
            "example": {
                "email": "testuser001@example.com",
                "mobile": "18566666666",
                "password": "testuser001password",
            }
        }


class UserListData(BaseModel):
    uuid: str = Field(..., description='用户uuid')
    username: str = Field(..., description='用户名')
    email: str = Field(..., description='电子邮箱')
    mobile: str = Field(..., description='手机号码')
    created: str = Field(..., description="创建时间")


class UserList(BaseModel):
    paginate: Paginate = dict()
    user_list: List[UserListData] = []
