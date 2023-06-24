import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from user.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.response import Response


# 用于列出或检索用户的视图集
class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     A viewset for viewing and editing user instances.
#     """
#     serializer_class = UserSerializer
#     queryset = User.objects.all()

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
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer


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


# 以rest_framework，查询我收藏的项目
