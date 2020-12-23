import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from jwt.exceptions import PyJWTError
from starlette.status import HTTP_401_UNAUTHORIZED
from app.core.config import settings
from app.core.jwt import ALGORITHM
from app.models.user import User
from app.schemas.token import TokenPayload
from app.core.redis_app import redis_client

reusable_oauth2 = HTTPBearer()


def get_current_user(token: HTTPAuthorizationCredentials = Depends(reusable_oauth2)):
    try:
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="用户认证失败，请重新登陆"
        )
    user = User.get(uuid=token_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    token_key = f'Token_{user.uuid.hex}'
    if not redis_client.exists(token_key):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="用户认证已过期，请重新登陆"
        )
    redis_token = redis_client.get(token_key).decode('utf-8')
    if redis_token != token.credentials:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="您的账号在他处登陆，如非本人操作请注意账号安全"
        )
    return user


def get_current_active_user(current_user: User = Security(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_superuser(current_user: User = Security(get_current_user)):
    if not current_user.user_type == 0:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_current_active_superuser(current_user: User = Security(get_current_user)):
    if not current_user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
