from fastapi import APIRouter, Depends, Request
from fastapi import Query
from fastapi import Path
from fastapi import File
from fastapi import UploadFile
from starlette.responses import FileResponse
from app.models.user import User
from app.models.blog import BlogSite, Category, Article, ArticleUpDown, Comment
from app.schemas.response import CustomResponse
from app.schemas.blog import ArticleList, CreateArticle, ArticleInfo, UpdateArticle
from app.schemas.blog import CreateBlogSite, CreateUserBlogSite, BlogSiteInfo, BlogSiteList, UpdateBlogSite
from app.schemas.blog import CreateCategory, UpdateCategory, CategoryInfo, CreateComment
from app.schemas.blog import UpDown
from app.api.utils.response import fail_response, success_response
from app.api.utils.security import get_current_user, get_current_superuser
from app.core.redis_app import redis_client
from app.core.config import settings
from fastapi.logger import logger
from app.db.database import database as db
from datetime import datetime
import random
import json
import re

router = APIRouter()


@router.get('/backend/blog_site', response_model=CustomResponse[BlogSiteList], name="后台查看博客站点列表")
def get_blog_sites(page: int = Query(1, description='页码'),
                   page_size: int = Query(settings.PAGE_SIZE, description='每页条数'),
                   search: str = Query(None, description='查询参数'),
                   current_user: User = Depends(get_current_superuser)
                   ):
    try:
        if not search:
            blog_sites = BlogSite.select().order_by(BlogSite.create_time.desc())
        else:
            blog_sites = BlogSite.select().where(
                BlogSite.title % f'%{search}%' |
                BlogSite.site_name % f'%{search}%' |
                BlogSite.theme % f'%{search}%').order_by(BlogSite.create_time.desc())
        paginate_blog_sites = blog_sites.paginate(page, page_size)
        paginate = {
            'page': page,
            'page_size': page_size,
            'total': blog_sites.count()
        }
        blog_site_list = []
        if not paginate_blog_sites:
            return success_response({
                'paginate': paginate,
                'product_list': []
            })
        for blog_site in paginate_blog_sites:
            # print(blog_site.to_dict())
            blog_site_list.append(
                blog_site.to_dict()
            )
        data = {
            'paginate': paginate,
            'blog_site_list': blog_site_list
        }
        return success_response(data)
    except Exception as e:
        logger.error(f'获取博客站点列表失败，失败原因：{e}')
        return fail_response('获取博客站点列表失败')


@router.post('/user/blog_site', name="个人创建博客站点")
@db.atomic()  # mysql 事务的作用
def create_blog_site(*, new_site: CreateBlogSite, current_user: User = Depends(get_current_user)):
    title = new_site.title
    site_name = new_site.site_name
    theme = new_site.theme
    blog_site = BlogSite.select().where(BlogSite.user_id == current_user.uuid)
    if blog_site:
        return fail_response('您的博客站点已存在,不能重复创建')
    try:
        BlogSite.create(title=title,
                        site_name=site_name,
                        theme=theme,
                        user_id=current_user.uuid)
        logger.info(f'创建博客站点name={site_name}站点成功')
        return success_response('添加成功')
    except Exception as e:
        db.rollback()
        logger.info(f'创建博客站点name={site_name}站点成功，失败原因：{e}')
        return fail_response('创建博客站点失败')


@router.post('/backend/blog_site', name="后台给个人创建博客站点")
@db.atomic()  # mysql 事务的作用
def create_user_blog_site(*, new_site: CreateUserBlogSite, current_user: User = Depends(get_current_superuser)):
    title = new_site.title
    site_name = new_site.site_name
    theme = new_site.theme
    user_id = new_site.user_id
    blog_site = BlogSite.select().where(BlogSite.user_id == user_id)
    if blog_site:
        return fail_response('博客站点已存在，不能重复创建')
    try:
        BlogSite.create(title=title,
                        site_name=site_name,
                        theme=theme,
                        user_id=user_id)
        logger.info(f'{current_user.username}创建博客站点{site_name}站点成功')
        return success_response('添加成功')
    except Exception as e:
        db.rollback()
        logger.info(f'创建博客站点name={site_name}站点成功，失败原因：{e}')
        return fail_response('创建博客站点失败')


@router.get('/blog_site/{site_id}', response_model=CustomResponse[BlogSiteInfo], name="个人博客站点详情")
def get_blog_site_info(site_id: str):
    blog_site = BlogSite.filter(id=site_id).first()
    if blog_site is None:
        return fail_response('博客站点不存在')
    return success_response(blog_site.to_dict())


@router.put('/backend/blog_site/{site_id}', name="后台修改博客站点信息")
@db.atomic()
def update_blog_site(site_id: int = Path(None, title="站点ID"),
                     the_blog_site: UpdateBlogSite = None,
                     current_user: User = Depends(get_current_user)):
    title = the_blog_site.title
    site_name = the_blog_site.site_name
    theme = the_blog_site.theme
    if current_user.user_type != 0:
        fail_response("用户权限不足")
    blog_site = BlogSite.filter(BlogSite.id == site_id).first()
    if blog_site is None:
        return fail_response('博客站点不存在')
    try:
        # 法一：
        query = BlogSite.update(title=title, site_name=site_name, theme=theme,
                                update_time=str(datetime.now())).where(
            BlogSite.id == site_id)
        query.execute()
        # 法二：
        # blog_site.title = title
        # blog_site.site_name = site_name
        # blog_site.theme = theme
        # blog_site.save()
        return success_response('更新修改博客站点成功')
    except Exception as e:
        db.rollback()
        logger.error(f'更新修改博客站点失败，失败原因：{e}')
        return fail_response('更新修改博客站点失败')


@router.delete('/backend/blog_site/{site_id}', name="后台删除博客站点信息")
@db.atomic()
def delete_blog_site(site_id: int = Path(..., title="站点ID"),
                     current_user: User = Depends(get_current_user)
                     ):
    if current_user.user_type != 0:
        fail_response("用户权限不足")
    blog_site = BlogSite.filter(BlogSite.id == site_id).first()
    if not blog_site:
        return fail_response('此博客站点不存在')
    try:
        result = blog_site.delete_instance()
        if not result:
            return fail_response('更新博客文章失败')
    except Exception as e:
        db.rollback()
        logger.error(f'更新博客文章失败，失败原因：{e}')
        return fail_response('删除博客文章失败')
    return success_response('删除博客文章成功')


@router.get('/category', name="个人博客分类列表")  # ,response_model=CustomResponse[CategoryList]
def get_category_list(page: int = Query(1, description='页码'),
                      page_size: int = Query(settings.PAGE_SIZE, description='每页条数'),
                      search: str = Query(None, description='查询参数'),
                      current_user: User = Depends(get_current_user)):
    try:
        blog_site = BlogSite.filter(BlogSite.user_id == current_user.uuid).first()
        if blog_site is None:
            return fail_response('此用户未创建博客站点，请先创建')
        if not search:
            categories = Category.select().where(Category.blog_id == blog_site.id).order_by(Category.create_time.desc())
        else:
            categories = Category.select().where(
                Category.blog_id == blog_site.id,
                Category.title % f'%{search}%' |
                Category.description % f'%{search}%'
            ).order_by(Category.create_time.desc())
        paginate_categories = categories.paginate(page, page_size)
        paginate = {
            'page': page,
            'page_size': page_size,
            'total': categories.count()
        }
        category_list = []
        if not paginate_categories:
            return success_response({
                'paginate': paginate,
                'product_list': []
            })
        for category in paginate_categories:
            category_list.append(category.to_dict())
        data = {
            'paginate': paginate,
            'article_list': category_list
        }
    except Exception as e:
        logger.error(f'获取个人博客分类列表失败，失败原因：{e}')
        return fail_response('获取个人博客分类列表失败')
    return success_response(data)


@router.post('/category', name="个人创建博客分类")
@db.atomic()
def create_category(*, new_category: CreateCategory, current_user: User = Depends(get_current_user)):
    title = new_category.title
    description = new_category.description
    blog_site = BlogSite.filter(BlogSite.user_id == current_user.uuid).first()
    if blog_site is None:
        return fail_response('此用户未创建博客站点，请先创建')
    category = Category.filter(Category.title == title, Category.blog_id == blog_site.id).first()
    if category:
        return fail_response("相同分类已存在！")
    try:
        Category.create(title=title,
                        description=description,
                        blog_id=blog_site.id)
    except Exception as e:
        db.rollback()
        logger.error(f'创建博客文章失败，失败原因：{e}')
        return fail_response('创建博客文章失败')
    return success_response('创建博客文章成功')


@router.get('/category/{category_id}', response_model=CustomResponse[CategoryInfo], name="个人查看博客分类详情")
def get_category_info(category_id: str, current_user: User = Depends(get_current_user)):
    blog_site = BlogSite.filter(BlogSite.user_id == current_user.uuid).first()
    if blog_site is None:
        return fail_response('此用户未创建博客站点，请先创建')
    category = Category.filter(Category.id == category_id, Category.blog_id == blog_site.id).first()
    if category is None:
        return fail_response("博客分类不存在")
    return success_response(category.to_dict())


@router.put('/category/{category_id}', name="个人修改博客分类")  # , response_model=CustomResponse[CategoryInfo]
@db.atomic()
def get_category_info(category_id: str, up_category: UpdateCategory, current_user: User = Depends(get_current_user)):
    blog_site = BlogSite.filter(BlogSite.user_id == current_user.uuid).first()
    if blog_site is None:
        return fail_response('此用户未创建博客站点，请先创建')
    category = Category.filter(Category.id == category_id, Category.blog_id == blog_site.id).first()
    if not category:
        return fail_response("博客分类不存在")
    try:
        query = Category.update(title=up_category.title, description=up_category.description,
                                update_time=str(datetime.now)).where(
            Category.id == category_id, Category.blog_id == blog_site.id)
        query.execute()
        return success_response('更新博客分类成功')
    except Exception as e:
        db.rollback()
        logger.error(f'更新博客分类失败，失败原因：{e}')
        return fail_response('更新博客分类失败')


@router.delete('/category/{category_id}', name="个人删除博客分类")  # , response_model=CustomResponse[CategoryInfo]
@db.atomic()
def delete_category(category_id: str, current_user: User = Depends(get_current_user)):
    # 法一：
    # blog_site = BlogSite.filter(BlogSite.user_id == current_user.uuid).first()
    # if blog_site is None:
    #     return fail_response('此用户未创建博客站点，请先创建')
    # category = Category.filter(Category.id == category_id, Category.blog_id == blog_site.id).first()
    # if not category:
    #     return fail_response("博客分类不存在")
    # try:
    #     result = category.delete_instance()
    #     if result:
    #         return success_response('删除博客文章成功')
    #     return fail_response('更新博客文章失败')
    # except Exception as e:
    #     db.rollback()
    #     logger.error(f'更新博客文章失败，失败原因：{e}')
    #     return fail_response('删除博客文章失败')
    # 法二：使用联表查询的方式
    category = Category.select().join(BlogSite, on=(Category.blog_id == BlogSite.id)).where(
        BlogSite.user_id == current_user.uuid, Category.id == category_id)
    if not category:
        return fail_response("博客分类不存在")
    try:
        # 先将这个用户下这个分类的文章的分类改为空值
        articles = Article.filter(Article.category_id == category_id)
        for article in articles:
            article.category_id = None
            article.save()
        # 再将这个文章分类删掉
        query = Category.delete().where(Category.id == category_id)
        result = query.execute()  # 删除成功返回 1  所以不等于1为失败
        if result != 1:
            return fail_response('更新博客文章失败')
    except Exception as e:
        db.rollback()
        logger.error(f'更新博客文章失败，失败原因：{e}')
        return fail_response('删除博客文章失败')
    return success_response('删除博客文章成功')


@router.get('/category/{category_id}/article', response_model=CustomResponse[ArticleList], name="分类下博客文章列表")
def get_article_list(
        category_id: str = Path(0, description="博客分类id"),
        page: int = Query(1, description='页码'),
        page_size: int = Query(settings.PAGE_SIZE, description='每页条数'),
        search: str = Query(None, description='查询参数'),
        # start_time: datetime = Query(None, description='工单开始时间'),
        # end_time: datetime = Query(None, description='工单结束时间'),
):
    try:
        if category_id == '0':
            category_id = None
        if not search:
            articles = Article.select().where(Article.category_id == category_id).order_by(Article.create_time.desc())
        else:
            # 法二：
            articles = Article.select().where(
                Article.category_id == category_id,
                Article.title.contains(search) |
                Article.desc.contains(search) |
                Article.content.contains(search)).order_by(Article.create_time.desc())
        # # 参数校验
        # if (not start_time or not end_time) and (start_time or end_time):
        #     return fail_response('时间错误')
        # if start_time and end_time:
        #     if start_time > end_time or (end_time - datetime.now()).total_seconds() > 24 * 60 * 60:
        #         return fail_response('时间错误')
        # if start_time and end_time:
        #     articles = articles.where(Article.create_time >= start_time, Article.create_time <= end_time)
        paginate_articles = articles.paginate(page, page_size)
        paginate = {
            'page': page,
            'page_size': page_size,
            'total': articles.count()
        }
        if not paginate_articles:
            return success_response({
                'paginate': paginate,
                'product_list': []
            })
        article_list = [article.to_dict() for article in paginate_articles]
        data = {
            'paginate': paginate,
            'article_list': article_list
        }
        return success_response(data)
    except Exception as e:
        logger.error(f'获取文章列表失败，失败原因：{e}')
        return fail_response('获取文章列表失败')


@router.get('/backend/article', response_model=CustomResponse[ArticleList], name="博客文章列表")
def get_article_list(
        page: int = Query(1, description='页码'),
        page_size: int = Query(settings.PAGE_SIZE, description='每页条数'),
        search: str = Query(None, description='查询参数'),
        start_time: datetime = Query(None, description='工单开始时间'),
        end_time: datetime = Query(None, description='工单结束时间'),
):
    try:
        if not search:
            articles = Article.select().order_by(Article.create_time.desc())
        else:
            # 法一：
            # articles = Article.select().where(
            #     Article.title % f'%{search}%' |
            #     Article.desc % f'%{search}%' |
            #     Article.content % f'%{search}%').order_by(Article.create_time.desc())
            # 法二：
            articles = Article.select().where(
                Article.title.contains(search) |
                Article.desc.contains(search) |
                Article.content.contains(search)).order_by(Article.create_time.desc())
        # 参数校验
        if (not start_time or not end_time) and (start_time or end_time):
            return fail_response('时间错误')
        if start_time and end_time:
            if start_time > end_time or (end_time - datetime.now()).total_seconds() > 24 * 60 * 60:
                return fail_response('时间错误')
        if start_time and end_time:
            articles = articles.where(Article.create_time >= start_time, Article.create_time <= end_time)
        paginate_articles = articles.paginate(page, page_size)
        paginate = {
            'page': page,
            'page_size': page_size,
            'total': articles.count()
        }
        if not paginate_articles:
            return success_response({
                'paginate': paginate,
                'product_list': []
            })
        # 法一：
        # article_list = []
        # for article in paginate_articles:
        #     article_list.append({
        #         'id': article.id,
        #         'title': article.title,
        #         'desc': article.desc,
        #         'content': article.content,
        #         'create_time': str(article.create_time),
        #         'update_time': str(article.update_time)
        #     })
        # 法二：（相应的模型需要加to_dict的方法）
        # for article in paginate_articles:
        #     article_list.append(article.to_dict())
        # 法三:使用列表推导式
        article_list = [article.to_dict() for article in paginate_articles]
        data = {
            'paginate': paginate,
            'article_list': article_list
        }

        return success_response(data)
    except Exception as e:
        logger.error(f'获取文章列表失败，失败原因：{e}')
        return fail_response('获取文章列表失败')


@router.get('/backend/query_article', response_model=CustomResponse[ArticleList], name="博客文章列表按自己想要的字段搜索")
def get_article_list(
        page: int = Query(1, description='页码'),
        page_size: int = Query(settings.PAGE_SIZE, description='每页条数'),
        article_id: int = Query(None, description='文章ID'),
        title: str = Query(None, description='文章标题'),
        desc: str = Query(None, description='文章描述'),
        content: str = Query(None, description='文章内容'),
):
    try:
        article_query = Article.select()
        if article_id:
            article_query = article_query.where(Article.id.contains(article_id))
        if title:
            article_query = article_query.where(Article.title.contains(title))
        if desc:
            article_query = article_query.where(Article.desc.contains(desc))
        if content:
            article_query = article_query.where(Article.content.contains(content))
        # paginate_articles = article_query.limit(page_size).offset((page-1)*page_size) # 得到的结果同下
        paginate_articles = article_query.paginate(page, page_size)
        paginate = {
            'page': page,
            'page_size': page_size,
            'total': article_query.count()
        }
        if not paginate_articles:
            return success_response({
                'paginate': paginate,
                'product_list': []
            })
        article_list = [article.to_dict() for article in paginate_articles]
        data = {
            'paginate': paginate,
            'article_list': article_list
        }

        return success_response(data)
    except Exception as e:
        logger.error(f'获取文章列表失败，失败原因：{e}')
        return fail_response('获取文章列表失败')


@router.post('/user/article', name="创建博客文章")
@db.atomic()
def create_article(*, new_article: CreateArticle,
                   current_user: User = Depends(get_current_user)):
    title = new_article.title
    desc = new_article.desc
    content = new_article.content
    category_id = new_article.category_id
    article = Article.filter(Article.user_id == current_user.uuid).first()
    if article:
        fail_response("您的博客文章已创建,不能重复创建")
    try:
        new_article = Article.create(title=title,
                                     desc=desc,
                                     content=content,
                                     user_id=current_user.uuid,
                                     category_id=category_id)
        print(new_article.title)
    except Exception as e:
        db.rollback()
        logger.error(f'创建博客文章失败，失败原因：{e}')
        return fail_response('创建博客文章失败')
    return success_response('创建博客文章成功')


@router.post('/article/upload_picture', name="博客图片上传")
async def create_upload_file(
        file: UploadFile = File(...),
):
    filename = file.filename
    # ALLOWED_EXTENSIONS = set('png', 'jpg', 'JPG', 'PNG')
    # and filename.rsplit('.', 1)[1] not in ALLOWED_EXTENSIONS
    if '.' not in filename:
        fail_response("图片格式不正确")
    # 保存上传的文件
    contents = await file.read()
    now_time = datetime.now().strftime("%Y%m%d%H%M%S")
    random_num = random.randint(0, 100)
    ext = filename.rsplit('.', 1)[1]
    picture_name = settings.BASE_DIR + settings.PICTURE_DIR + now_time + "_" + str(random_num) + ext
    with open(picture_name, "wb") as f:
        f.write(contents)
    picture_url = "/api/v1.0/blog/article/picture_url/" + now_time + "_" + str(random_num) + ext
    return {
        "picture_url": picture_url,
    }


@router.get('/article/picture_url/{picture_name}', name="博客图片url获取")
async def get_picture(picture_name: str):
    # 保存上传的文件
    # print(settings.BASE_DIR + settings.PICTURE_DIR, "123456")
    # picture_url = settings.BASE_DIR + settings.PICTURE_DIR + "test.png"
    if picture_name:
        picture_url = settings.BASE_DIR + settings.PICTURE_DIR + picture_name
        return FileResponse(picture_url, media_type="image/png")
    else:
        return fail_response("没有相关图片")


@router.get('/article/{article_id}', response_model=CustomResponse[ArticleInfo], name="博客文章详情展示")
def get_article_info(article_id: str):
    """
    在排行榜这款  需要把 标题也存进去
    :param article_id:
    :return:
    """
    article = Article.filter(Article.is_delete == 0, Article.id == article_id).first()
    if article:
        title = article.title
        res = redis_client.exists("article_rank_list")
        if not res:
            # 连有序集合都没有的情况 初始化分数
            redis_client.zadd("article_rank_list", {"article_%s_%s" % (article_id, title): 1})
            # print(redis_client.zscore("article_rank_list", "article_id_1"))
        else:
            # 存在了但是这个文章
            res_score = redis_client.zscore("article_rank_list", "article_%s_%s" % (article_id, title))
            if res_score is None:
                # 初始化分数
                redis_client.zadd("article_rank_list", {"article_%s_%s" % (article_id, title): 1})
            # 存在这个key的时候就分值增加 1
            redis_client.zincrby("article_rank_list", 1, "article_%s_%s" % (article_id, title))
        page_view = redis_client.zscore("article_rank_list", "article_%s_%s" % (article_id, title))
        # return success_response(score)
        # redis_client.incr('article_id:%s' % article_id)
        # page_view = redis_client.get('article_id:%s' % article_id)
        data = {"title": article.title,
                "desc": article.desc,
                "content": article.content,
                "create_time": str(article.create_time),
                "update_time": str(article.update_time),
                "page_view": page_view}

        return success_response(data)
    return fail_response("文章不存在")


@router.put('/article/{article_id}', name="修改博客文章")
@db.atomic()
def update_article(article_id: str,
                   new_article: UpdateArticle,
                   current_user: User = Depends(get_current_user)):
    title = new_article.title
    desc = new_article.desc
    content = new_article.content
    category_id = new_article.category_id
    article = Article.filter(Article.id == article_id, Article.user_id == current_user.uuid,
                             Article.is_delete == 0).first()
    if not article:
        return fail_response('此文章不存在')
    try:
        query = Article.update(title=title, desc=desc, content=content, category_id=category_id,
                               update_time=str(datetime.now)).where(
            Article.id == article_id, Article.user_id == current_user.uuid)
        query.execute()
        # 修改排行榜的标题
        res = redis_client.exists("article_rank_list")
        if not res:
            # 连有序集合都没有的情况 初始化分数 0
            redis_client.zadd("article_rank_list", {"article_%s_%s" % (article_id, title): 0})
            # print(redis_client.zscore("article_rank_list", "article_id_1"))
        else:
            # 存在了但是这个文章
            res_score = redis_client.zscore("article_rank_list", "article_%s_%s" % (article_id, title))
            if res_score is None:
                # 初始化分数
                redis_client.zadd("article_rank_list", {"article_%s_%s" % (article_id, title): 0})
            else:
                # 删除之前的分数记录
                redis_client.zrem("article_rank_list", "article_%s_%s" % (article_id, title))

                # 重新建立一个并将之前的分数给这个
                redis_client.zadd("article_rank_list", {"article_%s_%s" % (article_id, title): res_score})
            # 存在这个key的时候就分值增加 1
            redis_client.zincrby("article_rank_list", 1, "article_%s_%s" % (article_id, title))
        return success_response('更新博客文章成功')
    except Exception as e:
        db.rollback()
        logger.error(f'更新博客文章失败，失败原因：{e}')
        return fail_response('更新博客文章失败')


@router.delete('/article/{article_id}', name="删除博客文章")
@db.atomic()
def delete_article(article_id: str,
                   current_user: User = Depends(get_current_user)):
    article = Article.filter(Article.id == article_id, Article.user_id == current_user.uuid).first()
    if not article:
        return fail_response('此文章不存在')
    title = article.title
    try:
        # 之前这个是 物理删除
        # result = article.delete_instance()
        # 删除改为逻辑删除
        query = Article.update(is_delete=True).where(
            Article.id == article_id, Article.user_id == current_user.uuid)
        result = query.execute()
        # print(result, "运行后的结果")
        if result:
            res = redis_client.exists("article_rank_list")
            if res:
                # 存在了但是这个文章
                res_score = redis_client.zscore("article_rank_list", "article_%s_%s" % (article_id, title))
                if res_score:
                    # 删除之前的分数记录
                    redis_client.zrem("article_rank_list", "article_%s_%s" % (article_id, title))
            return success_response('删除博客文章成功')
        return fail_response('删除博客文章失败')
    except Exception as e:
        db.rollback()
        logger.error(f'删除博客文章失败，失败原因：{e}')
        return fail_response('删除博客文章失败')


@router.get('/article/{article_id}/like_count', name="某博客文章统计点赞数可放到博客详情")
def get_article_info(article_id: str):
    article = Article.filter(Article.id == article_id).first()
    if not article:
        return fail_response('此文章不存在')
    try:
        up_count = ArticleUpDown.filter(ArticleUpDown.article_id == article.id, ArticleUpDown.is_up == True).count()
    except Exception as e:
        db.rollback()
        logger.error(f'更新博客文章失败，失败原因：{e}')
        return fail_response('删除博客文章失败')
    return success_response({"article_id": article_id,
                             "up_count": up_count})


@router.get('/article/{article_id}/like_record', name="用户查看自己某篇博客文章点赞记录")
def get_article_up_count(article_id: str,
                         current_user: User = Depends(get_current_user)):
    article = Article.filter(Article.id == article_id, Article.user_id == current_user).first()
    if not article:
        return fail_response('此文章不存在')
    try:
        article_likes = ArticleUpDown.filter(ArticleUpDown.article_id == article.id, ArticleUpDown.is_up == True)
        user_list = [article_like.user_id.username for article_like in article_likes]
        up_count = article_likes.count()
    except Exception as e:
        db.rollback()
        logger.error(f'更新博客文章失败，失败原因：{e}')
        return fail_response('删除博客文章失败')
    return success_response({"user_list": user_list,
                             "up_count": up_count})


@router.post('/article/{article_id}/like', name="用户给博客文章点赞")
def article_up(article_id: str,
               up_down: UpDown,
               current_user: User = Depends(get_current_user)):
    is_up = up_down.is_up
    article = Article.filter(Article.id == article_id).first()
    if not article:
        return fail_response('此文章不存在')
    article_like = ArticleUpDown.filter(ArticleUpDown.user_id == current_user.uuid,
                                        ArticleUpDown.article_id == article_id).first()
    if article_like and article_like.is_up == is_up:
        pass
    elif article_like and article_like.is_up != is_up:
        article_like.is_up = is_up
        article_like.save()
    else:
        try:
            ArticleUpDown.create(user_id=current_user, article_id=article, is_up=is_up)
        except Exception as e:
            db.rollback()
            logger.error(f'点赞操作失败，失败原因：{e}')
            return fail_response('点赞操作失败')
    return success_response('操作成功成功')


@router.put('/article/{article_id}/like', name="用户给博客文章点赞取消")
def article_down(article_id: str,
                 up_down: UpDown,
                 current_user: User = Depends(get_current_user)):
    is_up = up_down.is_up
    article = Article.filter(Article.id == article_id).first()
    if not article:
        return fail_response('此文章不存在')
    article_like = ArticleUpDown.filter(ArticleUpDown.user_id == current_user.uuid,
                                        ArticleUpDown.article_id == article_id).first()
    if article_like and article_like.is_up == is_up:
        pass
    elif article_like and article_like.is_up != is_up:
        article_like.is_up = is_up
        article_like.save()
    else:
        return fail_response('点赞操作失败')
    return success_response('点赞操作成功')


@router.get('/article/{article_id}/comments', name="某篇博客文章评论列表")
def get_comment_list(article_id: str):
    article = Article.filter(Article.id == article_id).first()
    if not article:
        return fail_response('此文章不存在')
    comment_query = Comment.select().order_by(Comment.create_time.desc())
    count = comment_query.count()
    comment_list = [comment.to_dict() for comment in comment_query]
    return success_response({"count": count,
                             "comment_list": comment_list})


@router.post('/article/{article_id}/comment', name="用户给某篇博客文章评论")
@db.atomic()
def add_comment(create_comment: CreateComment,
                article_id: str = Path(2, description="博客文章id"),
                current_user: User = Depends(get_current_user)):
    content = create_comment.content
    article = Article.filter(Article.id == article_id).first()
    if not article:
        return fail_response('此文章不存在')
    try:
        Comment.create(article_id=article_id, user_id=current_user.uuid, content=content, parent_id=None)
    except Exception as e:
        db.rollback()
        logger.error(f'博客文章评论失败，失败原因：{e}')
        return fail_response('删除博客文章失败')
    return success_response('新增评论成功！')


@router.put('/article/{article_id}/comment/{comment_id}', name="用户修改给某篇文章评论")
@db.atomic()
def update_comment(article_id: str,
                   comment_id: str,
                   create_comment: CreateComment,
                   current_user: User = Depends(get_current_user)):
    content = create_comment.content
    article = Article.filter(Article.id == article_id).first()
    if not article:
        return fail_response('此文章不存在')
    comment = Comment.filter(Comment.article_id == article_id, Comment.id == comment_id,
                             Comment.user_id == current_user.uuid).first()
    if not comment:
        return fail_response('此评论不存在')
    try:
        comment.content = content
        comment.save()
    except Exception as e:
        db.rollback()
        logger.error(f'博客文章评论修改失败，失败原因：{e}')
        return fail_response('博客文章评论修改失败！')
    return success_response('博客文章评论修改成功！')


@router.delete('/article/{article_id}/comment/{comment_id}', name="用户给某篇文章删除评论")
@db.atomic()
def delete_comment(article_id: str,
                   comment_id: str,
                   current_user: User = Depends(get_current_user)):
    article = Article.filter(Article.id == article_id).first()
    if not article:
        return fail_response('此文章不存在')
    comment = Comment.filter(Comment.article_id == article_id, Comment.id == comment_id,
                             Comment.user_id == current_user.uuid).first()
    if not comment:
        return fail_response('此评论不存在或你没有删除权限')
    try:
        result = comment.delete_instance()
        if not result:
            return fail_response('删除评论失败')
    except Exception as e:
        db.rollback()
        logger.error(f'删除评论失败失败，失败原因：{e}')
        return fail_response('删除评论失败！')
    return success_response('删除评论成功！')


@router.post('/article/{article_id}/comment/{comment_id}', name="用户给某篇博客回复评论")
@db.atomic()
def reply_comment(create_comment: CreateComment,
                  article_id: str = Path(2, description="博客文章id"),
                  comment_id: str = Path(2, description="评论id"),
                  current_user: User = Depends(get_current_user)):
    content = create_comment.content
    article = Article.filter(Article.id == article_id).first()
    if not article:
        return fail_response('此文章不存在')
    if article.user_id == current_user.uuid:
        # 博主的情况
        comment = Comment.filter(Comment.id == comment_id, Comment.article_id == article_id,
                                 Comment.user_id != current_user.uuid).first()
    else:
        # 用户
        comment = Comment.filter(Comment.id == comment_id, Comment.article_id == article_id,
                                 Comment.user_id != current_user.uuid,
                                 Comment.parent_id != '').first()
    if not comment:
        return fail_response('此评论不存在或原评论你不能进行回复！')
    try:
        Comment.create(article_id=article_id, user_id=current_user.uuid, content=content, parent_id=comment.id)
    except Exception as e:
        db.rollback()
        logger.error(f'评论回复失败，失败原因：{e}')
        return fail_response('评论回复失败')
    return success_response('评论回复成功！')


@router.get('/backend/rank/article', name="获取排行榜文章列表")  # response_model=CustomResponse[ArticleList]
def get_article_rank_list():
    """
    获取排行榜 有排行榜id  和 排行榜标题
    :return:
    """
    try:
        article_rank_list = []
        # if not search:
        #     articles = Article.select().order_by(Article.create_time.desc())
        # else:
        #     # 法二：
        #     articles = Article.select().where(
        #         Article.title.contains(search) |
        #         Article.desc.contains(search) |
        #         Article.content.contains(search)).order_by(Article.create_time.desc())

        res = redis_client.exists("article_rank_list")
        if not res:
            # 初始化分数
            return fail_response("暂时没有排行榜")
        rank_list = redis_client.zrange("article_rank_list", 0, 4, desc=True, withscores=True)
        # print(rank_list)
        # res = Article.filter(Article.id == 1).first()
        # print(res.id)
        for article_key_val in rank_list:
            # article = Article.filter(Article.id == article_key_val[0].decode('utf-8').split("_")[2]).first()
            article_info = {
                "article_id": int(article_key_val[0].decode('utf-8').split("_")[1]),
                "article_title": article_key_val[0].decode('utf-8').split("_")[2],
                "page_view": article_key_val[1]
            }
            article_rank_list.append(article_info)

        # if len(article_rank_list) > 5:
        #     article_rank_list = article_rank_list[:4]
        return success_response(article_rank_list)
    except Exception as e:
        # print(e)
        logger.error(f'获取文章列表失败，失败原因：{e}')
        return fail_response('获取文章列表失败')
