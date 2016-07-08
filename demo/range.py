import pprint

from levenshtein.leven_squash import *
from itertools import product
from levenshtein.compression import Compressor, CRCCompression
from levenshtein.score import ScoreDistance
from levenshtein.distance import Absolute


def read(fname):
    with open(fname) as f:
        data = f.read().replace('\n', '')

    return data

distance = Absolute()

pp = pprint.PrettyPrinter(indent=4)

huck = read("../demo/data/adventures_of_huckleberry_finn.txt")
sawyer = read("../demo/data/adventures_of_tom_sawyer.txt")
sibbald = read("../demo/data/dantes_inferno_english_sibbald.txt")
longfellow = read("../demo/data/dantes_inferno_english_longfellow.txt")
italian = read("../demo/data/dantes_inferno_italian.txt")
sample_en = read("../demo/data/test1.txt")
sample_la = read("../demo/data/test2.txt")

dist_huck_sawyer = 124865
dist_sibbald_longfellow = 102076
dist_longfellow_italian = 106560
dist_huck_longfellow = 122229
dist_loremIpsum_en_la = 724

# print("calculating huck, sawyer")
# dist_dist = distance(huck, sawyer)
# print("calculating sibbald, longfellow: ")
# dist_sibbald_longfellow = distance(sibbald, longfellow)
# print("calculating longfellow, italian: ")
# dist_longfellow_italian = distance(longfellow, italian)
# print("calculating huck, longfellow")
# dist_huck_longfellow = distance(huck, longfellow)
# print("calculating lorem ipsum")
# dist_loremIpsum_en_la = distance(sample_en, sample_la)

C1 = 100
C2 = 200
N1 = 5
N2 = 50
STEP_C = 10
STEP_N = 5


def results_over_n(str1, str2, n1, n2, c, step=10):
    def LS(c, n): return LevenSquash(Compressor(CRCCompression(), C=c, N=n))


def estimate(str1, str2, c, n):
    def LS(_c, _n): return LevenSquash(
        Compressor(CRCCompression(), C=_c, N=_n))
    return LS(c, n).estimate(str1, str2)


def results_over_c_and_n(str1, str2, c1=C1, c2=C2, n1=N1, n2=N2, step_c=STEP_C,
                         step_n=STEP_N, true_dist=None):
    if not (n2 > n1 > 0) or not (c2 > c1 > 0):
        print()
        raise ValueError("n1,n2 and c1,c2 must be positive with x1<x2" +
                         "n1=%s,n2=%s : c1=%s,c2=%s" % (n1, n2, c1, c1))

    diff = ScoreDistance.difference
    c_and_n = product(xrange(c1, c2, step_c), xrange(n1, n2, step_n))

    def err(str1, str2, c, n, distance):
        return diff(estimate(str1, str2, c, n), distance)

    print ("estimating over ranges C=%s,%s and N=%s,%s" % (c1, c2, n1, n2))

    if true_dist is None:
        print("Calculating true distance...")
        true_dist = Absolute()(str1, str2)

    results = [(err(str1, str2, c, n, true_dist), c, n) for c, n in c_and_n]

    return sorted(results)


huck_sawyer = results_over_c_and_n(huck, sawyer, true_dist=dist_huck_sawyer)

sibbald_longfellow = results_over_c_and_n(
    sibbald, longfellow, true_dist=dist_sibbald_longfellow)

longfellow_italian = results_over_c_and_n(
    longfellow, italian, true_dist=dist_longfellow_italian)

huck_longfellow = results_over_c_and_n(
    huck, longfellow, true_dist=dist_huck_longfellow)
