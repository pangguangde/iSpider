# coding:utf8
import base64
import hashlib
import random

import time
from Crypto.Cipher import DES3

__author__ = 'pangguangde'


def che168_app_password(string):
    return encode_3des(encode_md5(string))


def generate_che168_sign(parmas):
    parma_arr = [(k, v) for k, v in parmas.items()]
    parma_arr.sort(key=lambda item: item[0])
    parmas_str = ''.join(['%s%s' % (k, v) for k, v in parma_arr])
    string = "com.che168.www%scom.che168.www" % parmas_str
    return encode_md5(string)

def encode_md5(string):
    if type(string) == unicode:
        string = string.encode('utf8')
    return hashlib.md5(string).hexdigest()


def decode_3des(string, secret_key='appapiche168comappapiche', mode=DES3.MODE_CBC, iv='appapich'):
    key = DES3.new(secret_key, mode=mode, IV=iv)
    or_str = key.decrypt(base64.b64decode(string))
    ret = ''
    for i in or_str:
        if ord(i) > 10:
            ret += i
        else:
            break
    return ret


def encode_3des(string, secret_key='appapiche168comappapiche', mode=DES3.MODE_CBC, iv='appapich'):
    remainder = len(string) % 8
    string += chr(8 - remainder) * (8 - remainder)  # 补位，缺 n 字节就补 n 个 ASCII 码为 n 的字符，虽然不知道是什么模式，姑且认为是 PKCS5Padding，可以这样设置跑的通啊ㄟ(▔,▔)ㄏ
    key = DES3.new(secret_key, mode=mode, IV=iv)
    return base64.b64encode(key.encrypt(string))


def random_hex_str(num):
    chars = '0123456789abcdef'
    return ''.join([random.choice(chars) for _ in range(num)])

def get_che168_udid():
    device_id = random_hex_str(40)
    ts = time.time()
    rand_num = random.randint(12345678, 99999999)
    original_str = '%s|%s%s|%s' % (device_id, ts, random.randint(1000, 9999), rand_num)
    print original_str
    return encode_3des(original_str)

if __name__ == '__main__':
    data = {
        "_appid": "2scapp.ios",
        "appversion": "5.6.1",
        "channelid" : "App Store",
        "cid": "330100",
        "cpcnum": "0",
        "dealertype": "9",
        "isloan": "0",
        "ispic": "0",
        "orderby": "0",
        "pageindex": "1",
        "pagesize": "24",
        "priceregion": "5-10",
        "pid": "330000",
        # "udid": encode_3des('b80099a6eefa49bd8ad6c932acbb6185ebcdfdf5|1487842134.693190|25221648'),
        "udid": 'C/tHzFGCpFKy/pTflxfmHMua98hzCq3QfgZ+oaNoz/zWNGLEe0I0YC5s86Vg6OaKNZoeG+Y5Hr8NFz7cH1vzfkHR4f5DWHJ+',
    }
    print generate_che168_sign(data) == '4b54f862fe1d09dfc8c5859f09ec3bec'
    # print random_hex_str(40)
    # print get_che168_udid()
    print decode_3des('C/tHzFGCpFKy/pTflxfmHMua98hzCq3QfgZ+oaNoz/zWNGLEe0I0YE4lsxhcSzVJqoX7uZtDVRKYDWnj46Eg73dEh5vL6S0y')
    print decode_3des('C/tHzFGCpFKy/pTflxfmHMua98hzCq3QfgZ+oaNoz/zWNGLEe0I0YJpvVfE+78EdUSQL+XNorStMhjEuJb+AlKiT83yL9p18')
    print get_che168_udid()
    # print encode_md5('123456')
    # print encode_md5( u'中国')