import logging.Logger

import distance
import compression
from file import normalize_from_file


logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    from utils.log import setup_logging
    setup_logging()

logger = logging.getLogger(__name__)


class LevenSquash:
    def __init__(self, compressor, dist_alg):
        # Default compression scheme. Note that this compresses by a factor of
        # 100, so small strings will be completely annihilated, and therefore
        # this default compression scheme is completely useless for them.
        if compressor is None:
            self._sc = compression.StringCompressorBasic()
            self._sc.setC(150)
            self._sc.setN(8)
        else:
            self._sc = compressor
        logger.info("Configured leven-squash with %s LD algorithm.",
                    self._dist_alg.__name__)

        # Default distance calculation alasgorithm is the standard algorithm
        # in n*m time and max(n,m) space complexity
        if dist_alg is None:
            self.dist_alg = distance.AbsoluteLD.distance
        else:
            self._dist_alg = dist_alg
        logger.info("Configured leven-squash with %s compression scheme.",
                    self._sc.__name__)

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

        sig1 = self._sc.compress(str1)
        sig2 = self._sc.compress(str2)
        logger.info('Computing signature distance...')
        try:
            squash_dist = self._dist_alg.distance(sig1, sig2)
        except AttributeError:
            warning = "%s%s%s" % ("Invalid distance algorithm, %s, of type %s",
                                  self._dist_alg.__name__,
                                  type(self._dist_alg).__name__)
            raise TypeError(warning)
        except:
            raise
        else:
            logger.info("Signature distance computed using %s LD algorithm",
                        type(self._dist_alg).__name__)

        logger.info("Distance computed.")
        return squash_dist

    def calculate(self, str1, str2):
        """
        Return LD distance calcuation between str1 and str2. This is a
        distance computation using the underlying leven-squash LD calculation
        algorithm, and not the leven-squash estimation process.
        """
        str1 = normalize_from_file(str1)
        str2 = normalize_from_file(str2)

        return self._dist_alg(str1, str2)
