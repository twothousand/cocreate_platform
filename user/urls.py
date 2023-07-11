"""
user路由
- 登录
- 退出登录
- 忘记密码
- 管理的项目
- 参与的项目
- 管理的项目的详细信息
"""
# django 模块
from django.urls import path, include
# rest_framework 模块
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
# app
from user import views

# 自动生成路由方法, 必须使用视图集
# router = SimpleRouter()  # 没有根路由  /user/ 无法识别
# router = DefaultRouter()  # 1.有根路由
# router.register(r'', views.UserViewSet, 'user')  # 2.配置路由

urlpatterns = [
    # http://127.0.0.1:8000/api/users/
    # path("", include(router.urls)),
    # http://127.0.0.1:8000/api/users/login/
    path('login/', views.LoginView.as_view()),  # 登录
    # http://127.0.0.1:8000/api/users/logout/
    path('logout/', views.LogoutView.as_view()),  # 退出登录
    # http://127.0.0.1:8000/api/users/forgot_password/
    path('forgot_password/', views.ForgetPwdView.as_view()),  # 忘记密码
    # http://127.0.0.1:8000/api/users/refresh_token/
    path('refresh_token/', TokenRefreshView.as_view()),  # 刷新Token
    # http://127.0.0.1:8000/api/users/verify_token/
    path('verify_token/', TokenVerifyView.as_view()),  # 校验Token
    # http://127.0.0.1:8000/api/users/{id}/
    path('<str:pk>/', views.UserView.as_view({"get": "retrieve"})),  # 获取单个用户信息
    # http://127.0.0.1:8000/api/users/1/managed_projects/
    path('<str:pk>/managed_projects/', views.UserManagedProjectsView.as_view()),  # 管理的项目
    # http://127.0.0.1:8000/api/users/2/managed_projects/1  # 获取特定用户管理的特定项目的详细信息
    path('<str:pk>/managed_projects/<int:project_id>', views.UserManagedProjectDetailView.as_view()),
    # http://127.0.0.1:8000/api/users/1/joined_projects/
    path('<str:pk>/joined_projects/', views.UserJoinedProjectsView.as_view()),  # 参与的项目
    # http://127.0.0.1:8000/api/users/2/joined_projects/1  # 获取特定用户参与的特定项目的详细信息
    path('<str:pk>/joined_projects/<int:project_id>', views.UserJoinedProjectDetailView.as_view()),
]
# urlpatterns += router.urls
