import sys

# this is mostly just practice for using nose and python
class BaseCompressorTestClass:
    """
    Base test class for Compressor classes.
    """

    __test__ = False

    setup_method_msg = "Calling a Compressor test method."
    teardown_method_msg = "Tearing down a Compressor test method."
    setup_class_msg = "Setting up a Compressor test class."
    teardown_class_msg = "Tearing down Compressor test class."

    sc = None
    filename = "/home/dwcoates/workspace/leven-squash/data/10001.txt"
    finput = ''
    with open(self.filename, 'r') as f:
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

        for base in cls.__class__.__bases__:
            cls.assertEquals(base.__name__, "ACompressor")

    @classmethod
    def teardown_class(cls):
        print(cls.teardown_class_msg)

    def setup(self):
        print(self.setup_method_msg)
        print("Compression factor: " + str(self.sc.getC()))
        print("Neighborhood size: " + str(self.sc.getN()))
        print("Location of data to be compressed: " + self.filename)

    def teardown(self):
        print(self.teardown_method_msg)
