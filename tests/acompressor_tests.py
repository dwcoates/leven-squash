from levenshtein.compression import ACompressor

from base_compressor_test_class import BaseCompressorTestClass


class TestACompressor(BaseCompressorTestClass):
    setup_method_msg = "Calling ACompressorTest method: "
    teardown_method_msg = "Tearing down ACompressorTest function"
    setup_class_msg = ""
    teardown_class_msg = "Tearing down ACompressorTest class"

    def __init__(self):
        self.sc = ACompressor()
        self.filename = "/home/dwcoates/workspace/leven-squash/data/10001.txt"
        with open(self.filename, 'r') as f:
            self.finput = f.read()

    @classmethod
    def setup_class(self):
        pass

    @classmethod
    def teardown_class(self):
        print(ACompressorTest.teardown_class_msg)

    def setup(self):
        print(ACompressorTest.setup_method_msg)
        print("Compression factor: " + str(self.sc.C))
        print("Neighborhood size: " + str(self.sc.N))
        print("Location of data to be compressed: " + self.filename)

    def teardown(self):
        print(ACompressorTest.teardown_method_msg)

    def test_get_and_set(self):
        """For testing working @properties. Mostly for sanity-checking relavent Python knowledge."""

        n = 6
        print("Setting value of neighborhood size N to: " + str(n))
        self.sc.N = n

        c = 40
        print("Setting value of compression factor C to: " + str(c))
        self.sc.C = c

        try:
            print("Compressor.getN(): " + str(self.sc.N))
            print("Compressor.getC(): " + str(self.sc.C))
        except Exception as ex:
            print(ex.message())
