import sys
import os
import json
import levenshtein.distance


class TrueDistanceCache:

    def __init__(self, filename=None, data_dir=None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(__file__), "data/")
        if filename is None:
            filename = os.path.join(data_dir, "cache", "cache.json")

        self.filename = filename
        self.data_dir = data_dir

        if os.path.isfile(filename):
            with open(filename) as cache_file:
                self.cache = json.load(cache_file)
        else:
            self.cache = {}

        self.levenshtein = levenshtein.distance.Absolute()

    def serialize(self, filename1, filename2):
        return "__AND__".join(sorted((filename1, filename2)))

    def distance(self, filename1, filename2):
        filename1 = os.path.join(self.data_dir, filename1)
        filename2 = os.path.join(self.data_dir, filename2)

        with open(filename1) as file1, open(filename2) as file2:
            return self.levenshtein(file1.read(), file2.read())

    def get(self, filename1, filename2):
        key = self.serialize(filename1, filename2)
        if key not in self.cache:
            self.cache[key] = self.distance(filename1, filename2)
            self.save()
        return self.cache[key]

    def __getitem__(self, files):
        return self.get(*files)

    def save(self, filename=None):
        if filename is None:
            filename = self.filename

        with open(filename, 'w') as cache_file:
            json.dump(self.cache, cache_file)

cache = TrueDistanceCache()
self = sys.modules[__name__]

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: %s filename1 filename2\n" % sys.argv[0])
        sys.stderr.flush()
        sys.exit(1)
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    print cache.get(filename1, filename2)
else:
    sys.modules[__name__] = cache
