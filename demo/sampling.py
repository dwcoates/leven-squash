from itertools import combinations, islice
from os import listdir
from os.path import isfile, join
import pprint
import time

from levenshtein.utils.stringer import random_string as r
from levenshtein.distance import Absolute
from levenshtein.utils.misc import nCr


data_dir = "./data/"

distance = Absolute()

pp = pprint


def read(fname):
    with open(fname) as f:
        data = f.read().replace('\n', '')

    return data


def average(samples):
    return sum([distance(str1, str2) for str1, str2 in samples]) / len(samples)


def average_random(length, num):
    s = 0
    count = 0
    start = time.clock()
    for i in xrange(num):
        count += 1
        print("Progress: %s/%s" % (count, num))
        s += distance(r(length), r(length))

    print("Time to compute: %s" % (time.clock() - start))

    return s / float(num)


def average_file(directory, length, num):
    files = [join(directory, f)
             for f in listdir(directory) if isfile(join(directory, f))]

    # make sure there are enough text chunks to make num combinations
    # of them.
    txt = ""
    count = 0
    for f in files:
        print("reading %s..." % (f))
        txt += read(f)
        num_chunks = len(txt) / length
        count = count + 1
        if num < nCr(num_chunks, 2):
            break

    print("Read %s/%s files in '%s'" % (count, len(files), directory))

    chunks = [txt[x:x + length] for x in range(0, len(txt), length)]

    print("Calculating distance average of %s measurements of text " +
          "strings length %s...") % (num, length)
    sources = list(islice(combinations(chunks, 2), 0, num))

    dists = []
    count = 0
    for x, y in sources:
        count = count + 1
        print("Progress: %s/%s" % (count, len(sources)))
        dists.append(distance(x, y))

    return sum(dists) / float(len(sources)) / float(length)
