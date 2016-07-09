from itertools import combinations, islice
from os import listdir
from os.path import isfile, join
import pprint
import math

pp = pprint

from levenshtein.utils.stringer import random_string as r
from levenshtein.distance import Absolute


data_dir = "./data/"
distance = Absolute()


def read(fname):
    with open(fname) as f:
        data = f.read().replace('\n', '')

    return data


def nCr(n, r):
    f = math.factorial
    return f(n) / f(r) / f(n - r)


def average(samples):
    return sum([distance(str1, str2) for str1, str2 in samples]) / len(samples)


def average_random(length, num):
    s = 0
    for i in xrange(num):
        s += distance(r(length), r(length))

    return s / float(num)


def average_file(directory, length, num):
    files = [join(directory, f)
             for f in listdir(directory) if isfile(join(directory, f))]

    # make sure there are enough text length-length chunks to make
    # num combinations of them.
    txt = ""
    for f in files:
        print("reading %s..." % (f))
        txt += read(f)
        num_chunks = len(txt) / length
        if num < nCr(num_chunks, 2):
            break

    chunks = [txt[x:x + length] for x in range(0, len(txt), length)]

    print("Calculating distance average of %s measurements of text " +
          "strings length %s..." %
          (num, length))
    sources = list(islice(combinations(chunks, 2), 0, num))

    s = sum([distance(x, y) for x, y in sources]) / float(len(sources))

    return s / float(length)
