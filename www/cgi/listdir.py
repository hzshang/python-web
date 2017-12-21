# coding=utf-8
from const import *
import os

def dir_is_empty(x):
    return os.listdir(x)==[]

def main(get, post):

    #相对于www/ftp/文件夹的路径,用于函数参数
    relative_path = get["dir"]

    #相对于/www的路径，用于下载文件
    www_path=WWW+relative_path

    #相对于/ 的绝对路径,用于程序操作
    real_path = ABS + www_path

    array = os.listdir(real_path)
    dirs = [x for x in array if os.path.isdir(join(real_path,x))]
    files = [x for x in array if not os.path.isdir(join(real_path,x))]
    print """<a id="dir" onclick="listFile('%s')" class="list-group-item list-group-item-action active">%s</a>"""%(relative_path, relative_path)
    for i in dirs:
        tmp_dir=join(real_path,i)
        if dir_is_empty(tmp_dir):
            btn="""<a class="badge btn btn-danger" onclick="removeFile('%s')">删除</a>"""%join(relative_path,i)
        else:
            btn=""
        print  """<li class="list-group-item">
                    <i class="ion-ios-folder"></i>
                    <a onclick="listFile('%s')">
                        %s
                    </a>
                    %s
                </li>""" % (join(relative_path,i), i, btn)

    for i in files:
        print """<li class="list-group-item">
                    <i class="ion-document-text"></i>
                    <a href="%s" target="_blank">
                        %s
                    </a>
                    <a class="badge btn btn-danger" onclick="removeFile('%s')">删除</a>
                </li>""" % (join(www_path,i), i, join(relative_path,i))
