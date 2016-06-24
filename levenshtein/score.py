import inspect
import time

from levenshtein.leven_squash import LevenSquash


class ScoreDistance():
    """
    Class for assessing qualities of leven-squash distance calculations.
    """
    _distance_functions = [LevenSquash.calculate.__name__,
                           LevenSquash.estimate.__name__,
                           LevenSquash.estimate_corrected.__name__]

    def __init__(self, str1, str2, ls=LevenSquash()):
        # hmm
        # self.log = logging.getLogger()
        self._cache = CalculationCache()

        self._str1 = str1
        self._str2 = str2

        self._ls = ls

    def reset_cache(self, *ignore):
        self._cache.reset_cache(ignore)

    def _provide_cache_stat(self, get_stat, function):
        if function not in ScoreDistance._distance_functions:
            raise ValueError("Function '" + function + "' is not a " +
                             "known distance function of LevenSquash.")

        s = get_stat(function)

        if s is None:
            start = time.clock()
            v = getattr(self._ls, function)(self._str1, self._str2)
            end = time.clock()
            t = end - start
            self._cache.add(function, v, t)

        return get_stat(function)

    def time(self, function):
        return self._provide_cache_stat(self._cache.get_time, function)

    def value(self, function):
        return self._provide_cache_stat(self._cache.get_value, function)

    def set_strings(self, str1, str2):
        self._str1 = str1
        self._str2 = str2

        self.reset_cache()

    def get_strings(self):
        return (self._str1, self._str2)

    def set_leven_squash(self, ls):
        self.reset_cache(self.calculate.__name__)

        self._ls = ls

    def get_leven_squash(self):
        """
        Returns a deep copy of the LevenSquash module being scored.
        """
        # CURRENTLY RETURNS REFERENCE. WARNING.
        return self._ls

    def getC(self):
        return self._ls.getC()

    def getN(self):
        return self._ls.getN()

    def setC(self, c):
        self._ls.setC(c)

        self.reset_cache("calculate")

    def setN(self, n):
        self._ls.setN(n)

        self.reset_cache("calculate")

    def compress(self, string):
        # doesn't cache at the moment, not really very important that it does.
        return self._ls.compress(string)

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

    def _similarity(self, alg):
        """
        Uses dist_alg to compute the distance between str1 and str2.
        Returns the similarity of the two strings, which is 1 minus
        the difference ratio.
        """
        diff = self.value(alg)

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

    # Adjust an estimate for the difference between the LD of randomly chosen
    # English text and the LD of the corresponding signatures differs.
    # Signatures have higher entropy, hence a relatively greater LD.
    # sigRatio is the average ratio of the LD of signatures to the
    # corresponding string lengths to the ratio of the LD of the original
    # strings to the string length  (for same-length originals).
    def fudgeFactor(self, in_):
        correctionFactor = self.sigRatio - self.wholeFileRatio
        v = in_ + (in_ * correctionFactor)
        return v

    # The expected distance of two random strings of lengths s1 and s2, give
    # the expected contraction of LD (fudge factor);
    def expectedDistance(self, s1, s2):
        return self.fudgeFactor(max(s1, s2)) + abs(s1 - s2)

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


class CalculationCache:

    def __init__(self):
        self._cache = dict()

    def get_value(self, key):
        if key in self._cache:
            return self._cache[key][0]
        else:
            return None

    def get_time(self, key):
        if key in self._cache:
            return self._cache[key][1]
        else:
            return None

    # ScoreDistance should never add a key that already exists or remove a key
    # that doesnt, so these methods raise errors.
    def add(self, key, value, time):
        if key in self._cache:
            raise ValueError("Cache already has value and time for key '" +
                             key + "': (" + self.get_value[key] + ", " +
                             self.get_time[key] + ". Remove with clear(key) " +
                             "before adding.")
        else:
            self._cache[key] = (value, time)

    def clear(self, key):
        if key not in self._cache:
            raise ValueError("Removal of key '" + key + "' failed. Cache " +
                             "does not contain key.")
        else:
            del self._cache[key]

    def reset_cache(self, ignore):
        delete = list()

        for key in self._cache:
            if key not in ignore:
                delete.append(key)

        for i in delete:
            self.clear(i)
