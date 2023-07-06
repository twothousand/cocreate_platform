from django.urls import path, include
from rest_framework.routers import DefaultRouter
from project.views import ProjectViewSet, ProjectMembersView, ProjectSearchView, ProjectFilterView

router = DefaultRouter()  # 可以处理视图的路由器
router.register('', ProjectViewSet, 'project')  # 向路由器中注册视图集

urlpatterns = [
    # http://127.0.0.1:8000/api/projects/
    path("", include(router.urls)),
    # http://127.0.0.1:8000/api/projects/?search=keyword
    path("search/<str:keyword>/", ProjectSearchView.as_view(), name="project-search"),
    # http://127.0.0.1:8000/api/projects?project_tags=AI%E5%85%B6%E4%BB%96
    # path("", ProjectFilterView.as_view(), name="project-filter"),  # TODO 未实现
    # http://127.0.0.1:8000/api/projects/1/members/
    path('<int:project_id>/members/', ProjectMembersView.as_view()),  # 查看项目成员

]
urlpatterns += router.urls  # 将路由器中的所以路由信息追到到django的路由列表中
