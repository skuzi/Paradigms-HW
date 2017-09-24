import numpy as np
import math


def strassen(a, b):
    n = len(a)
    assert n == len(b)
    assert len(a[0]) == len(b[0])
    half = n//2
    if n <= 64:
        return np.dot(a, b)
    else:
        a11 = a[:half, :half]
        a12 = a[:half, half:]
        a21 = a[half:, :half]
        a22 = a[half:, half:]

        b11 = b[:half, :half]
        b12 = b[:half, half:]
        b21 = b[half:, :half]
        b22 = b[half:, half:]

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
    read_a = [[int(j) for j in input().split()] for i in range(n)]
    read_b = [[int(j) for j in input().split()] for i in range(n)]
    realsize = 2 ** (math.ceil(math.log(n, 2)))
    a = np.zeros((realsize, realsize))
    b = np.zeros((realsize, realsize))
    a[:n, :n] = read_a
    b[:n, :n] = read_b
    c = strassen(a, b)
    print(c[:n, :n])


if __name__ == "__main__":
    main()
