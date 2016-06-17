from unittest import assertTrue

from numpy import log2

from utils import random_strings, entropy, alphabet


class TestEntropy:
    def test_entropy_on_random_set(self):
        """
        Test utils.entropy on random set generated from alphanumerics.
        """

        STRING_LENGTH = 500000
        ALPHABET = alphabet.ALPHABET_BASIC
        random_str = random_strings.random_string(STRING_LENGTH,
                                                  ALPHABET)

        ent_calc = entropy.calc_entropy(random_str, ALPHABET)

        p = 1/len(ALPHABET)

        # this is the expected Shannon entropy for a uniform distribution
        exp_ent = STRING_LENGTH * p * log2(p)

        accepted_err = 0.001

        assertTrue(exp_ent-accepted_err <=
                   ent_calc <=
                   exp_ent+accepted_err)
