import logging

from levenshtein import distance, compression
from levenshtein.utils.filer import normalize_from_file

if __name__ == '__main__':
    from levenshtein.utils.log import setup_logging
    setup_logging()

logger = logging.getLogger(__name__)


class LevenSquash:
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

    def compress(self, string):
        """
        Use set compression scheme to compress string
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
