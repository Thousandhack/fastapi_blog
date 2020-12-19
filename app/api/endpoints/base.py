from fastapi import APIRouter, Depends, Request
from app.schemas.base import UserDetail, UserCreate, UserLogin
from app.schemas.response import CustomResponse, success_response
from app.schemas.token import Token
from app.core.jwt import create_access_token
from app.api.utils.security import get_current_user
from app.models.user import User
from app.api.utils.response import fail_response
from app.core.redis_app import redis_client
from datetime import timedelta
from app.core.config import settings

router = APIRouter()


@router.post('/register', response_model=CustomResponse[UserDetail], name='用户注册')
def user_register(
        *,
        user_in: UserCreate,
):
    """
    注册用户
    :param user_in:
    :return:
    """
    user = User.select().where(User.username == user_in.username)
    if user:
        return fail_response('该用户名已注册')
    if not user_in.email and not user_in.mobile:
        return fail_response('电子邮箱和手机号码必须选择一个')
    if user_in.email:
        user = User.select().where(User.email == user_in.email)
        if user:
            return fail_response('该电子邮箱已注册')
    if user_in.mobile:
        user = User.select().where(User.mobile == user_in.mobile)
        if user:
            return fail_response('该手机号码已注册')
    user = User.create(**user_in.dict())
    return success_response(user)


@router.post('/login', response_model=CustomResponse[Token], name='用户登陆')
def user_login(*, user_in: UserLogin):
    """
    用户登陆
    :param user_in:
    :return:
    """
    if not user_in.username and not user_in.email and not user_in.mobile:
        return fail_response('必须使用用户名、电子邮箱和手机号码中的其中一种方式登陆')
    elif user_in.username:
        user = User.select().where(User.username == user_in.username)
    elif user_in.mobile:
        user = User.select().where(User.mobile == user_in.mobile)
    else:
        user = User.select().where(User.email == user_in.email)
    if user:
        login_user = user.first()
        if login_user.verify_password(user_in.password):
            token_expire_timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            user_id = login_user.uuid.hex
            redis_key = f'Token_{user_id}'
            access_token = create_access_token(data={'user_id': user_id}, expires_delta=token_expire_timedelta)
            redis_client.set(redis_key, access_token, ex=token_expire_timedelta)
            return success_response({'access_token': access_token, "token_type": "bearer"})
    return fail_response('用户名、电子邮箱、手机号码或密码错误')


@router.get('/profile', response_model=CustomResponse[UserDetail], name='个人资料')
def user_profile(request: Request, current_user: User = Depends(get_current_user)):
    return success_response(current_user)
