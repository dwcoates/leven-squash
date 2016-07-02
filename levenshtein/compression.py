import logging
import binascii
import md5
import copy

from levenshtein.utils import alphabet
from levenshtein.utils.computation import CalculationCache
from levenshtein.utils.process import *
from compressor import basic


class Compression (Process):

    def _execute(self, string, alphabet, C, N):
        raise NotImplementedError("Compression is a template for " +
                                  "compression algorithms. Not implemented.")

    def _core(self, string, alphabet, C, N):
        sig = list()
        str_pos = 0
        str_len = len(string)

        while str_pos + N < str_len:
            h = self._hash_neighborhood(string, str_pos, N)
            self._add_char(sig, alphabet, h, C)
            str_pos = str_pos + 1

        return ''.join(sig)

    def _hash_neighborhood(self, string, str_pos, N):
        raise NotImplementedError("The '" + self.__class__.__name__ +
                                  "' compressor module has not implemented " +
                                  "_hash_neighborhood.")

    def _add_char(self, signature, alphabet, h, C):
        """
        Accept a list of characters 'signature' and append a random character
        from alphabet with 1/C liklihood. This is a function of '_hash'. That
        is, identical values of '_hash' must always add the same character.
        """
        alpha_len = len(alphabet)

        if h % C == 0:
            indx = h % alpha_len
            char = alphabet[indx]
            signature.append(char)


class BasicCompression (Compression):
    """
    A basic compressor using a simple, fast algorithm.
    """
    # log = Logger.getLogger(StringCompressorBasic)

    def _execute(self, string, alphabet, C, N):
        return self._core(string, alphabet, C, N)

    def _hash_neighborhood(self, string, str_pos, N):
        acc = 0
        for i in xrange(N):
            val = ord(string[str_pos + i])
            val <<= i * 8 % 56
            acc ^= val
            acc = abs(acc)

        return acc


class CRCCompression (Compression):

    def _execute(self, string, alphabet, C, N):
        return self._core(string, alphabet, C, N)

    def _hash_neighborhood(self, string, str_pos, N):
        return binascii.crc32(string[str_pos:str_pos + N]) + 2**32


class MD5Compression (Compression):

    def _execute(self, string, alphabet, C, N):
        return self._core(string, alphabet, C, N)

    def _hash_neighborhood(self, string, str_pos, N):
        return int(md5.new(string[str_pos:str_pos + N]).hexdigest(), 16)


class CBasicCompression (Compression):

    def _execute(self, string, alphabet, C, N):
        # This will probably have to be Swig C call,
        # return compressor.core(string, my_C_hash_n, my_C_add_char)
        return self._core(string, alphabet, C, N)

    def _hash_neighborhood(self, string, str_pos, N):
        return basic(string, str_pos, N)


class Compressor (Calculation):
    _alphabet = alphabet.ALPHABET_BASIC

    def __init__(self, compression=BasicCompression(), C=150, N=8,
                 alphabet=None, **kwargs):
        super(Compressor, self).__init__(compression, **kwargs)

        self.C = C
        self.N = N

        self.logger = logging.getLogger(__name__)

        if alphabet is not None:
            self.set_alphabet(alphabet)

    def __copy__(self):
        c = type(self)()
        c.__dict__.update(self.__dict__)
        return c

    def setC(self, c):
        self.C = c

    def setN(self, n):
        self.N = n

    def getC(self):
        return self.C

    def getN(self):
        return self.N

    def get_algorithm(self):
        return self._compression

    def set_algorithm(self, alg):
        self._compression = alg

    def get_alphabet(self):
        return self._alphabet

    def set_alphabet(self, chars):
        try:
            if len(chars) >= 0:
                self._alphabet = chars
            else:
                raise ValueError("Character alphabet for compression scheme " +
                                 "must be non-zero in length")
        except TypeError:
            raise TypeError("'alphabet' provided is not a string.")

    def compress(self, string):
        """
        Compress 'string' into a signature of length 1/C.
        """
        if self.C <= 0 or self.N <= 0:
            warning = '%s%s' % (type(self).__name__,
                                '.compress(string) has received ' +
                                'non-positive N or C.')
            raise ValueError(warning)
        if len(string) == 0:
            warning = '%s%s' % (type(self).__name__,
                                '.compress(string) has received an empty ' +
                                'string to compress.')
            self.logger.warning(warning)

        print("type to copmress: " + str(type(string)))
        print("type alphabet: " + str(type(self._alphabet)))
        print("type N: " + str(type(self.N)))
        print("type C: " + str(type(self.C)))
        print("algorithm: " + self.get_algorithm().__class__.__name__)
        return self.get_algorithm().__call__(string, self._alphabet,
                                             self.C, self.N)
