# 系统模块
import uuid
# rest_framework
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
# django
from django.db import transaction
from django.contrib.auth import get_user_model
# app
from apps.user.permissions import IsOwnerOrReadOnly
from apps.function.models import Image, VerifCode, System
from apps.function import serializers
# common
from common.mixins import my_mixins
from common.utils import time_utils, upload_img, aliyun_green

User = get_user_model()


def generate_unique_filename():
    # 获取当前时间戳（精确到毫秒）
    timestamp = time_utils.get_current_long_timestamp()

    # 生成一个随机数（使用UUID的随机数生成方法）
    random_string = str(uuid.uuid4().hex)[:6]  # 取UUID的前6位作为随机数

    # 将时间戳和随机数拼接成文件名
    filename = f"{timestamp}_{random_string}"

    return filename


class ImageViewSet(my_mixins.LoggerMixin, my_mixins.CreatRetrieveUpdateModelViewSet):
    parser_classes = [MultiPartParser, JSONParser, FormParser]
    ALLOWED_CATEGORIES = ['avatar', 'product', 'project', 'system']
    ALLOWED_SUBCATEGORIES = ['cover', 'show_qrcode', 'group_qrcode']
    ALLOWED_IMAGE_FORMATS = ['jpg', 'jpeg', 'png']

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:  # 对于POST、PUT和DELETE请求
            permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]  # 需要用户被认证
        else:  # 对于其他请求方法，比如GET、PATCH等
            permission_classes = [AllowAny]  # 允许任何人，不需要身份验证
        return [permission() for permission in permission_classes]

    @transaction.atomic
    @action(methods=['POST'], detail=False)
    def upload_image(self, request, *args, **kwargs):
        try:
            # Get the JSON data from the request
            category = request.data.get('category', 'tmp')
            sub_category = request.data.get('sub_category', '')
            user_id = request.user.id

            file = request.FILES.get('image')
            if not file:
                message = '未提供图片文件。'
                response_data = {
                    'message': message,
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            # 检查图片大小
            max_image_size = 20 * 1024 * 1024  # 20MB in bytes
            if file.size > max_image_size:
                message = '图片超过允许大小（20MB）。'
                response_data = {
                    'message': message,
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            img_format = file.name.split('.')[-1].lower()
            if img_format not in self.ALLOWED_IMAGE_FORMATS:
                message = '不支持的图片格式。仅支持 jpg、jpeg、png 格式。'
                response_data = {
                    'message': message,
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            if category not in self.ALLOWED_CATEGORIES:
                message = "不支持的category"
                response_data = {
                    'message': message,
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            if sub_category !='' and sub_category not in self.ALLOWED_SUBCATEGORIES:
                message = "不支持的sub_category"
                response_data = {
                    'message': message,
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            image_data = file.read()

            if sub_category == '':
                target_folder = category
            else:
                target_folder = category + '/' + sub_category
            filename = generate_unique_filename()

            image_url = upload_img.compress_and_upload_image(image_data, target_folder, filename, img_format)

            if image_url:
                # 图片审核
                s = aliyun_green.AliyunModeration()
                if category == 'avatar':
                    check_res = s.image_moderation("profilePhotoCheck", image_url)
                else:
                    check_res = s.image_moderation("baselineCheck", image_url)
                if check_res['code'] != 1:
                    response_data = {
                        'message': '图片检测违规:'+check_res['message'],
                        'data': None,
                    }
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                # current_user_instance = get_object_or_404(User, id=user_id)
                image_instance = Image.objects.create(
                    upload_user=user_id,
                    image_url=image_url,
                    image_path=f'{target_folder}/{filename}.{img_format}',
                    category=target_folder
                )
                image_serializer = serializers.ImageSerializer(image_instance)
                response_data = {
                    'message': '图片上传成功。',
                    'data': image_serializer.data,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                # 显式地触发回滚操作
                transaction.set_rollback(True)
                message = '图片处理和上传失败。'
                response_data = {
                    'message': message,
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # 显式地触发回滚操作
            transaction.set_rollback(True)
            message = '图片上传失败。'
            response_data = {
                'message': message,
                'data': {'errors': str(e)},
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    @action(methods=['DELETE'], detail=False)
    def delete_image(self, request, *args, **kwargs):
        try:
            # Get the JSON data from the request
            image_id = request.data.get('image_id', None)
            user_id = request.user.id
            # current_user_instance = get_object_or_404(User, id=user_id)
            # 检查当前用户是否是上传图片的人，只有上传图片的人才能删除
            image = Image.objects.filter(upload_user=user_id, id=image_id)
            is_uploader = image.exists()
            if not is_uploader:
                response_data = {
                    'message': '只有上传者才有权限删除',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_403_FORBIDDEN)
            image_instance = image.first()
            # 物理删除图片记录
            image_instance.delete()
            msg = upload_img.delete_image_from_oss(image_instance.image_url)
            if msg == "图片删除成功":
                response_data = {
                    'message': '图片删除成功。',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                # 显式地触发回滚操作
                transaction.set_rollback(True)
                response_data = {
                    'message': msg,
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # 显式地触发回滚操作
            transaction.set_rollback(True)
            message = '图片删除失败。'
            response_data = {
                'message': message,
                'data': {'errors': str(e)},
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifCodeViewSet(my_mixins.CustomResponseMixin, my_mixins.CreatModelViewSet):
    serializer_class = serializers.VerifCodeSerializer
    # throttle_classes = [AnonRateThrottle, ]  # 限流，限制验证码发送频率
    permission_classes = [AllowAny, ]
    custom_message = "验证码发送成功！"

    def send_sms_test(self, request, *args, **kwargs):
        mobile_phone = request.data.get("mobile_phone")
        verification_code = "123456"  # request.data.get("verification_code")
        verif_code = VerifCode.create(mobile_phone=mobile_phone, verification_code=verification_code)
        result = {
            "id": verif_code.id,
            "mobile_phone": verif_code.mobile_phone
        }
        return Response(result, status=status.HTTP_200_OK)


class SystemView(my_mixins.LoggerMixin, my_mixins.ListCreatRetrieveUpdateModelViewSet):
    @action(detail=False, methods=['GET'])  # Use detail=False for list-level actions
    def get_system_content(self, request):
        try:
            content_name_en = self.request.query_params.get('content_name_en')
            system_page = self.request.query_params.get('system_page')
            content_title = self.request.query_params.get('content_title')

            queryset = System.objects.filter(is_deleted=False)

            # 应用过滤条件
            if content_name_en:
                queryset = queryset.filter(content_name_en=content_name_en)
            if system_page:
                queryset = queryset.filter(system_page=system_page)
            if content_title:
                queryset = queryset.filter(content_title=content_title)

            serialized_data = serializers.SystemSerializer(queryset, many=True).data  # Replace with your serializer
            response_data = {
                "message": "成功获取系统资料",
                "data": serialized_data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                'message': '查询系统资料失败',
                'data': {'errors': str(e)}
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)