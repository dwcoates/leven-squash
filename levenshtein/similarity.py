from math import sqrt
from collections import Counter
from numpy import histogram
from compression import *
from leven_squash import *
from levenshtein.utils.stringer import random_string as r

BIG_NUM = 100000

c = Compressor(CRCCompression(), C=150, N=35, alpha_len=2**16)


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

print("\n")
print("LENGTHS OF STRINGS: ")
print("\thuck: " + str(len(huck)))
print("\tsawyer: " + str(len(sawyer)))
print("\tlongfellow: " + str(len(longfellow)))
print("\titalian: " + str(len(italian)))
print("\tsample_en: " + str(len(sample_en)))
print("\tsample_la: " + str(len(sample_la)))


r1 = Counter(c.compress(r(BIG_NUM)))
r2 = Counter(c.compress(r(BIG_NUM)))
blank = ''.join([' ' for x in range(BIG_NUM)])


def length(vect):
    return sqrt(sum([vect[entry]**2 for entry in vect]))


def dot_product(vect1, vect2):
    return sum([vect1[entry] * vect2[entry] for entry in vect2 & vect2])


def cosine(vect1, vect2):
    cos = dot_product(vect1, vect2) / (length(vect1) * length(vect2))
    if cos < 0:
        raise ValueError("Cosine between two count vectors should be positive")
    return cos


def _cosine(str1, str2, c, n):
    comp = Compressor(CRCCompression(), C=c, N=n, alpha_len=2**16)

    v1 = Counter(comp.compress(str1))
    v2 = Counter(comp.compress(str2))

    return cosine(v1, v2)


def average_over_n(str1, str2, n1, n2, step=10, c=150):
    print ("Calculating average for two strings over ranges N=" +
           str(n1) + "," + str(n2) + "...")

    if n2 > n1 > 0:
        return sum([_cosine(str1, str2, c, n) for n in xrange(n1, n2)]) / (n2 - n1)
    else:
        raise ValueError("n1 and n2 must be positive with n2 greater than n1")


def max_over_n(str1, str2, n1, n2, step=10, c=150):
    if n2 > n1 > 0:
        return max([(_cosine(str1, str2, c, n), i * step + n1)
                    for i, n in enumerate(xrange(n1, n2, step))])
    else:
        raise ValueError("n1 and n2 must be positive with n2 greater than n1")


n1 = 5
n2 = 15

print("AVERAGE OVER N: ")
# print("\thuck and sawyer -- N=" + str(n1) + "," +
#       str(n2) + ": " + str(average_over_n(huck, sawyer, n1, n2)))
# print("\tsibbald and longfellow -- N=" + str(n1) + "," +
#       str(n2) + ": " + str(average_over_n(sibbald, longfellow, n1, n2)))
# print("\tsibbald and italian -- N=" + str(n1) + "," +
#       str(n2) + ": " + str(average_over_n(sibbald, italian, n1, n2)))
# print("\tsample_en and sample_la -- N=" + str(n1) + "," +
#       str(n2) + ": " + str(average_over_n(sample_en, sample_la, n1, n2)))
# print("\ttwo random strings -- N=" + str(n1) + "," +
#       str(n2) + ": " + str(average_over_n(r(BIG_NUM), r(BIG_NUM), n1, n2)))

print("MAX OVER N: ")
print("\thuck and sawyer -- N=" + str(n1) + "," +
      str(n2) + ": " + str(max_over_n(huck, sawyer, n1, n2, step=1)))
print("\thuck and italian -- N=" + str(n1) + "," +
      str(n2) + ": " + str(max_over_n(huck, italian, n1, n2, step=1)))
# print("\tsibbald and longfellow -- N=" + str(n1) + "," +
#       str(n2) + ": " + str(max_over_n(sibbald, longfellow, n1, n2)))
# print("\tsibbald and italian -- N=" + str(n1) + "," +
#       str(n2) + ": " + str(max_over_n(sibbald, italian, n1, n2)))
# print("\tsample_en and sample_la -- N=" + str(n1) + "," +
#       str(n2) + ": " + str(max_over_n(sample_en, sample_la, n1, n2)))
print("\ttwo random strings -- N=" + str(n1) + "," +
      str(n2) + ": " + str(max_over_n(r(BIG_NUM), r(BIG_NUM), n1, n2)))

NUM = 100
# random_average = sum([cosine(Counter(c.compress(r(BIG_NUM))), Counter(
#     c.compress(r(BIG_NUM)))) for x in range(NUM)]) / NUM
# ouput = 0.0202056466416

random_average = 0.0202056466416
print("average for " + str(NUM) + " random strings: " + str(random_average))
