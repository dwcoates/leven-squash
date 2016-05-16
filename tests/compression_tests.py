from levenshtein.compression import Compressor, StringCompressorBasic

import sys

# this is mostly just practice for using nose and python
class TestCompression:
    sc = Compressor()
    filename = "/home/dwcoates/workspace/leven-squash/data/10001.txt"
    finput = ''
    with open(filename, 'r') as f:
        finput = f.read()

    @classmethod
    def setup(self):
<<<<<<< HEAD
<<<<<<< HEAD
        print("Calling TestCompression method: ")
=======
>>>>>>> 5b2bc16... Debug compression.py, add unit test
=======
>>>>>>> 5b2bc16... Debug compression.py, add unit test
        print("Compression factor C: " + str(TestCompression.sc.getC()))
        print("Neighborhood size N: " + str(TestCompression.sc.getN()))

    @classmethod
    def teardown(self):
<<<<<<< HEAD
<<<<<<< HEAD
        print("Tearing down TestCompression function")
    @classmethod
    def setup_class(self):
        print("TestCompression:setup_class()")
=======
        print("TestCompression:teardown()")
    @classmethod
    def setup_class(self):
>>>>>>> 5b2bc16... Debug compression.py, add unit test
=======
        print("TestCompression:teardown()")
    @classmethod
    def setup_class(self):
>>>>>>> 5b2bc16... Debug compression.py, add unit test
        n = 6
        print("Setting value of neighborhood size N to: " + str(n))
        TestCompression.sc.setN(n)

        c = 40
        print("Setting value of compression factor C to: " + str(c))
        TestCompression.sc.setC(c)
<<<<<<< HEAD
<<<<<<< HEAD
    @classmethod
    def teardown_class(self):
        print("Tearing down TestCompression class")

    def test_basic(name):
        print("TestCompression:test_basic -- Test base class Compressor: ")

        try:
            # add asserts here to check for getC and setC
            print("Compressor.getC(): " + str(TestCompression.sc.getC()))
            print("Compressor.getN(): " + str(TestCompression.sc.getN()))
=======
=======
>>>>>>> 5b2bc16... Debug compression.py, add unit test
        print("TestCompression:setup_class()")
    @classmethod
    def teardown_class(self):
        print("TestCompression:teardown_class()")

    def test_basic(name):
        print("TestCompression:test_construction to test Compressor")

        try:
            print("Compressor.getN(): " + str(x.getN()))
            print("Compressor.getC(): " + str(x.getC()))
<<<<<<< HEAD
>>>>>>> 5b2bc16... Debug compression.py, add unit test
=======
>>>>>>> 5b2bc16... Debug compression.py, add unit test
        except Exception as e:
            print("Print error: " + str(e))

class TestCompressionBasic (TestCompression):
    sc = StringCompressorBasic()

    def setup(self):
        print("Compression factor C: " + str(TestCompressionBasic.sc.getC()))
        print("Neighborhood size N: " + str(TestCompressionBasic.sc.getN()))
    def teardown(self):
        print("")

    @classmethod
    def setup_class(self):
<<<<<<< HEAD
<<<<<<< HEAD
        print("Setting up TestCompressorBasic for testing StringCompressionBasic module: ")
=======
>>>>>>> 5b2bc16... Debug compression.py, add unit test
=======
>>>>>>> 5b2bc16... Debug compression.py, add unit test
        # will need to modify c and n for testing
        pass
    @classmethod
    def teardown_class(self):
        print("Tearing down TestCompressionBasic...")

    def test_compression(self):
        print("Compression of contents at '" + TestCompressionBasic.filename + "':\n" + str(TestCompressionBasic.sc.compress(TestCompressionBasic.finput)))
