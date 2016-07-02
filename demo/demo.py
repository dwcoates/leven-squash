import pprint
import pickle
import time

import levenshtein
from levenshtein.leven_squash import LevenSquash
from levenshtein.compression import *
from levenshtein.utils.entropy import ShannonBasic
from levenshtein.utils.computation import *
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


class Demo(object):

    def __init__(self, result, note="NOT SPECIFIED", **kwargs):
        self._note = note
        self._result = result

    def get(self):
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


class Description(Demo):
    pass


class Assessment(Demo):
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

    def __init__(self, note, string, limit=1000):
        self._note = note
        self._string = string
        self._entropy = ShannonBasic().calculate(self._string)
        self._string_limit = limit

    def get(self):
        """
        Return a dict representation of data.
        """
        d = dict()

        d["NOTE"] = self._note
        d["TEXT"] = self._string[0:self._string_limit]
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

    def __init__(self, name, compressor, string_desc):
        string = string_desc.get_text()
        signature = ComputationManager.CREATE_COMPUTATION(
            compressor.compress, string)
        print type(signature.value())
        diff = ScoreDistance.difference

        if name is None:
            self._name = compressor.__class__.__name__
        else:
            self._name = name
        self._source_len = string_desc.get_length()
        self._source_entropy = string_desc.get_entropy()
        self._sig_desc = StringDescription(
            "Signature: " + self._name, signature.value())
        self._time = signature.time()
        self._accuracy = diff(self._sig_desc.get_length(),
                              len(string) / float(compressor.getC()))

    def add(self, C, N):
        if N not in self._compressions:
            self._compressions[N] = dict()

        self._compressions[N][C] = CompressorDescription(
            self._compressor, C, N)

    def get(self):
        d = dict()

        d["SOURCE LENGTH"] = self._source_len
        d["SOURCE ENTROPY"] = self._source_entropy
        d["SIGNATURE DESCRIPTION"] = self._sig_desc.get()
        d["TIME"] = self._time
        d["ACCURACY"] = self._accuracy
        d["DESCRIPTION"] = self._name

        return d


class CompressorAssessment(Assessment):

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
        for n in self._compressions:
            for c in self._compressions[n]:
                d[n][c] = self._compressions[n][c].get()

        return d

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


class FileDescription(Demo):

    def __init__(self, fname):
        file_info = self._parse_file(fname)

        self._content = StringDescription(file_info[1], file_info[0])
        self._description = fname

    def get(self):
        """
        Return a dict representation.
        """
        d = dict()

        d["CONTENTS"] = self._content.get()
        d["DESCRIPTION"] = self._description

        return d

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


class FileComparison(Demo):

    def __init__(self, fname1, fname2, difference="NOT SPECIFIED"):
        self._f1 = FileDescription(fname1)
        self._f2 = FileDescription(fname2)
        self._note = "Difference: " + difference

    def get(self):
        d = dict()

        d["FILE 1"] = self._f1.get()
        d["FILE 2"] = self._f2.get()

        return d


class MeasureDescription(Demo):
    """
    Produce a set of statistics on ls.calculate(). Returns a dict with keys
    VALUE, SPEED, SIMILARITY
    """

    def __init__(self, note, sd, measure):
        c = sd.get(measure)
        self._value = c.value()
        self._time = c.time()
        self._description = note + measure.__name__

    def get(self):
        d = dict()

        d["VALUE"] = self._value
        d["TIME"] = self._time
        d["DESCRIPTION"] = self._description

        return d


class EstimationDescription(MeasureDescription):

    def __init__(self, note, sd):
        super(type(self), self).__init__(note, sd, LevenSquash.estimate)
        self._error = sd.diff(
            LevenSquash.estimate, LevenSquash.calculate)

    def get(self):
        d = dict()
        d["ERROR"] = self._error
        d.update(super(type(self), self).get())

        return d


class DistanceDescription(MeasureDescription):

    def __init__(self, note, sd):
        super(type(self), self).__init__(note, sd, LevenSquash.calculate)


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


def describe_LD_algorithm(algorithm):
    """
    Produce a set of descriptions of the LD algorithm instance 'algorithm'.
    Returns dict with keys TYPE and DESCRIPTION.

    """
    d = dict()

    d["TYPE"] = algorithm.__class__.__name__

    d["DESCRIPTION"] = algorithm.__doc__.replace('\n', '')

    return d
