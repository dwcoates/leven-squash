from Levenshtein import StringMatcher
import time

class PythonLevenshteinTests:
    def setup(self):
        pass
    def teardown(self):
        pass
    def setup_class(self):
        pass
    def teardown_cass(self):
        pass

    def verify_distance_function(self):
        s1 = "hello"
        s2 = s1 + ", world"
        s3 = s1 + ", dodge"
        sm_diff_len = StringMatcher.StringMatcher(None, s1, s2)
        sm_same_len = StringMatcher.StringMatcher(None, s3, s2)

        print("StringMatcher distance for '" + s1 + "' and '"
              +  s2 + "': " + str(sm_diff_len.distance()))
        print("StringMatcher distance for '" + s3 + "' and '" +  s2
              + "': " + str(sm_same_len.distance()))

    def benchmark_distance_function(self):
        data_path = '/home/dwcoates/workspace/leven-squash/data/'
        filename1 = 'infile1.txt'
        filename2 = 'infile2.txt'
        s1 = ''
        s2 = ''
        with open(data_path + filename1) as f:
            s1 = f.read()
        with open(data_path + filename2) as f:
            s2 = f.read()

        print(len(s1))
        print(len(s2))

        t0 = time.clock()
        dist = StringMatcher.StringMatcher(None, s1, s2).distance()
        t1 = time.clock()
        print("Distance between " + filename1 + " and " + filename2 + ": " + str(dist))
        print("Time to compute absolutely: " + str(t1-t0) + "s")

test = PythonLevenshteinTests()
test.verify_distance_function()
test.benchmark_distance_function()
