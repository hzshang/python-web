# coding = utf-8
def main(get,post):
    file_name=post["file_name"].replace("./","")
    file=post["file"]
    with open("www/tmp/"+file_name,"w+") as f:
        f.write(file)
    print '<a href="/tmp/%s">file saved in tmp/%s</a>'%(file_name,file_name)
