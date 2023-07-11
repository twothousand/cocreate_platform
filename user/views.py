# 系统模块
import random
import re
import time
# django模块
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import get_user_model
# rest_framework模块
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
# common
from common.aliyun_message import AliyunSMS
from common import Constant
# functions
from functions import TimeUtils
# app
from project.models import Project
from project.serializers import UserManagedProjectsSerializer, UserJoinedProjectsSerializer, ProjectSerializer
from user.serializers import UserSerializer
from user.permissions import IsOwnerOrReadOnly
from user.models import VerifCode
from team.models import Team, Member

User = get_user_model()


def check_verif_code(mobile_phone: str, code_id: int, verification_code: str) -> (bool, dict):
    """
    校验验证码
    @param mobile_phone: 手机号码
    @param code_id: 验证码id
    @param verification_code: 验证码
    @return: 如果验证码有效，返回True，否则返回False
    """
    result = {}
    if VerifCode.objects.filter(id=code_id, verif_code=verification_code, mobile_phone=mobile_phone).exists():  # 验证码存在
        obj = VerifCode.objects.get(id=code_id)
        if obj.is_used:
            result["error"] = "验证码已被使用，请重新获取验证码"
            return False, result
        if not TimeUtils.is_within_valid_period(obj.created_at, valid_period=Constant.CAPTCHA_TIMEOUT):
            result["error"] = "验证码已过期，请重新获取验证码"
            return False, result
        obj.is_used = True  # 设置为被使用过了
        obj.save()
    else:
        result["error"] = "验证码验证失败，请重新获取验证码"
        return False, result
    return True, result


class RegisterView(APIView):
    def post(self, request):
        """
        用户注册接口
        @param request:
        @return:
        """
        result = {}
        # 接收用户参数
        username = request.data.get("username")
        password = request.data.get("password")
        password_confirmation = request.data.get("password_confirmation")
        verification_code = request.data.get("verification_code")
        code_id = int(request.data.get("code_id"))

        # 参数校验
        if not username:
            result["error"] = "手机号码不能为空"
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not password:
            result["error"] = "密码不能为空"
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not password_confirmation:
            result["error"] = "确认密码不能为空"
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not verification_code:
            result["error"] = "验证码不能为空"
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not code_id:
            result["error"] = "验证码ID不能为空"
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if User.objects.filter(username=username).exists():
            result["error"] = "该手机号已注册"
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if password != password_confirmation:
            result["error"] = "两次密码不一致"
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # TODO: 是否需要校验密码复杂度
        if not (6 <= len(password) <= 18):
            result["error"] = "密码长度需要在6到18位之间"
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 验证码校验
        res, result = check_verif_code(mobile_phone=username, code_id=code_id, verification_code=verification_code)
        if not res:
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # 创建用户
        # TODO: 其他默认字段设置
        obj = User.objects.create_user(username=username, password=password)
        if obj:
            result["message"] = "用户创建成功"
            result.update({
                "id": obj.id,
                "username": obj.username
            })
            return Response(result, status=status.HTTP_201_CREATED)
        else:
            result["error"] = "用户创建失败"
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 登录
class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        # 自定义登录成功返回的结果
        result = serializer.validated_data
        # result["token"] = result.pop("access")
        # TODO 看前端需要什么字段
        result["id"] = serializer.user.id
        result["username"] = serializer.user.username

        return Response(result, status=status.HTTP_200_OK)


# 退出登录
class LogoutView(View):
    def get(self, request):
        return HttpResponse("LogoutView GET")

    def post(self, request):
        return HttpResponse("LogoutView POST")


class UserView(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer  # 优先使用 get_serializer_class 返回的序列化器
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def upload_avatar(self, request, *args, **kwargs):
        """
        上传用户头像接口
        @param request:
        @param args:
        @param kwargs:
        @return:
        """
        # TODO: 使用云存储，可扩展性高
        pass

    def update_password(self, request, *args, **kwargs):
        """
        修改密码
        @param request:
        @param args:
        @param kwargs:
        @return:
        """
        result = {}
        user = self.get_object()
        # 接收用户参数
        username = request.data.get("username")
        verification_code = request.data.get("verification_code")
        password = request.data.get("password")
        password_confirmation = request.data.get("password_confirmation")
        code_id = request.data.get("code_id")
        # 参数校验
        if not all([username, password, password_confirmation, verification_code, code_id]):
            result["error"] = "参数不能为空"
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if password != password_confirmation:
            result["error"] = "两次密码不一致"
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if username != user.username:
            result["error"] = "该手机号与绑定手机号不一致"
        # 验证码校验
        res, result = check_verif_code(mobile_phone=username, code_id=code_id, verification_code=verification_code)
        if not res:
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # 修改密码
        user.set_password(password)
        user.save()
        result["message"] = "密码修改成功！"
        return Response(result, status=status.HTTP_200_OK)


class SendSMSView(APIView):
    def post(self, request):
        result = {}
        # 获取手机号码
        phone = request.data.get("phone", "")
        # 手机号码校验
        res = re.match(r"^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$", phone)
        if not res:
            result["error"] = "无效的手机号码"
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # 随机生成六位数验证码
        code = self.get_random_code()
        # 发送短信验证码
        aliyun_sms = AliyunSMS()
        res = aliyun_sms.send_msg(phone=phone, code=code)
        if res["code"] == "OK":
            obj = VerifCode.objects.create(mobile_phone=phone, verif_code=code)
            res["code_id"] = obj.id
            return Response(res, status=status.HTTP_200_OK)
        else:
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

    def get_random_code(self):
        """
        随机生成六位数验证码
        @return:
        """
        code = "".join([str(random.choice(range(10))) for _ in range(6)])
        return code


# 用于列出或检索用户的视图集
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer  # 优先使用 get_serializer_class 返回的序列化器
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        重写get_permissions，实例化并返回此视图需要的权限列表。
        @return: # 返回相应的权限列表
        """
        if self.action == 'create':  # 如果操作是 'create' （对应POST请求，即注册）
            permission_classes = [AllowAny]  # 允许任何人，不需要身份验证
        else:  # 其他操作
            permission_classes = [IsAuthenticated]  # 需要用户被认证
        return [permission() for permission in permission_classes]

    # TODO 用户注册接口重写
    def create(self, request, *args, **kwargs):
        """
        重写用户注册接口
        @param request:
        @param args:
        @param kwargs:
        @return:
        """
        result = {}
        # 接收用户参数
        username = request.data.get("username")
        password = request.data.get("password")
        password_confirmation = request.data.get("password_confirmation")
        verification_code = request.data.get("verification_code")

        # 参数校验
        if not all([username, password, password_confirmation, verification_code]):
            result["error"] = "参数不能为空"
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if User.objects.filter(username=username).exists():
            result["error"] = "该手机号已注册"
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if password != password_confirmation:
            result["error"] = "两次密码不一致"
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # TODO: 是否需要校验密码复杂度
        if not (6 <= len(password) <= 18):
            result["error"] = "密码长度需要在6到18位之间"
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # TODO: 缺少手机验证码检验

        # 创建用户
        # TODO: 其他默认字段设置
        obj = User.objects.create_user(username=username, password=password)
        if obj:
            result["message"] = "用户创建成功"
            result.update({
                "id": obj.id,
                "username": obj.username
            })
            return Response(result, status=status.HTTP_201_CREATED)
        else:
            result["message"] = "用户创建失败"
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 获取特定用户管理的所有项目
class UserManagedProjectsView(APIView):
    def get(self, request, user_id):
        # 获取特定用户管理的所有队伍ID列表
        team_ids = Member.objects.filter(
            user_id_id=user_id,
            is_leader=True,
            member_status="正常"
        ).values('team_id').distinct()

        # 查询与这些队伍关联的项目
        managed_projects = Project.objects.filter(team__id__in=team_ids)

        # 使用序列化器来序列化数据
        serializer = UserManagedProjectsSerializer(managed_projects, many=True)
        response_data = serializer.data

        return Response(response_data)


# 特定用户管理的特定项目的详细信息（获取、更新、删除）
class UserManagedProjectDetailView(APIView):
    # 检查特定用户是否管理该项目
    def get_project(self, user_id, project_id):
        try:
            project = Project.objects.get(
                id=project_id,
                team__member__user_id=user_id,
                team__member__is_leader=True
            )
            return project
        except Project.DoesNotExist:
            return None

    def get(self, request, user_id, project_id):
        project = self.get_project(user_id, project_id)
        if project:
            serializer = UserManagedProjectsSerializer(project)
            return Response(serializer.data)
        else:
            return Response({"error": "Project not found or user is not the manager."}, status=404)

    def put(self, request, user_id, project_id):
        project = self.get_project(user_id, project_id)
        if project:
            serializer = UserManagedProjectsSerializer(project, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({"error": "Project not found or user is not the manager."}, status=404)

    def delete(self, request, user_id, project_id):
        project = self.get_project(user_id, project_id)
        if project:
            project.delete()
            return Response({"success": True, "message": "Project deleted successfully!"})
        else:
            return Response({"error": "Project not found or user is not the manager."}, status=404)


# 获取特定用户加入的所有项目
class UserJoinedProjectsView(APIView):
    def get(self, request, user_id):
        # 获取符合条件的队伍ID列表
        team_ids = Member.objects.filter(
            user_id_id=user_id,
            is_leader=False,
            member_status="正常"
        ).values('team_id').distinct()

        # 查询与这些队伍关联的项目
        joined_projects = Project.objects.filter(team__id__in=team_ids)  # 通过team__id__in来筛选与给定队伍ID列表相关联的项目

        # 使用序列化器来序列化数据
        serializer = UserJoinedProjectsSerializer(joined_projects, many=True)
        response_data = serializer.data

        return Response(response_data)


# 特定用户参与的特定项目的详细信息（获取、更新、删除）
class UserJoinedProjectDetailView(APIView):
    # 检查特定用户是否参与该项目
    def get_project(self, user_id, project_id):
        try:
            project = Project.objects.get(
                id=project_id,
                team__member__user_id=user_id,
                team__member__is_leader=True
            )
            return project
        except Project.DoesNotExist:
            return None

    def get(self, request, user_id, project_id):
        project = self.get_project(user_id, project_id)
        if project:
            serializer = UserJoinedProjectsSerializer(project)
            return Response(serializer.data)
        else:
            return Response({"error": "Project not found or user is not the manager."}, status=404)

    def put(self, request, user_id, project_id):
        project = self.get_project(user_id, project_id)
        if project:
            serializer = UserJoinedProjectsSerializer(project, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({"error": "Project not found or user is not the manager."}, status=404)

    def delete(self, request, user_id, project_id):
        project = self.get_project(user_id, project_id)
        if project:
            project.delete()
            return Response({"success": True, "message": "Project deleted successfully!"})
        else:
            return Response({"error": "Project not found or user is not the manager."}, status=404)
