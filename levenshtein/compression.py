import logging
import binascii
import md5

from levenshtein.utils import alphabet
from compressor import basic


class ACompressor:
    _chars = alphabet.ALPHABET_BASIC

    def __init__(self, C=150, N=8, alphabet=None):
        self.C = C
        self.N = N

        self.logger = logging.getLogger(__name__)

        # STYLE QUESTION to ask yury about here.
        if alphabet is not None:
            self.set_alphabet(alphabet)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        # There should probably be getters and setters to check for positivity
        # of C and N. Zero value C will throw a division-by-zero error and
        # non-positive N will result in infinite loop.

    def setC(self, c):
        self.C = c

    def setN(self, n):
        self.N = n

    def getC(self):
        return self.C

    def getN(self):
        return self.N

    def get_alphabet(self):
        return self._chars

    def set_alphabet(self, chars):
        try:
            if len(chars) >= 0:
                self._chars = chars
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

        return self._compress(string)

    def _compress(self, string):
        raise NotImplementedError('ACompressor does not implement a ' +
                                  'compression algorithm.')

    def _core(self, string):
        sig = list()
        str_pos = 0
        str_len = len(string)

        while str_pos + self.N < str_len:
            h = self._hash_neighborhood(string, str_pos, self.N)
            self._add_char(sig, h)
            str_pos = str_pos + 1

        return ''.join(sig)

    def _hash_neighborhood(self, string, str_pos, N):
        raise NotImplementedError("The '" + self.__class__.__name__ +
                                  "' compressor module has not implemented " +
                                  "_hash_neighborhood.")

    def _add_char(self, signature, _hash):
        """
        Accept a list of characters 'signature' and append a random character
        from alphabet with 1/C liklihood. This is a function of '_hash'. That
        is, identical values of '_hash' must always add the same character.
        """
        alpha_len = len(self.get_alphabet())

        if _hash % self.C == 0:
            indx = _hash % alpha_len
            char = self.get_alphabet()[indx]
            signature.append(char)


class StringCompressorBasic (ACompressor):
    """
    A basic compressor using a simple, fast algorithm.
    """
    # log = Logger.getLogger(StringCompressorBasic)

    def _compress(self, string):
        return self._core(string)

    def _hash_neighborhood(string, str_pos, N):
        acc = 0
        for i in xrange(N):
            val = ord(string[str_pos + i])
            val <<= i * 8 % 56
            acc ^= val
            acc = abs(acc)

        return acc


class StringCompressorCRC(ACompressor):

    def _compress(self, string):
        return self._core(string)

    def _hash_neighborhood(string, str_pos, N):
        return binascii.crc32(string[str_pos:str_pos + N]) + 2**32


class StringCompressorMD5(ACompressor):

    def _compress(self, string):
        return self._core(string)

    def _hash_neighborhood(string, str_pos, N):
        return int(md5.new(string[str_pos:str_pos + N]).hexdigest(), 16)


class StringCompressorCBasic(ACompressor):

    def _compress(self, string):
        # this will probably have to be Swig C call
        # return compressor.core(string, my_C_hash_n, my_C_add_char)
        return self._core(string)

    def _hash_neighborhood(string, str_pos, N):
        return basic(string, str_pos, N)
