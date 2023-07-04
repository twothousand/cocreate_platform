from django.urls import path, include
from rest_framework.routers import DefaultRouter
from project.views import ProjectViewSet, ProjectMembersView

router = DefaultRouter()  # 可以处理视图的路由器
router.register('', ProjectViewSet, 'project')  # 向路由器中注册视图集

urlpatterns = [
    # http://127.0.0.1:8000/api/projects/
    path("", include(router.urls)),
    # /api/projects/?search=关键词
    path("search/<str:keyword>/", ProjectViewSet.as_view({"get": "search"}), name="project-search"),
    # http://127.0.0.1:8000/api/projects/1/members/
    path('<int:project_id>/members/', ProjectMembersView.as_view()),  # 项目成员
]
urlpatterns += router.urls  # 将路由器中的所以路由信息追到到django的路由列表中
