from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.shortcuts import render, redirect
from functions.decorators import login_required
from functions import send_email
from django.urls import reverse
from itertools import chain
import os


# Create your views here.
# 主页
# def index(request):
#     all_news = News.objects.order_by('-id')[:12]
#     user = None
#     try:
#         user = request.session.get("passport_id")
#         # databases_user_id = Developers.objects.get(user_id=user)
#     except Exception as e:
#         print(e)
#         return render(request, 'cocreate/index.html', locals())
#     return render(request, 'cocreate/index.html', locals())


# # 项目列表页
# def projects(request):
#     # 显示项目 -- 分页 加装饰器(只有GET请求)
#     if request.method != 'GET':
#         return HttpResponse("请使用GET请求数据! ")
#
#     # 有查询字符串 参考 day04  没有查询字符串的情况下 按照发布时间 降序排序
#     all_projects = Projects.objects.filter().order_by("-post_datetime")
#
#     # 1.按照类别分类搜索
#     all_kind = KindChoice.objects.all()
#     # 取出筛选项目类型
#     kind = request.GET.get('kind', '')
#     # 在结果集里面做筛选
#     if kind:
#         all_projects = all_projects.filter(kind=kind)
#
#     # 2.按照开发语言搜索
#     all_language = LanguageChoice.objects.all()
#     # 取出筛选开发语言类型
#     language = request.GET.get('language', '')
#     if language:
#         all_projects = all_projects.filter(language=language)
#
#     # 查询每种项目类型的5个最新  和４个最多浏览的信息
#     app_data_new = Projects.objects.get_projects_by_type(APP, limit=5, sort='new')
#     desktop_data_new = Projects.objects.get_projects_by_type(DESK_APP, limit=5, sort='new')
#     manage_data_new = Projects.objects.get_projects_by_type(MANAGE_SYSTEM, limit=5, sort='new')
#     pc_data_new = Projects.objects.get_projects_by_type(WEBSITE, limit=5, sort='new')
#     ui_data_new = Projects.objects.get_projects_by_type(UI, limit=5, sort='new')
#     small_program_data_new = Projects.objects.get_projects_by_type(SMALL_PROGRAM, limit=5, sort='new')
#     game_data_new = Projects.objects.get_projects_by_type(GAME, limit=5, sort='new')
#     other_data_new = Projects.objects.get_projects_by_type(OTHER, limit=5, sort='new')
#     # 查询每种项目类型的最多浏览的信息[浏览不常用 以后去掉]
#     project_data_hot = Projects.objects.get_projects_by_type(APP, limit=10, sort='hot')
#
#     # 分页
#     paginator = Paginator(all_projects, 5)
#     cur_page = request.GET.get('page', 1)  # 得到默认的当前页
#     page_obj = paginator.page(cur_page)
#
#     # 右侧top10展示 按照预算的高低 存储的是字符串 先转成数字
#     projects_top10 = Projects.objects.extra(select={'budget': 'budget+0'})
#     projects_top10 = projects_top10.extra(order_by=["-budget"])
#
#     # 按照项目类别分类
#     obj = Projects.objects.all().values("kind")
#
#     # 用户收藏
#     user = request.session.get("passport_id")
#     u_project_id = Collection.objects.filter(user_id=user)
#     collected_list = []
#     for obj in u_project_id:
#         collected_list.append(obj.projects_id_id)
#
#     # 获取当前时间
#     from django.utils import timezone
#     now = timezone.now()
#     import time
#     t = int(time.time())
#     print("t------------", t)
#     # 项目发布时间
#     new_publish = []
#     for date in all_projects:
#         # 得到时间戳
#         import datetime
#         import time
#         # 先把date转变为字符串,然后转换为datetime格式
#         this_date = datetime.datetime.strptime(str(date.post_datetime), '%Y-%m-%d %H:%M:%S.%f')
#         # 把datetime转变为时间戳
#         this_date = time.mktime(this_date.timetuple())
#         this_date = int(t - this_date)
#         days_5 = int(432000)
#         # 5天的时间戳为 432000
#         if this_date < days_5:
#             new_publish.append(date)
#     print("new_publish------------", new_publish)
#     return render(request, 'cocreate/projects.html', locals())
