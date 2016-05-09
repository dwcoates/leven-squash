# procedures for variably compressing a string with SHA1 hash.

import hashlib
#import logger
from array import array

class Compressor:
    def __init__(self):
        self.N = 0
        self.C = 0

    def getN(self):
        return self.N
    def setN(self, n):
        self.N = n
    def getC(self):
        return self.C
    def setC(self, c):
        self.C = c


class StringCompressorBasic (Compressor):
    #log = Logger.getLogger(StringCompressorBasic)
    PRINT_DIAG = False

    chars ="qrZ126stucRSTHfgmnoPQJKLIdeM345UVhvwxDEFGWXY7ij890NOakyzABClbp"

    # TODO Revisit this. It looks correct, but it takes n steps at each position.
    @staticmethod
    def compress_alt(string, n, c):
        # temp divbyzero check, please fix
        # possibly should throw a ValueError
        if c == 0 or n == 0:
            print("c or n are 0")
            return ''

        retstr = ''   # should this be over-allocated?
        strPos = 0
#        if SQUEEZE_WHITE:
#           string=squeezeWhite(string)

        strLen = len(string)
        # this should throw an exception
        if strLen == 0:
            print("compress has received an empty string")
            return ''

        # Accumulate a value for each position that included an entire neighborhood.
        while strPos+n < strLen:
            curSum = 0;
            # Starting with no bits set in an accumulator
            # for each element in the neighborhood
            # XOR in the element at a fresh position.
            # Wrap around and keep going if n is long enough to
            # exhaust the 64 bits in a long.
            # TODO: This keeps shifting by 8. Maybe for each time it wraps
            # around is should increment by 8+1, 8_2,
            # etc. This might scramble better if some value is repeating.
            for i in range(0, n):
                val = ord(string[strPos+i])
                #val<<=i*8%64
                val <<= i*8%56
                curSum ^= val
            curSum = abs(curSum)
            if curSum%c == 0:
                indx = curSum%len(StringCompressorBasic.chars)
                outChar = StringCompressorBasic.chars[indx]
                if StringCompressorBasic.PRINT_DIAG:
                    print(str(outChar))
                retstr += outChar
            strPos = strPos+1
        if StringCompressorBasic.PRINT_DIAG:
            print("") # nothing just yet
        return retstr

    # compress a string down to about 1/c of its size using neighborhood size n
    def compress(self, string):
        return self.compress_alt(string, self.getN(), self.getC())


    # Replace all multiple white spaces in the string with a single white space.
    # @param value
    # @return
    def squeezeWhite(value):
        string = value.replaceAll("\\s+", " ")
        return string.trim()
