# Calculate average similarity between random strings of equal length
from math import sqrt

from levenshtein import leven_squash
from levenshtein.utils import stringer

str_len = 1000
num_iters = 10000
sum = 0
r = stringer.random_string
ls = leven_squash.LevenSquash()

print("Calculating for str_len=%s, num_iters=%s..." % (str_len, num_iters))
for i in range(num_iters):
    est = ls.calculate(r(str_len), r(str_len))
    # est = 1 - int(r(str_len) == r(str_len))
    # est = distance(r(str_len), r(str_len))
    sum += est
calc_diff = abs(1 - sum / float(str_len * num_iters))

print("Done.")

comp = ls.get_compressor()
alg = ls.get_ld_alg()

alpha_len = comp.get_alpha_len()

# The expected difference between two strings is probability of a collision
# between two randomly generated strings for a given character (1/alpha_len)
# divided by the length of the strings (str_len).

exp_diff = 1 / float(alpha_len)

# The previous comment is *wrong*. This is because we are using Levenshtein
# distance to determine similarity, not Hamming distance. Substitutions and
# insertions lessen these average distances. The expected similarity is
# 1 / sqrt(alpha_len), according to Navarro. Example: "abcde" and "acdeb"
# have a Hamming distance of 4 and a Levenshtein distance of 1. The ability
# to transpose is responsible for this (transpose 'b' in first string with
# 'b' in second string).

true_exp_diff = 1 / sqrt(alpha_len)

print("Compression scheme: " + comp.get_algorithm().__class__.__name__ +
      "\nCompression alphabet length: " + str(alpha_len) +
      "\nLD algorithm: " + alg.get_algorithm().__class__.__name__ +
      "\nCalculated similarity: " + str(calc_diff) +
      "\nExpected similarity: " + str(exp_diff) +
      "\nTrue expected similarity: " + str(true_exp_diff))
