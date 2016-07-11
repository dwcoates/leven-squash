import pprint

from levenshtein.distance import Absolute
import cache

data_dir = "./data/"
results_dir = "./data/results"

string_distance = Absolute()
file_distance = cache.get

pp = pprint


def read(fname):
    with open(fname) as f:
        data = f.read().replace('\n', '')

    return data

exclude_files = ["__init__.py"
                 ]
