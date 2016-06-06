from array import array
import logging.Logger

class ACompressor:
    chars ="qrZ126stucRSTHfgmnoPQJKLIdeM345UVhvwxDEFGWXY7ij890NOakyzABClbp"

    def __init__(self):
        self.N = 0
        self.C = 0

        # this is probably not a good idea.
        log = logging.getLogger(__name__)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        log.addHandler(ch)

    # I don't think this is a correct implementation of a virtual method
    @classmethod
    def compress(self, string):
        pass

    def getN(self):
        return self.N
    def setN(self, n):
        self.N = n
    def getC(self):
        return self.C
    def setC(self, c):
        self.C = c


# A basic compressor using a simple, fast algorithm
class StringCompressorBasic (ACompressor):
    #log = Logger.getLogger(StringCompressorBasic)

    # TODO Revisit this. It looks correct, but it takes n steps at each position.
    def compress(self, string):
        # temp divbyzero check, please fix
        # possibly should throw a ValueError
        if self.C <= 0 or self.N <= 0:
            # should log here
            print("c or n are 0")
            raise ValueError('StringCompressorBasic.compress() called with non-positive C or N values.')

        retstr = ''   # should this be over-allocated? Probably doesn't matter.
        strPos = 0

        strLen = len(string)
        # This should throw an exception
        if strLen == 0:
            # should log here
            print("compress has received an empty string")
            return ''

        # Accumulate a value for each position that included an entire neighborhood.
        while strPos+self.N < strLen:
            acc = 0;
            # Starting with no bits set in an accumulator, for each element in the
            # neighborhood, XOR in the element at a fresh position. Wrap around and
            # keep going if N is long enough to exhaust the 64 bits in a long.
            # TODO: This keeps shifting by 8. Maybe for each time it wraps around is
            # should increment by 8+1, 8_2, etc. This might scramble better if some
            # value is repeating.
            for i in range(0, self.N):
                val = ord(string[strPos+i])
                #val<<=i*8%64
                val <<= i*8%56
                acc ^= val
                acc = abs(acc)
            if acc%self.C == 0:
                indx = acc%len(StringCompressorBasic.chars)
                outChar = StringCompressorBasic.chars[indx]
                retstr += outChar
            strPos = strPos+1
        return retstr
