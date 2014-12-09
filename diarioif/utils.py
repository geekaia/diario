# -*- coding: utf-8 -*-

#from decimal import Decimal
from decimal import *
from unicodedata import normalize



class fakefloat(float):
    def __init__(self, value):
        self._value = value
    def __repr__(self):
        return str(self._value)

def defaultencode(o):
    if isinstance(o, Decimal):
        # Subclass float with custom repr?
        return fakefloat(o)
    raise TypeError(repr(o) + " is not JSON serializable")


def remover_acentos(txt, codif='utf-8'):
    #print "Txt: ", txt
    try:
        decoded = txt.decode(codif)
    except:
        #print "Tipo: ",  type(txt)
        decoded = txt


    return normalize('NFKD', decoded).encode('ASCII', 'ignore')

    if __name__ == '__main__':
        from doctest import testmod
        testmod()
