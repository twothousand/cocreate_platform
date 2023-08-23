# django
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Q
from django.contrib.auth import get_user_model
# rest_framework
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
# common
from common.mixins import my_mixins
from common.utils import aliyun_green
# app
from user.permissions import IsOwnerOrReadOnly
from dim.models import Model, Industry, AITag
from function.models import Image
from team.models import Team, Member
from project.models import Project
from product.models import Product, Version
from product.serializers import ProductSerializer, ProductDetailSerializer

User = get_user_model()

# 自定义分页器
class CustomPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductViewSet(my_mixins.LoggerMixin, my_mixins.CreatRetrieveUpdateModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:  # 对于POST、PUT和DELETE请求
            permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]  # 需要用户被认证
        else:  # 对于其他请求方法，比如GET、PATCH等
            permission_classes = [AllowAny]  # 允许任何人，不需要身份验证
        return [permission() for permission in permission_classes]

    # 接口：产品发布（POST）
    @transaction.atomic
    @action(methods=['POST'], detail=True)
    def create_product_with_version(self, request, *args, **kwargs):
        try:
            # Extract data from the request data
            version_data = request.data
            # Check if the user is leader
            user_id = request.user.id
            current_user_instance = get_object_or_404(User, id=user_id)  # 获取当前用户
            project_id = version_data['project_id']
            try:
                team_instance = Team.objects.get(project_id=project_id)
                # 检查当前用户是否是队长
                is_leader = Member.objects.filter(team=team_instance, user=current_user_instance,
                                                  is_leader=True).exists()
                if not is_leader:
                    response_data = {
                        'message': '只有队长才有权限发布产品',
                        'data': None,
                    }
                    return Response(response_data, status=status.HTTP_403_FORBIDDEN)
            except Team.DoesNotExist:
                # 未进行过组队招募
                project_instance = Project.objects.get(id=project_id)
                # 检查当前用户是否是队长
                if project_instance.project_creator_id!=user_id:
                    response_data = {
                        'message': '用户权限不足',
                        'data': None,
                    }
                    return Response(response_data, status=status.HTTP_404_NOT_FOUND)

            # 校验产品内容信息是否内容合规
            s = aliyun_green.AliyunModeration()
            check_res = s.text_moderation("pgc_detection",
                                          version_data['product_name']+"。"+version_data['product_description'])
            if check_res['code'] != 1:
                response_data = {
                    'message': '文本检测违规:' + check_res['message'],
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            # Check if a product with the given project_id already exists
            product_instance, created = Product.objects.get_or_create(project_id=project_id)
            # 如果产品存在，返回
            product_serializer = ProductSerializer(product_instance)
            # if created==False:
            #     response_data = {
            #         'message': '产品已创建过，请调用产品更新接口',
            #         'data': {
            #             'product': product_serializer.data,
            #         },
            #     }
            #     return Response(response_data, status=status.HTTP_200_OK)
            product_display_qr_code_instance = get_object_or_404(Image, id=version_data['product_display_qr_code']) if version_data['product_display_qr_code'] != '' else None
            test_group_qr_code_instance = get_object_or_404(Image, id=version_data['test_group_qr_code']) if version_data['test_group_qr_code'] != '' else None
            # 更新或创建产品信息
            product_instance.product_name = version_data['product_name']
            product_instance.product_source = version_data['product_source']
            product_instance.product_description = version_data['product_description']
            product_instance.product_type = version_data['product_type']
            product_instance.product_display_link = version_data['product_display_link']
            product_instance.product_display_qr_code = product_display_qr_code_instance
            product_instance.test_group_qr_code = test_group_qr_code_instance
            product_instance.save()

            image_instances = Image.objects.filter(id__in=version_data['promotional_image'])
            model_instances = Model.objects.filter(id__in=version_data['model'])
            industry_instances = Industry.objects.filter(id__in=version_data['industry'])
            aitag_instances = AITag.objects.filter(id__in=version_data['ai_tag'])
            version_instance = Version.objects.create(product=product_instance,
                                                      version_number=version_data['version_number'],
                                                      product_name=version_data['product_name'],
                                                      product_description=version_data['product_description'],
                                                      product_type=version_data['product_type'],
                                                      product_display_link=version_data["product_display_link"],
                                                      product_display_qr_code=product_display_qr_code_instance,
                                                      test_group_qr_code=test_group_qr_code_instance
                                                      )
            #更新版本与标签关系
            version_instance.promotional_image.set(image_instances)
            version_instance.model.set(model_instances)
            version_instance.industry.set(industry_instances)
            version_instance.ai_tag.set(aitag_instances)
            # 更新产品与标签关系
            product_instance.promotional_image.set(image_instances)
            product_instance.model.set(model_instances)
            product_instance.industry.set(industry_instances)
            product_instance.ai_tag.set(aitag_instances)

            # Serialize and return the data
            product_serializer = ProductSerializer(product_instance)
            response_data = {
                'message': '产品及版本信息创建成功' if created else '产品信息更新成功',
                'data': {
                    'product': product_serializer.data,
                    'version': version_instance.id,
                },
            }
            return Response(response_data, status=status.HTTP_200_OK if created else status.HTTP_201_CREATED)
        except Exception as e:
            # 显式地触发回滚操作
            transaction.set_rollback(True)
            response_data = {
                'message': '创建或更新产品及版本信息失败',
                'data': {'errors': str(e)}
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)



    # 更新产品信息（PUT）
    @transaction.atomic
    @action(methods=['PUT'], detail=True)
    def update_product_with_version(self, request, *args, **kwargs):
        try:
            # Extract data from the request data
            version_data = request.data
            # Check if the user is leader
            user_id = request.user.id
            current_user_instance = get_object_or_404(User, id=user_id)  # 获取当前用户
            product_instance = get_object_or_404(Product, id=version_data['product_id'])
            try:
                print('product_instance.project_id',product_instance.project_id)
                team_instance = Team.objects.get(project_id=product_instance.project_id)
                # 检查当前用户是否是队长
                is_leader = Member.objects.filter(team=team_instance, user=current_user_instance,
                                                  is_leader=True).exists()
                if not is_leader:
                    response_data = {
                        'message': '只有队长才有权限发布产品',
                        'data': None,
                    }
                    return Response(response_data, status=status.HTTP_403_FORBIDDEN)
            except Team.DoesNotExist:
                # 未进行过组队招募
                project_instance = Project.objects.get(id=product_instance.project_id)
                # 检查当前用户是否是队长
                if project_instance.project_creator_id != user_id:
                    response_data = {
                        'message': '用户权限不足',
                        'data': None,
                    }
                    return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            # 校验产品内容信息是否内容合规
            s = aliyun_green.AliyunModeration()
            check_res = s.text_moderation("pgc_detection",
                                          version_data['product_name'] + "。" + version_data['product_description'])
            if check_res['code'] != 1:
                response_data = {
                    'message': '文本检测违规:' + check_res['message'],
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            product_display_qr_code_instance = get_object_or_404(Image, id=version_data['product_display_qr_code']) if \
            version_data['product_display_qr_code'] != '' else None
            test_group_qr_code_instance = get_object_or_404(Image, id=version_data['test_group_qr_code']) if \
            version_data['test_group_qr_code'] != '' else None

            # 更新产品信息
            product_instance.product_name = version_data['product_name']
            product_instance.product_source = version_data['product_source']
            product_instance.product_description = version_data['product_description']
            product_instance.product_type = version_data['product_type']
            product_instance.product_display_link = version_data['product_display_link']
            product_instance.product_display_qr_code = product_display_qr_code_instance
            product_instance.test_group_qr_code = test_group_qr_code_instance
            product_instance.save()

            image_instances = Image.objects.filter(id__in=version_data['promotional_image'])
            model_instances = Model.objects.filter(id__in=version_data['model'])
            industry_instances = Industry.objects.filter(id__in=version_data['industry'])
            aitag_instances = AITag.objects.filter(id__in=version_data['ai_tag'])
            version_instance = Version.objects.create(product=product_instance,
                                                      version_number=version_data['version_number'],
                                                      product_name=version_data['product_name'],
                                                      product_description=version_data['product_description'],
                                                      product_type=version_data['product_type'],
                                                      product_display_link=version_data["product_display_link"],
                                                      product_display_qr_code=product_display_qr_code_instance,
                                                      test_group_qr_code=test_group_qr_code_instance
                                                      )
            # 更新版本与标签关系
            version_instance.model.set(model_instances)
            version_instance.industry.set(industry_instances)
            version_instance.ai_tag.set(aitag_instances)
            version_instance.promotional_image.set(image_instances)

            # 更新产品与标签关系
            product_instance.model.set(model_instances)
            product_instance.industry.set(industry_instances)
            product_instance.ai_tag.set(aitag_instances)
            product_instance.promotional_image.set(image_instances)

            # Serialize and return the data
            product_serializer = ProductSerializer(product_instance)
            response_data = {
                'message': '产品及版本信息更新成功',
                'data': {
                    'product': product_serializer.data,
                    'version': version_instance.id,
                },
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            # 显式地触发回滚操作
            transaction.set_rollback(True)
            response_data = {
                'message': '更新产品及版本信息失败',
                'data': {'errors': str(e)}
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    # 获取产品信息（GET）
    @action(methods=['GET'], detail=False)
    def get_product_info(self, request, product_id, *args, **kwargs):
        try:
            # Extract project_id from the query parameters
            # product_id = request.data.get('product_id', None)
            if not product_id:
                response_data = {
                    'message': '产品ID未提供',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            # Check if a product with the given project_id exists
            product_instance = get_object_or_404(Product, id=product_id)
            # # Query the ProductVersion table to get the latest version number for the given product_id
            # latest_version = Version.objects.filter(product_id=product_id).aggregate(Max('created_at'))[
            #     'created_at__max']
            # print(' latest_version', latest_version)
            # latest_version_instance = Version.objects.filter(product_id=product_id, created_at=latest_version).first()
            #
            # if latest_version_instance:
            #     latest_version_number = latest_version_instance.version_number
            # else:
            #     latest_version_number = None

            # Serialize and return the product data
            product_serializer = ProductSerializer(product_instance)
            response_data = {
                'message': '产品查询成功',
                'data': {
                    'product': product_serializer.data,
                },
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            response_data = {
                'message': '未找到符合条件的产品',
                'data': None,
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response_data = {
                'message': '查询产品信息失败',
                'data': {'errors': str(e)},
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 根据项目ID获取产品ID（GET）
    @action(methods=['GET'], detail=False)
    def get_product_id(self, request, project_id, *args, **kwargs):
        try:
            if not project_id:
                response_data = {
                    'message': '项目ID未提供',
                    'data': {
                        'product_id': None,
                    },
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            try:
                project_instance = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                response_data = {
                    'message': '未找到符合条件的项目ID',
                    'data': {
                        'product_id': None,
                    },
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)

            try:
                product_instance = Product.objects.get(project=project_instance)
                product_serializer = ProductSerializer(product_instance)
                response_data = {
                    'message': '产品ID查询成功',
                    'data': {
                        'product_id': product_serializer.data['id'],
                    },
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                response_data = {
                    'message': '未找到符合条件的产品ID',
                    'data': {
                        'product_id': None,
                    },
                }
                return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                'message': '查询产品ID失败',
                'data': {'product_id': None,
                         'errors': str(e)},
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 产品的过滤和搜索视图
class ProductFilterAndSearchView(my_mixins.CustomResponseMixin, my_mixins.ListCreatRetrieveUpdateModelViewSet):
    pagination_class = CustomPagination
    permission_classes = [AllowAny]

    # 过滤产品（GET）
    @action(methods=['GET'], detail=False)
    def search_filter_products(self, request, *args, **kwargs):
        try:
            keyword = self.request.GET.get('keyword')
            industry = self.request.GET.getlist('industry')
            ai_tag = self.request.GET.getlist('ai_tag')
            product_type = self.request.GET.get('product_type')
            model_name = self.request.GET.getlist('model_name')

            queryset = Product.objects.all()

            # 应用过滤条件
            if product_type:
                queryset = queryset.filter(type=product_type)
            if len(model_name) > 0 and model_name[0] != '':
                queryset = queryset.filter(model__model_name__in=model_name)
            if len(industry) > 0 and industry[0] != '':
                queryset = queryset.filter(industry__industry__in=industry)
            if len(ai_tag) > 0 and ai_tag[0] != '':
                queryset = queryset.filter(ai_tag__ai_tag__in=ai_tag)

            # 应用搜索条件
            if keyword:
                queryset = queryset.filter(
                    Q(product_name__icontains=keyword) |
                    Q(product_description__icontains=keyword)
                )

            queryset = queryset.order_by('-id')
            # 使用分页器的 paginate_queryset() 方法分页
            paginated_queryset = self.paginate_queryset(queryset)
            serializer = ProductDetailSerializer(paginated_queryset, many=True)

            if serializer.data:
                response_data = {
                    'message': '已成功检索到产品！',
                    'data': serializer.data
                }
            else:
                response_data = {
                    'message': '未检索到任何符合的产品！',
                    'data': []
                }

            return self.get_paginated_response(response_data)
        except Exception as e:
            response_data = {
                'message': str(e),
                'data': []
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)