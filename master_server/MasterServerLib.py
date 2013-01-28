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
        print("> Entering function: " + self.fun.__name__ + "\nArgs: ")
        for i in args :
            print(i + ", ")
        print("\n")
        ret = self.fun(*args, **kargs)
        print("< Function " + self.fun.__name__ + " returned: " + ret + "\n")

