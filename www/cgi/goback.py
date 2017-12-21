import os
import listdir
def main(get,post):
    dir=get["dir"]
    parent=os.path.dirname(dir)
    listdir.main({"dir":parent},[])
