from .models import Product, Version
from .serializers import ProductSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from team.models import Team, Member
from user.models import User
from project.models import Project
from django.shortcuts import get_object_or_404
from django.db.models import Q
from datetime import date
from dim.models import Model, Industry, AITag

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # 接口：产品发布（POST）
    @action(methods=['POST'], detail=True)
    def create_product_with_version(self, request, *args, **kwargs):
        try:
            # Extract data from the request data
            version_data = request.data
            # Check if the user is leader
            team_instance = get_object_or_404(Team, project_id=version_data['project_id'])
            current_user_instance = get_object_or_404(User, id=version_data['user_id'])  # 获取当前用户

            # 检查当前用户是否是队长
            is_leader = Member.objects.filter(team=team_instance, user=current_user_instance, is_leader=True).exists()
            if not is_leader:
                response_data = {
                    'message': '只有队长才有权限发布产品',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_403_FORBIDDEN)
            # Check if a product with the given project_id already exists
            project_id = version_data['project_id']
            product_instance, created = Product.objects.get_or_create(project_id=project_id)
            # 如果产品存在，返回
            product_serializer = ProductSerializer(product_instance)
            if created:
                response_data = {
                    'message': '产品已创建过，请调用产品更新接口',
                    'data': {
                        'product': product_serializer.data,
                    },
                }
                return Response(response_data, status=status.HTTP_200_OK)
            # 更新或创建产品信息
            product_instance.name = version_data['name']
            product_instance.product_source = version_data['product_source']
            product_instance.promotional_image = version_data['promotional_image']
            product_instance.description = version_data['description']
            product_instance.type = version_data['type']
            product_instance.product_display_link = version_data['product_display_link']
            product_instance.product_display_qr_code = version_data['product_display_qr_code']
            product_instance.test_group_qr_code = version_data['test_group_qr_code']
            product_instance.save()

            model_instances = Model.objects.filter(id__in=version_data['model'])
            industry_instances = Industry.objects.filter(id__in=version_data['industry'])
            aitag_instances = AITag.objects.filter(id__in=version_data['ai_tag'])
            version_instance = Version.objects.create(product=product_instance,
                                                      version_number=version_data['version_number'],
                                                      name=version_data['name'],
                                                      promotional_image=version_data['promotional_image'],
                                                      description=version_data['description'],
                                                      type=version_data['type'],
                                                      product_display_link=version_data["product_display_link"],
                                                      product_display_qr_code=version_data["product_display_qr_code"],
                                                      test_group_qr_code=version_data["test_group_qr_code"]
                                                      )
            #更新版本与标签关系
            version_instance.model.set(model_instances)
            version_instance.industry.set(industry_instances)
            version_instance.ai_tag.set(aitag_instances)
            # 更新产品与标签关系
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
            response_data = {
                'message': '创建或更新产品及版本信息失败',
                'data': {'errors': str(e)}
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)



    # 更新产品信息（PUT）
    @action(methods=['PUT'], detail=True)
    def update_product_with_version(self, request, *args, **kwargs):
        try:
            # Extract data from the request data
            version_data = request.data
            # Check if the user is leader
            product_instance = get_object_or_404(Product, id=version_data['product_id'])
            team_instance = get_object_or_404(Team, project_id=product_instance.project_id)
            current_user_instance = get_object_or_404(User, id=version_data['user_id'])  # 获取当前用户

            # 检查当前用户是否是队长
            is_leader = Member.objects.filter(team=team_instance, user=current_user_instance, is_leader=True).exists()
            if not is_leader:
                response_data = {
                    'message': '只有队长才有权限更新产品',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_403_FORBIDDEN)
            # Check if a product with the given project_id already exists
            project_id = product_instance.project_id
            product_instance = get_object_or_404(Product, project_id=project_id)

            # 更新产品信息
            product_instance.name = version_data['name']
            product_instance.product_source = version_data['product_source']
            product_instance.promotional_image = version_data['promotional_image']
            product_instance.description = version_data['description']
            product_instance.type = version_data['type']
            product_instance.product_display_link = version_data['product_display_link']
            product_instance.product_display_qr_code = version_data['product_display_qr_code']
            product_instance.test_group_qr_code = version_data['test_group_qr_code']
            product_instance.save()

            model_instances = Model.objects.filter(id__in=version_data['model'])
            industry_instances = Industry.objects.filter(id__in=version_data['industry'])
            aitag_instances = AITag.objects.filter(id__in=version_data['ai_tag'])
            version_instance = Version.objects.create(product=product_instance,
                                                      version_number=version_data['version_number'],
                                                      name=version_data['name'],
                                                      promotional_image=version_data['promotional_image'],
                                                      description=version_data['description'],
                                                      type=version_data['type'],
                                                      product_display_link=version_data["product_display_link"],
                                                      product_display_qr_code=version_data["product_display_qr_code"],
                                                      test_group_qr_code=version_data["test_group_qr_code"]
                                                      )
            # 更新版本与标签关系
            version_instance.model.set(model_instances)
            version_instance.industry.set(industry_instances)
            version_instance.ai_tag.set(aitag_instances)
            # 更新产品与标签关系
            product_instance.model.set(model_instances)
            product_instance.industry.set(industry_instances)
            product_instance.ai_tag.set(aitag_instances)

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
            response_data = {
                'message': '更新产品及版本信息失败',
                'data': {'errors': str(e)}
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    # 获取产品信息（GET）
    @action(methods=['GET'], detail=False)
    def get_product_info(self, request, *args, **kwargs):
        try:
            # Extract project_id from the query parameters
            product_id = request.data.get('product_id', None)
            if not product_id:
                response_data = {
                    'message': '产品ID未提供',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            # Check if a product with the given project_id exists
            product_instance = get_object_or_404(Product, id=product_id)

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