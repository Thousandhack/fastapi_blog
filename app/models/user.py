from peewee import Model, CharField, UUIDField, DateTimeField, IntegerField
from passlib.context import CryptContext
from app.db.database import database
from uuid import uuid4
import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Model):
    """
    用户信息表：
    """
    uuid = UUIDField(primary_key=True, index=True, default=uuid4)
    username = CharField(max_length=32, unique=True, verbose_name='用户名')
    password_hash = CharField(max_length=128)
    created = DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')
    email = CharField(max_length=128, null=True, verbose_name='电子邮箱')
    user_type = IntegerField(default=1, verbose_name='1:博主，0：管理员')
    mobile = CharField(max_length=11, null=True, unique=True, verbose_name='手机号码')
    modified = DateTimeField(default=datetime.datetime.now, verbose_name='修改时间')

    def save(self, *args, **kwargs):
        self.modified = datetime.datetime.now()
        return super(User, self).save(*args, **kwargs)

    @property
    def password(self):
        raise ValueError('密码不可读')

    @password.setter
    def password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    class Meta:
        database = database
