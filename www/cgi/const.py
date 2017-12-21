import os
ABS = "www/"
WWW="ftp/"
ABS_WWW=ABS+WWW
def join(*list):
    str=os.path.normpath("/".join(list))
    return str.replace("//","/")
def main(get,post):
    pass