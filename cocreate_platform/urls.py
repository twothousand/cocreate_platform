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
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls  # 自动生成API文档

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('user.urls')),

    # http://127.0.0.1:8000/api/users/xxx
    path('api/users/', include('user.urls'), name='user'),

    # http://127.0.0.1:8000/api/projects/xxx
    path('api/projects/', include('project.urls'), name='project'),

    # http://127.0.0.1:8000/docs/
    path('docs/', include_docs_urls(title='CoCreate API 文档', description='CoCreate API 文档')),  # 自动生成API文档

    # # http://127.0.1:8000/schema/
    # path('schema/', schema_view),  # 自动生成API文档

    # http://127.0.0.1:8000/
    # re_path(r'^', include('cocreate.urls')),

    # path('index/', views.index, name='main-view'),
    # path('bio/<username>/', views.bio, name='bio'),
]
# urlpatterns += router.urls
