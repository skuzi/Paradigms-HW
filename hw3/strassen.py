import numpy as np
import math


def strassen(a, b):
    n = len(a)
    assert n == len(b)
    assert len(a[0]) == len(b[0])
    if n <= 64:
        return np.dot(a, b)
    else:
        a11 = a[:(n//2), :(n//2)]
        a12 = a[:(n//2), (n//2):]
        a21 = a[(n//2):, :(n//2)]
        a22 = a[(n//2):, (n//2):]

        b11 = b[:(n//2), :(n//2)]
        b12 = b[:(n//2), (n//2):]
        b21 = b[(n//2):, :(n//2)]
        b22 = b[(n//2):, (n//2):]

        p1 = strassen(a11 + a22, b11 + b22)
        p2 = strassen(a21 + a22, b11)
        p3 = strassen(a11, b12 - b22)
        p4 = strassen(a22, b21 - b11)
        p5 = strassen(a11 + a12, b22)
        p6 = strassen(a21 - a11, b11 + b12)
        p7 = strassen(a12 - a22, b21 + b22)

        c11 = p1 + p4 - p5 + p7
        c12 = p3 + p5
        c21 = p2 + p4
        c22 = p1 - p2 + p3 + p6

        return np.vstack((np.hstack((c11, c12)), np.hstack((c21, c22))))


def main():
    n = int(input())
    a = [[int(j) for j in input().split()] for i in range(n)]
    b = [[int(j) for j in input().split()] for i in range(n)]
    realsize = 2 ** (math.ceil(math.log(n, 2)))
    print(realsize)
    a = np.array(a)
    print(a)
    b = np.array(b)
    print(b)
    if realsize != n:
        a = np.vstack((np.hstack((a, np.array([[0 for i in range(realsize - n)] for j in range(n)]))), np.array([[0 for i in range(realsize)] for j in range(realsize - n)])))
        b = np.vstack((np.hstack((b, np.array([[0 for i in range(realsize - n)] for j in range(n)]))), np.array([[0 for i in range(realsize)] for j in range(realsize - n)])))
    c = strassen(a, b)
    print(c[:n, :n])


if __name__ == "__main__":
    main()
