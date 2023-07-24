from django.urls import path, include
from rest_framework.routers import DefaultRouter
from team.views import  TeamRecruitmentView, TeamApplicationView, TeamMemberViewSet

# 创建一个路由器并注册TeamViewSet和TeamMemberViewSet
router = DefaultRouter()


urlpatterns = [
    # 将router.urls添加到urlpatterns中
    path('', include(router.urls)),

    # http://127.0.0.1:8000/api/team/recruitment/
    path('recruitment/', TeamRecruitmentView.as_view(), name='team_recruitment'),

    # 创建申请表单
    path('create_application/', TeamApplicationView.as_view({'post': 'create_application'}), name='team_application_create'),

    # 处理申请：同意加入/拒绝
    path('application_update/', TeamApplicationView.as_view({'put': 'application_update'}), name='team_application_update'),

    # 获取待处理状态的申请消息
    path('get_pending_applications/', TeamApplicationView.as_view({'get': 'get_pending_applications'}), name='get_pending_applications'),

    # 队伍管理：转让队长
    path('transfer_leadership/', TeamMemberViewSet.as_view({'put': 'transfer_leadership'}), name='transfer_leadership'),

    # 队伍管理：移除队员
    path('remove_member/', TeamMemberViewSet.as_view({'put': 'remove_member'}), name='remove_member'),

    # 队伍管理：自动退出
    path('auto_exit/', TeamMemberViewSet.as_view({'put': 'auto_exit'}), name='auto_exit'),

    # 队伍管理：添加队员
    path('add_member/', TeamMemberViewSet.as_view({'post': 'add_member'}), name='add_member'),

    # 队伍管理：查询队员信息
    path('get_all_members/', TeamMemberViewSet.as_view({'get': 'get_all_members'}), name='get_all_members'),
]
