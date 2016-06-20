#from levenshtein.config.logging import LoggerManager
import logging

from nose.tools import assert_true, assert_equals


class TestCompressorClassBase:
    """
    Base test class for Compressor test classes.
    """
#    __test__ = False

    logger = logging.getLogger()
    #logger = LoggerManager.get_logger()

    Compressor = None

    setup_method_msg = "Calling a Compressor test method."
    teardown_method_msg = "Tearing down a Compressor test method."
    setup_class_msg = "Setting up a Compressor test class."
    teardown_class_msg = "Tearing down Compressor test class."

    filename = "/home/dwcoates/workspace/leven-squash/levenshtein/demo/data/10001.txt"
    finput = ''
    with open(filename, 'r') as f:
        finput = f.read()

    def shortDescription(self):
        """
        Get the one-liner description of the function to be displayed.
        """

        doc = self._testMethodDoc
        doc = doc and doc.split("\n")[0].strip() or ""
        if "%(component)s" in doc:
            doc = doc % {'component':self.component.__name__}
        doc = "%s : %s" % (self.__class__.__name__, doc)

        return doc

    @classmethod
    def setup_class(cls):
        print(cls.setup_class_msg)

        # for base in cls.__bases__:
        #     assert_equals(base.__name__, "ACompressor")

    @classmethod
    def teardown_class(cls):
        print(cls.teardown_class_msg)

    def setup(self):
        print(self.setup_method_msg)

    def teardown(self):
        print(self.teardown_method_msg)

    def test_compression_signature_size(self):
        pass

    @classmethod
    def _test_compression_signature_size(cls, string, c, n):
        sc = cls.Compressor(c, n)

        signature = sc.compress(string)
        sig_length = len(signature)
        sig_expected_len = len(string)/sc.getC()

        error = abs(sig_expected_len-sig_length)/sig_expected_len

        acceptable_error = .01

        assert_true(error <= acceptable_error)

        #produce error messages
