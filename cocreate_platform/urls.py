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

urlpatterns = [
    path('admin/', admin.site.urls),

    # http://127.0.0.1:8000/user/xxx
    path('user/', include('user.urls'), name='user'),

    # http://127.0.0.1:8000/project/xxx
    path('project/', include('project.urls'), name='project'),





    # http://127.0.0.1:8000/
    # re_path(r'^', include('cocreate.urls')),

    # path('index/', views.index, name='main-view'),
    # path('bio/<username>/', views.bio, name='bio'),
]
