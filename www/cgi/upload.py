# coding = utf-8
from const import *
def main(get,post):
    name=post["name"].decode("utf-8")
    file=post["file"]
    dir=post["dir"]
    real_path= join(ABS_WWW,dir,name)
    with open (real_path,"w+") as f:
        f.write(file)

