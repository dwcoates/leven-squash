# Calculate average similarity between random strings of equal length

from levenshtein import leven_squash
from levenshtein.utils import stringer

str_len = 1
num_iters = 2000
sum = 0
r = stringer.random_string
ls = leven_squash.LevenSquash()

print("Calculating...")
for i in range(num_iters):
    est = ls.calculate(r(str_len), r(str_len))
    sum += est
calc_diff = abs(1 - sum / float(str_len*num_iters))

print("Done.")

comp = ls.get_compressor()
alg = ls.get_ld_alg()

alpha_len = len(comp.get_alphabet())
# The expected difference between two strings is probability of a collision between
# two randomly generated strings for a given character (1/alpha_len) divided by the 
# length of the strings (str_len).
exp_diff = 1/float(alpha_len)

print("Compression scheme: " + comp.__class__.__name__ +
      "\nCompression alphabet length: " + str(alpha_len) +
      "\nLD algorithm: " + alg.__class__.__name__ +
      "\nCalculated similarity: " + str(calc_diff) +
      "\nExpected similarity: " + str(exp_diff))
