from levenshtein.compression import Compressor, StringCompressorBasic

import TestCompressor

# Tests for the most basic compression algorithm.
class BasicCompressorTest (TestCompression):
    def __init__(self):
        self.sc = StringCompressorBasic()

    @classmethod
    def setup_class(cls):
        BasicCompressorTest.setup_method_msg = "Calling TestCompression method: "
        BasicCompressorTest.teardown_method_msg = "Tearing down TestCompression function"
        BasicCompressorTest.setup_class_msg = ""
        BasicCompressorTest.teardown_class_msg = "Tearing down TestCompression class"
    @classmethod
    def teardown_class(cls):
        pass

    def setup(self):
        pass
    def teardown(self):
        pass

    def basic_compression_algorithm_test(self):
        print("Testing StringCompressorBasic.compress(str)...")
        print("Compression of contents at '" +
              BasicCompressorTest.filename +
              "':\n" +
              str(BasicCompressorTest.sc.compress(BasicCompressorTest.finput)))
