from levenshtein.compression import Compressor

import BaseCompressorTestClass

import sys

# this is mostly just practice for using nose and python
class ACompressorTest(BaseCompressorTestClass):
    setup_method_msg = "Calling ACompressorTest method: "
    teardown_method_msg = "Tearing down ACompressorTest function"
    setup_class_msg = ""
    teardown_class_msg = "Tearing down ACompressorTest class"

    def __init__(self):
        self.sc = Compressor()
        pself.filename = "/home/dwcoates/workspace/leven-squash/data/10001.txt"
        finput = ''
        with open(self.filename, 'r') as f:
            finput = f.read()

    @classmethod
    def setup_class(self):
        pass

    @classmethod
    def teardown_class(self):
        print(ACompressorTest.teardown_class_msg)

    def setup(self):
        print(ACompressorTest.setup_method_msg)
        print("Compression factor: " + str(self.sc.getC()))
        print("Neighborhood size: " + str(self.sc.getN()))
        print("Location of data to be compressed: " + self.filename)

    def teardown(self):
        print(ACompressorTest.teardown_method_msg)

    def get_and_set_test(self):
        print("ACompressorTest:get_and_set_test -- Test base class ACompressor: ")

        n = 6
        print("Setting value of neighborhood size N to: " + str(n))
        self.sc.setN(n)

        c = 40
        print("Setting value of compression factor C to: " + str(c))
        self.sc.setC(c)

        try:
            print("Compressor.getN(): " + str(self.sc.getN()))
            print("Compressor.getC(): " + str(self.sc.getC()))
        except Exception as ex:
            print(ex.message())
