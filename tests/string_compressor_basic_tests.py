from levenshtein.compression import StringCompressorBasic

from base_compressor_test_class import BaseCompressorTestClass

# Tests for the most basic compression algorithm.
class TestStringCompressorBasic (BaseCompressorTestClass):
    @classmethod
    def setup_class(cls):
        TestStringCompressorBasic.setup_method_msg = "Calling TestCompression method: "
        TestStringCompressorBasic.teardown_method_msg = "Tearing down TestCompression function"
        TestStringCompressorBasic.setup_class_msg = ""
        TestStringCompressorBasic.teardown_class_msg = "Tearing down TestCompression class"

    @classmethod
    def teardown_class(cls):
        pass

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_compression_signature_size(self):
        # logger start msg

        # get some test files
        filename = ''

        for i in range(50, 150):
            self._test_compression_signature_size(filename, i, 8)
