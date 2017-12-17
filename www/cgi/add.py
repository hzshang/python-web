

def main(get,post):
    if "a" not in get or "b" not in get:
        print "<center><h1>It's a calculator</h1></center>"
    else:
        a=int(get["a"])
        b=int(get["b"])
        print "<center><h1>a + b="+str(a+b)+"</h1></center>"
