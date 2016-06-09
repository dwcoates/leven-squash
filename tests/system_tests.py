import sys


class TestSystem():
    """
    Class for testing system configurations and nose tests

    """

    @classmethod
    def setup_class(self):
        pass

    @classmethod
    def teardown_class(self):
        pass

    def test_sys_path(self):
        assert sys.path is not None
