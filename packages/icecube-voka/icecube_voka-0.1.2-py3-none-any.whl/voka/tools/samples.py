'''
This module contains useful tools for creating samples from pickle files.
'''

import os
import pickle
import logging

import numpy

def create_filelist(path, file_select):
    '''
    Walk the path and find all the I3Files matching the given filter.
    file_filter is a callable that returns True/False.
    e.g.
    filter_icecube = lambda fn: "_IT.pkl" not in fn
    '''
    result = list()
    for root, dirs, files in os.walk(path):
        for fn in files:
            if file_select(fn):
                result.append(os.path.join(root, fn))
    return result

def create_sample(filelist, clamp_to_min=dict()):
    '''
    Given a list of input pickle files, add the histograms together.
    The result is a dictionary of only 'bin_values' (type numpy.array),
    which are directly consumable by voka.
    '''
    result = dict()
    for file_path in filelist:
        histograms = pickle.load(open(file_path, 'rb'))
        if 'filelist' in histograms:
            del histograms['filelist']

        # The pickle files contain a 'filelist' member alongside
        # the histograms, so not everything's a histogram.
        # Make sure we only care about objects with 'bin_values'
        if not result:
            result = {k:numpy.array(v['bin_values'])
                      for k,v in histograms.items()
                      if 'bin_values' in v}
            # if we want to include nan_count, over, and under we can do that here.
        else:
            # add histograms
            for k,v in histograms.items():
                if 'bin_values' not in v:
                    continue
                if k not in result:
                    result[k] = numpy.array(v['bin_values'])
                else:
                    h = numpy.array(result[k])
                    r = numpy.add(h, numpy.array(v['bin_values']))
                    result[k] = r
    return result

