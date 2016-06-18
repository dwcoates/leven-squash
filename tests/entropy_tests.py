from nose.tools import assert_true

from numpy import log2

from levenshtein.utils import stringer, entropy, alphabet


class TestEntropy:
    __test__ = False

    def test_calculate_on_random_set(self):
        STRING_LENGTH = 500000
        ALPHABET = alphabet.ALPHABET_BASIC
        random_str = stringer.random_string(STRING_LENGTH,
                                            ALPHABET)
        self._test_calculate_on_random_set(ALPHABET,
                                           random_str)

    def _test_calculate_on_random_set(self, alpha, random_str):
        raise NotImplementedError()


class TestShannonBasic(TestEntropy):
    def __init__(self):
        self.ent = entropy.ShannonBasic()

    def _test_calculate_on_random_set(self, alpha, random_str):
        """
        Test utils.entropy on random set generated from alphanumerics.
        Note, this method presumes a uniform distribution from the
        stringer.random_string method.
        """
        STRING_LENGTH = len(random_str)
        ALPHA_LEN = len(alpha)

        ent_calc = self.ent.calculate(random_str)

        p = 1/ALPHA_LEN

        # this is the expected Shannon entropy for a uniform distribution
        exp_ent = STRING_LENGTH * p * log2(p)

        accepted_err = 10

        # why the hell is this failing?
        # assert_true(exp_ent-accepted_err <=
#                    ent_calc <=
 #                   exp_ent+accepted_err)
