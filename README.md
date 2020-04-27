# Genetic-Algorithm-Simulator
Allows tests on variations of the genetic algorithm with user-modifiable 
parameters

## Summary
The purpose of this project is to preform tests on parameters of the genetic 
algorithm. This includes:
* Determing the effects of different rates of mutation on the time it takes to 
find an optimal solution
* Examing the influence of noise (random error) in the fitness function on the 
genetic algorithm's ability to find a solution
* Evaluating the performance of different fitness functions

## Table of Contents

## Usage
This project requires Python3 or Python2.7. General use of the project involves
modifying `Bitstring.py` or `genetic_algorithm.py`.The scripts 
`make_experiment.py` and `generate_tests.py` set up the experiment and copy 
'Bitstring.py' and `genetic_alogirthm.py`, so that the original scripts can be 
reused for further experiments.

### Overview
To run a genetic algorithm experiment:
1. From a terminal, run `make_experiment.py` with Python. Optionally, specify 
any desired arguments (see [`make_experiment.py`]() for details on commandline 
arguments to `make_experiement.py`)
2. Enter a name for the experiment
3. Enter the number of tests to run. Note that this step will be skipped if 
either the -s or -n option were specified when invoking `make_experiment.py`
4. Specify a value a base name for the configuration files for each test. The 
name of the configuration file for a given test 
will be the base name with the test number appended. 
5. Specify a value for each configuration parameter. See 
[Configuration Parameters]() for more information about each parameter. This 
skipped will be stepped if the -d flag is specified
6. Move into the newly-created experiment directory
7. Make the experimental modifications to `Bitstream.py` or 
`genetic_algorithm.py`
8. Run `run.py` with Python. The output should of each test will appear in a 
file with the same name name as the associated configuration file, but with a 
different extension.

To add more tests to the experiment:
1. With the experiment directory, from a terminal, run `generate_tests.py` with
Python. Optionally, specify any desired arguments (see [`generate_tests.py`]() 
for details on commandline arguments to `generate_tests .py`)
2. Specify a value a base name for the configuration files for each test. The 
name of the configuration file for a given test will be the base name with the 
test number appended. 
3. Specify a value for each configuration parameter. See 
[Configuration Parameters]() for more information about each parameter. This 
skipped will be stepped if the -d flag is specified

### The difference between `make_experiment.py` and `generate_tests.py`
`make_experiment.py` is used to generate the entire collection of files and 
structures for each experiment. Part of this involves invoking 
`generate_tests.py`. `generate_tests.py` is rarely used on it's own; generally,
only when additional tests needed to added that were not anticipated when the 
experiment was created.

### `make_experiment.py`

Option Name|Long Flag|Short Flag|Argument|Description
-----------|---------|----------|--------|------------
Make statistical plot|--make-statistical-plot|-s|None|What do I do
do this work|help|me|