import logging

from levenshtein import distance, compression
from levenshtein.utils.filer import normalize_from_file
from copy import deepcopy

if __name__ == '__main__':
    from levenshtein.utils.log import setup_logging
    setup_logging()

logger = logging.getLogger(__name__)


class LevenSquash:
    # Amount by which the LD of a pair of equal length random text strings is
    # smaller than their length. This is used to fudge the product of
    # signature LD and compression factor to adjust the expectation.
    # Note, this is a function of the alphabet length of the compression
    # scheme.
    wholeFileRatio = 0.022

    # Amount by which the LD of a pair of equal size plain-generated
    # signatures is smaller than their length. This is used to fudge product
    # of signature LD and compression factor to adjust the expectation.
    sigRatio = 0.030

    def __init__(self, compressor=None, dist_alg=None):
        # Default compression scheme. Note that this has a fairly large C,
        # so small strings will be completely annihilated, and therefore
        # this default compression scheme is completely useless for them.
        if compressor is None:
            self._sc = compression.StringCompressorBasic()
        else:
            self._sc = compressor
        logger.info("Configured leven-squash with %s compression scheme.",
                    self._sc.__class__.__name__)

        # Default distance calculation alasgorithm is the standard algorithm
        # in n*m time and max(n,m) space complexity
        if dist_alg is None:
            self._dist_alg = distance.AbsoluteLD()
        else:
            self._dist_alg = dist_alg

        logger.info("Configured leven-squash with %s LD algorithm.",
                    self._dist_alg.__class__.__name__)

    def setN(self, n):
        self.get_compressor().setN(n)

    def getN(self):
        return self.get_compressor().getN()

    def setC(self, c):
        self.get_compressor().setC(c)

    def getC(self):
        return self.get_compressor().getC()

    def get_compressor(self):
        return self._sc

    def get_ld_alg(self):
        return self._dist_alg

    def set_compressor(self, compressor):
        self._sc = compressor

    def set_ld_alg(self, dist_alg):
        self._dist_alg = dist_alg

    def compute_sig_dist(self, str1, str2):
        """
        Accepts two strings, returning their leven-squash signature distance.
        """
        logger.info("Determining distance of two string signatures...")

        str1 = normalize_from_file(str1)
        str2 = normalize_from_file(str2)

        sig1 = self.compress(str1)
        sig2 = self.compress(str2)
        logger.info('Computing signature distance...')

        squash_dist = self.calculate(sig1, sig2)

        logger.info("Signature distance computed using %s LD algorithm",
                    type(self._dist_alg).__name__)

        return squash_dist

    def _estimate(self, str1, str2):
        logger.info("Squashing distance between two strings...")

        sig_dist = self.compute_sig_dist(str1, str2)

        approx = sig_dist * self._sc.getC()

        logger.info("Signature distance " +
                    str(sig_dist) +
                    " Scaled by compression factor " +
                    str(self._sc.getC()) + ": " +
                    str(approx))

        return approx

    def estimate(self, str1, str2):
        """
        Accepts two strings, and returns the approximation of their distance.
        This is computed by squashing them, getting the distance between
        squashes, then scaling the result by the compresson factor.
        """
        logger.info("Computing basic squash estimate...")

        return self._estimate(str1, str2)

    def estimate_corrected(self, str1, str2):
        """
        Accepts two strings, and returns the approximation of their distance.
        This is derived from LevenSquash.estimate() by multiplying the result
        by a correction factor.
        """
        logger.info("Computing corrected squash estimate...")

        est = self._estimate(str1, str2)

        # TODO: correct est by correction factor
        est_corrected = 0 * est

        logger.info("Corrected distance: " + str(est_corrected))

        return est_corrected

    def compress(self, string):
        """
        Use set compression scheme to compress string.
        """
        return self._sc.compress(string)

    def calculate(self, str1, str2):
        """
        Return LD distance calcuation between str1 and str2. This is a
        distance computation using the underlying leven-squash LD calculation
        algorithm, and not the leven-squash estimation process.
        Accepts either strings or filenames to be read from.
        """
        str1 = normalize_from_file(str1)
        str2 = normalize_from_file(str2)

        try:
            dist = self._dist_alg.distance(str1, str2)
        except AttributeError:
            warning = ("Invalid distance algorithm, " +
                       "'{}'").format(self._dist_alg.__class__.__name__)

            raise TypeError(warning)

        return dist


class LevenSquasher:

    def __init__(self, str1, str2, ls=LevenSquash()):
        # hmm
        #self.log = logging.getLogger()

        # strings should be stored as hashtable keys
        # values are signatures and time to compute them

        self._str1 = str1
        self._str2 = str2

        self._ls = ls

        self._cache = dict()

    def reset_cache(self):
        """
        Reset the ScoreDistance instance's cache. Useful externally if you
        want to recalculate computation time for some cached method.
        """
        self._cache = dict()

    def _get_value(self, fun, *args):
        """
        Return the cached value of the calling function + args if they've
        already been computed. Otherwise, compute the function and return the
        result.
        """
        for arg in args:
            if arg != self._str1 and arg != self._str2:
                self.reset_cache()
                break

        key = fun.__name__ + ''.join(args)

        if key in self._cache:
            return self._cache[key]

        val = fun(*args)
        self._cache[key] = val

        return val

    def get_leven_squash(self):
        """
        Returns a deep copy of the LevenSquash module being scored.
        """
        return deepcopy(self._ls)

    def set_leven_squash(self, ls):
        self.reset_cache()
        self._ls = ls

    def set_strings(self, str1=None, str2=None):
        """
        Sets the strings to str1 and str2. If strx is None, then it is unaffected.
        """
        pass

    def get_strings():
        """
        Returns a tuple consisting of the stings being used by the squasher
        """
        pass

    def set_str1(self, str1):
        self.reset_cache()

        self._cache[self._str1] = self._ls.compress(self._str1)
        self._str1 = str1

    def set_str2(self, str2):
        self.reset_cache()

        self._cache[self._str2] = self._ls.compress(self._str2)
        self._str2 = str2

    def get_str1(self):
        return self._str1

    def get_str2(self):
        return self._str2

    def compress(self, string):
        # this is possibly a resource leak
        # should return sig1 or sig2 or compute the signature, and if
        return self._get_value(self._ls.compress, string)

    def calculate(self):
        return self._get_value(self._ls.calculate, self._str1, self._str2)

    def estimate(self):
        return self._get_value(self._ls.estimate, self._str1, self._str2)

    def estimate_corrected(self):
        return self._get_value(self._ls.estimate_corrected,
                               self._str1,
                               self._str2)
