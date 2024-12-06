import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def expand_key(key):
    key = str(key)
    len_original_key = len(key)
    times= int(16/len_original_key)+5
    return (key * times)[2:18].encode('utf-8')  


def jiami(key, input_text):
    """
    加密
    :key: 明文密钥认证
    :input_text: 需要加密的内容
    :return: 扩展后的16字节密钥
    """
    key = expand_key(key)
    KEY = key 
    cipher = AES.new(KEY, AES.MODE_CBC)
    iv = cipher.iv
    encrypted = cipher.encrypt(pad(str(input_text).encode("utf-8"), AES.block_size))
    return base64.b64encode(iv + encrypted).decode("utf-8")


def jiemi(key, encrypted_text):
    """
    解密
    :key: 明文密钥认证
    :encrypted_text: 需要解密的内容
    :return: 被加密的原文
    """
    key = expand_key(key)
    KEY = key 
    encrypted_data = base64.b64decode(str(encrypted_text))
    iv = encrypted_data[:AES.block_size]
    encrypted_message = encrypted_data[AES.block_size:]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(encrypted_message), AES.block_size)
    return decrypted.decode("utf-8")




