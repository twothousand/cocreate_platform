from django.urls import path, re_path
from user import views
from project.views import ProjectViewSet, ProjectTypeView
from rest_framework.routers import DefaultRouter

# app_name = 'project'
# urlpatterns = [
#     # http://127.0.0.1:8000/project/
#     path('', ProjectViewSet.as_view(actions={'get': 'list', 'post': 'create'})),  # 全部数据
#     # http://127.0.0.1:8000/project/1/
#     re_path(r'(\d+)/', ProjectViewSet.as_view(actions={'get': 'list', 'post': 'create'})),  # 单条数据
# ]


urlpatterns = []

router = DefaultRouter()  # 可以处理视图的路由器
router.register('', ProjectViewSet, basename='project')  # 向路由器中注册视图集
# router.register(r'type/(?P<project_type>\w+)/', ProjectTypeView, basename='project-type-search')

# router.register('type', ProjectTypeView, basename='project_type')
# 按照项目类型搜索项目，参数为项目类型
# router.register('type/', ProjectTypeView)


urlpatterns += router.urls  # 将路由器中的所以路由信息追到到django的路由列表中
