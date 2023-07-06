"""cocreate_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# django库
from django.contrib import admin
from django.urls import path, include
# drf_yasg库
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# 配置Swagger文档视图
schema_view = get_schema_view(
    openapi.Info(
        title="CoCreate Platform API 文档",
        default_version='v1',
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('user.urls')),

    # http://127.0.0.1:8000/
    # path('', include('project.urls'), name='project'),

    # http://127.0.0.1:8000/api/users/xxx
    path('api/users/', include('user.urls'), name='user'),

    # http://127.0.0.1:8000/api/projects/xxx
    path('api/projects/', include('project.urls'), name='project'),

    # http://127.0.0.1:8000/api/teams/xxx
    path('api/teams/', include('team.urls'), name='team'),

    # http://127.0.0.1:8000/swagger/   swagger API 文档
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # http://127.0.0.1:8000/redoc/  使用Redoc UI来显示API文档
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
