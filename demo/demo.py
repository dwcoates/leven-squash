import pprint

import time
import levenshtein
from levenshtein.utils.entropy import ShannonBasic
from levenshtein.score import ScoreDistance


# + TOP
#   + FILENAMES
#     + FILE 1
#       + FILENAME
#       + TEXT
#       + DESCRIPTION
#       + ENTROPY
#       + LENGTH
#       + COMPRESSION
#         + BASIC
#           + TIME
#           + ENTROPY
#           + LENGTH
#           + ACCURACY (to len(string)/C)
#         + CRC
#           + TIME
#           + ENTROPY
#           + LENGTH
#           + ACCURACY (to len(string)/C)
#         + C BASIC
#           + TIME
#           + ENTROPY
#           + LENGTH
#           + ACCURACY (to len(string)/C)
#         + MD5
#           + TIME
#           + ENTROPY
#           + LENGTH
#           + ACCURACY (to len(string)/C)
#     + FILE 2
#       + FILENAME
#       + TEXT
#       + DESCRIPTION
#       + ENTROPY
#       + LENGTH
#       + COMPRESSION
#         + BASIC
#           + TEXT
#           + TIME
#           + ENTROPY
#           + LENGTH
#           + ACCURACY (to len(string)/C)
#         + CRC
#           + TEXT
#           + TIME
#           + ENTROPY
#           + LENGTH
#           + ACCURACY (to len(string)/C)
#         + C BASIC
#           + TEXT
#           + TIME
#           + ENTROPY
#           + LENGTH
#           + ACCURACY (to len(string)/C)
#         + MD5
#           + TEXT
#           + TIME
#           + ENTROPY
#           + LENGTH
#           + ACCURACY (to len(string)/C)
#   + LEVENSQUASH
#     + COMPRESSOR
#       + TYPE (current compressor module)
#       + DESCRIPTION
#       + COMPRESSION FACTOR
#       + NEIGHBORHOOD SIZE
#     + LD ALGORITHM
#       + TYPE
#       + DESCRIPTION
#   + RESULTS
#     + METRICS
#       + ABSOLUTE
#         + VALUE
#         + SPEED
#         + SIMILARITY
#       + ESTIMATE
#         + VALUE
#         + SPEED
#         + SIMILARITY
#           + VALUE
#           + ERROR
#       + CORRECTED ESTIMATE
#         + VALUE
#         + CORRECTION FACTORS
#         + SPEED
#         + SIMILARITY
#           + VALUE
#           + ERROR
#         + IMPROVEMENT (over ESTIMATE)


def test():
    # throeaway test
    from levenshtein.leven_squash import LevenSquash
    ls = LevenSquash()

    pp = pprint.PrettyPrinter(indent=4)

    pp.pprint(demo("data/test.txt", ls))


def demo(f1, ls):
    d = dict()

    files_description = assess_file(f1, ls.get_compressor())
    levensquash_description = describe_levensquash(ls)

    d["FILES"] = files_description
    d["LEVENSQUASH MODULE"] = levensquash_description

    return d


def assess_files(f1, f2, diff_string=None):
    """
    Read in files 'f1' and 'f2' and produce their descriptions. Returns a dict
    with key FILES consisting of dicts returned by assess_file(f1) and
    assess_file(f2), and, if 'diff_string' is provided, with key DIFFERENCE.
    """
    d = dict()

    if diff_string is not None:
        d["DIFFERENCE"] = diff_string

    f1_description = assess_file(f1)
    f2_description = assess_file(f2)

    d["FILES"] = dict(f1_description).update(f2_description)

    return d


def assess_file(fname, compressor):
    """
    Produce a description of the file 'fname' as a set of values, including
    general description and compression properties. Returns a dict composed of
    describe_file(fname) and assess_compression(file_text) under keys
    ATTRIBUTES and COMPRESSION.
    """

    d = dict()
    d["ATTRIBUTES"] = describe_file(fname)
    file_text = d["TEXT"]
    compression_descriptions = assess_compression(
        file_text, compressor.getC(), compressor.getN())

    d["COMPRESSION"] = compression_descriptions

    return d


def describe_levensquash(ls):
    """
    Produce a set of descriptions of the LevenSquash instance 'ls'. Returns
    dict composed of describe_compressor and describe_LD_algorithm with keys
    COMPRESSOR and 'LD ALGORITHM'.

    """
    d = dict()

    compressor_description = describe_compressor(ls.get_compressor())
    algorithm_description = describe_LD_algorithm(ls.get_ld_alg())

    d["COMPRESSOR"] = compressor_description
    d["LD ALGORITHM"] = algorithm_description

    return d


def describe_compressor(compressor):
    """
    Produce a set of descriptions of the compressor instance 'compressor'.
    Returns dict with keys TYPE, C, N, and DESCRIPTION.

    """
    d = dict()

    d["TYPE"] = compressor.__class__.__name__
    d["C"] = compressor.getC()
    d["N"] = compressor.getN()

    d["DESCRIPTION"] = compressor.__doc__.replace('\n', '')

    return d


def describe_LD_algorithm(algorithm):
    """
    Produce a set of descriptions of the LD algorithm instance 'algorithm'.
    Returns dict with keys TYPE and DESCRIPTION.

    """
    d = dict()

    d["TYPE"] = algorithm.__class__.__name__

    d["DESCRIPTION"] = algorithm.__doc__.replace('\n', '')

    return d


def parse_file(fname):
    """
    Read file, and parse for description and text. Returns dict with keys
    FILENAME, TEXT and DESCRIPTION.
    """
    d = dict()
    d["FILENAME"] = fname

    with open(fname) as f:
        d["TEXT"] = f.read().replace('\n', '')

    # Currently just returns file text
    d["DESCRIPTION"] = ""

    return d


def describe_string(string):
    """
    Produce a set of basic attributes of the string 'string'. Returns a dict
    with keys LENGTH and ENTROPY.
    """
    d = dict()

    d["LENGTH"] = len(string)

    sb = ShannonBasic()
    ent = sb.calculate(string)
    d["ENTROPY"] = ent

    return d


def describe_file(fname):
    """
    Produce a description of the file 'fname' as a set of values. Returns a
    dict composed of parse_file(fname) and describe_string(file_text)
    """

    d = parse_file(fname)
    file_text = d["TEXT"]
    file_text_description = describe_string(file_text)

    d.update(file_text_description)

    return d


def assess_compression(string, C, N):
    """
    Produce data on the various compressors acting on string.
    """
    d = dict()

    d["BASIC"] = describe_compression(
        string, levenshtein.compression.StringCompressorBasic(C, N))
    d["C BASIC"] = describe_compression(
        string, levenshtein.compression.StringCompressorCBasic(C, N))
    d["CRC"] = describe_compression(
        string, levenshtein.compression.StringCompressorCRC(C, N))
    d["BASIC"] = describe_compression(
        string, levenshtein.compression.StringCompressorMD5(C, N))

    return d


def describe_compression(string, compressor):
    """
    Produce data on compressor 'compressor' acting on 'string'. Returns a dict
    with keys 'TIME' and 'ACCURACY' composed with a dict returned by
    describe_string(string).
    """
    d = dict()

    start = time.clock()
    sig = compressor.compress(string)
    end = time.clock()
    t = end - start

    d["TEXT"] = sig

    d["TIME"] = t

    sig_description = describe_string(sig)
    d.update(sig_description)

    difference = levenshtein.score.ScoreDistance.difference
    accuracy = difference(sig_description["LENGTH"],
                          (1 / float(compressor.getC())))

    d["ACCURACY"] = accuracy

    return d


def describe_ls_module(ls):
    """
    Returns a description of LevenSquash module 'ls' as a set of values.
    """

    # Returns TOP/LEVENSQUASH

    pass


def compare_strings(str1, str2, ls):
    """
    Produce a set of statistics on the difference between the two strings,
    'str1' and 'str2', using different measures. Returns a dict composed of
    assess_distance_measures(str1, str2, ls)

    """

    # Returns TOP/RESULTS/METRICS

    pass


def assess_string(string):
    """
    Return a set of statistics on the string 'string'. This includes, length,
    entropy, description, and effects of compression on the string.
    """
    pass


def assess_compressors(string):
    """
    Return a set of statistics on the compression string 'string' using the
    various compressors.
    """

    # Calls assess_compressor
    pass


def assess_compressor(string, compressor):
    """
    Return a set of statistics on the compression string 'string' using
    compressor 'compressor'.
    """

    pass


def assess_distance_measures(str1, str2, ls):
    """
    Return a set of statistics on various distance evaluations for 'str1'.
    and 'str2'. This includes, length, and entropy.
    """
    pass


def dist_measure_statistics(str1, str2, measure):
    """
    Return a set of statistics on distance calculation 'measure' for 'str1'.
    and 'str2'. This includes value, speed, and measured similarity.
    """

    # Called by assess_calculate, assess_estimate, assess_estimate_corrected

    pass


def assess_calculate(str1, str2, ls):
    """
    Return a set of statistics on ls.calculate().
    """
    pass


def assess_estimate(str1, str2, ls):
    """
    Return a set of statistics on ls.estimate(). Also specifies value of
    similarity and error of similarity value.
    """
    pass


def assess_estimate_corrected(str1, str2, ls):
    """
    Return a set of statistics on ls.estimate_corrected(). Also specifies
    value of similarity, error of similarity value, and improvement over
    ls.estimate().
    """
    pass


def assess_compressors(string):
    """
    Return a dict comprised of assessments on all implemented compressors.
    """
    pass


def assess_compressor(string, compressor):
    """
    Return a set of statistics on the compression quality of 'compressor' on
    'string'. Returns information on entropy of input / output, signature length,
    speed, etc.
    """
    pass


def assess_LD_calculation(string, ls):
    """
    Return a set of basic statistics on LD algorithm implementation of ls.
    """
