from django.urls import path, include
from rest_framework.routers import DefaultRouter
from team.views import TeamViewSet, TeamRecruitmentView, TeamApplicationView, TeamMemberViewSet

# 创建一个路由器并注册TeamViewSet和TeamMemberViewSet
router = DefaultRouter()
router.register('team', TeamViewSet, 'team')  # 注册TeamViewSet

urlpatterns = [
    # 将router.urls添加到urlpatterns中
    path('', include(router.urls)),

    # http://127.0.0.1:8000/api/team/recruitment/
    path('recruitment/', TeamRecruitmentView.as_view(), name='team_recruitment'),

    # 不带id参数的情况,创建申请表单
    path('application/', TeamApplicationView.as_view({'post': 'create'}), name='team_application_create'),

    # 带有id参数的情况，修改申请表单
    path('application/<str:id>/', TeamApplicationView.as_view({'put': 'update'}), name='team_application_update'),

    # 队伍管理：转让队长
    path('transfer_leadership/', TeamMemberViewSet.as_view({'put': 'transfer_leadership'}), name='transfer_leadership'),

    # 队伍管理：移除队员
    path('remove_member/', TeamMemberViewSet.as_view({'put': 'remove_member'}), name='remove_member'),

    # 队伍管理：自动退出
    path('auto_exit/', TeamMemberViewSet.as_view({'put': 'auto_exit'}), name='auto_exit'),

    # 队伍管理：添加队员
    path('add_member/', TeamMemberViewSet.as_view({'post': 'add_member'}), name='add_member'),
]
