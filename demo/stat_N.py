from demo import cache
import glob
import os
import itertools
import json
from collections import defaultdict
import sys

def get_errors(N):
    C = 140

    data_dir = os.path.join(os.path.dirname(__file__), "data")
    results_dir = os.path.join(data_dir, "results")
    
    errors = []

    with open(os.path.join(results_dir, "run_%s_%s.json" % (N, C))) \
            as data_file:
        data = json.load(data_file)
        for key in data:
            error = (data[key] - cache.cache[key]) / float(cache.cache[key])
            error = abs(error)
            errors.append(error)

    average = sum(errors) / float(len(errors))
    return N, max(errors), min(errors), average

errors = []
for N in range(1, 41):
    errors.append(get_errors(N))

errors.sort(key=lambda x: x[3])
for line in errors:
    print line
