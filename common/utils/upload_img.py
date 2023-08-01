# 系统模块
import re
from io import BytesIO
from PIL import Image
# 阿里云oss服务模块
import oss2
# common
from common.config import *


# 初始化OSS客户端
auth = oss2.Auth(ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, ALIBABA_OSS_ENDPOINT, ALIBABA_OSS_BUCKET_NAME)


def compress_and_upload_image(image_data, target_folder, filename, img_format, target_max_size=2 * 1024 * 1024):
    try:
        # 打开图片
        image = Image.open(BytesIO(image_data))

        # 获取图片的原始大小
        image_size = len(image_data)

        # 检查图片是否需要压缩
        if image_size > target_max_size:
            # 计算压缩比例
            compress_ratio = (target_max_size / image_size) ** 0.5

            # 根据压缩比例进行图片压缩
            width, height = image.size
            new_width = int(width * compress_ratio)
            new_height = int(height * compress_ratio)
            image = image.resize((new_width, new_height), Image.ANTIALIAS)

        # 将图片保存到内存中
        compressed_image_data = BytesIO()
        image.save(compressed_image_data, format=img_format)
        compressed_image_data.seek(0)

        # 生成上传到OSS的路径和文件名（可自行设定）
        oss_path = f'{target_folder}/' + f'{filename}.' + img_format

        # 上传到OSS
        bucket.put_object(oss_path, compressed_image_data)

        # 获取图片持久化的链接
        # image_url = f"https://{ALIBABA_OSS_BUCKET_NAME}.{ALIBABA_OSS_ENDPOINT.lstrip('https://')}/{oss_path}" #原始
        image_url = f"https://{IMG_DOMAIN}/{oss_path}"

        return image_url
    except Exception as e:
        print("图片处理和上传到OSS失败：", e)
        return None

def delete_image_from_oss(image_url):
    try:
        pattern = r"https://.*?/(.*)"
        match = re.match(pattern, image_url)
        if match:
            object_key = match.group(1)
        else:
            return '图片路径错误'
        # Delete the object from OSS
        bucket.delete_object(object_key)

        return "图片删除成功"
    except Exception as e:
        error_msg = "删除失败: "+e
        return error_msg