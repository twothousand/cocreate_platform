from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views import View
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from project.models import Project
from project.serializers import ProjectSerializer
from user.serializers import UserSerializer
from .models import User


# 用于列出或检索用户的视图集
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer  # 优先使用 get_serializer_class 返回的序列化器
    permission_classes = [IsAuthenticated]

    # # 根据不同的请求, 获得不同的序列化器
    # def get_serializer_class(self):
    #     if self.action == 'unactived':
    #         return UserUnActiveSerializer
    #     else:
    #         return UserSerializer
    #
    # @action(methods=['get'], detail=False)
    # def unactived(self, request, *args, **kwargs):
    #     # 获取查询集, 过滤出未激活的用户
    #     qs = self.queryset.filter(is_active=False)
    #     # 使用序列化器, 序列化查询集, 并且是
    #     ser = self.get_serializer(qs, many=True)
    #     return Response(ser.data)
    #
    # @action(methods=['get'], detail=False)
    # def actived(self, request, *args, **kwargs):
    #     # 获取查询集, 过滤出未激活的用户
    #     qs = self.queryset.filter(is_active=True)
    #     # 使用序列化器, 序列化查询集, 并且是
    #     ser = self.get_serializer(qs, many=True)
    #     return Response(ser.data)

    # def perform_create(self, serializer):
    #     serializer.save()

    # def list(self, request):
    #     queryset = User.objects.all()
    #     serializer = UserSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, pk=None):
    #     queryset = User.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)


# 获取特定用户的所有项目（project_creator有问题）
class UserProjectsView(APIView):
    def get(self, request, user_id):
        projects = Project.objects.filter(project_creator=user_id)  # 根据用户ID过滤项目
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


#
class LoginView(View):
    def get(self, request):
        return HttpResponse("LoginView GET")

    def post(self, request):
        return HttpResponse("LoginView POST")
        # # 接收数据
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # remember = request.POST.get('remember')
        #
        # # 校验数据
        # if not all([username, password, remember]):
        #     return JsonResponse({'res': 2})
        #
        # # 业务处理：登录校验
        # passport = User.objects.get_one_passport(username=username, password=password)
        # if passport:
        #     next_url = reverse('cocreate:index')
        #     jres = JsonResponse({'res': 1, 'next_url': next_url})
        #
        #     # 判断是否需要记住用户名
        #     if remember == 'true':
        #         # 记住用户名
        #         jres.set_cookie('username', username, max_age=7 * 24 * 3600)
        #     else:
        #         # 不要记住用户名
        #         jres.delete_cookie('username')
        #
        #     # 记住用户的登录状态
        #     request.session['islogin'] = True
        #     request.session['username'] = username
        #     request.session['passport_id'] = passport.id
        #     return jres
        # else:
        #     # 用户名或密码错误
        #     return JsonResponse({'res': 0})


# 以rest_framework，查询个人信息


class UserInfoView(APIView):
    def get(self, request, format=None):
        user = User.objects.get(user=request.user)
        serializer = UserSerializer(user)
        return Response(serializer.data)


# 以rest_framework，修改个人信息
class UserUpdateView(APIView):
    def post(self, request, format=None):
        user = User.objects.get(user=request.user)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
