# coding=utf8
import os
from const import *
def main(get,post):
    file= ABS+WWW+post['file']
    if os.path.exists(file):
        if os.path.isdir(file):
            os.rmdir(file)
        else:
            os.remove(file)
