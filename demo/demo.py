import pprint
import pickle
import time

import levenshtein
from levenshtein.leven_squash import LevenSquash
from levenshtein.utils.entropy import ShannonBasic
from levenshtein.score import ScoreDistance


# + TOP
#   + FILES
#     + *file name* (first file)
#       + FILENAME
#       + DESCRIPTION
#       + CONTENT
#         + TEXT
#         + ENTROPY
#         + LENGTH
#     + *file name* (second file)
#       + FILENAME
#       + DESCRIPTION
#       + CONTENT
#         + TEXT
#         + ENTROPY
#         + LENGTH
#   + COMPRESSION
#     [
#     . . .
#     . . .
#       + *file name* (first file)
#         + N
#         + C
#         + RESULTS
#           + BASIC
#             + SIGNATURE
#               + TEXT
#               + ENTROPY
#               + LENGTH
#             + TIME
#             + ACCURACY (to len(string)/C)
#           + CRC
#             + SIGNATURE
#               + TEXT
#               + ENTROPY
#               + LENGTH
#             + TIME
#             + ACCURACY (to len(string)/C)
#           + C BASIC
#             + TIME
#             + SIGNATURE
#               + TEXT
#               + ENTROPY
#               + LENGTH
#             + TIME
#             + ACCURACY (to len(string)/C)
#           + MD5
#             + SIGNATURE
#               + TEXT
#               + ENTROPY
#               + LENGTH
#             + TIME
#             + ACCURACY (to len(string)/C)
#       + *file name* (second file)
#         + N
#         + C
#         + RESULTS
#           + BASIC
#             + SIGNATURE
#               + TEXT
#               + ENTROPY
#               + LENGTH
#             + TIME
#             + ACCURACY (to len(string)/C)
#           + CRC
#             + SIGNATURE
#               + TEXT
#               + ENTROPY
#               + LENGTH
#             + TIME
#             + ACCURACY (to len(string)/C)
#           + C BASIC
#             + TIME
#             + SIGNATURE
#               + TEXT
#               + ENTROPY
#               + LENGTH
#             + TIME
#             + ACCURACY (to len(string)/C)
#           + MD5
#             + SIGNATURE
#               + TEXT
#               + ENTROPY
#               + LENGTH
#             + TIME
#             + ACCURACY (to len(string)/C)
#     . . .
#     . . .
#     ]
#   + DISTANCE
#       + ABSOLUTE
#         + VALUE
#         + SPEED
#         + DIFFERENCE
#   + ESTIMATATION
#     [
#     . . .
#     . . .
#       + LEVENSQUASH
#         + COMPRESSOR
#           + TYPE (current compressor module)
#           + DESCRIPTION
#           + C
#           + N
#         + LD ALGORITHM
#           + TYPE
#           + DESCRIPTION
#       + ESTIMATE
#         + VALUE
#         + SPEED
#         + DIFFERENCE
#         + ERROR
#       + CORRECTED ESTIMATE
#         + VALUE
#         + CORRECTION FACTORS
#         + SPEED
#         + DIFFERENCE
#         + ERROR
#         + IMPROVEMENT
#       + SIMILARITY
#         + TBD
#     . . .
#     . . .
#     ]

def parse_file(fname):
    """
    Read file, and parse for description and text. Returns tuple with elements
    (text, description)
    """
    with open(fname) as f:
        text = f.read().replace('\n', '')

    # Currently just returns file text
    description = ""

    return (text, description)


def assess_estimation(sd):
    """
    Produce a set of statistics on the difference between the two strings,
    'str1' and 'str2', using different measures. Returns a dict composed of
    describe_levenshquash(ls) and assess_distance_measures(str1, str2, ls)
    under keys "LEVENSQUASH MODULE" and "DISTANCE"
    """
    d = dict()

    d["LEVENSQUASH MODULE"] = describe_levensquash(sd.get_leven_squash())
    d["ESTIMATE"] = describe_measure(LevenSquash.estimate, sd)
    d["CORRECTED"] = describe_measure(LevenSquash.estimate_corrected, sd)
    return d


def describe_file(fname):
    """
    Produce an assessment of the file 'fname' as a set of values. Returns a
    dict composed of describe_file(fname) and describe_compression(file_text)
    under keys ATTRIBUTES and COMPRESSION.
    """
    d = dict()

    file_contents = parse_file(fname)
    file_text = file_contents[0]
    file_description = file_contents[1]

    d["PATH"] = fname
    d["DESCRIPTION"] = file_description
    d["CONTENT"] = describe_string(file_text)

    return d


def describe_files(f1, f2, diff_string="NOT SPECIFIED"):
    """
    Read in files 'f1' and 'f2' and produce their assessment. Returns a dict
    with key DIFFERENCE and key FILES, consisting of dicts returned by
    describe_file(f1) and describe_file(f2).
    """
    d = dict()

    d["DIFFERENCE"] = diff_string

    d[f1] = describe_file(f1)
    d[f2] = describe_file(f2)

    return d


def describe_levensquash(ls):
    """
    Produce a set of descriptions of the LevenSquash instance 'ls'. Returns
    dict composed of describe_compressor and describe_LD_algorithm with keys
    COMPRESSOR and 'LD ALGORITHM'.

    """
    d = dict()

    d["COMPRESSOR"] = describe_compressor(ls.get_compressor())
    d["DISTANCE ALGORITHM"] = describe_LD_algorithm(ls.get_ld_alg())

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


def describe_string(string):
    """
    Produce a set of basic attributes of the string 'string'. Returns a dict
    with keys LENGTH and ENTROPY.
    """
    d = dict()

    d["TEXT"] = string
    d["LENGTH"] = len(string)
    d["ENTROPY"] = ShannonBasic().calculate(string)

    return d


def describe_compression(string, C, N):
    """
    Produce data on the various compressors acting on string.
    """
    d = dict()

    d["C"] = C
    d["N"] = N
    d["COMPRESSION"] = assess_compressors(string, C, N)

    return d


def assess_compressors(string, C, N):
    d = dict()

    d["BASIC"] = assess_compressor(
        string, levenshtein.compression.StringCompressorBasic(C, N))
    d["C BASIC"] = assess_compressor(
        string, levenshtein.compression.StringCompressorCBasic(C, N))
    d["CRC"] = assess_compressor(
        string, levenshtein.compression.StringCompressorCRC(C, N))
    d["BASIC"] = assess_compressor(
        string, levenshtein.compression.StringCompressorMD5(C, N))

    return d


def assess_compressor(string, compressor):
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

    sig_description = describe_string(sig)

    difference = ScoreDistance.difference
    accuracy = difference(sig_description["LENGTH"],
                          (len(string) / float(compressor.getC())))

    d["SIGNATURE"] = sig_description
    d["TIME"] = t
    d["ACCURACY"] = accuracy

    return d


def assess_string(string, compressor):
    """
    Produce a set of statistics on the string 'string'. Returns a dict
    composed ofdescribe_string(string) and
    describe_compression(string, compressor) under keys COMPRESSION and
    ATTRIBUTES.

    """
    d = describe_string(string)

    d["COMPRESSION"] = describe_compression(
        string, compressor.getC(), compressor.getN())

    return d


def describe_measure(measure, sd):
    """
    Produce a set of statistics on ls.calculate(). Returns a dict with keys
    VALUE, SPEED, SIMILARITY
    """
    d = dict()
    diff = ScoreDistance.difference
    m = measure.__name__

    d["VALUE"] = sd.value(m)
    d["TIME"] = sd.time(m)
    d["ERROR"] = diff(sd.value(m), sd.value("calculate"))

    return d


def assess_calculate(str1, str2, ls):
    """
    Produce a set of statistics on ls.calculate(). Returns a dict with keys
    VALUE, SPEED, SIMILARITY
    """
    return describe_measure(str1, str2, ls.calculate)


def assess_estimate(str1, str2, ls):
    """
    Return a set of statistics on ls.estimate(). Also specifies value of
    similarity and error of similarity value.
    """
    d = describe_measure(str1, str2, ls.estimate)

    start = time.clock()
    exact = ls.calculate()
    end = time.clock()
    t_exact = end - start

    d["SPEEDUP"] = ScoreDistance.difference(d["TIME"], t_exact)
    d["ACCURACY"] = ScoreDistance.difference(d["VALUE"], exact)

    pass


def assess_estimate_corrected(str1, str2, ls):
    """
    Return a set of statistics on ls.estimate_corrected(). Also specifies
    value of similarity, error of similarity value, and improvement over
    ls.estimate().
    """
    pass


################################################
##############    TEST FUNCTIONS ###############
################################################


def test():
    # throeaway test
    from levenshtein.leven_squash import LevenSquash
    t = 0
    d = dict()

    print("TEST: PROCESSING 4 DEMOS...")
    print("\n\nTEST: DEMO 1...")
    f1 = "data/adventures_of_huckleberry_finn.txt"
    f2 = "data/adventures_of_tom_sawyer.txt"
    d.update(clean(demo(f1, f2, LevenSquash(),
                        "Two similar stories written by the same author"), f1, f2))
    t += d["DEMO RUN TIME"]
    save_data(d, "huck_and_sawyer")

    print("\n\nTEST: DEMO 2...")
    f1 = "data/dantes_inferno_english_sibbald.txt"
    f2 = "data/dantes_inferno_english_longfellow.txt"
    d.update(clean(demo(f1, f2, LevenSquash(),
                        "Two different translations of the same book"), f1, f2))
    t += d["DEMO RUN TIME"]
    save_data(d, "sibbald_and_longfellow")

    print("\n\nTEST: DEMO 3...")
    f1 = "data/adventures_of_huckleberry_finn.txt"
    f2 = "data/dantes_inferno_english_sibbald.txt"
    d.update(clean(demo(f1, f2, LevenSquash(),
                        "Two totally different english books"), f1, f2))
    t += d["DEMO RUN TIME"]
    save_data(d, "huck_and_sibbald")

    print("\n\nTEST: DEMO 4...")
    f1 = "data/dantes_inferno_italian.txt"
    f2 = "data/dantes_inferno_english_longfellow.txt"
    d.update(clean(demo(f1, f2, LevenSquash(),
                        "Same book in two different languages"), f1, f2))
    t += d["DEMO RUN TIME"]
    save_data(d, "italian_and_english")

    print("\n\nTEST: FINISHED.")
    print("\TEST: TIME TO COMPLETE: " + str(t))

    return d
    # return pp.pformat(demo(ls, f1, f2))
    # print(pp.pformat(demo(ls, f1, f2)))


def clean(d, f1, f2):
    d["INPUT"][f1]["CONTENT"]["TEXT"] = ""
    d["INPUT"][f2]["CONTENT"]["TEXT"] = ""

    return d


def test_load(d="data"):
    return load_data(d)


def pdemo(demo_results):
    pp = pprint.PrettyPrinter(indent=4)

    pp.pprint(demo_results)

    # return pp.pformat(demo(ls, f1, f2))
    # print(pp.pformat(demo(ls, f1, f2)))


def demo(f1, f2, ls=LevenSquash(), description=""):
    start = time.clock()
    print("DEMO: DEMO START...")

    d = dict()

    print("DEMO: READING FILES '" + f1 + "' AND '" + f2 + "'...")
    d["INPUT"] = describe_files(f1, f2, description)

    f1_text = d["INPUT"][f1]["CONTENT"]["TEXT"]
    f2_text = d["INPUT"][f2]["CONTENT"]["TEXT"]

    print("DEMO: CALCULATING ABSOLUTE LEVENSHTEIN DISTANCE...")
    sd = ScoreDistance(f1_text, f2_text, ls)

    d["DISTANCE"] = describe_measure(LevenSquash.calculate, sd)

    n1 = 2
    n2 = 10
    c1 = 100
    c2 = 250
    print("DEMO: ESTIMATING OVER RANGES OF C=" + str(c1) + ",C=" + str(c2) +
          " AND N=" + str(n1) + ",N=" + str(n2) + " ...")
    print("DEMO: N BETWEEN " + str(n1) + " AND " + str(n2))
    estimates = list()
    compressions = list()
    for n in xrange(n1, n2):
        print("DEMO: N=" + str(n))
        sd.setN(n)
        for c in xrange(c1, c2, 10):
            sd.setC(c)
            estimates.append(estimate(sd))
            compressions.append(
                compress(f1_text, f2_text, f1, f2, sd.getC(), sd.getN()))

    # computations = compute(f1_text, f2_text, sd, f1, f2)

    d["ESTIMATION"] = estimates
    d["COMPRESSION"] = compressions

    end = time.clock()
    t = end - start

    print("DEMO: FINISH.")
    print("DEMO: TIME TO PROCESS: " + str(t))

    d["DEMO RUN TIME"] = t

    return d


def estimate(sd):
    d = dict()

    d = assess_estimation(sd)

    return d


def compress(str1, str2, str1_name, str2_name, C, N):
    d = dict()

    d[str1_name] = describe_compression(str1,
                                        C,
                                        N)
    d[str2_name] = describe_compression(str2,
                                        C,
                                        N)

    return d


class DemoBase:

    def get():
        """
        Return a dict representation.
        """
    def __repr__():
        """
        Return formatted string-represented dict.
        """

        raise NotImplementedError()

    def __str__():
        """
        Return formatted string-represented dict. May truncate long strings.
        """
        raise NotImplementedError()

    def save_data(d, name):
        # TODO: Implement
        with open('records/' + name + '.pkl', 'wb') as f:
            pickle.dump(d, f, pickle.HIGHEST_PROTOCOL)

    def load_data(name):
        # TODO: Implement
        with open('records/' + name + '.pkl', 'rb') as f:
            return pickle.load(f)


class Description(DemoBase):
    pass


class Assessment(DemoBase):
    _DESCRIPTION_TYPE = None

    def __init__(self, DESCRIPTION_TYPE):
        self._descriptions = dict()
        self._DESCRIPTION_TYPE = DESCRIPTION_TYPE

    def add(self, name, description):
        provided_desc_typename = description.__class__.__name__
        class_desc_typename = self.__class__._DESCRIPTION_TYPE
        if provided_desc_typename != class_desc_typename:
            raise TypeError("Demo Assessment class '" +
                            self.__class__.__name__ +
                            "' only adds Descriptions of type '" +
                            class_desc_typename +
                            ". Recieved Description of type '" +
                            provided_desc_typename)
        self._descriptions[name] = description

    def _get_values(self, get_attribute_method):
        d = dict()

        for key in self._descriptions:
            d[key] = self._descriptions[key].get_attribute_method()

        return d

    def __repr__(self):
        """
        Returns a formatted dict of demo results, generally with computation
        results at the lowests levels of the dictionary. For example, a
        CompressorAssessment may have 100 CompressorDescriptions, but will not
        simply return a list of CompressorDescription.__repr__(). Instead, for
        example, TIME/ will contain 100 entries, instead of 100 TIME entries
        (one for each CompressorDescription), each with one subentry.
        """
        raise NotImplementedError()


class StringDescription(Description):

    def __init__(self, string, note):
        self._string = string
        self._note = note
        self._entropy = ShannonBasic().calculate(string)

    def get(self):
        """
        Return a dict representation of data.
        """
        d = dict()

        d["TEXT"] = self._string
        d["LENGTH"] = self.get_length()
        d["ENTROPY"] = self._entropy

        return d

    def get_length(self):
        return len(self._string)

    def get_text(self):
        return self._string

    def get_entropy(self):
        return self._entropy


class CompressorDescription(Description):

    def __init__(self, compressor, string):
        signature = compressor.compress(string)
        diff = ScoreDistance.difference
        self._name = compressor.__class__.__name__
        self._sig_desc = StringDescription(signature.value())
        self._time = signature.time()
        self._accuracy = diff(self._sig_desc.get_length(),
                              len(string) / compressor.getC())

    def add(self, C, N):
        if N not in self._compressions:
            self._compressions[N] = dict()

        self._compressions[N][C] = CompressorDescription(
            self._compressor, C, N)


class CompressorAssessment(DemoBase):

    def __init__(self, compressor):
        self._compressions = dict()
        self._compressor = compressor

    def add(self, C, N):
        if N not in self._compressions:
            self._compressions[N] = dict()

        self._compressions[N][C] = CompressorDescription(
            self._compressor, C, N)

    def get(self):
        """
        Return a dict representation.
        """
        d = dict()

        # create array of signatures
        # create array of lengths
        # create array

        pass

    def _foo(d, quality):
        """
        Accepts a dict of descriptions, and returns a list of key:values,
        the keys for which are the keys of the provided dict, and the values
        are the values are the qualities in the provided key's corresponding
        descprition
        """


class FileDescription(DemoBase):

    def __init__(self, fname):
        file_info = self._parse_file(fname)

        self._content = StringDescription(file_info[0])
        self._description = file_info[1]

    def get(self):
        """
        Return a dict representation.
        """
        d = dict()

        d["CONTENTS"] = self._text.get()
        d["DESCRIPTION"] = self._description
        pass

    @staticmethod
    def _parse_file(fname):
        """
        Read file, and parse for description and text. Returns tuple with
        elements (text, description)
        """
        with open(fname) as f:
            text = f.read().replace('\n', '')

        # Currently just returns file text
        description = ""

        return (text, description)
