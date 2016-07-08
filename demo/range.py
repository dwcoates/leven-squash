import cPickle
import pprint
from os import listdir
from os.path import isfile, join

from levenshtein.leven_squash import *
from itertools import product
from levenshtein.compression import Compressor, CRCCompression
from levenshtein.score import ScoreDistance
import levenshtein.distance


def read(fname):
    with open(fname) as f:
        data = f.read().replace('\n', '')

    return data

data_dir = "./data/"
exclude_files = ["__init__.py"
                 ]

absolute_distance = levenshtein.distance.Absolute()

pp = pprint.PrettyPrinter(indent=4)

C1 = 100
C2 = 200
N1 = 5
N2 = 75
STEP_C = 10
STEP_N = 5


def estimate(str1, str2, c, n):
    if str1 is None or str2 is None:
        raise TypeError("Strings to be estimated must be str")

    def LS(_c, _n): return LevenSquash(
        Compressor(CRCCompression(), C=_c, N=_n))

    return LS(c, n).estimate(str1, str2)


def results_over_c_and_n(str1, str2, c1, c2, n1, n2, step_c, step_n, true_dist=None):
    if not (n2 > n1 > 0) or not (c2 > c1 > 0):
        raise ValueError("n1,n2 and c1,c2 must be positive with x1<x2" +
                         "n1=%s,n2=%s : c1=%s,c2=%s" % (n1, n2, c1, c1))

    diff = ScoreDistance.difference
    c_and_n = product(xrange(c1, c2, step_c), xrange(n1, n2, step_n))

    def err(s1, s2, c, n, distance):
        # print("Calling estimate on c=%s, n=%s" % (c, n))
        return diff(estimate(s1, s2, c, n), distance)

    if true_dist is None:
        print("Calculating true distance...")
        print("Input length: %s, %s" % (len(str1), len(str2)))
        true_dist = absolute_distance(str1, str2)
        print("Done. Distance: " + str(true_dist))
    else:
        print("True distance: " + str(true_dist))

    print ("Estimating over ranges C=%s,%s and N=%s,%s (distance=%s)" %
           (c1, c2, n1, n2, true_dist))
    results = [(err(str1, str2, c, n, true_dist), c, n) for c, n in c_and_n]
    print("Number of results: %s (expected=%s)" %
          (len(results), ((c2 - c1) / step_c) * ((n2 - n1) / step_n)))

    return sorted(results)


def file_results(f1, f2):
    str1 = read(f1)
    str2 = read(f2)

    print("Producing range results for '%s' and '%s'..." % (f1, f2))
    results = results_over_c_and_n(
        str1, str2, c1=C1, c2=C2, n1=N1, n2=N2, step_c=STEP_C, step_n=STEP_N)

    return zip(results, [("%s__AND__%s" % (f1, f2)) for i in range(len(results))])


def dir_results(directory=data_dir):
    dir_files = [join(data_dir, f)
                 for f in listdir(data_dir) if isfile(join(data_dir, f))]
    dir_files = [f for f in dir_files if f not in exclude_files]

    file_pairs = [(a, b) for (a, b) in product(dir_files, dir_files) if a != b]
    sources = []
    for (a, b) in file_pairs:
        if (b, a) not in sources:
            sources.append((a, b))

    print("Getting range results for appropriate files in '" + data_dir + "'")
    print("%s such file pairs for which to produce range results." %
          (len(sources)))

    return zip(*[file_results(f1, f2) for (f1, f2) in sources])


def test_and_save(test_name, directory=data_dir):
    res = dir_results(directory)

    cPickle.dump(res, open(join(directory, test_name) + '.p', 'wb'))

    return res


def load_test_results(test_name, directory=data_dir):
    return cPickle.load(open(join(directory, test_name) + '.p', 'rb'))
