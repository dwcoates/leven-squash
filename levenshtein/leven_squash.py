import logging.Logger

import distance
import compression


logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    from utils.log import setup_logging
    setup_logging()

logger = logging.getLogger(__name__)


def leven_squash(sc, dist_alg, str1, str2):
    """Accepts a string compressor, LD algorithm, and two strings,
    returning the leven_squash Default compressor is StringCompressorBasic,
    and default LD algorithm is StringMatcher.distance"""
    logger.info("Determining similarity of two string signatures...")
    if dist_alg is None:
        dist_alg = distance.AbsoluteLD.distance
    logger.info("Configured leven-squash with %s LD algorithm.",
                dist_alg.__name__)

    if sc is None:
        # Default compression scheme. Note that this compresses by a factor of
        # 100, so small strings will be completely annihilated, and therefore
        # this default compression scheme is completely useless for them.
        sc = compression.StringCompressorBasic()
        sc.C = 100
        sc.N = 5
    logger.info("Configured leven-squash with %s compression scheme.",
                sc.__name__)

    sig1 = sc.compress(str1)
    sig2 = sc.compress(str2)

    logger.info('Computing signature distance...')
    try:
        squash_dist = dist_alg.distance(sig1, sig2)
    except AttributeError as ae:
        warning = "%s%s%s" % ("Invalid distance algorithm, %s, of type %s",
                              dist_alg.__name__,
                              type(dist_alg).__name__)
        raise TypeError(warning)
    except:
        raise
    else:
        logger.info("Signature distance computed using %s LD algorithm",
                    type(dist_alg).__name__)

    logger.info("Distance computed.")

    return squash_dist
