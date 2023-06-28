# cocreate_platform
AIGC共创平台项目仓库，让AI创新触手可及！

# 环境搭建
```bash
cd cocreate_platform

# 安装virtualenv
pip install virtualenv 

# 创建一个虚拟环境
virtualenv venv --python=python3.9

# 激活虚拟环境
## windows系统
### 直接把./venv/Scripts/activate.bat拖到cmd中

## MacOS或Linux系统
source venv/bin/activate
## 激活虚拟环境后，在终端的每行最前面还有(venv)这个标志

# 激活环境后安装项目依赖包
pip install -r requirements.txt

# 在cocreate_platform/setting.py文件中找到数据库配置，在本地按照配置文件，新建好数据库后
# django数据库表结构迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级管理员
python manage.py createsuperuser

# 运行项目
python manage.py runserver
# 打开页面http://127.0.0.1:8000/admin/ ，用刚刚创建的超级管理员账号登录
```

## 技术架构
Vue(3) + Django(3.2.5) + MySQL(8.0)

Django REST framework 前后端分离模式

## 部分接口
- 项目信息 http://127.0.0.1:8000/api/projects/
- 具体项目 http://127.0.0.1:8000/api/projects/1/
- 用户列表 http://127.0.0.1:8000/api/users/
- 具体用户 http://127.0.0.1:8000/api/users/1/
- 获取特定用户参与的所有项目 http://127.0.0.1:8000/api/users/1/projects/
- 后台管理 http://127.0.0.1:8000/admin/

## 参考文档
- [Django3.2文档](https://docs.djangoproject.com/zh-hans/3.2/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [产品需求文档](https://fa9xss3fg96.feishu.cn/wiki/MzoEwap1SiurhikutYBc0LcRnNb)
