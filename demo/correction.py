from itertools import product, combinations
from os import listdir
from os.path import isfile, join
import time
import json

from ranges import read, absolute_distance, exclude_files
from levenshtein.score import ScoreDistance
from levenshtein.compression import Compressor
from utils import *


n = 10
c = 140
correction_factor = .784 / 0.953
diff = ScoreDistance.difference


def file_results(f1, f2):
    comp = Compressor(C=c, N=n)

    name = "%s__AND__%s" % (f1, f2)

    print("Calculating distance of %s..." % name)
    true_dist = file_distance(f1.split('/')[1], f2.split('/')[1])

    str1 = read(f1)
    str2 = read(f2)

    print("Estimating...")
    sig1 = comp.compress(str1)
    sig2 = comp.compress(str2)

    estimate = Absolute()(sig1, sig2) * c

    corrected_estimate = estimate * correction_factor

    print("Done.")
    return (name,
            true_dist,
            (estimate, diff(estimate, true_dist)),
            (corrected_estimate, diff(corrected_estimate, true_dist)))


def dir_results(directory):
    print("N=%s" % n)
    print("Correction factor: %s" % correction_factor)
    dir_files = [join(directory, f)
                 for f in listdir(directory) if isfile(join(directory, f))]
    dir_files = [f for f in dir_files if f not in exclude_files]

    sources = list(combinations(dir_files, 2))

    print("Getting range results for appropriate files in '" + directory + "'")
    print("%s usable files in '%s'" % (len(dir_files), directory))
    print("%s such file pairs for which to produce range results.\n\n" %
          (len(sources)))

    res = []
    count = 0
    t = 0
    for f1, f2 in sources:
        print("Producing results for '%s' and '%s'" % (f1, f2))
        count = count + 1
        start = time.clock()
        res.append(file_results(f1, f2))
        end = time.clock() - start
        t += end
        print("%s/%s sources processed. Result time: %s\nTotal time: %s\n\n" %
              (count, len(sources), end, t))

    with open("estimations_stats.json", 'w') as f:
        json.dump(res, f)

    return res
