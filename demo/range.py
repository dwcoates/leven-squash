import cPickle
import pprint
import math
from os import listdir
from os.path import isfile, join

from levenshtein.leven_squash import *
from itertools import product, combinations
from levenshtein.compression import Compressor, CRCCompression
from levenshtein.score import ScoreDistance
import levenshtein.distance


def read(fname):
    with open(fname) as f:
        data = f.read().replace('\n', '')

    return data

data_dir = "./data/test"
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

    error = ScoreDistance.error
    c_and_n = product(xrange(c1, c2, step_c), xrange(n1, n2, step_n))

    def err(s1, s2, _c_, _n_, distance):
        # print("Calling estimate on c=%s, n=%s" % (c, n))
        return error(distance, estimate(s1, s2, _c_, _n_))

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
    print("Number of results: %s (expected=%s)\n" %
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
    print("%s such file pairs for which to produce range results.\n\n" %
          (len(sources)))

    return zip(*[file_results(f1, f2) for (f1, f2) in sources])


def test_and_save(test_name, directory=data_dir):
    res = dir_results(directory)

    cPickle.dump(res, open(join(directory, test_name) + '.p', 'wb'))

    return res


def load_test_results(test_name, directory=data_dir):
    return cPickle.load(open(join(directory, test_name) + '.p', 'rb'))


def sanity_check(test_results):
    """
    Test to ensure that results list is organized as expected.
    """
    checks = 0
    length_test = len(test_results[0])
    for x in xrange(len(test_results)):
        if len(test_results[x]) != length_test:
            raise Exception(
                "Results test[%s] and test[%s] have different length" %
                (x, y))
        for y in xrange(x + 1, len(test_results)):
            for i in xrange(len(test_results[x])):
                err_x_i = test_results[x][i][0][0]
                err_y_i = test_results[y][i][0][0]
                if test_results[x][i][0][0] > test_results[y][i][0][0]:
                    error = "Error for test[%s]=%s < test[%s]=%s" % (
                        x, err_x_i, y, err_y_i)
                    error = ("If x<y, error of test[x][i] should be less " +
                             " than test[y][i] for all i")
                    print "TEST RESULTS " + str(x)
                    pp.pprint(test_results[x])
                    print "\n\nTEST RESULTS " + str(y)
                    pp.pprint(test_results[y])
                    raise Exception(error)
                checks += 1

    print("error in test[x][i] < error in test[y][i] : x < y for all i")
    print("%s checks. Expected %s checks" %
          (checks, length_test * sum(xrange(len(test_results))))
          )
