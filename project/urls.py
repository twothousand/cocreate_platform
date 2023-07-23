from django.urls import path, include
from rest_framework.routers import DefaultRouter
from project.views import ProjectViewSet, ProjectSearchView, ProjectFilterView

router = DefaultRouter()  # 可以处理视图的路由器
router.register('', ProjectViewSet, 'project')  # 向路由器中注册视图集

urlpatterns = [
    # http://127.0.0.1:8000/api/projects/
    path("", include(router.urls)),
    # http://127.0.0.1:8000/api/projects/search?keyword=AI
    path("search", ProjectSearchView.as_view(), name='project-search'),
    # http://127.0.0.1:8000/api/projects/filter?ai_tag=AI%E5%8C%BB%E7%96%97&project_status=%E5%B7%B2%E5%AE%8C%E6%88%90
    path('filter', ProjectFilterView.as_view(), name='project-filter'),
]
urlpatterns += router.urls  # 将路由器中的所以路由信息追到到django的路由列表中
