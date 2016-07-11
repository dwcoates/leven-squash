import time

from decimal import *

from levenshtein.utils import stringer
from levenshtein.leven_squash import SmartLevenSquash
from levenshtein.score import ScoreDistance
from levenshtein.compression import Compressor
from levenshtein.utils.computation import ComputationManager

getcontext().prec = 6

r = stringer.random_string

create_comp = ComputationManager.CREATE_COMPUTATION


def demo(compressor=None):
    if compressor is None:
        compressor = Compressor()

    ls = SmartLevenSquash(compressor)
    BIG_STR_LEN = 100000

    print("Random string length: " + str(BIG_STR_LEN))

    r1 = create_comp(r, BIG_STR_LEN)
    r2 = create_comp(r, BIG_STR_LEN)

    print("Time to generate two random strings: %ss\n" %
          (abs(r1.time() - r2.time())))

    compression_factor = ls.getC()
    print("Compression factor: %s\n" % (compression_factor))

    expected_sig_len = BIG_STR_LEN / compression_factor

    def compress_(string):
        sig = ls.compress(string)

        print("Time to compress random string: %ss" % (sig.time()))

        sig_len = len(sig.value())

        print("Compressed string length: %s" % (len(sig.value())))
        print("Expected Compressed string length: %s" % (expected_sig_len))
        print("Difference: %s\n" % (ScoreDistance.difference(sig_len,
                                                             expected_sig_len)))

        return sig

    sig1 = compress_(r1.value())
    sig2 = compress_(r2.value())

    t_sig_total = sig1.time() + sig2.time()
    print("Total time to compress strings into signatures: " +
          str(t_sig_total) + "\n")

    print("Calculating distance between strings length %s, %s" %
          (len(r1.value()), len(r2.value())))

    calc = ls.calculate(r1.value(), r2.value())

    print("Calculated distance: %s" % (calc.value()))
    print("Time to calculate LD: %ss\n" % (calc.time()))

    sig_dist = ls.calculate(sig1.value(), sig2.value())
    t_est_total = sig_dist.time() + t_sig_total
    est = create_comp(lambda: sig_dist.value() * compression_factor)
    t_est = sig_dist.time() + est.time()

    print("Estimated distance: " + str(est.value()))
    print("Time to estimate LD (not including compression): " + str(t_est))
    print("Time to estimate LD (total time): " + str(t_est_total) + "\n")

    est_err = ScoreDistance.difference(est.value(), calc.value())
    print("Estimate error: " + "{:.3f}%".format(est_err * 100))

    print("Speedup (not including compression time): " +
          str(int(calc.time() / t_est)) +
          "x")
    print("Speedup (including compression time): " +
          str(int(calc.time() / t_est_total)) +
          "x")

    compression_time_factor = t_sig_total / t_est_total
    print("Portion of estimation time spent on compression: " +
          str(Decimal(compression_time_factor) * Decimal(100)) + "%")


def time_compression(comp=None):
    BIG_STR_LEN = 10000
    t_total = 0
    num_iters = 100
    len_sum = 0

    if comp is None:
        comp = Compressor()

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
    t_avg = t_total / num_iters

    print("Finished.")
    print("Time to compress '" + str(num_iters) + "' strings of length '" +
          str(BIG_STR_LEN) + "': " + str(t_total))
    print("Average time per compression: " + str(t_avg))
    print("Average length of compressions: " + str(avg_len))
