from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from user.permissions import IsOwnerOrReadOnly
from common.utils.upload_img import compress_and_upload_image, delete_image_from_oss
from django.shortcuts import get_object_or_404
from dim.models import Image
from user.models import User
from .serializers import ImageSerializer
import time
import uuid
import json
from common.mixins import my_mixins
from django.db import transaction

def generate_unique_filename():
    # 获取当前时间戳（精确到毫秒）
    timestamp = int(time.time() * 1000)

    # 生成一个随机数（使用UUID的随机数生成方法）
    random_string = str(uuid.uuid4().hex)[:6]  # 取UUID的前6位作为随机数

    # 将时间戳和随机数拼接成文件名
    filename = f"{timestamp}_{random_string}"

    return filename


class ImageViewSet(my_mixins.LoggerMixin, my_mixins.CustomResponseMixin, my_mixins.CreatRetrieveUpdateModelViewSet):
    parser_classes = [MultiPartParser, JSONParser, FormParser]
    ALLOWED_CATEGORIES = ['avatar', 'product', 'project']
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
            json_data_str = request.data.get('json_data', {})
            user_id = request.user.id
            try:
                json_data = json.loads(json_data_str)
            except json.JSONDecodeError:
                message = '无效的JSON数据。'
                response_data = {
                    'message': message,
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            # Now you can access the JSON data and its values as needed
            category = json_data.get('category', None)

            # Check if category is in the allowed list
            if category not in self.ALLOWED_CATEGORIES:
                message = 'category必须在这个范围内：' + ', '.join(self.ALLOWED_CATEGORIES)
                response_data = {
                    'message': message,
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            file = request.FILES.get('image')
            if not file:
                message = '未提供图片文件。'
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

            image_data = file.read()

            target_folder = category if category else "tmp"  # 上传到OSS的目标文件夹，根据实际情况修改
            filename = generate_unique_filename()

            image_url = compress_and_upload_image(image_data, target_folder, filename, img_format)

            if image_url:
                current_user_instance = get_object_or_404(User, id=user_id)
                image_instance = Image.objects.create(
                    upload_user=current_user_instance,
                    image_url=image_url,
                    image_path=target_folder+'/'+filename,
                    category=target_folder
                )
                image_serializer = ImageSerializer(image_instance)
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
            current_user_instance = get_object_or_404(User, id=user_id)
            # 检查当前用户是否是上传图片的人，只有上传图片的人才能删除
            image = Image.objects.filter(upload_user=current_user_instance, id=image_id)
            is_uploader = image.exists()
            if not is_uploader:
                response_data = {
                    'message': '只有上传者才有权限删除',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_403_FORBIDDEN)
            image_instance = image.first()
            msg = delete_image_from_oss(image_instance.image_url)
            if msg == "图片删除成功":
                image_instance.is_deleted = 1
                image_instance.save()
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