# django库
from django.urls import path, include
# rest_framework库
from rest_framework.routers import DefaultRouter
# app
from user.views import *

# 自动生成路由方法, 必须使用视图集
# router = SimpleRouter()  # 没有根路由  /user/ 无法识别
router = DefaultRouter()  # 1.有根路由
router.register(r'', UserViewSet, 'user')  # 2.配置路由
# router.register(r"userReg", UserRegViewSet, 'userReg')  # POST请求即为注册，无需配置路由

urlpatterns = [
    path("", include(router.urls)),
    # http://127.0.0.1:8000/api/users/login/
    path('login/', LoginView.as_view()),
    # http://127.0.0.1:8000/api/users/forgot_password/
    path('forgot_password/', ForgetPwdView.as_view()),
    # http://127.0.0.1:8000/api/users/1/projects/
    path('<int:user_id>/projects/', UserProjectsView.as_view()),
    # http://127.0.0.1:8000/api/users/1/managed_projects/
    path('<int:user_id>/managed_projects/', UserManagedProjectsView.as_view()),  # 管理的项目
    # http://127.0.0.1:8000/api/users/1/joined_projects/
    path('<int:user_id>/joined_projects/', UserJoinedProjectsView.as_view()),  # 参与的项目
]
urlpatterns += router.urls

# app_name = 'user'
# urlpatterns = [
#     # re_path(r'^$', views.user, name='user'),
#     # path('user', views.user, name='user'),
#     path('', views.test_index, name='user'),
#     path('login/', LoginView.as_view()),
#     # url(r'^collection/$', views.collection, name='collection'),
#     # url(r'^user_change/$', views.user_change, name='user_change'),
#     # url(r'^register/$', views.register, name='register'),
#     # url(r'^register_handle/$', views.register_handle, name='register_handle'),
#     # url(r'^login/$', views.login, name='login'),
#     # url(r'^login_check/$', views.login_check, name='login_check'),
#     # url(r'^logout/$', views.logout, name='logout'),
#     # url(r'^my_publish/$', views.my_publish, name='my_publish'),
#     # url(r'^my_develop/$', views.my_develop, name='my_develop'),
#     # url(r'^my_jingbiao/$', views.my_jingbiao, name='my_jingbiao'),
# ]
