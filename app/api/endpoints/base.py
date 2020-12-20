from fastapi import APIRouter, Depends, Request
from fastapi import Query
from fastapi.logger import logger
from app.schemas.base import UserDetail, UserCreate, UserLogin, UserUpdate, UserList
from app.schemas.base import VerificationCode
from app.schemas.response import CustomResponse
from app.schemas.token import Token
from app.core.jwt import create_access_token
from app.api.utils.security import get_current_user
from app.api.utils.security import get_current_superuser
from app.models.user import User
from app.api.utils.response import fail_response, success_response
from app.core.redis_app import redis_client
from datetime import timedelta
from app.core.config import settings
import random
import json
import re

router = APIRouter()


@router.post('/verification_code', name="验证码")
def verification_code(request: Request, verification: VerificationCode):
    ip = request.client.host
    # 获取客户端ip
    print(ip, "11111111111111111")
    mobile_phone = verification.mobile
    code_type = verification.type
    if not re.match(r'^1[3456789]\d{9}$', mobile_phone):
        return fail_response('手机格式不正确')
    user = User.filter(User.mobile == mobile_phone).first()
    if code_type == "register" or code_type == 'bind':
        if user:
            return fail_response('该手机号码已注册')
        redis_key = '%s_%s' % (code_type, mobile_phone)

        last_time = redis_client.ttl("%s_%s" % (code_type, mobile_phone))
        if last_time > settings.SMS_EXPIRE_TIME - settings.SMS_REPEAT_TIME:
            return fail_response('请勿重复获取验证码')
        # 3.1 生成随机的短信验证码
        code = "%06d" % random.randint(0, 999999)

        # template = {
        #     'code': code,
        # }
        # # 第三方短信接口返回成功的一个判断
        # try:
        #     res = send_sms(template, phone=mobile_phone)
        # except:
        #     return fail_response('获取验获取失败')
        # print(res)
        # res_dict = json.loads(res)
        # print(res)
        # if res_dict.get('Message') == 'OK' and res_dict.get('Code') == 'OK':
        res = 1
        if res == 1:
            redis_client.set(redis_key, code)
            redis_client.expire(redis_key, settings.SMS_EXPIRE_TIME)
        # redis_key
        # 在生产中需要将 下面code的返回数据去掉
        data = {'code': code}
        return success_response(data)
    elif code_type == "login" or code_type == "forget":
        if not user:
            return fail_response('该手机号码未注册')


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
    用户登陆借口
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


@router.get('/profile', response_model=CustomResponse[UserDetail], name='用户显示个人资料')
def user_profile(request: Request, current_user: User = Depends(get_current_user)):
    return success_response(current_user)


@router.put('/profile', response_model=CustomResponse[UserDetail], name='用户修改个人资料')
def user_profile(*, user_update: UserUpdate, current_user: User = Depends(get_current_user)):
    """
    修改的字段都需要重新提交
    修改数据的所有参数字段都需要重新提交，无论修改的数据有没有修改
    :param user_update:
    :param current_user:
    :return:
    """
    user_obj = User.filter(User.uuid == current_user.uuid).first()
    password = user_update.password
    email = user_update.email
    mobile = user_update.mobile
    if password and email and mobile:
        ex_email = User.filter(User.uuid != current_user.uuid, User.email == user_obj.email).first()
        if ex_email:
            return fail_response('用户名不能重复')
        ex_mobile = User.filter(User.uuid != current_user.uuid, User.email == user_obj.email).first()
        if ex_mobile:
            return fail_response('手机号已经被注册,不能修改为这个手机号！')
        user_obj.email = email
        user_obj.mobile = mobile
        user_obj.password = password
        user_obj.save()
    else:
        return fail_response('修改参数错误')
    return success_response(current_user)


@router.get('/user_list', response_model=CustomResponse[UserList], name="用户列表与搜索")
def get_user_list(
        page: int = Query(1, description='页码'),
        page_size: int = Query(settings.PAGE_SIZE, description='每页条数'),
        search: str = Query(None, description='查询参数'),
        current_user: User = Depends(get_current_superuser)
):
    try:
        if not search:
            users = User.select().where(User.user_type != current_user.user_type).order_by(User.created.desc())
        else:
            users = User.select().where(
                User.username % f'%{search}%' |
                User.email % f'%{search}%' |
                User.mobile % f'%{search}%', User.user_type != current_user.user_type).order_by(User.created.desc())
        paginate_users = users.paginate(page, page_size)
        paginate = {
            'page': page,
            'page_size': page_size,
            'total': users.count()
        }
        user_list = []
        if not paginate_users:
            return success_response({
                'paginate': paginate,
                'product_list': []
            })
        for user in paginate_users:
            user_list.append({
                'uuid': str(user.uuid),
                'username': user.username,
                'created': str(user.created),
                'email': user.email,
                'mobile': user.mobile,
            })
        data = {
            'paginate': paginate,
            'user_list': user_list
        }
        return success_response(data)
    except Exception as e:
        logger.error(f'获取用户列表失败，失败原因：{e}')
        return fail_response('获取用户列表失败')
