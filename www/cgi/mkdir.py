# coding=utf8

from const import *

def main(get,post):
    dir=post["dir"]
    dir=join(ABS_WWW,post["parent"],dir)
    if not os.path.exists(dir):
        os.mkdir(dir)
