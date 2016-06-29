import logging

from levenshtein import distance, compression
from levenshtein.compression import CachedCompressor
from levenshtein.distance import CachedLDAlgorithm
from levenshtein.utils.filer import normalize_from_file
from copy import deepcopy

if __name__ == '__main__':
    from levenshtein.utils.log import setup_logging
    setup_logging()

logger = logging.getLogger(__name__)


class LevenSquash():
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
    nn        self._sc = compression.StringCompressorBasic()
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

    def _estimate(self, str1, str2):
        logger.info("Squashing distance between two strings...")

        sig1 = self.compress(str1)
        sig2 = self.compress(str2)

        logger.info('Computing signature distance...')

        squash_dist = self.calculate(sig1, sig2)

        logger.info("Signature distance computed using %s LD algorithm",
                    type(self._dist_alg).__name__)

        approx = squash_dist * self._sc.getC()

        logger.info("Signature distance " +
                    str(squash_dist) +
                    " Scaled by compression factor " +
                    str(self._sc.getC()) + ": " +
                    str(approx))

        return approx
