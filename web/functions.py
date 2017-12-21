# coding=utf8
import StringIO
import gzip
import zlib
import os

import re

urldecoder = re.compile('%([0-9a-fA-F]{2})')

def urldecode(s):
    bs = bytearray(s)
    offset = 0
    for encoded in urldecoder.finditer(s):
        start, end = encoded.span()
        bs[start + offset:end + offset] = chr(int(encoded.group(1), 16))
        offset += (start - end + 1)
    return str(bs)


# gzip 压缩
def gzip(data):
    out = StringIO.StringIO()
    with gzip.GzipFile(fileobj=out, mode="w") as f:
        f.write(data)
    return out.getvalue()


# deflated 压缩
def deflate(data):
    return zlib.compress(data)


# 生成响应头部
def dic2title(dic):
    buf = []
    for key, value in dic.iteritems():
        buf.append(key + ": " + value)
    return "\r\n".join(buf) + "\r\n"


# 解析GET参数
def parase_params(str):
    str = urldecode(str)
    array = str.split('&')
    dic = {}
    for i in array:
        pos = i.find('=')
        dic[i[:pos]] = i[pos + 1:]
    return dic


# 解析header数组
def parase_array(str):
    array = str.replace(" ", "").split(',')
    def sharp(str):
        index = str.find(';')
        if index != -1:
            first = str[:index]
            tmp = str[index + 1:]
            second = tmp[tmp.find("=") + 1:]
        else:
            first = str
            second = ""
        return [first, second]

    return [sharp(x) for x in array]


# 解析请求头部
def parase_header(header):
    header = header.replace("\r", "")
    array = header.split('\n')
    dic = {}
    first_line = array[0]
    url = urldecode(first_line).split(' ')
    dic["type"] = url[0]
    # 解析参数
    if dic["type"] == "GET" or dic["type"] == "POST":
        tmp = url[1]
        tmp_index = tmp.find("?")
        if tmp_index != -1:
            dic["path"] = tmp[:tmp_index].replace("../", "").replace("./", "")
            dic["get_params"] = parase_params(tmp[tmp_index + 1:])
        else:
            dic["path"] = tmp
            dic["get_params"] = {}
    else:
        print dic["type"]

    for i in array[1:]:
        if i != '':
            pos = i.find(': ')
            dic[i[:pos].lower()] = i[pos + 2:]
    # 解析压缩格式
    if "accept-encoding" in dic:
        dic["accept-encoding"] = parase_array(dic["accept-encoding"])
    else:
        dic["accept-encoding"] = [[None, None]]
    # 解析请求格式
    if "accept" in dic:
        dic["accept"] = parase_array(dic["accept"])
    else:
        dic["accept"] = ["text/html"]
    # 解析Content-Type
    if "content-type" in dic:
        dic["content-type"] = parase_array(dic["content-type"])
    return dic


# 解析POST的body内容
def parase_body(body, boundary):
    if boundary not in body:
        body = urldecode(body)
        dic = parase_params(body)
    else:
        body = body.replace("--" + boundary + "--\r\n", "")
        array = body.split("--" + boundary)
        dic = {}

        def get_post_params(item):
            pos = item.find("\r\n\r\n")
            value = item[pos + 4:]
            header = item[:pos]
            name_pos = header.find("name=") + 6;
            name_end = header.find("\"", name_pos);
            name = header[name_pos:name_end];
            dic[name] = value

        for item in array:
            if item == "":
                continue
            get_post_params(item[2:-2])

    return dic


def get_extenstion(file):
    return os.path.splitext(file)[1]



