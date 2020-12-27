from pydantic import BaseModel, Field, EmailStr, UUID4
from typing import Optional
from typing import List, Set, Dict


class Paginate(BaseModel):
    page: int = Field(1, description="页码数")
    page_size: int = Field(None, description="每页数量")
    total: int = Field(description="数据总量")


class CreateBlogSite(BaseModel):
    title: str = Field(..., description="博客标题")
    site_name: str = Field(..., description="站点名称")
    theme: str = Field(..., description="博客主题")

    class Config:
        schema_extra = {
            "example": {
                "title": "人生苦短--测试数据",
                "site_name": "hsz的博客站点--测试数据",
                "theme": "本博客站点主要记录的是Python编程相关--测试数据"
            }
        }


class CreateUserBlogSite(CreateBlogSite):
    user_id: str = Field(..., description="用户ID")

    class Config:
        schema_extra = {
            "example": {
                "title": "人生苦短--测试数据",
                "site_name": "hsz的博客站点--测试数据",
                "theme": "本博客站点主要记录的是Python编程相关--测试数据",
                "user_id": "8488162f61dc480b8048d7a9e0ef5adc"
            }
        }


class BlogSiteInfo(BaseModel):
    title: str = Field(..., description="博客标题")
    site_name: str = Field(..., description="站点名称")
    theme: str = Field(..., description="博客主题")
    create_time: str = Field(description="创建时间")
    update_time: str = Field(description="更新时间")


class BlogSiteAllInfo(BlogSiteInfo):  # 这边使用了嵌套模型
    id: str = Field(description="站点ID")

    # title: str = Field(description="博客标题")
    # site_name: str = Field(description="站点名称")
    # theme: str = Field(description="博客主题")
    # create_time: str = Field(description="创建时间")
    # update_time: str = Field(description="更新时间")


class BlogSiteList(BaseModel):
    paginate: Paginate = dict()
    blog_site_list: List[BlogSiteAllInfo] = []

    class Config:
        schema_extra = {
            "example": {
                "paginate": {
                    "page": 1,
                    "page_size": 10,
                    "total": 2
                },
                "blog_site_list": [
                    {
                        "title": "人生苦短--测试数据1111",
                        "site_name": "hsz的博客站点--测试数据111",
                        "theme": "本博客站点主要记录的是Python编程相关--测试数据111",
                        "create_time": "2020-12-08 11:08:47",
                        "update_time": "2020-12-08 11:08:47",
                        "id": "4"
                    },
                    {
                        "title": "人生苦短--测试数据",
                        "site_name": "hsz的博客站点--测试数据",
                        "theme": "本博客站点主要记录的是Python编程相关--测试数据",
                        "create_time": "2020-12-08 11:01:10",
                        "update_time": "2020-12-08 11:01:10",
                        "id": "1"
                    }
                ]
            }
        }


class UpdateBlogSite(CreateBlogSite):
    pass
# 到这

class CreateCategory(BaseModel):
    title: str = Field(description="分类标题")
    description: str = Field(description="分类描述")

    class Config:
        schema_extra = {
            "example": {
                "title": "python",
                "description": "python学习的分类",
            }
        }


class UpdateCategory(CreateCategory):
    pass

    class Config:
        schema_extra = {
            "example": {
                "title": "python修改后",
                "description": "python学习的分类修改后",
            }
        }


class CategoryInfo(BaseModel):
    id: str = Field(description="分类ID")
    title: str = Field(description="分类标题")
    description: str = Field(description="分类描述")
    # blog_id: str = Field(description="关联字段站点ID")
    create_time: str = Field(description="创建时间")
    update_time: str = Field(description="更新时间")


class ArticleListData(BaseModel):
    id: int = Field(description="文章id")
    title: str = Field(description="文章标题")
    desc: str = Field(description="文章描述")
    content: str = Field(description="文章内容")
    create_time: str = Field(description="创建时间")
    update_time: str = Field(description="更新时间")


class ArticleList(BaseModel):
    paginate: Paginate = dict()
    article_list: List[ArticleListData] = []


class QueryList(BaseModel):
    id: int = Field(description="文章id")
    title: str = Field(description="文章标题")
    desc: str = Field(description="文章描述")
    content: str = Field(description="文章内容")


class CreateArticle(BaseModel):
    title: str = Field(..., min_length=2, max_length=50, description='文字标题')
    desc: str = Field(..., min_length=2, max_length=255, description='文字标题')
    content: str = Field(..., description='文字内容')
    category_id: int = Field(None, description="博客分类ID")

    class Config:
        schema_extra = {
            "example": {
                "title": "测试的第一篇博客文章",
                "desc": "这个是测试的第一篇文字的描述，主要用于测试使用",
                "content": "本篇文章主要用于测试，这个是测试的内容",
                "category_id": 4
            }
        }


class ArticleInfo(BaseModel):
    title: str = Field(..., description='文字标题')
    desc: str = Field(..., description='文字标题')
    content: str = Field(..., description='文字内容')
    create_time: str = Field(..., description="创建时间")
    update_time: str = Field(..., description="更新时间时间")
    page_view: int = Field(..., description="文章访问量")


class UpdateArticle(BaseModel):
    title: str = Field(..., min_length=2, max_length=50, description='文字标题')
    desc: str = Field(..., min_length=2, max_length=255, description='文字标题')
    content: str = Field(..., description='文字内容')
    category_id: int = Field(None, description="博客分类ID")

    class Config:
        schema_extra = {
            "example": {
                "title": "测试的第一篇博客文章修改了",
                "desc": "这个是测试的第一篇文字的描述，主要用于测试使用",
                "content": "本篇文章主要用于测试，这个是测试的内容",
                "category_id": 4
            }
        }


class UpDown(BaseModel):
    is_up: bool = Field(..., description='点赞 true 为赞 false为取消')


class ChangeUpDown(BaseModel):
    is_up: bool = Field(False, description='点赞 true 为赞 false为取消')


class CreateComment(BaseModel):
    content: str = Field(..., min_length=2, max_length=128, description='评论内容')

    class Config:
        schema_extra = {
            "example": {
                "content": "文章写的非常好，666！",
            }
        }
