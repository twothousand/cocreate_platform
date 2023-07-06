"""
user路由
- 登录
- 退出登录
- 忘记密码
- 管理的项目
- 参与的项目
- 管理的项目的详细信息
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import *

# 自动生成路由方法, 必须使用视图集
# router = SimpleRouter()  # 没有根路由  /user/ 无法识别
router = DefaultRouter()  # 1.有根路由
router.register(r'', UserViewSet, 'user')  # 2.配置路由

urlpatterns = [
    # http://127.0.0.1:8000/api/users/
    # path("", include(router.urls)),
    # http://127.0.0.1:8000/api/users/login/
    path('login/', LoginView.as_view()),  # 登录
    # http://127.0.0.1:8000/api/users/logout/
    path('logout/', LogoutView.as_view()),  # 退出登录
    # http://127.0.0.1:8000/api/users/forgot_password/
    path('forgot_password/', ForgetPwdView.as_view()),  # 忘记密码
    # http://127.0.0.1:8000/api/users/1/managed_projects/
    path('<int:user_id>/managed_projects/', UserManagedProjectsView.as_view()),  # 管理的项目
    # http://127.0.0.1:8000/api/users/2/managed_projects/1  # 获取特定用户管理的特定项目的详细信息
    path('<int:user_id>/managed_projects/<int:project_id>', UserManagedProjectDetailView.as_view()),
    # http://127.0.0.1:8000/api/users/1/joined_projects/
    path('<int:user_id>/joined_projects/', UserJoinedProjectsView.as_view()),  # 参与的项目
    # http://127.0.0.1:8000/api/users/2/joined_projects/1  # 获取特定用户参与的特定项目的详细信息
    path('<int:user_id>/joined_projects/<int:project_id>', UserJoinedProjectDetailView.as_view()),

]
urlpatterns += router.urls
