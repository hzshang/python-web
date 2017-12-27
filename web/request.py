# -*- coding: utf-8 -*-
from const import *
from functions import *
from os import path
import magic
from www.cgi import cgi
import traceback

class request(object):
    """request context"""

    def __init__(self, root, index):
        self.root = root
        self.index = index

    def process_data(self, sock):
        data = sock.recv(4096)
        index = data.find("\r\n\r\n")
        header = data[:index]
        left=data[index+4:]
        try:
            self.request_header = parase_header(header)
            if self.request_header["type"] == "POST":
                buf = [left]
                sock.settimeout(0.5)
                while True:
                    try:
                        tmp_data = sock.recv(4096)
                        buf.append(tmp_data)
                    except Exception as e:
                        break
                sock.setblocking(0)
                body = "".join(buf)
                self.body = parase_body(body, self.request_header["content-type"][0][1])
            else:
                self.body={}
            self.__locate_request_file()
        except Exception as e:
            traceback.print_exc()
            self.request_header = {
                "type": "GET",
                "path": BAD_REQUEST_PATH,
                "accept-encoding": ["deflate"],
                "accept": ["text/html"]
            }
            self.status = 400

    # 解析请求的文件地址
    def __locate_request_file(self):
        try:
            tmp = self.root + "/" + self.request_header["path"]
        except Exception as e:
            print self.request_header

        if path.exists(tmp):
            if path.isfile(tmp):
                self.status = 200
                self.request_header["path"] = tmp
            else:
                self.status = 404
                self.request_header["path"] = NOT_FOUND_PATH
                for index in self.index:
                    tmp_path = tmp + "/" + index
                    if path.exists(tmp_path):
                        self.request_header["path"] = tmp_path
                        self.status = 200
                        break
        else:
            self.status = 404
            self.request_header["path"] = NOT_FOUND_PATH

    def get_response(self):
        buf = []
        dic = {
            200: GOOD_REQUEST,
            400: BAD_REQUEST,
            404: NOT_FOUND,
            500: SERVER_ERROR,
        }
        content = self.__get_content()
        if content == None:
            self.status=500
            self.request_header["path"]=ERROR_REQUEST_PATH
            content=self.__get_content()

        buf.append(dic[self.status])
        buf.append("Server: python-web")
        accept_encoding=[i[0] for i in self.request_header["accept-encoding"]];
        # comp 压缩函数
        if "deflate" in accept_encoding:
            comp = deflate
            buf.append("Content-Encoding: deflate")
        elif "gzip" in accept_encoding:
            comp = gzip
            buf.append("Content-Encoding: gzip")
        else:
            comp = lambda x: x

        compressed=comp(content)
        buf.append("Content-Type: %s" % self.__get_content_type())
        buf.append("Content-Length: %d" % len(compressed))
        header = "\r\n".join(buf) + "\r\n\r\n"
        print header
        return header + compressed


    def __get_content(self):
        tmp_path=self.request_header["path"]
        if get_extenstion(tmp_path)==CGI_FILE:
            base = path.basename(tmp_path)
            func = path.splitext(base)[0]
            try:
                data = cgi.map()[func](self.__get_params(), self.__post_params())
            except  Exception as e:
                # traceback.print_exc()
                data = None
        else:
            with open(tmp_path) as f:
                data = f.read()
        return data

    def __get_params(self):
        return self.request_header["get_params"]

    def __post_params(self):
        return self.body

    def __get_content_type(self):
        if get_extenstion(self.request_header["path"])==CGI_FILE:
            file_type="text/html"
        else:
            mime = magic.Magic(mime=True)
            file_type = mime.from_file(self.request_header["path"])
        return file_type
