# fastapi_blog
项目主要使用了FastAPI框架
项目主要使用了peewee的orm
主要需求是编写了一个后端的简单的博客

## 需求概述
```
企业级博客设计从功能、应用程序安全性、稳定性、响应速度以及界面美观性、易懂性等各方面提出了较高的需求。
从功能方面来说，博客系统具有8个方面的功能模块：
    用户管理、
    安全设置、
    博客管理、
    评论管理、
    评论管理、
    点赞管理、
    分类管理、
    标签管理和首页搜索管理；
    从非功能方面来讲，采用目前较为流行的技术来提高博客系统的安全性、稳定性、交互性以及美观性等。
```



## 功能需求与功能分析

● 用户管理：
    用户可以进行注册账号，账号注册完成之后便可登录博客系统，
    用户分为两种：博主和管理员，注册的时候默认用户是博主。
    其中博主只能对自己个人信息进行操作，包括头像更换和其他基本信息的修改，
    而管理员不仅可以对个人信息进行修改，还可以具有对其他用户进行相关操作，
    包括修改他人信息、删除用户以及设置管理员，管理员也可以根据用户名进行搜索进而对指定用户进行操作。

● 安全设置：安全设置包括两方面的内容
    角色授权和权限设置。用户角色分为博主和管理员，
    只有管理员才能进入到管理界面进行用户管理，
    普通博主只能对自己的博客和个人信息进行管理，
    如果未登录则无法对博客文章进行点赞和评论。

● 博客管理： 
    用户登录后可以发表博客，编辑博客内容时可以插入图片，
    在发布博客的时候可以对博客进行分类和设置标签，
    博客发布之后用户可以对自己的博客进行编辑、修改和删除，
    所有用户均可根据关键字在某博主的主页对博客进行模糊查询，
    同时，博客文章每次被访问之后阅读量会自动加1，
    阅读量也会显示在阅读博客页面中。

● 评论管理：
    用户登录后在阅读博客的时候可以对博客进行评论，也可以删除自己的评论，
    无法对别人的评论进行删除。
    每次增加或减少评论之后，都会对评论量进行更新，
    博客的评论量也会在阅读博客页面进行展示。

● 点赞管理:
    和评论管理的流程差不多，
    用户登录后在查看博客时可以进行点赞，
    若已经点过赞了，则无法再次点赞，
    可以取消点赞，每次进行点赞或者取消点赞操作之后都会对点赞量进行跟新。

● 分类管理：
    博主在个人主页中可以进行分类的创建、删除、修改，(博客下的分类删除的话，这个字段制空，对应分类下的博客变成未分类)
    通过分类管理可以方便用户有目标的查询博客，
    某一分类被点击后，会出现该用户在该分类下的所有博客文章，
    在发布博客的时候可以为该博客选择一个分类，以便对博客进行分类管理。不选择的话，默认未分类

● 标签管理：
    在发布博客时可以给博客增加多个标签，
    编辑博客时也可以删除标签，
    在博客系统的主页用户可以根据点击标签进行查询。

● 首页搜索管理：
    为方便用户快速获取自己想要的博客文章，在首页提供可全文检索功能。
    可以按发布时间对博客进行排序（最新文章排序），
    也可根据访问量、点赞量、评论量综合排序（最热文章排序），
    同时，首页也会展示热门标签、热门用户、热门文章，用户可以直接点击对应区域进行搜索操作。


# 数据迁移的步骤
```
(fastapi_blog) root@hsz-virtual-machine:/opt/myproject/fastapi_blog# pem init
Configuration file 'migrations.json' was created.
(fastapi_blog) root@hsz-virtual-machine:/opt/myproject/fastapi_blog# pem add app.models.user.User
Model 'app.models.user.User' was added to watch list.
(fastapi_blog) root@hsz-virtual-machine:/opt/myproject/fastapi_blog# pem watch
Migration `0001_migration_202012041607` has been created.
(fastapi_blog) root@hsz-virtual-machine:/opt/myproject/fastapi_blog# pem migrate
```
# 出现的一些问题的解决方法
```
# 问题 1
"Changing sql mode 'NO_AUTO_CREATE_USER' is deprecated
# 解决方法：
set @@GLOBAL.sql_mode='';
set sql_mode ='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
```

# redis 密码设置
127.0.0.1:6379> config set requirepass 123456

