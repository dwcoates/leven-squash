from levenshtein.utils import entropy
from levenshtein.utils import stringer
from levenshtein.utils import alphabet


class TestStringer:
    def test_random_string_entropy(self):
        ent = entropy.ShannonBasic()
        r = stringer.random_string
        alphab = alphabet.ALPHABET_BASIC
        alphab_len = len(alphab)
        calc_ent = ent.calculate(r(10000, alphab))

        # Theoretical probability of a given character being selected from alphabet
        alphab_prob = 1/alphab_len
        distr = dict()
        for char in alphab:
            # assume uniform distribution of random characters
            distr[char] = alphab_prob
        exp_ent = ent.get_entropy(distr.values())
        print("calculated entropy: " + str(calc_ent) +
              "expected entropy: " + str(exp_ent))
