from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from common.utils.upload_img import compress_and_upload_image
import time
import uuid
import json

def generate_unique_filename():
    # 获取当前时间戳（精确到毫秒）
    timestamp = int(time.time() * 1000)

    # 生成一个随机数（使用UUID的随机数生成方法）
    random_string = str(uuid.uuid4().hex)[:6]  # 取UUID的前6位作为随机数

    # 将时间戳和随机数拼接成文件名
    filename = f"{timestamp}_{random_string}"

    return filename


class ImageViewSet(ModelViewSet):
    parser_classes = [MultiPartParser, JSONParser, FormParser]
    ALLOWED_CATEGORIES = ['avatar', 'product', 'project']
    ALLOWED_IMAGE_FORMATS = ['jpg', 'jpeg', 'png']
    @action(methods=['POST'], detail=False)
    def upload_image(self, request, *args, **kwargs):
        try:
            # Get the JSON data from the request
            json_data_str = request.data.get('json_data', {})
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
                response_data = {
                    'message': '图片上传成功。',
                    'data': {'image_url': image_url},
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                message = '图片处理和上传失败。'
                response_data = {
                    'message': message,
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            message = '图片上传失败。'
            response_data = {
                'message': message,
                'data': {'errors': str(e)},
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
