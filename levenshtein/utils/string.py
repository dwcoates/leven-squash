from random import choice
import re

import alphabet


def random_string(length, alpha=alphabet.ALPHABET_BASIC):
    try:
        lis = list(alpha)
        return ''.join(choice(lis) for _ in xrange(length))
    except ValueError:
        error_str = ''
        if length <= 0:
            error_str += "Random string must be of non-zero length"
        if alpha <= 0:
            error_str += '\n' + "Invalid alphabet supplied."
        raise ValueError(error_str)
    except:
        raise


def normalize_english(text):
    """
    Normalize text. Remove punctuation, make all lower case, etc. To be used for determining the entropy of English text, not for signatures.
    """
    cleaner = re.compile('[^a-z]+')

    return cleaner.sub(' ',text.lower().strip())
