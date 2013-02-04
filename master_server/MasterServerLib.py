import string
import random

def genRandString(dl = 10):
    """
    Zwraca losowy ciag znakow dlugosci dl. Znaki to male i duze litery alfabetu angielskiego oraz cyfry.
    """
    ret = ''
    for i in range(dl) :
        ret += random.choice(string.ascii_letters + string.digits)
    return ret

class myDebug(object) :
    """
    Klasa do debugu
    Opakowanie nia metody zapewni wypisanie jej wywolan, argumentow i rezultatu
    """
    def __init__(self, fun) :
        self.fun = fun
    def __call__(self, *args, **kargs) :
        print("> Entering function: " + self.fun.__name__ + "\nArgs: ")
        for i in args :
            print(i + ", ")
        print("\n")
        ret = self.fun(*args, **kargs)
        print("< Function " + self.fun.__name__ + " returned: " + ret + "\n")

