from levenshtein.leven_squash import LevenSquash
from levenshtein.compression import Compressor, CRCCompression
import sys
import os
import glob
import argparse
import itertools
import json

def serialize(filename1, filename2):
    return "__AND__".join(sorted((filename1, filename2)))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-N", metavar="N", type=int, required=True)
    parser.add_argument("-C", metavar="C", type=int, required=True)

    args = parser.parse_args()
    N = args.N
    C = args.C

    data_dir = os.path.join(os.path.dirname(__file__), "data")
    results_dir = os.path.join(data_dir,"results")

    ls = LevenSquash(compressor=Compressor(CRCCompression(), N=N, C=C))

    results_filename = os.path.join(results_dir, "run_%s_%s.json" % (N, C))
    results = {}

    files = map(os.path.basename, glob.glob(os.path.join(data_dir, "*.txt")))
    for filename1, filename2 in itertools.combinations(files, 2):
        with open(os.path.join(data_dir, filename1)) as f1, \
                open(os.path.join(data_dir, filename2)) as f2:
            s1 = f1.read()
            s2 = f2.read()
            results[serialize(filename1, filename2)] = ls.estimate(s1, s2)

    with open(results_filename, 'w') as results_file:
        json.dump(results, results_file)

if __name__ == "__main__":
    main()

