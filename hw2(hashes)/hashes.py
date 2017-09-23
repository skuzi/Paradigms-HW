import sys
import os
from hashlib import sha1 as hasherr

pathes = []
hasher = hasherr()


def go(directory):
    for d, dirs, files in os.walk(directory):
        for f in files:
            if f[0] != '~' and f[0] != '.' and not os.path.islink(f_pname):
                pathes.append(os.path.join(d, f))
        for dirr in dirs:
            go(dirr)


def get_hash(filename):
    with open(filename, mode='rb') as f:
        while True:
            data = f.read(8192)
            if not data:
                break
            hasher.update(data)
    return hasher.digest()

def main():
    params = sys.argv
    if len(params) > 1:
        directory = params[1]
    go(directory)
    hashes = {}
    for path in pathes:
        h = get_hash(path)
        if h not in hashes:
            hashes[h] = [1, [path]]
        else:
            hashes[h][1].append(path)
            hashes[h][0] += 1
        hasher = hasherr()
    for cnt, files in hashes.values():
        if cnt > 1:
            print(':'.join(files))
if __name__ == "__main__":
    main()