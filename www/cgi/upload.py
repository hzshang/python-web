# coding = utf-8
from const import *
def main(get,post):
    name=post["name"]
    file=post["file"]
    dir=post["dir"]
    real_path= join(ABS_WWW,dir,name)
    with open (real_path,"w+") as f:
        f.write(file)

