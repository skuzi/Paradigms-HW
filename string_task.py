def verbing(s):
    if len(s) >= 3:
        if s[-3:] == "ing":
            s += "ly"
        else:
            s += "ing"
    return s


def not_bad(s):
    a = s.find('not')
    b = s.find('bad')
    if a < b:
        s = s[:a] + 'good' + s[b + 3:]
    return s


def front_back(a, b):
    n = len(a)
    m = len(b)
    a_front = a[:(n + 1)//2]
    b_front = b[:(m + 1)//2]
    a_back = a[(n + 1)//2:]
    b_back = b[(m + 1)//2:]
    return a_front + b_front + a_back + b_back