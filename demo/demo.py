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

        self._name = file_info[1]
        self._content = StringDescription(
            "contents of " + self._name, file_info[0])
        self._description = fname

    def get(self):
        """
        Return a dict representation.
        """
        d = dict()

        d["CONTENTS"] = self._content.get()
        d["DESCRIPTION"] = self._description

        return d

    def get_name(self):
        return self._name

    def get_text(self):
        return self._content.get_text()

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
        self._files = dict()

        f1 = FileDescription(fname1)
        f2 = FileDescription(fname2)
        self._files[fname1] = f1
        self._files[fname2] = f2

        self._note = "Difference: " + difference

    def get(self):
        d = dict()

        for f in self._files:
            d[f] = self._files[f].get()
        d["DIFFERENCE"] = self._note

        return d

    def get_file_desc(self, fname):
        return self._files[fname]


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


class EstimateDescription(MeasureDescription):

    def __init__(self, note, sd):
        super(type(self), self).__init__(note, sd, LevenSquash.estimate)
        # print("estimate: " + str(sd.get(LevenSquash.estimate)))
        # print("calculate: " + str(sd.get(LevenSquash.calculate)))
        self._error = sd.diff(
            LevenSquash.estimate, LevenSquash.calculate).value()

    def get(self):
        d = dict()
        d["ERROR"] = self._error
        d.update(super(type(self), self).get())

        return d


class DistanceDescription(MeasureDescription):

    def __init__(self, note, sd):
        super(type(self), self).__init__(note, sd, LevenSquash.calculate)


class SquashDescription(Demo):
    """
    Produce a set of statistics on the difference between the two strings,
    'str1' and 'str2', using different measures. Returns a dict composed of
    describe_levenshquash(ls) and assess_distance_measures(str1, str2, ls)
    under keys "LEVENSQUASH MODULE" and "DISTANCE"
    """

    def __init__(self, note, sd):
        self._ls_desc = LevenSquashDescription(
            "ls module desc", sd.get_leven_squash())
        self._estimate_desc = EstimateDescription("a super cool estimate", sd)
        self._corrected_desc = None

    def get(self):
        d = dict()

        d["LEVENSQUASH MODULE"] = self._ls_desc.get()
        d["ESTIMATE"] = self._estimate_desc.get()
        d["CORRECTED"] = ""

        return d


class LevenSquashDescription(Demo):
    """
    Produce a set of descriptions of the LevenSquash instance 'ls'. Returns
    dict composed of describe_compressor and describe_LD_algorithm with keys
    COMPRESSOR and 'LD ALGORITHM'.
    """

    def __init__(self, note, ls):
        self._comp_desc = ProcessDescription(
            ls.get_compressor().get_algorithm())
        self._alg_desc = ProcessDescription(ls.get_ld_alg().get_algorithm)

    def get(self):
        d = dict()

        d["COMPRESSOR"] = self._comp_desc.get()
        d["DISTANCE ALGORITHM"] = self._alg_desc.get()

        return d


class ProcessDescription(Demo):

    def __init__(self, process):
        self._type = process.__class__.__name__
        # self._desc = process.__doc__.replace('\n', '')

    def get(self):
        d = dict()

        d["TYPE"] = self._type

        return d


class DemoFiles(Demo):

    def add(ls):
        """
        Add results for ls to demo
        """
        pass

    def __init__(self, f1, f2, ls):
        start = time.clock()
        print("DEMO: DEMO START...")

        print("DEMO: READING FILES '" + f1 + "' AND '" + f2 + "'...")
        self._file_comp = FileComparison(f1, f2)
        text1 = self._file_comp.get_file_desc(f1).get_text()
        text2 = self._file_comp.get_file_desc(f2).get_text()

        self._score = ScoreDistance(text1, text2, ls)
        print("DEMO: CALCULATING ABSOLUTE LEVENSHTEIN DISTANCE...")
        self._distance = DistanceDescription(
            "absolute distance: ", self._score)

        print("DEMO: PRODUCING SQUASH DEMO...")
        self._squash_desc = SquashDescription("squash desc", self._score)

        print("DEMO: FINISH.")
        print("DEMO: TIME TO PROCESS: " + str(time.clock() - start))

    def get(self):
        d = dict()

        d["FILES"] = self._file_comp.get()
        d["SQUASH"] = self._squash_desc.get()
        d["DISTANCE"] = self._distance.get()

        return d

"""
DistributedDemos contain ListedDemos or other DistributedDemos.
ListedDemos can only contain Descriptions (terminal assessments)
Both define an add() function that accepts the corresponding Description
assessments either:
   extend their related interface
   are more generic

N
C
NAME
IS_CACHED
SIGNATURE_DESCRIPTION

every demo should have a name
"""


class ListedDemo(Demo):

    def __init__(self, demos=[], name=""):
        super(type(self), self).__init__(name)
        self._demos = demos

    def add(demo):
        """
        Add demo to list of demos
        """
        self._demos.append(demos)

    def __repr__(self):
        d = dict()

        d[self.get_name()] = map(lambda d: d.__repr__(), self._demos)

        return str(d)

    def get(item=None):
        if item is None:
            return self._demos
        else:
            try:
                item_results = map(lambda d: d.get(item), self._demos)
                return ListedDemo(item_results, str(item) +
                                  "s in '" + self._name + "'")
            except:
                ValueError()


class DistributedDemo(ListedDemo):

    def __init__(self, demos=[], name=""):
        super(type(self), self).__init__(demos, name)
        for demo in self._demos:
            self.add(demo)

    def add(self, demo):
        pass
