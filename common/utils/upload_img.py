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


def compress_and_upload_image(image_data, target_folder, filename, img_format, target_max_size=2 * 1024 * 1024, compress_step=0.9):
    try:
        # Open the image
        image = Image.open(BytesIO(image_data))

        # Get the original image size
        image_size = len(image_data)

        # Check if the image needs compression
        if image_size > target_max_size:
            # Perform compression in a loop until the target size is achieved or exceeded
            while image_size > target_max_size:
                # Calculate compression ratio
                compress_ratio = compress_step

                # Resize the image based on the compression ratio
                image = image.resize((int(image.width * compress_ratio), int(image.height * compress_ratio)),
                                     Image.ANTIALIAS)

                # Save the compressed image to memory
                compressed_image_data = BytesIO()
                image.save(compressed_image_data, format=img_format)
                compressed_image_data.seek(0)

                # Get the size of the compressed image
                image_size = len(compressed_image_data.getvalue())
        else:
            # If the image is already smaller than the target size, use the original image data
            compressed_image_data = BytesIO(image_data)

        # Generate the OSS path and filename (can be customized)
        oss_path = f'{target_folder}/{filename}.{img_format}'

        # Upload to OSS
        bucket.put_object(oss_path, compressed_image_data)

        # Get the URL of the persisted image
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