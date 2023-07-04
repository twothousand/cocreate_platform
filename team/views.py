from django.shortcuts import render

# Create your views here.
# 判断是否开启组队招募
# if 开启组队招募:
#     # 检查组队信息表是否存在该项目的记录
#     if 组队信息.objects.filter(项目=新项目).exists():
#         # 修改组队信息表中的数据
#         组队信息.objects.filter(项目=新项目).update(是否开启招募=True)
#     else:
#         # 插入一条新的数据到组队信息表
#         组队信息.objects.create(项目=新项目, 是否开启招募=True)

