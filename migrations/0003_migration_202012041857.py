# auto-generated snapshot
from peewee import *
import datetime
import peewee
import uuid


snapshot = Snapshot()


@snapshot.append
class Article(peewee.Model):
    title = CharField(max_length=50)
    desc = CharField(max_length=255)
    content = TextField()
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)
    class Meta:
        table_name = "article"


@snapshot.append
class User(peewee.Model):
    uuid = UUIDField(default=uuid.uuid4, index=True, primary_key=True)
    username = CharField(max_length=32, unique=True)
    password_hash = CharField(max_length=128)
    created = DateTimeField(default=datetime.datetime.now)
    email = CharField(max_length=128, null=True)
    mobile = CharField(max_length=11, null=True, unique=True)
    modified = DateTimeField(default=datetime.datetime.now)
    class Meta:
        table_name = "user"


@snapshot.append
class Blog(peewee.Model):
    title = CharField(max_length=64)
    site_name = CharField(max_length=64)
    theme = CharField(max_length=32)
    user_id = snapshot.ForeignKeyField(backref='user', index=True, model='user', null=True)
    update_time = DateTimeField(default=datetime.datetime.now)
    class Meta:
        table_name = "blog"


@snapshot.append
class Tag(peewee.Model):
    title = CharField(max_length=32)
    blog_id = snapshot.ForeignKeyField(backref='blog', index=True, model='blog')
    update_time = DateTimeField(default=datetime.datetime.now)
    class Meta:
        table_name = "tag"


@snapshot.append
class ArticleTag(peewee.Model):
    article_id = snapshot.ForeignKeyField(index=True, model='article')
    tag_id = snapshot.ForeignKeyField(index=True, model='tag')
    class Meta:
        table_name = "article_tag"


@snapshot.append
class ArticleUpDown(peewee.Model):
    user_id = snapshot.ForeignKeyField(index=True, model='user')
    article_id = snapshot.ForeignKeyField(index=True, model='article')
    is_up = BooleanField(default=True)
    class Meta:
        table_name = "article_up"


@snapshot.append
class Category(peewee.Model):
    title = CharField(max_length=32)
    blog_id = snapshot.ForeignKeyField(backref='blog', index=True, model='blog')
    update_time = DateTimeField(default=datetime.datetime.now)
    class Meta:
        table_name = "category"


@snapshot.append
class Comment(peewee.Model):
    article_id = snapshot.ForeignKeyField(index=True, model='article')
    user_id = snapshot.ForeignKeyField(index=True, model='user')
    content = CharField(max_length=255)
    create_time = DateTimeField(default=datetime.datetime.now)
    parent_id = snapshot.ForeignKeyField(backref='children', index=True, model='@self', null=True)
    class Meta:
        table_name = "comment"


