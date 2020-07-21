# GEM2020_tutorial
Files and code supplementing my Geospace Environment Modeling student tutorial on coding.
The tutorial covers the development of code for a hypothetical project from conception to
pushing to a repository.

## Hypothetical Project
Suppose we are interested in studying potential relationships between conditions before a geomagnetic storm and the storm itself.
Can the conditions preceeding an event change the storm dynamics later?
We’re going to start very simply: given start time of a storm, what are the average solar wind conditions during the preceding 24 hours?
We’ll use hourly data from the [OMNIWeb database](https://omniweb.gsfc.nasa.gov/form/dx1.html) as inputs.
The IMF magnitude, clock angle, and solar wind dynamic pressure will be investigated, specifically.

## Program Files 
The Python source code files are illustrations of programming progress towards achieving the project goals above.

- **precond1.py** is a simple prototype.  It is hard coded, does not use functions, and uses a brute-force approach.
- **precond2.py** is our second attempt.  It uses functions to make the software more reusable.  It also takes advantage of specialized Python data types, including `datetimes`, and is more elegant in its implementation than its predecessor.  
- **test_precond.py** contains the test suite for `precond2.py`.  It uses Python's built in `unittest` module.

## The Bugged Branch
While the master branch passes all tests, the "bugged" branch does not.  It "features" several mistakes in implementation that can commonly arise in every day life.  Use `git checkout bugged` to switch to this branch and explore how the code fails.  Use `git diff master bugged` to see what is different between the two branches.

## Using This Code
I recommend running this software through the IPython interface.

**precond1.py** is a simple linear script.  Within IPython, use `run precond1.py` to execute it.  Values are printed to screen.

**precond2.py** can be executed as a script (`run precond2.py`) or imported as a module, which will provide access to the individual functions.  For example,
```
import precond2
data = precond2.load('data/omni_test.lst')
```
Running **precond2.py** in script mode runs a basic functionality test that is expanded upon in **test_precond.py**.

**test_precond.py** can by run directly from the Unix-like command line interface via Python (e.g., `python3 test_precond.py`).  For more information on unittest, see the excellent [Python documentation](https://docs.python.org/3/library/unittest.html) or any of the [thorough online tutorials](https://realpython.com/python-testing/).
