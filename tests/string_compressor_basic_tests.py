from levenshtein.compression import StringCompressorBasic

from base_compressor_test_class import TestCompressorClassBase
from levenshtein.utils.stringer import random_string


# Tests for the most basic compression algorithm.
class TestStringCompressorBasic(TestCompressorClassBase):
    Compressor = StringCompressorBasic

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_compression_signature_size_on_random_string(self):
        """
        Ensure compressed random string size within a small amount of error.
        """
        r = random_string
        LARGE_STR_LEN = 100000

        test_str = r(LARGE_STR_LEN)

        for i in range(149, 150):
            self._test_compression_signature_size(test_str, i, 8)
