from pydantic import BaseModel
from pydantic import Field


class Token(BaseModel):
    access_token: str = Field(description='访问token')
    token_type: str = Field(description='访问token的类型,默认bearer')

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiY2U1MThlMDAxODY2NDAwN2I1OGZhNWJmZWY2NTIyZTQiLCJleHAiOjE1ODgyMjcwNzgsInN1YiI6ImFjY2VzcyJ9.EpiNeMcXQMbLZiAd15plkdKAP1Y06GrSIdKzM5tqKUM",
                "token_type": "bearer"
            }
        }


class TokenPayload(BaseModel):
    user_id: str = None
