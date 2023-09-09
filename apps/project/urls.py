from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.project.views import ProjectViewSet, ProjectFilterAndSearchView, ProjectMembersView, ProjectTeamMembersView

router = DefaultRouter()  # 可以处理视图的路由器
router.register('', ProjectViewSet, 'project')  # 向路由器中注册视图集

urlpatterns = [
    # http://127.0.0.1:8000/api/projects/
    path("", include(router.urls)),
    # http://127.0.0.1:8000/api/projects/filter-search?ai_tag=AI%E5%8C%BB%E7%96%97&project_status=%E5%B7%B2%E5%AE%8C%E6%88%90
    path('filter-search', ProjectFilterAndSearchView.as_view({'get': 'search_filter_projects'}), name='project-filter-and-search'),
    # http://127.0.0.1:8000/api/projects/862c583f-511e-4e6a-8f8d-05128dabbc0d/members/
    path('<str:project_id>/members/', ProjectMembersView.as_view(), name='project-members'),
    # http://127.0.0.1:8000/api/projects/862c583f-511e-4e6a-8f8d-05128dabbc0d/members/
    path('<str:project_id>/team-members/', ProjectTeamMembersView.as_view(), name='project-members'),
]
urlpatterns += router.urls
