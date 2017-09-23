import sys
import os
from hashlib import sha1 as hasherr


def get_hash(filename, hasher):
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
    pathes = []
    hasher = hasherr()
    for d, _, files in os.walk(directory):
        for f in files:
            if f[0] != '~' and f[0] != '.' and not os.path.islink(f):
                pathes.append(os.path.join(d, f))
    hashes = {}
    for path in pathes:
        h = get_hash(path, hasher)
        if h not in hashes:
            hashes[h] = [path]
        else:
            hashes[h].append(path)
        hasher = hasherr()
    for files in hashes.values():
        if len(files) > 1:
            print(':'.join(files))


if __name__ == "__main__":
    main()