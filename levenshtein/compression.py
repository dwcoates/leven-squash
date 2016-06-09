import logging


class ACompressor:
    chars = "qrZ126stucRSTHfgmnoPQJKLIdeM345UVhvwxDEFGWXY7ij890NOakyzABClbp"

    def __init__(self):
        self.N = 0
        self.C = 0

        self.logger = logging.getLogger(__name__)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        # There should probably be getters and setters to check for positivity
        # of C and N. Zero value C will throw a division-by-zero error and
        # non-positive N will result in infinite loop.

    def compress(self, string):
        if self.C <= 0 or self.N <= 0:
            warning = '%s%s' % (type(self).__name__,
                                '.compress(string) has received non-positive N or C.')
            raise TypeError(warning)
        if len(string) == 0:
            warning = '%s%s' % (type(self).__name__,
                                '.compress(string) has received an empty string to compress.')
            self.logger.warning(warning)

        self._compress(string)

    def _compress(self, string):
        raise NotImplementedError("ACompressor does not implement a compression algorithm.")


class StringCompressorBasic (ACompressor):
    """A basic compressor using a simple, fast algorithm."""
    # log = Logger.getLogger(StringCompressorBasic)

    # TODO Revisit this. It looks correct, but it takes n steps at each position.
    def compress(self, string):
        retstr = ''   # should this be over-allocated? Probably doesn't matter.
        strPos = 0
        strLen = len(string)

        # Accumulate a value for each position that included an entire neighborhood.
        while strPos+self.N < strLen:
            acc = 0
            # Starting with no bits set in an accumulator, for each element in the
            # neighborhood, XOR in the element at a fresh 8-bit position. Wrap around and
            # keep going if N is long enough to exhaust the 64 bits in a long.
            for i in range(0, self.N):
                val = ord(string[strPos+i])
                # val<<=i*8%64
                val <<= i*8 % 56
                acc ^= val
                acc = abs(acc)
            if acc % self.C == 0:
                indx = acc % len(StringCompressorBasic.chars)
                outChar = StringCompressorBasic.chars[indx]
                retstr += outChar
            strPos = strPos+1
        return retstr
