from itertools import combinations, islice
from os import listdir
from os.path import isfile, join
import pprint

pp = pprint

from levenshtein.utils.stringer import random_string as r
from levenshtein.distance import Absolute

distance = Absolute()


def read(fname):
    with open(fname) as f:
        data = f.read().replace('\n', '')

    return data


def average(samples):
    return sum([distance(str1, str2) for str1, str2 in samples]) / len(samples)


def average_random(length, num):
    s = 0
    for i in xrange(num):
        s += distance(r(length), r(length))

    return s / float(num)


def average_file(fname, num, length):
    txt = read(fname)[0:num * length]

    chunks = [txt[x:x + length] for x in range(0, len(txt), length)]

    sources = list(islice(combinations(chunks, 2), 0, num))

    s = sum([distance(x, y) for x, y in sources]) / float(len(sources))

    return s / float(length)
