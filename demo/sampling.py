from itertools import combinations, islice
from os import listdir
from os.path import isfile, join
import time
import cPickle

from levenshtein.utils.stringer import random_string as r
from levenshtein.utils.misc import nCr
from levenshtein.compression import Compressor, CRCCompression


def read(fname):
    with open(fname) as f:
        data = f.read().replace('\n', '')

    return data


def read_files(directory, length, num):
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

    return list(islice(combinations(chunks, 2), 0, num))


def average(samples):
    return sum([distance(str1, str2) for str1, str2 in samples]) / len(samples)


def average_file(directory, length, num):
    sources = read_files(directory, length, num)

    dists = []
    count = 0
    for x, y in sources:
        count = count + 1
        print("Progress: %s/%s" % (count, len(sources)))
        dists.append(distance(x, y))

    return sum(dists) / float(len(sources)) / float(length)


def average_random(length, num):
    s = 0
    count = 0
    start = time.clock()
    for i in xrange(num):
        count += 1
        print("Progress: %s/%s" % (count, num))
        s += (r(length), r(length))

    print("Time to compute: %s" % (time.clock() - start))

    return s / float(num)


def average_sig_file(directory, length, num, c, n1, n2, compressor=None):
    if compressor is None:
        compressor = Compressor(compression=CRCCompression(), N=10)
    sources = read_files(directory, length, num)

    count = 0
    res = []
    for n in xrange(n1, n2):
        dists = []
        compressor.setN(n)
        count = count + 1
        print("Progress: %s/%s" % (count, (n2 - n1)))
        for (x, y) in sources:
            sigx = compressor.compress(x)
            sigy = compressor.compress(y)
            if len(sigx) + len(sigy) != 0:
                dists.append(distance(sigx, sigy) /
                             ((len(sigx) + len(sigy)) / 2.0))

        res.append((sum(dists) / float(len(sources)), n, c))

    cPickle.dump(res, open(join(directory, "avg_sig_distance") + '.p', 'wb'))

    return res
