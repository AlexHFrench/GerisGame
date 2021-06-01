

def white_black():
    """ Infinitely yields:
                'White'
                'Black'
                'White'
                'Black'
                ..etc..
    """
    while True:
        yield 'White'
        yield 'Black'


def flatten(l, ltypes=(list, tuple)):
    """ Flattens an arbitrarily large list or tuple
        Apparently very fast
        Pulled from online >> https://rightfootin.blogspot.com/2006/09/more-on-python-flatten.html
        Author: Mike C. Fletcher, Distribution: BasicTypes library.
    """
    ltype = type(l)
    l = list(l)
    i = 0
    while i < len(l):
        while isinstance(l[i], ltypes):
            if not l[i]:
                l.pop(i)
                i -= 1
                break
            else:
                l[i:i + 1] = l[i]
        i += 1
    return ltype(l)


def sign(a):
    """ Returns one of (-1, 0, 1) for a given integer or float as a representation of its sign
    """
    return bool(a > 0) - bool(a < 0)