from fastapi import APIRouter, Depends
from fastapi import Path
from app.models.user import User
from app.models.blog import BlogSite
from app.schemas.response import CustomResponse
from app.schemas.blog import CreateBlogSite, CreateUserBlogSite, BlogSiteInfo, BlogSiteList, UpdateBlogSite
from app.api.utils.response import fail_response, success_response
from app.api.utils.security import get_current_user, get_current_superuser
from app.core.config import settings
from fastapi.logger import logger
from app.db.database import database as db
from datetime import datetime

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
        logger.error(f'获取文章列表失败，失败原因：{e}')
        return fail_response('获取文章列表失败')


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
