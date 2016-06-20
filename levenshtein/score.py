import inspect

from levenshtein.leven_squash import LevenSquash


class ScoreDistance:
    """
    Class for assessing qualities of leven-squash distance calculations.
    """
    def __init__(self, ls=LevenSquash()):
        # hmm
        # self.log = logging.getLogger()
        self._ls = ls

    def get_leven_squash(self):
        """
        Returns a deep copy of the LevenSquash module being scored.
        """
        pass

    def set_leven_squash(self, ls):
        self.reset_cache()
        self._ls = ls

    def compress(self, string):
        return self._ls.compress(string)

    def calculate(self, str1, str2):
        return self._ls.calculate(str1, str2)

    def estimate(self, str1, str2):
        return self._ls.estimate(str1, str2)

    def estimate_corrected(self, str1, str2):
        return self._ls.estimate_corrected(str1, str2)

    @staticmethod
    def difference(a, b):
        """
        Accepts two numbers, 'a' and 'b',  and returns a score of how
        different a is from b. Return value is between -1 and 1, with negative
        values denoting a < b and positive values a > b. That is, how much
        different is a from b.
        """
        return (a - b) / float(b)

    @staticmethod
    def error(calculation, approximation):
        return abs(ScoreDistance.difference(approximation, calculation))

    @staticmethod
    def similarity(self, dist_alg, str1, str2):
        """
        Uses dist_alg to compute the distance between str1 and str2.
        Returns the similarity of the two strings, which is 1 minus
        the difference ratio.
        """
        diff = dist_alg(str1, str2)
        longer = max(len(str1), len(str2))

        similarity = 1 - diff/longer

        return similarity

    def similarity_absolute(self, str1, str2):
        """
        Computes the exact similarity between strings str1 and str2.
        Uses the underlying LevenSquash instance's distance algorithm.
        """
        alg = self.calculate

        return ScoreDistance.similarity(alg, str1, str2)

    def similarity_estimate(self, str1, str2):
        """
        Computes the approximate similarity between strings str1 and str2.
        Uses the underlying LevenSquash instance's basic estimation process
        (squash distance scaled by compression factor).
        """
        alg = self.estimate

        return ScoreDistance.similarity(alg, str1, str2)

    def similarity_corrected_estimate(self, str1, str2):
        """
        Computes the approximate similarity between strings str1 and str2.
        Uses the underlying LevenSquash instance's corrected estimation process
        (squash distance scaled by compression factor, then multiplied by a
        correction factor).
        """
        alg = self.estimate_corrected

        return ScoreDistance.similarity(alg, str1, str2)

    def score_corrected_estimate(self, str1, str2):
        """
        Returns the improvement factor of LS.estimate_corrected(str1, str2)
        over LS.estimate(str1, str2). Value returned is between -1 and 1.
        """
        absolute_dist = self.calculate(str1, str2)
        estimated_dist = self.estimate(str1, str2)
        corrected_dist = self.estimate_corrected(str1, str2)

        err_estimate = ScoreDistance.difference(estimated_dist,
                                                absolute_dist)
        err_corrected = ScoreDistance.difference(corrected_dist,
                                                 absolute_dist)

        return ScoreDistance.difference(abs(err_corrected),
                                        abs(err_estimate))


    # Adjust an estimate for the difference between the LD of randomly chosen
    # English text and the LD of the corresponding signatures differs.
    # Signatures have higher entropy, hence a relatively greater LD.
    # sigRatio is the average ratio of the LD of signatures to the
    # corresponding string lengths to the ratio of the LD of the original
    # strings to the string length  (for same-length originals).
    def fudgeFactor(self, in_):
        correctionFactor = self.sigRatio - self.wholeFileRatio
        v = in_ + (in_*correctionFactor)
        return v

    # The expected distance of two random strings of lengths s1 and s2, give
    # the expected contraction of LD (fudge factor);
    def expectedDistance(self, s1, s2):
        return self.fudgeFactor(max(s1, s2)) + abs(s1-s2)

    # Given two signatures and the length of the length of the longer original
    # string, compute the raw estimate as LD(sig1,sig2)/longerSigLen
    # longerOriginalStringLen. Adjust this string by the fudge factor that
    # considers the ratio of LD to string lengths for originals and signatures
    # (they differ).
    def getLDEst(self, sig1, sig2, longerUnCompressed, shorterUncompressed):
        longer = max(sig1.length(), sig2.length())
        ld = self._ls.calculate(sig1, sig2)
        computedLenRatioPlain = ld / float(longer)
        estimatedUnadjusted = computedLenRatioPlain
        return self.fudgeFactor(estimatedUnadjusted)

