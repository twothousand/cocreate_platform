"""
Django settings for cocreate_platform project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)km-62r9w*s#ka(+e6m81nnteakm8l*m80l#i8sxa6ks9nxf2@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'simpleui',  # 后台管理界面美化
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # rest_framework 前后端分离
    "phonenumber_field",  # 手机号码验证
    'cocreate',  # 暂时未使用
    'user',  # 用户模块
    'project',  # 项目模块
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',  # 解决跨域问题
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cocreate_platform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cocreate_platform.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# MySQL数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cocreate_platform',  # 数据库名称
        'USER': 'root',  # 用户名
        'PASSWORD': '1qaz',  # 密码
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'  # 中文

TIME_ZONE = 'Asia/Shanghai'  # 时区

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 离线模式
SIMPLEUI_STATIC_OFFLINE = True
# 隐藏主机信息
SIMPLEUI_HOME_INFO = False

STATIC_URL = '/static/'
# 静态文件的存储目录
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_URL = '/static/media/'
# 存储用户主动上传的文件 用来记录上传文件的位置
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

# STATIC_URL = '/static/'
# MEDIA_URL = 'static/media/'
if DEBUG:
    MEDIA_URL = 'media/'
#
# 去除自动补/ get会帮忙加 post不会
# APPEND_SLASH = False
#
# ALIPAY_KEY_DIRS = os.path.join(BASE_DIR, 'static/key_file/')
# ALIPAY_APP_ID = "2016101700705690"
#
# # 配置富文本编辑器ckeditor
# CKEDITOR_UPLOAD_PATH = 'upload/'
#
# # 只能上传图片
# CKEDITOR_ALLOW_NONIMAGE_FILES = False
# X_FRAME_OPTIONS = 'SAMEORIGIN'
# # ckeditor在后台管理员界面的配置
# CKEDITOR_CONFIGS = {
#     'default': {
#         'toolbar': 'full',  # 工具条功能
#         'height': 500,  # 编辑器高度
#         'width': 1000,  # 编辑器宽
#     },
# }
#
# # 设置simpleUI为离线模式
# SIMPLEUI_STATIC_OFFLINE = True
# # 隐藏项目链接
# SIMPLEUI_HOME_INFO = False
# # 更改模块图标
# SIMPLEUI_ICON = {
#     '技术圈': 'far fa-comments',  # name: 模块名字，请注意不是model的命名，而是菜单栏上显示的文本   icon: 图标
#     '项目分享': 'fas fa-user-tie'
# }
#
# # 发送邮件设置
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 固定写法
# EMAIL_HOST = 'smtp.qq.com'  # 腾讯QQ邮箱 SMTP 服务器地址  'smtp.163.com'
# EMAIL_PORT = 25  # SMTP服务的端口号
# EMAIL_HOST_USER = '2951121599@qq.com'  # 发送邮件的QQ邮箱
# EMAIL_HOST_PASSWORD = 'zxnulqzuaafddebf'  # 在QQ邮箱->设置->帐户->“POP3/IMAP......服务” 里得到的在第三方登录QQ邮箱授权码
# EMAIL_USE_TLS = True  # 与SMTP服务器通信时，是否启动TLS链接(安全链接)默认false  加密True

# 分页允许您控制每页返回多少个对象
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
