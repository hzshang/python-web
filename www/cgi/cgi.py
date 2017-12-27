import os
import importlib
from cStringIO import StringIO
import sys


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


def dup(func):
    def dup_fun(*args, **kw):
        with Capturing() as output:
            func(*args, **kw)
        return "\r\n".join(output)

    return dup_fun


def map():
    files = os.listdir("./www/cgi/")
    files.remove("__init__.py")
    files.remove("cgi.py")
    dir = {}
    files = [x[:-3] for x in files if x[-3:] == ".py"]
    for i in files:
        tmp = importlib.import_module("www.cgi." + i)
        reload(tmp)
        func = getattr(tmp, "main")
        dir[i] = dup(func)
    return dir
