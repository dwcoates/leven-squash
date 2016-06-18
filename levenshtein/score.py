from levenshtein.leven_squash import LevenSquash


class ScoreDistance:
    """
    Class for assessing qualities of leven-squash distance estimateoutput
    """
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

    def __init__(self, ls=LevenSquash()):
        self._ls = ls
        # hmm
        self.log = logging.getLogger()

    def get_distance(self):
        return self._ls.get_ld_alg()

    def get_compressor(self):
        return self._ls.get_compressor()

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

