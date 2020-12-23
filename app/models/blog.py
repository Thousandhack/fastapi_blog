from peewee import Model, CharField
from peewee import UUIDField, DateTimeField, AutoField
from peewee import ForeignKeyField
from peewee import TextField
from peewee import BooleanField
from app.db.database import database
import datetime
from .user import User


class BlogSite(Model):
    """
    博客站点表
    用户和站点一对一关系，
    """
    id = AutoField(primary_key=True)
    title = CharField(max_length=64, verbose_name='个人博客标题')
    site_name = CharField(max_length=64, verbose_name='站点名称')
    theme = CharField(max_length=32, verbose_name='博客主题')
    user_id = ForeignKeyField(User, null=True, backref='user')
    create_time = DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')
    update_time = DateTimeField(null=False, default=datetime.datetime.now, verbose_name='修改时间')

    def save(self, *args, **kwargs):
        self.update_time = datetime.datetime.now()
        return super(BlogSite, self).save(*args, **kwargs)

    def to_dict(self):
        data = {
            "id": self.id,
            "title": self.title,
            "site_name": self.site_name,
            "theme": self.theme,
            "create_time": str(self.create_time),
            "update_time": str(self.update_time)
        }
        return data

    class Meta:  # 迁移指定数据库
        database = database
        table_name = 'blog_site'


class Category(Model):
    """
    标签
    站点和标签绑定的是一对多的关系
    """
    id = AutoField(primary_key=True)
    title = CharField(max_length=32, verbose_name='分类标题')
    description = CharField(max_length=128, verbose_name='分类描述')
    blog_id = ForeignKeyField(BlogSite, backref='blog', verbose_name="多对一站点表")
    create_time = DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')
    update_time = DateTimeField(null=False, default=datetime.datetime.now, verbose_name='修改时间')

    def save(self, *args, **kwargs):
        self.update_time = datetime.datetime.now()
        return super(Category, self).save(*args, **kwargs)

    def to_dict(self):
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "blog_id": self.blog_id.id,
            "create_time": str(self.create_time),
            "update_time": str(self.update_time)
        }
        return data

    class Meta:
        database = database
        table_name = 'category'


class Tag(Model):
    """
    博主个人文章分类表：Linux、python、面试心得、鸡汤
    分类表和用户表是多对一的关系，由于用户和站点是一对一，分类表与站点也是多对一的关系
    多
    """
    id = AutoField(primary_key=True)
    title = CharField(max_length=32, verbose_name='标签名称')
    blog_id = ForeignKeyField(BlogSite, backref='blog', verbose_name="多对一站点表")
    create_time = DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')
    update_time = DateTimeField(null=False, default=datetime.datetime.now, verbose_name='修改时间')

    def save(self, *args, **kwargs):
        self.update_time = datetime.datetime.now()
        return super(Tag, self).save(*args, **kwargs)

    class Meta:
        database = database
        table_name = 'tag'


class Article(Model):
    """
    文章表
    分类和文章的关系在这里设置为一对多关系（为了与文章和标签关系形成区分） 也就是一篇博客只能在一个分类下面
    用户和文章是一对多的关系
    标签与文章是多对多的关系（用中介模型创建第三张表）
    # backref是反查的字段，如果有related_name用related_name反查，如果没有直接用petties反查
    关于联表删除
    """
    id = AutoField(primary_key=True)
    title = CharField(max_length=50, verbose_name='文章标题')
    desc = CharField(max_length=255, verbose_name='文章描述')  # 摘要
    content = TextField(verbose_name='文章内容')
    category_id = ForeignKeyField(Category, null=True, backref='category')
    user_id = ForeignKeyField(User, null=True, backref='user')
    create_time = DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')  # 发布时间
    update_time = DateTimeField(null=False, default=datetime.datetime.now, verbose_name='修改时间')

    def save(self, *args, **kwargs):
        self.update_time = datetime.datetime.now()
        return super(Article, self).save(*args, **kwargs)

    def to_dict(self):
        data = {
            "id": self.id,
            "title": self.title,
            "desc": self.desc,
            "content": self.content,
            "category_id": self.category_id,
            "user_id": self.user_id,
            "create_time": str(self.create_time),
            "update_time": str(self.update_time)
        }
        return data

    class Meta:
        database = database
        table_name = 'article'


class ArticleTag(Model):
    """
    文章标签关系表
    此表为文章表与标签表多对多关系产生的第三张表

    """
    article_id = ForeignKeyField(Article)
    tag_id = ForeignKeyField(Tag)

    class Meta:
        database = database
        table_name = 'article_tag'


class ArticleUpDown(Model):
    """
    文章点赞表
    哪个用户对哪个文章点赞或点灭
    """
    id = AutoField(primary_key=True)
    user_id = ForeignKeyField(User)
    article_id = ForeignKeyField(Article)
    is_up = BooleanField(default=True)  # True：赞，  False：灭
    create_time = DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')  # 发布时间
    update_time = DateTimeField(null=False, default=datetime.datetime.now, verbose_name='修改时间')

    def save(self, *args, **kwargs):
        self.update_time = datetime.datetime.now()
        return super(ArticleUpDown, self).save(*args, **kwargs)

    class Meta:
        unique_together = [('article_id', 'user_id'), ]
        database = database
        table_name = 'article_up'


class Comment(Model):
    """
    评论表
    根评论：对文章的评论
    子评论：对评论的评论
    哪一个用户对哪一篇文章在什么时间做了什么评论内容
    nid    user_id  article_id    content    parent_comment_id(null=True)
    1       1           1           111             null
    2       2           1           222             null
    3       3           1           333             null
    4       4           1           444               1
    5       5           1           555               4
    """
    id = AutoField(primary_key=True)
    article_id = ForeignKeyField(Article)
    user_id = ForeignKeyField(User)
    content = CharField(max_length=255, verbose_name='评论内容')
    create_time = DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')
    update_time = DateTimeField(null=False, default=datetime.datetime.now, verbose_name='修改时间')
    # parent_comment = models.ForeignKey("Comment")   # 关联Comment表，本身就在Comment表中，因此是自关联
    parent_id = ForeignKeyField('self', null=True, backref='children')  # 设置null=True,为null的情况不用存值了

    def save(self, *args, **kwargs):
        self.update_time = datetime.datetime.now()
        return super(Comment, self).save(*args, **kwargs)

    def to_dict(self):
        data = {
            "id": self.id,
            "article_id": self.article_id.id,
            "user_id": self.user_id.username,
            "content": self.content,
            "parent_id": self.parent_id,
            "create_time": str(self.create_time),
            "update_time": str(self.update_time)
        }
        return data

    class Meta:
        database = database
        table_name = 'comment'
