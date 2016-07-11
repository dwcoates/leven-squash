from levenshtein.leven_squash import *
from levenshtein.utils.computation import Computation


class ScoreDistance():
    """
    Class for assessing qualities of leven-squash distance calculations.
    """
    _DISTANCE_FUNCTIONS = [LevenSquash.calculate.__name__,
                           LevenSquash.estimate.__name__,
                           LevenSquash.estimate_corrected.__name__]

    def __init__(self, str1, str2, ls=LevenSquash()):
        # hmm
        # self.log = logging.getLogger()
        self._str1 = str1
        self._str2 = str2

        self._sls = SmartLevenSquash(ls.get_compressor(), ls.get_ld_alg())

    def set_leven_squash(self, ls):
        self._sls = SmartLevenSquash(ls.get_compressor(), ls.get_ld_alg())

    def get_leven_squash(self):
        """
        Returns a deep copy of the LevenSquash module being scored.
        """
        return self._sls

    def getC(self):
        return self._sls.getC()

    def getN(self):
        return self._sls.getN()

    def setC(self, c):
        self._sls.setC(c)

    def setN(self, n):
        self._sls.setN(n)

    def get(self, dist_alg):
        if dist_alg.__name__ not in self._DISTANCE_FUNCTIONS:
            raise ValueError("'" + dist_alg.__name__ +
                             "' is not an accepted LevenSquash distance " +
                             "measure.")
        else:
            return getattr(self._sls, dist_alg.__name__)(self._str1, self._str2)

    def diff(self, dist_alg1, dist_alg2):
        c1 = self.get(dist_alg1)
        c2 = self.get(dist_alg2)

        return Computation(self.difference(c1.value(), c2.value()),
                           self.difference(c1.time(), c2.time()))

    @staticmethod
    def difference(a, b):
        """
        Accepts two numbers, 'a' and 'b',  and returns a score of how
        different a is from b. Return value is between -1 and 1, with negative
        values denoting a < b and positive values a > b. That is, how much
        different is a from b.
        """
        if a == b:
            return 0

        return (a - b) / float(b)

    @staticmethod
    def error(calculation, approximation):
        return abs(ScoreDistance.difference(approximation, calculation))

    def _similarity(self, dist_alg):
        """
        Uses dist_alg to compute the distance between str1 and str2.
        Returns the similarity of the two strings, which is 1 minus
        the difference ratio.
        """
        diff = self.get(dist_alg).value()

        longer = max(len(self._str1), len(self._str2))

        similarity = 1 - diff / float(longer)

        return similarity

    def similarity_absolute(self):
        """
        Computes the exact similarity between strings str1 and str2.
        Uses the underlying LevenSquash instance's distance algorithm.
        """
        alg = "calculate"

        return self._similarity(alg)

    def similarity_estimate(self):
        """
        Computes the approximate similarity between strings str1 and str2.
        Uses the underlying LevenSquash instance's basic estimation process
        (squash distance scaled by compression factor).
        """
        alg = "estimate"

        return self._similarity(alg)

    def similarity_corrected_estimate(self):
        """
        Computes the approximate similarity between strings str1 and str2.
        Uses the underlying LevenSquash instance's corrected estimation process
        (squash distance scaled by compression factor, then multiplied by a
        correction factor).
        """
        alg = "estimate_corrected"

        return self._similarity(alg)

    def score_corrected_estimate(self, str1, str2):
        """
        Returns the improvement factor of LS.estimate_corrected(str1, str2)
        over LS.estimate(str1, str2). Value returned is between -1 and 1.
        """
        absolute_dist = self.value("calculate")
        estimated_dist = self.value("estimate")
        corrected_dist = self.value("estimate_corrected")

        err_estimate = ScoreDistance.difference(estimated_dist,
                                                absolute_dist)
        err_corrected = ScoreDistance.difference(corrected_dist,
                                                 absolute_dist)

        return ScoreDistance.difference(abs(err_corrected),
                                        abs(err_estimate))
