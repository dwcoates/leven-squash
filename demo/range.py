from levenshtein.leven_squash import *
from itertools import product
from levenshtein.compression import Compressor, CRCCompression
from levenshtein.score import ScoreDistance


def read(fname):
    with open(fname) as f:
        data = f.read().replace('\n', '')

    return data

huck = read("../demo/data/adventures_of_huckleberry_finn.txt")
sawyer = read("../demo/data/adventures_of_tom_sawyer.txt")
sibbald = read("../demo/data/dantes_inferno_english_sibbald.txt")
longfellow = read("../demo/data/dantes_inferno_english_longfellow.txt")
italian = read("../demo/data/dantes_inferno_italian.txt")
sample_en = read("../demo/data/test1.txt")
sample_la = read("../demo/data/test2.txt")

true_huck_sawyer = 124865


def results_over_n(str1, str2, n1, n2, c, step=10):
    def LS(c, n): return LevenSquash(Compressor(CRCCompression(), C=c, N=n))
    if n2 > n1 > 0:
        return zip(xrange(n1, n2), [LS(n, c).estimate(str1, str2) for n in xrange(n1, n2)])
    else:
        raise ValueError("n1 and n2 must be positive with n2 greater than n1")


def estimate(str1, str2, c, n):
    def LS(_c, _n): return LevenSquash(
        Compressor(CRCCompression(), C=_c, N=_n))
    return LS(c, n).estimate(str1, str2)


def results_over_c_and_n(str1, str2, c1, c2, n1, n2, step_c, step_n):
    c_and_n = product(xrange(c1, c2, step_c), xrange(n1, n2, step_n))
    diff = ScoreDistance.difference

    print("calculating distance...")

    def err(str1, str2, c, n):
        # print("estimate: N=%s, C=%s" % (n, c))
        return diff(estimate(str1, str2, c, n), true_huck_sawyer)
    results = [(err(str1, str2, c, n), c, n) for c, n in c_and_n]

    return results

print("Calculating...")
r = results_over_c_and_n(huck, sawyer, c1=100, c2=200,
                         n1=5, n2=50, step_c=10, step_n=5)
