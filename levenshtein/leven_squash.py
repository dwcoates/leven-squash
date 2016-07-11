import logging

from levenshtein.distance import *
from levenshtein.compression import *
from levenshtein.utils.computation import ComputationManager
from copy import deepcopy

if __name__ == '__main__':
    from levenshtein.utils.log import setup_logging
    setup_logging()

logger = logging.getLogger(__name__)


class LevenSquash(object):
    # The average Levenshtein normalized distance between two pieces of
    # English text of considerable size.
    avg_english_dist = 0.78415552

    # The average Levenshtein normalized distance between two ransom strings
    # of considerable size.
    avg_random_dist = 0.94574417

    # We expect random strings, i.e., signatures, to have considerably more
    # random composition than English text, of course. Therefore, their
    # distance will be on average greater. This correction factor can be
    # used to greatly improve estimates.
    correction_factor = avg_english_dist / avg_random_dist

    def __init__(self, compressor=None, dist_alg=None):
        # Default compression scheme. Note that this has a fairly large C,
        # so small strings will be completely annihilated, and therefore
        # this default compression scheme is completely useless for them.
        if compressor is None:
            self._compressor = Compressor()
        else:
            self._compressor = compressor
        logger.info("Configured leven-squash with %s compression scheme.",
                    self._compressor.__class__.__name__)

        # Default distance calculation alasgorithm is the standard algorithm
        # in n*m time and max(n,m) space complexity
        if dist_alg is None:
            self._dist_alg = LevenDistance()
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
        return self._compressor

    def get_ld_alg(self):
        return self._dist_alg

    def set_compressor(self, compressor):
        self._compressor = compressor

    def set_ld_alg(self, dist_alg):
        self._dist_alg = dist_alg

    def _compress(self, string):
        return self.get_compressor().compress(string)

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
        by a correction factor. The derivation of this correction factor is
        shown in demo.
        """
        logger.info("Computing corrected squash estimate...")

        est = self._estimate(str1, str2)

        est_corrected = self.correction_factor * est

        logger.info("Corrected distance: " + str(est_corrected))

        return est_corrected

    def calculate(self, str1, str2):
        """
        Return LD distance calcuation between str1 and str2. This is a
        distance computation using the underlying leven-squash LD calculation
        algorithm, and not the leven-squash estimation process.
        Accepts either strings or filenames to be read from.
        """
        try:
            dist = self._dist_alg.distance(str1, str2)
        except AttributeError:
            warning = ("Invalid distance algorithm, " +
                       "'{}'").format(self._dist_alg.__class__.__name__)

            raise TypeError(warning)

        if dist is None:
            warn = "%s.distance called on objects typed '%s' and '%s' has returned None" % (
                self._dist_alg.__class__.__name__,
                str1.__class__.__name__,
                str2.__class__.__name__)
            warn += ("\nSTRING LENGTHS: %s, %s" % (len(str1), len(str2)))
            raise Exception(warn)

        return dist

    def _estimate(self, str1, str2):
        logger.info("Squashing distance between two strings...")

        sig1 = self._compress(str1)
        sig2 = self._compress(str2)

        logger.info('Computing signature distance...')

        squash_dist = self.calculate(sig1, sig2)

        logger.info("Signature distance computed using %s LD algorithm",
                    type(self._dist_alg).__name__)

        approx = squash_dist * self._compressor.getC()

        logger.info("Signature distance " +
                    str(squash_dist) +
                    " Scaled by compression factor " +
                    str(self._compressor.getC()) + ": " +
                    str(approx))

        return approx


class SmartLevenSquash:

    def __init__(self, compressor=None, dist_alg=None):
        # this should do a deepcopy
        if compressor is not None:
            compressor = copy.copy(compressor)
            compressor.set_cache(True)
        if dist_alg is not None:
            dist_alg = copy.copy(dist_alg)
            dist_alg.set_cache(True)

        self._ls = LevenSquash(compressor, dist_alg)

    def setN(self, n):
        self._ls.setN(n)

    def getN(self):
        return self._ls.getN()

    def setC(self, c):
        self._ls.setC(c)

    def getC(self):
        return self._ls.getC()

    def get_compressor(self):
        return self._ls.get_compressor()

    def get_ld_alg(self):
        return self._ls.get_ld_alg()

    def set_compressor(self, compressor):
        self._ls.set_compressor(compressor)

    def set_ld_alg(self, dist_alg):
        self._ls.set_ld_alg(dist_alg)

    def compress(self, string):
        return ComputationManager.CREATE_COMPUTATION(self._ls._compress,
                                                     string)

    def estimate(self, str1, str2):
        return ComputationManager.CREATE_COMPUTATION(self._ls.estimate,
                                                     str1,
                                                     str2)

    def estimate_corrected(self, str1, str2):
        return ComputationManager.CREATE_COMPUTATION(self._ls.estimate_corrected,
                                                     str1,
                                                     str2)

    def calculate(self, str1, str2):
        return ComputationManager.CREATE_COMPUTATION(self._ls.calculate,
                                                     str1,
                                                     str2)
