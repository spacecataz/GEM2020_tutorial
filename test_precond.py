#!/usr/bin/env python
'''
This is the test suite for our repository.  It uses Python's built in tools,
"unittest".  Instructions on using unittest can be found here:

https://docs.python.org/3/library/unittest.html

To use this script, just call it from the command line:

>>> python3 test_precond.py

There are alternative testing tools for Python, including Pytest and Nose.
These are not in the Python standard library (they need to be installed
separately, like Numpy or Matplotlib).  They have additional functionality
and are well liked by the community, but we don't need anything too fancy here.
'''

import unittest
import datetime as dt
from numpy import array
from numpy.testing import assert_array_equal
import precond2

class TestLoadOmni(unittest.TestCase):
    '''
    Test functionality of OMNI data reader.
    '''

    # Start with some known results to test against.
    # In this case, it's the entire omni_test.lst data and
    # the final record from the omni_july2000.lst files.
    knownData = {'b': array([ 1.,  2.,  3.,  4.,  5.,  6.]),
                 'bx': array([ 1.,  1.,  1.,  1.,  1.,  1.]),
                 'by': array([ 0.,  1.,  0., -1.,  1.,  1.]),
                 'bz': array([ 1.,  0., -1.,  0.,  1.,  1.]),
                 'dens': array([ 12.5,  12.5,  12.5,  12.5,  12.5,  12.5]),
                 'dst': array([-57., -57., -57., -57., -57., -57.]),
                 'pdyn': array([ 9.3,  9.3,  9.3,  9.3,  9.3,  9.3]),
                 'time': array([dt.datetime(2000, 7, 14, 12, 0),
                                dt.datetime(2000, 7, 14, 13, 0),
                                dt.datetime(2000, 7, 14, 16, 0),
                                dt.datetime(2000, 7, 14, 18, 0),
                                dt.datetime(2000, 7, 15, 13, 0),
                                dt.datetime(2000, 7, 15, 14, 0)],
                               dtype=object),
                 'v': array([ 610.,  610.,  610.,  610.,  610.,  610.])}

    knownRecord = {'b':7.4, 'bx':4.4, 'by':5.7, 'bz':-1.7,
                   'dens':3.3, 'v':478.0, 'pdyn':1.58, 'dst':-61.0,
                   'time':dt.datetime(2000,7,20,23,0,0)}

    def testReadSimple(self):
        data = precond2.load_omni('data/omni_test.lst')
        for k in self.knownData:
            assert_array_equal( self.knownData[k], data[k])

    def testReadJuly(self):
        data = precond2.load_omni('data/omni_july2000.lst')
        for k in self.knownRecord:
            self.assertEqual(self.knownRecord[k], data[k][-1])
            
class TestClock(unittest.TestCase):
    knownClock = array([  90.,    0.,  -90.,  180.,   45.,   45.])

    def testClock(self):
        data = precond2.load_omni('data/omni_test.lst')
        precond2.calc_clock(data)
        assert_array_equal(self.knownClock, data['clock'])

class TestPrecond(unittest.TestCase):
    knownMeans = {'b': 3.5,
                  'bx': 1.0,
                  'by': 0.25,
                  'bz': 0.0,
                  'clock': 33.75,
                  'dens': 12.5,
                  'dst': -57.0,
                  'pdyn': 9.3000000000000007,
                  'v': 610.0}

    def testMeans(self):
        
        t = dt.datetime(2000,7,15,13,0,0)
        filename = 'data/omni_test.lst'
        means = precond2.get_precond(filename, t)

        for m in self.knownMeans:
            self.assertEqual(self.knownMeans[m], means[m])
        
if __name__ == '__main__':
    unittest.main()
