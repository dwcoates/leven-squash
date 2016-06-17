from collections import defaultdict

from scipy.stats import entropy
import numpy as np


# There are various approaches to calculating entropy depending on the
# structure of the data. For english, which is a distribution for which the
# likelihook of an event occuring is dependent on the occurances of previous
# events, this metric is not best approximated by the basic Shannon entropy,
# and instead is done by some stochastic process.
class Entropy:
    def calculate(self, string):
        raise NotImplementedError()

    @staticmethod
    def char_distribution(string):
        """
        Returns a dict comprised of the frequency of characters indx
        string. Checks against intended alphabet if supplied.
        """

        distr = defaultdict(lambda: 0)

        string_len = len(string)

        for char in string:
            distr[char] += 1

        for k in distr:
            distr[k] /= float(string_len)

        return distr


class ShannonBasic(Entropy):
    def calculate(self, string):
        """
        Estimate the entropy of string in Shannons. That is, this method assumes that the frequency of characters in the input string is exactly equal to the probability mass function.
        """
        probs = Entropy.char_distribution(string).values()

        # calculates entropy in Nats
        ent_nat = entropy(probs)

        # convert to Shannons
        ent_shan = ent_nat * 1/np.log(2)

        return ent_shan
