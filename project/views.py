# django库
from django.conf import settings
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
# rest_framework库
from rest_framework import filters, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
# app
from .models import Project
from .serializers import ProjectSerializer, ProjectMembersSerializer
from team.models import Member


# 项目视图集
class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    search_fields = ['project_name', 'project_description']
    ordering = ['-id']

    # 重写list方法，返回项目列表
    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            response_data = {
                'message': '获取项目列表成功！',
                'data': response.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                'message': '获取项目列表失败！！！',
                'data': str(e)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    # 重写create方法，创建项目 TODO：(1048, "Column 'project_creator_id' cannot be null")
    def create(self, request, *args, **kwargs):
        try:
            # 设置项目创建者ID为当前登录用户的ID
            request.data['project_creator_id'] = request.user.id
            response = super().create(request, *args, **kwargs)
            response_data = {
                'message': '创建项目成功！',
                'data': response.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            response_data = {
                'message': '创建项目失败！！！',
                'data': str(e)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    # 重写retrieve方法，获取项目详细信息
    def retrieve(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request, *args, **kwargs)
            response_data = {
                'message': '获取项目详细信息成功！',
                'data': response.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                'message': '获取项目详细信息失败！！！',
                'data': str(e)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    # 重写partial_update方法，更新项目信息
    def partial_update(self, request, *args, **kwargs):
        try:
            response = super().partial_update(request, *args, **kwargs)
            response_data = {
                'message': '更新项目信息成功！',
                'data': response.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                'message': '更新项目信息失败！！！',
                'data': str(e)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    # 重写destroy方法，删除项目
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            response_data = {
                'message': '删除项目成功！',
                'data': None
            }
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            response_data = {
                'message': '删除项目失败！！！',
                'data': str(e)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    # 获取项目成员列表
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        try:
            project = self.get_object()
            members = Member.objects.filter(team__project_id=project.id, member_status='正常')
            serializer = ProjectMembersSerializer(members, many=True)
            response_data = {
                'message': '获取项目成员列表成功！',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                'message': '获取项目成员列表失败！！！',
                'data': str(e)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


# 按关键词搜索项目
class ProjectSearchView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            keyword = self.request.GET.get('keyword')
            if keyword:
                queryset = Project.objects.filter(project_name__icontains=keyword) | \
                           Project.objects.filter(project_description__icontains=keyword)
                queryset = queryset.order_by('-id')
                serializer = ProjectSerializer(queryset, many=True)
                # 检查序列化的数据是否为空
                if serializer.data:
                    response_data = {
                        'message': '已成功检索到项目！',
                        'data': serializer.data
                    }
                else:
                    response_data = {
                        'message': '未检索到任何符合的项目！',
                        'data': serializer.data
                    }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    'message': '未提供搜索关键词！！！',
                    'data': []
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response_data = {
                'message': str(e),
                'data': []
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 按参数过滤项目
class ProjectFilterView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            industry = self.request.GET.get('industry')
            ai_tag = self.request.GET.get('ai_tag')
            project_type = self.request.GET.get('project_type')
            project_status = self.request.GET.get('project_status')
            model_name = self.request.GET.get('model_name')

            filter_conditions = Q()

            if project_status:
                filter_conditions &= Q(project_status__icontains=project_status)
            if project_type:
                filter_conditions &= Q(project_type__icontains=project_type)
            if model_name:
                filter_conditions &= Q(model__model_name__icontains=model_name)
            if industry:
                filter_conditions &= Q(industry__industry__icontains=industry)
            if ai_tag:
                filter_conditions &= Q(ai_tag__ai_tag__icontains=ai_tag)

            queryset = Project.objects.filter(filter_conditions).order_by('-id')
            serializer = ProjectSerializer(queryset, many=True)

            if serializer.data:
                response_data = {
                    'message': '已成功检索到项目！',
                    'data': serializer.data
                }
            else:
                response_data = {
                    'message': '未检索到任何符合的项目！',
                    'data': serializer.data
                }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                'message': str(e),
                'data': []
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 查看特定项目的成员列表
class ProjectMembersView(APIView):
    def get(self, request, project_id):
        try:
            # 获取指定项目的成员列表
            # members = Member.objects.filter(team__project_id=project_id, member_status='正常', is_leader=False)  # 不包含队长
            members = Member.objects.filter(team__project_id=project_id, member_status='正常')  # 包含队长

            # 序列化成员列表数据
            serializer = ProjectMembersSerializer(members, many=True)

            return Response(serializer.data)
        except Member.DoesNotExist:
            return Response(status=404)
