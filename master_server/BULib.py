import string
import random

def genRandString(dl = 10):
    ret = ''
    for i in range(dl) :
        ret += random.choice(string.ascii_letters + string.digits)
    return ret

class myDebug(object) :
    """ class to debug - print args, resaults and names """
    def __init__(self, fun) :
        self.fun = fun
    def __call__(self, *args, **kargs) :
        argsList = ""
        for i in args :
            argsList += str(i) + ", "
        print("> Entering function: " + self.fun.__name__ + "\nArgs: " + argsList)
        ret = self.fun(*args, **kargs)
        print("< Function " + self.fun.__name__ + " returned: " + str(ret) + "\n")
        return ret
