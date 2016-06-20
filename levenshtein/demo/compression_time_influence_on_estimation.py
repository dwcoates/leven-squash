import time

from decimal import *

from levenshtein.utils import stringer
from levenshtein.leven_squash import LevenSquash
from levenshtein.score import ScoreDistance
from levenshtein.compression import StringCompressorBasic

getcontext().prec = 6

r = stringer.random_string


def demo():
    ls = LevenSquash()

    BIG_STR_LEN = 10000

    print("Random string length: " + str(BIG_STR_LEN))

    start = time.clock()
    r1 = r(BIG_STR_LEN)
    r2 = r(BIG_STR_LEN)
    end = time.clock()

    print("Time to generate two random strings: " + str(end-start) + "\n")

    compression_factor = ls.get_compressor().getC()
    print("Compression factor: " + str(compression_factor) + "\n")

    start = time.clock()
    sig1 = ls.compress(r1)
    end = time.clock()
    t_sig1 = end-start

    print("Time to compress random string: " + str(t_sig1))

    sig1_len = len(sig1)
    expected_len = BIG_STR_LEN/compression_factor

    print("Compressed string length: " + str(sig1_len))
    print("Expected Compressed string length: " + str(expected_len))
    print("Difference: " + str(ScoreDistance.difference(sig1_len,
                                                        expected_len)) +
          "\n")

    start = time.clock()
    sig2 = ls.compress(r2)
    end = time.clock()
    t_sig2 = end-start

    print("Time to compress random string: " + str(t_sig2))

    sig2_len = len(sig2)
    expected_len = BIG_STR_LEN/compression_factor

    print("Compressed string length: " + str(sig2_len))
    print("Expected Compressed string length: " + str(expected_len))
    print("Difference: " + str(ScoreDistance.difference(sig2_len,
                                                        expected_len)) +
          "\n")

    t_sig_total = t_sig1 + t_sig2
    print("Total time to compress strings into signatures: " +
          str(t_sig_total) + "\n")

    start = time.clock()
    calc = ls.calculate(r1, r2)
    end = time.clock()
    t_calc = end-start

    print("Calculated distance: " + str(calc))
    print("Time to calculate LD: " + str(t_calc) + "\n")

    start = time.clock()
    sig_dist = ls.calculate(sig1, sig2)
    end = time.clock()
    t_est = end-start
    t_est_total = t_est + t_sig_total
    est = sig_dist*compression_factor

    print("Estimated distance: " + str(est))
    print("Time to estimate LD (not including compression): " + str(t_est))
    print("Time to estimate LD (total time): " + str(t_est_total) + "\n")

    est_err = ScoreDistance.error(est, calc)
    print("Estimate error: " + "{:.3f}%".format(est_err*100))

    print("Speedup (not including compression time): " + str(int(t_calc/t_est)) +
          "x")
    print("Speedup (including compression time): " + str(int(t_calc/t_est_total)) +
          "x")

    compression_time_factor = t_sig_total/t_est_total
    print("Portion of estimation time spent on compression: " +
          str(Decimal(compression_time_factor)*Decimal(100)) + "%")


def time_compression(sc=StringCompressorBasic()):
    BIG_STR_LEN = 10000
    t_total = 0
    num_iters = 100
    len_sum = 0

    print("Compressing with " + sc.compress.__name__ + "...")
    print("Compression factor C: " + str(sc.getC()))
    print("Neighborhood size N: " + str(sc.getN()))

    for i in xrange(num_iters):
        r1 = r(BIG_STR_LEN)

        start = time.clock()
        sig = sc.compress(r1)
        end = time.clock()
        t = end - start
        sig_len = len(sig)

        len_sum += sig_len
        t_total += t

    avg_len = len_sum / num_iters
    t_avg = t_total/num_iters

    print("Finished.")
    print("Time to compress '" + str(num_iters) + "' strings of length '" +
          str(BIG_STR_LEN) + "': " + str(t_total)) 
    print("Average time per compression: " + str(t_avg))
    print("Average length of compressions: " + str(avg_len))
