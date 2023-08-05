"""
Django settings for cocreate_platform project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
import time
from datetime import timedelta
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
AUTH_USER_MODEL = "user.User"  # 覆盖掉django自带的用户模型

# 定义app
INSTALLED_APPS = [
    'simpleui',  # 后台管理界面美化
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',  # 过滤器
    'rest_framework',  # 前后端分离
    'rest_framework_simplejwt',  # 用户鉴权
    'drf_yasg',  # Swagger
    'drf_api_logger',
    'user',  # 用户模块
    'project',  # 项目模块
    'team',  # 组队模块
    'product',  # 产品模块
    'dim',  # 维度模块
    'feedback',  # 反馈模块
    'function',  # 功能模块
]

# rest_framework 配置
REST_FRAMEWORK = {
    # 分页设置
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12,

    # 配置登录鉴权设置
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],

    # 异常处理
    # 'EXCEPTION_HANDLER': 'common.mixins.my_mixins.custom_exception_handler',

    # 配置限流频率功能
    "DEFAULT_THROTTLE_RATES": {
        "anon": "1/minute"
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # 解决跨域问题
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'drf_api_logger.middleware.api_logger_middleware.APILoggerMiddleware',
]

ROOT_URLCONF = 'cocreate_platform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# MySQL数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cocreate_platform',  # 数据库名称
        'USER': 'root',  # 用户名
        # 'PASSWORD': '1qaz',  # 密码
        'PASSWORD': '123456',  # 密码
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

USE_TZ = False  # USE_TZ=True本地使用的是'Asia/Shanghai'时间，但是写到数据库中的时间会自动转换为UTC时间，读取的时候也会自动转换为本地时间

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 自定义用户认证类进行身份认证登录
# AUTHENTICATION_BACKENDS = [
#
# ]

# JWT配置
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=12),  # Access Token的有效期
    'REFRESH_TOKEN_LIFETIME': timedelta(days=12),  # Refresh Token的有效期

    # 对于大部分情况，设置以上两项就可以了，以下为默认配置项目，可根据需要进行调整

    # 是否自动刷新Refresh Token
    'ROTATE_REFRESH_TOKENS': False,
    # 刷新Refresh Token时是否将旧Token加入黑名单，如果设置为False，则旧的刷新令牌仍然可以用于获取新的访问令牌。需要将'rest_framework_simplejwt.token_blacklist'加入到'INSTALLED_APPS'的配置中
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',  # 加密算法
    'SIGNING_KEY': SECRET_KEY,  # 签名密匙，这里使用Django的SECRET_KEY

    # 如为True，则在每次使用访问令牌进行身份验证时，更新用户最后登录时间
    "UPDATE_LAST_LOGIN": True,
    # 用于验证JWT签名的密钥返回的内容。可以是字符串形式的密钥，也可以是一个字典。
    "VERIFYING_KEY": "",
    "AUDIENCE": None,  # JWT中的"Audience"声明,用于指定该JWT的预期接收者。
    "ISSUER": None,  # JWT中的"Issuer"声明，用于指定该JWT的发行者。
    "JSON_ENCODER": None,  # 用于序列化JWT负载的JSON编码器。默认为Django的JSON编码器。
    "JWK_URL": None,  # 包含公钥的URL，用于验证JWT签名。
    "LEEWAY": 0,  # 允许的时钟偏差量，以秒为单位。用于在验证JWT的过期时间和生效时间时考虑时钟偏差。

    # 用于指定JWT在HTTP请求头中使用的身份验证方案。默认为"Bearer"
    "AUTH_HEADER_TYPES": ("Bearer",),
    # 包含JWT的HTTP请求头的名称。默认为"HTTP_AUTHORIZATION"
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    # 用户模型中用作用户ID的字段。默认为"id"。
    "USER_ID_FIELD": "id",
    # JWT负载中包含用户ID的声明。默认为"user_id"。
    "USER_ID_CLAIM": "user_id",

    # 用于指定用户身份验证规则的函数或方法。默认使用Django的默认身份验证方法进行身份验证。
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    #  用于指定可以使用的令牌类。默认为"rest_framework_simplejwt.tokens.AccessToken"。
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    # JWT负载中包含令牌类型的声明。默认为"token_type"。
    "TOKEN_TYPE_CLAIM": "token_type",
    # 用于指定可以使用的用户模型类。默认为"rest_framework_simplejwt.models.TokenUser"。
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    # JWT负载中包含JWT ID的声明。默认为"jti"。
    "JTI_CLAIM": "jti",

    # 在使用滑动令牌时，JWT负载中包含刷新令牌过期时间的声明。默认为"refresh_exp"。
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    # 滑动令牌的生命周期。默认为5分钟。
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    # 滑动令牌可以用于刷新的时间段。默认为1天。
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    # 用于生成访问令牌和刷新令牌的序列化器。
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    # 用于刷新访问令牌的序列化器。默认
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    # 用于验证令牌的序列化器。
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    # 用于列出或撤销已失效JWT的序列化器。
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    # 用于生成滑动令牌的序列化器。
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    # 用于刷新滑动令牌的序列化器。
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

# 日志系统中的 mail_admins
ADMINS = [
    ('plutos', 'plutos@aliyun.com'),
    ('Mary', 'mary@example.com'),
]

BASE_LOG_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(BASE_LOG_DIR):
    # 检查日志文件
    os.mkdir(BASE_LOG_DIR)

LOGGING = {
    'version': 1,  # 保留字
    'disable_existing_loggers': False,  # 禁用已经存在的logger实例
    # 日志文件的格式
    'formatters': {
        # 详细的日志格式
        'standard': {
            # 'format': '[%(levelname)s] [%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s] (%(filename)s:%(lineno)d), %(module)s::%(funcName)s [%(message)s]'
            'format': '[%(levelname)s] [%(asctime)s][%(thread)d][%(name)s] %(funcName)s: %(message)s'

        },
        # 简单的日志格式
        'simple': {
            'format': '[%(levelname)s] [%(asctime)s] %(message)s'
        },
        # 定义一个特殊的日志格式
        'collect': {
            'format': '%(message)s'
        }
    },
    # 过滤器
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # 处理器
    'handlers': {
        # 在终端打印
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],  # 只有在Django debug为True时才在屏幕打印日志
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        # 默认的
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, 'info_' + time.strftime("%Y-%m-%d", time.localtime()) + '.log'),
            # # 日志文件
            # 'maxBytes': 1024 * 1024 * 50 * 1024,  # 5G大小
            'when': 'D',
            'backupCount': 30,  # 最多备份几个
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        # 专门用来记错误日志
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, 'error_' + time.strftime("%Y-%m-%d", time.localtime()) + '.log'),
            # # 日志文件
            # 'maxBytes': 1024 * 1024 * 50 * 1024,  # 5G大小
            'when': 'D',
            'backupCount': 30,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        # 专门定义一个收集特定信息的日志
        'collect': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, 'collect_' + time.strftime("%Y-%m-%d", time.localtime()) + '.log'),
            # 'maxBytes': 1024 * 1024 * 50 * 1024,  # 5G大小
            'when': 'D',
            'backupCount': 30,  # 最多备份几个
            'formatter': 'collect',
            'encoding': "utf-8"
        }
    },
    'loggers': {
        # 默认的logger应用如下配置
        '': {
            'handlers': ['default', 'console', 'error'],  # 上线之后可以把'console'移除
            'level': 'DEBUG',
            'propagate': True,  # 向不向更高级别的logger传递
        },
        # 名为 'collect'的logger还单独处理
        'drf_api_logger': {
            'handlers': ['default', 'console', 'error'],
            'level': 'DEBUG',
        }
    },
}

# DRF_API_LOGGER_DATABASE = True  # 存储到数据库
DRF_API_LOGGER_SIGNAL = True  # Listen to the signal as soon as any API is called. So you can log the API data into a file or for different use-cases.
DRF_LOGGER_QUEUE_MAX_SIZE = 50  # 多少条日志写入 Default to 50 if not specified.
DRF_LOGGER_INTERVAL = 10  # 间隔多久写入 In Seconds, Default to 10 seconds if not specified.
DRF_API_LOGGER_SKIP_NAMESPACE = []  # 指定app不写入
DRF_API_LOGGER_SKIP_URL_NAME = []  # 指定url不写入
DRF_API_LOGGER_DEFAULT_DATABASE = 'default'  # 指定数据库 如果未指定，默认为“default”确保迁移 DRF_API_LOGGER_DEFAULT_DATABASE 中指定的数据库。
DRF_API_LOGGER_PATH_TYPE = 'ABSOLUTE'  # 完整路径
DRF_API_LOGGER_SLOW_API_ABOVE = 200  # 额外标识超过200ms的请求 默认为无
DRF_API_LOGGER_EXCLUDE_KEYS = []  # 敏感数据将被替换为“***FILTERED***”。

# ----- SIMPLEUI -----
# 离线模式
SIMPLEUI_STATIC_OFFLINE = True
# 隐藏项目链接
SIMPLEUI_HOME_INFO = False

# ----- STATIC -----
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'
# 静态文件的存储目录
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# 存储用户主动上传的文件 用来记录上传文件的位置
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

if DEBUG:
    MEDIA_URL = 'media/'
else:
    MEDIA_URL = '/static/media/'

# 去除自动补/ get会帮忙加 post不会
# APPEND_SLASH = False

# ----- ckeditor -----
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


#
# # 发送邮件设置
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 固定写法
# EMAIL_HOST = 'smtp.qq.com'  # 腾讯QQ邮箱 SMTP 服务器地址  'smtp.163.com'
# EMAIL_PORT = 25  # SMTP服务的端口号
# EMAIL_HOST_USER = '2951121599@qq.com'  # 发送邮件的QQ邮箱
# EMAIL_HOST_PASSWORD = 'zxnulqzuaafddebf'  # 在QQ邮箱->设置->帐户->“POP3/IMAP......服务” 里得到的在第三方登录QQ邮箱授权码
# EMAIL_USE_TLS = True  # 与SMTP服务器通信时，是否启动TLS链接(安全链接)默认false  加密True
