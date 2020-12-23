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
