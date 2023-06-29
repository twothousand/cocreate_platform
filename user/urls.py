from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import UserViewSet, UserProjectsView

# 自动生成路由方法, 必须使用视图集
# router = SimpleRouter()  # 没有根路由  /user/ 无法识别
router = DefaultRouter()  # 1.有根路由
router.register(r'', UserViewSet, 'user')  # 2.配置路由

urlpatterns = [
    path("", include(router.urls)),
    # path('forgot-password/', LoginView.as_view()),
    # http://127.0.0.1:8000/api/users/1/projects/
    path('<int:user_id>/projects/', UserProjectsView.as_view()),
    path('user-info/', UserProjectsView.as_view(), name='user-info')
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
