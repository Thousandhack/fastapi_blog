from pydantic import BaseModel, Field, EmailStr, UUID4
from typing import Optional


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
                "mobile": "13888888888",
                "password": "testuser01password",
            }
        }


class UserDetail(BaseModel):
    uuid: UUID4
    username: str
    email: Optional[EmailStr]
    mobile: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "uuid": "cf895bb5-c1ef-485f-acac-b8b13378ff41",
                "username": "testuser01",
                "email": "testuser01@example.com",
                "mobile": "13888888888",
            }
        }


class UserLogin(BaseModel):
    username: Optional[str] = Field(None, min_length=6, max_length=32, description='用户名')
    email: Optional[EmailStr] = Field(None, description='电子邮箱')
    mobile: Optional[str] = Field(None, description='手机号码')
    password: str = Field(..., min_length=8, max_length=32, description='密码')






