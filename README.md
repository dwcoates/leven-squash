<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#sec-1">1. levensquash</a>
<ul>
<li><a href="#sec-1-1">1.1. LevenSquash</a></li>
</ul>
</li>
<li><a href="#sec-2">2. demo</a>
<ul>
<li><a href="#sec-2-1">2.1. ranges</a></li>
</ul>
</li>
</ul>
</div>
</div>

# levensquash<a id="sec-1" name="sec-1"></a>

## LevenSquash<a id="sec-1-1" name="sec-1-1"></a>

To compute the approximate LD with N=10, C=140, run the following.

    from levenshtein.leven_squash import LevenSquash
    
    comp = Compressor(compression=CRCCompression(), C=140, N=10)
    
    long_string1 = "foo"
    long_string2 = "bar"
    
    ls = LevenSquash(compressor=comp)
    
    est = ls.estimate(longStr1, longStr2)

To produce the corrected distance:

    est_corrected = ls.estimate_corrected(long_str1, long_str2)

The actual true distance is available:

    true = ls.calculate(long_str1, long_str2)

There is a SmartLevenSquash module, a wrapper for LevenSquash. It caches results and produces information like computation time. See API for details.

# demo<a id="sec-2" name="sec-2"></a>

## ranges<a id="sec-2-1" name="sec-2-1"></a>

Runs tests for ranges N=n1-n2, C=c1-c2 in steps of step c, step n. Tests are performed on all non-redundant pairs of files in 'directory'. 

    from ranges import *
    
    n1 = 2
    n2 = 10
    c1 = 100
    c2 = 150
    step_c = 10
    step_n = 1
    
    name = "my_cool_test"
    d = "dir_with_text_files"
    r = "dir_for_results"
    
    test_and_save(name, directory=d, results_dir=r)
    
    results = load_test_results(name, r)

Results is a list of range(n1, n2) \* range(c1, c2) sublists. Each sublists contains exactly results for each of the file pairs, for a total of num<sub>pairs</sub> results in a sublist. These sublists are ordered such that lowest error is first. That is, the lowest error produced for each of the files pairs is stored in as the first sublist, the second lowest errors are in the second sublist, etc. They have the following structure:

    pp.pprint(results[0][0])

Has the following output

    ((0.034853, 140, 5), "some_file__AND__some_other_file")

The next element in the sublist will have larger error.

    pp.pprint(results[0][1])

The next smallest error, packaged with the corresponding C and N value, and the file operated on.

    ((0.04221, 110, 6), "a_third_file__AND__some_other_file")

Use stat(results) to squash the sublists into statistical results. So stats[i] returns a set of statistics on sublist results[i]:

    stats = stat(results)
    
    pp.pprint(stat[0])

Output, for example,

    (1,
     {'MAX':    {'C': 190, 'ERROR': 0.034703203554769815,  'N': 10},
      'MEAN':   {'C': 138, 'ERROR': 0.0094129152080824,    'N': 4},
      'MEDIAN': {'C': 130, 'ERROR': 0.00714506625641351,   'N': 4},
      'MIN':    {'C': 100, 'ERROR': 6.275395742143989e-05, 'N': 2},
      'RANGE':  {'C': 90,  'ERROR': 0.034640449597348376,  'N': 8}})

This data structure can be flattened, filtered, unzipped, etc, to be analyzed. It was called on directories with 15 full-sized book text documents, for a total of 105 file pair. The ranges for N and C were n1=2, n2=40, c1=100, c2=200, with c and n stepping in 10, 1, respectively, for a total of 390 N and C value pairs. This amounted to ~40,000 estimations.