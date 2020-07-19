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

This script is written in the simplest manner possible as a demonstration.

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
10 Flow pressure                 F6.2
11 Dst-index, nT                 I6

DTW, 2020, GEM Student Tutorial
'''

###### HOW TO USE THIS FILE TO LEARN ######
# Start IPython, and `run precond1.py`.
# Then, copy and paste each line into your command prompt.
# Print variables, play with statements one-at-a time to see how
# they function and what they do.  Add your own comments to this
# file to document your understanding of each line.  Use print statements
# to figure out how things are functioning, especially over loops.
# Use Python's docstrings to learn about different functions.
# Google commands and functions if you need more information.

# Always start with imports at the top!
import numpy as np

##### PARAMETERS TO CHANGE:

# The epoch of storm start:
doy, hour  = 197, 13  # Note the multiple assignment here.
epoch = doy + hour/24 # Time format described below

# Our file to read/open:
filename = 'data/omni_july2000.lst'

##### Read/Parse data:
# We'll open and "slurp" data into a list.
# Note that we should be considering a "with" block here.
# See Python3 PEP 343 for details, google "python with" for examples.
f = open(filename, 'r') # Open the file as an object.
lines = f.readlines()   # "Slurp" in the lines as a list.
f.close()               # Close our file.
    
# Get the size of the data- how many variables, how many records?
#### ERROR 1 IS HERE: Should read "lines[0].split()"
nVar = len(lines[0].split()) # Number of variables = number of columns.
                             # "Split" splits a line into substrings by whitespace.
nRec = len(lines) # No header to the data, this is the number of records
                  # (with one record per line).

# Create a container for our incoming data.  Let's use Numpy.
data = np.zeros((nRec, nVar)) # An array of zeros big enough to hold everything.

# Loop through our data file and read every single line.
# Split it into parts by whitespace.  Numpy will convert the strings into
# numbers for us.  It's very convenient.
for i, line in enumerate(lines):
    data[i,:] = line.split()

# Now, we can calculate values from this data array!
# Let's start with time- how do we handle time?  Here, we'll keep it super
# simple.  The file gives us DOY and hour; let's turn that into decimal
# DOY.  Not great, but it'll do.
time = data[:,1] + data[:,2]/24.

# Let's get clock angle, which is the angle of the IMF projected into
# the X=constant plane as measured from the z=0 direction.  This means that
# Angle = 0       : IMF Bz north
# Angle = 90      : IMF By positive
# Angle = 180     : IMF Bz south
# Angle = 270     : IMF By negative
# Most scientific/engineering languages will have two arctangent functions
# with "arctan2" better handling the angle quadrant.
clock = (180.0/np.pi)*np.arctan2(data[:,5], data[6])

# Finally, we extract values between epoch minus 24 hours through epoch.
# Here, we do this is a very clunky way and will improve upon it in
# future iterations.  Let's loop through the times and find the indexes
# where time is within epoch and epoch minus 1 day.
iStart, iStop = -1, -1  # Initial values of our indices.
for i, tnow in enumerate(time):  # Python loops are cool.
    # If the current time surpasses epoch-1 for the first time, get index.
    if tnow > epoch-1.0 and iStart==-1: iStart=i
    # If we pass epoch, save index and break.
    if tnow >= epoch:
        iStop = i
        break

# DEBUG INFORMATION:  Let's print to screen what we found in
# our time analysis above.  See notes on "format" syntax below.
# Note that we unzip our time back into DOY and Hour.  
print('Epoch is DOY {} Hour {:.1f}'.format(
    int(epoch), 24*(epoch-int(epoch))))
print('Start time: i={}, DOY {} Hour {:.1f}'.format(
    iStart, int(time[iStart]), 24*(time[iStart]-int(time[iStart]))))
print('End time: i={}, DOY {} Hour {:.1f}'.format(
    iStop, int(time[iStop]), 24*(time[iStop]-int(time[iStop]))))
    
# Report values to screen and quit.
# `.mean` does the averaging.  The indexing handles controlling the range.
# String formatting is an important skill, see here for more details:
# https://docs.python.org/3/library/string.html#format-string-syntax
print('Average values leading up to storm:')
print('\t|B|:\t{:.2f}'.format(data[iStart:iStop,3].mean()))
print('\tIMF Bz:\t{:.2f}'.format(data[iStart:iStop,6].mean()))
print('\tPdyn  :\t{:.2f}'.format(data[iStart:iStop,9].mean()))
print('\tClock :\t{:.2f}'.format(clock[iStart:iStop].mean()))

# ...and we're done.
