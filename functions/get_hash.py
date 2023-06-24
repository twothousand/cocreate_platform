import hashlib


# 密码加密
def get_hash(str):
    # 取一个字符串的hash值
    sh = hashlib.sha1()  # 40位16进制
    # sh = hashlib.md5()  # 32位16进制
    sh.update(str.encode('utf8'))
    return sh.hexdigest()
