#!/usr/bin/env python
'''
This script reads in an OMNIWeb solar wind file and, given a storm start time
("epoch"), will do the following:

 - Read the data file, parse the contents.
 - Calculate the clock angle of the solar wind.
 - Identify the portion of the data that is within 24 hours before
 - the given epoch.
 - Calculates and writes the mean and median of certain values to screen.

The input file MUST be an omniweb data file obtained via 
https://omniweb.gsfc.nasa.gov/form/dx1.html.

This version is more modular and leverages more "pythonic" language features.

DTW, 2020, GEM Student Tutorial
'''

# Always start with imports at the top!
import datetime as dt
import numpy as np

#### Function definitions:
def load_omni(filename):
    '''
    Read a *.lst file obtained from https://omniweb.gsfc.nasa.gov/form/dx1.html.
    Return a dictionary of values where each value is a numpy array.

    Data is assumed to be regularly spaced in time.
    File must have the following variables in this order: 
    1 YEAR                          I4
    2 DOY                           I4
    3 Hour                          I3
    4 Scalar B, nT                  F6.1
    5 BX, nT (GSE, GSM)             F6.1
    6 BY, nT (GSM)                  F6.1
    7 BZ, nT (GSM)                  F6.1
    8 SW Proton Density, N/cm^3     F6.1
    9 SW Plasma Speed, km/s         F6.0
    10 Flow pressure                F6.2
    11 Dst-index, nT                I6


    Parameters
    ==========
    filename : string
       Path/name of file to load.

    Other Parameters
    ================

    Returns
    =======
    data : dict
        A dictionary of numpy vectors containing the parsed data.

    Examples
    ========
    >>> data = load_omni('data/omni_test.py')
    >>> data.keys()
    >>> data['bx']

    '''

    # Because we assume the layout of our file, the variable list can be
    # hard coded.  This is a major limitation...
    varnames = ['b', 'bx', 'by', 'bz', 'dens', 'v', 'pdyn', 'dst']
    
    # Open file and slurp in contents using "with" statement.
    with open(filename,'r') as f:
        lines = f.readlines()

    # Get number of records in the file:
    nRec = len(lines)

    # Create a container to hold the data.  We'll use a dictionary, which
    # is an associative array in Python.  Each "key" will be the variable
    # name (as we define above in `varnames`) and each "value" will be a
    # numpy array with the correct number of records.
    data = {} # Empty dict.
    for v in varnames:
        data[v] = np.zeros(nRec)
    # We're using datetimes, so the numpy array for time is a bit special.
    data['time'] = np.zeros(nRec, dtype=object)

    # Now, read the file.  Loop over all lines, keeping track of the
    # line number.
    for i, l in enumerate(lines):
        
        # Break the line into parts based on whitespace:
        parts = l.split()

        # For time, we want to create datetimes instead of DOY.HH floats.
        # We have Year, DOY, and Hour in the file.  We'll turn that into
        # a date time by creating a datetime of the year and adding the
        # days and hours to that.
        data['time'] = dt.datetime(int(parts[0]), 1, 1, 0, 0) + \
                       dt.timedelta(days=int(parts[1]), hours=int(parts[2]))

        # The rest of the values can just be stuffed into the right spot in
        # the dictionary!
        for j, v in enumerate(varnames):
            data[v][i] = parts[j+2]

    # Return the dictionary to the caller:
    return data
        
def calc_clock(data):
    '''
    Given a dictionary of values produced by load_omni, calculate the
    IMF clock angle and add to the dictionary.

    Parameters
    ==========
    data : dict
       Dictionary of solar wind values as given by the load_omni function.

    Other Parameters
    ================

    Returns
    =======
    None

    Examples
    ========
    >>> data = load_omni('data/omni_test.py')
    >>> calc_clock(data)
    >>> data['clock']

    '''

    # See precond1.py for details on this calculation.
    data['clock'] = (180.0/np.pi)*np.arctan2(data['bz'], data['by'])

def get_precond(filename, epoch, span=24, debug=False):
    '''
    For a OMNIweb hourly data file and epoch of a geomagnetic storm start,
    find the mean solar wind characteristics for the time leading up to it.
    Parameters
    ==========
    data : dict
       Dictionary of solar wind values as given by the load_omni function.

    Other Parameters
    ================

    Returns
    =======
    None

    Examples
    ========
    >>> import datetime as dt
    >>> epoch = dt.datetime(2000,7,15,13,0,0)
    >>> means = get_precond(filename, epoch)
    >>> print(means)

    '''

    # Open file, load data:
    data = load_omni(filename)

    # Calculate clock angle:
    calc_clock(data)

    # Now, let's get to work.  We want to create a mask
    # that hides times not within our window.  Numpy can
    # do this very easily!  "mask" will be an array of
    # booleans that has the same time and shape as data['time'].
    # However, it will only be `True` when the conditions pass:
    mask = (data['time']>=epoch-dt.timedelta(days=1))&(data['time']<=epoch)

    # Create a container of output:
    means = {}
    
    # Now, we can get means for all values using this mask:
    for varname in data.keys():
        # Don't average time, of course.
        if varname=='time': continue
        # Note how we use the boolean array to index our data:
        means[varname] = data[varname][mask].mean()

    # Some debug work.  Note the use of "f-strings": formatted
    # strings that begin with f before the quotes.
    # Google on how to format times in strings as below.
    if debug:
        print(f'DEBUG INFO:')
        print(f'\tFilename = {filename}')
        print(f'\tEpoch = {epoch:%Y-%m-%d %H UT}')
        print(f'\tStart time = {data["time"][mask][ 0]:%Y-%m-%d %H UT}')
        print(f'\tEnd time   = {data["time"][mask][-1]:%Y-%m-%d %H UT}')
              
        
    # And that's it!
    return means

if __name__ == '__main__':
    # If we run this file as a script, execute this portion.
    # If we import this file and use it as an API, this part
    # is not executed.

    # Storm epoch:
    t = dt.datetime(2000,7,15,13,0,0)

    # Our file to read/open:
    filename = 'data/omni_july2000.lst'

    data1 = load_omni(filename)
