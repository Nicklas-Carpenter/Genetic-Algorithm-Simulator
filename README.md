# Genetic-Algorithm-Simulator
Allows tests on variations of the genetic algorithm with user-modifiable 
parameters. 

## Summary
The purpose of this project is to perform tests on parameters of the genetic 
algorithm. This includes:
* Determing the effects of different rates of mutation on the time it takes to 
find an optimal solution
* Examing the influence of noise (random error) in the fitness function on the 
genetic algorithm's ability to find a solution
* Evaluating the performance of different fitness functions

## Table of Contents
* [Genetic-Algorithm-Simulator](#genetic-algorithm-simulator)
* [Summary](#summary)
* [Table of Contents](#table-of-contents)
* [Usage](#usage)
   * [Overview](#overview)
   * [The Difference Between `make_experiment.py` and `generate_tests.py`](
       #the-difference-between-make_experimentpy-and-generate_testspy)
   * [Options for `make_experiment.py` and `generate_tests.py`](
       #options-for-make_experimentpy-and-generate_testspy)
      * [Make Statistical Plot](#make-statistical-plot)
      * [Specify Number of Tests](#specify-number-of-tests)
      * [Use Default Parameters](#use-default-parameters)
   * [Options Specific to `generate_tests.py`](
       #options-specific-to-generate_testspy)
      * [Enable Interactive Mode](#enable-interactive-mode)
      * [Generate Temporary Files](#generate-temporary-files)
   * [Configuration File](#configuration-file)
      * [OPTIONS](#options)
      * [PARAMETERS](#parameters)
      * [Probability Distribution Parameters](
         #probability-distribution-parameters)
         * [UNIFORM](#uniform)
         * [EXPONENTIAL](#exponential)
         * [GAUSS](#gauss)
* [Contributing](#contributing)
* [License](#license)

## Usage
This project requires Python 3 or Python 2.7. General use of the project 
involves modifying [`Bitstring.py`](Bitstring.py) or
[`genetic_algorithm.py`](genetic_algorithm.py). The 
scripts [`make_experiment.py`](make_experiment.py) and [`generate_tests.py`](
generate_tests.py) set up the experiment and copy [`Bitstring.py`](
Bitstring.py) and [`genetic_algorithm.py`](genetic_algorithm.py), so that the 
original scripts can be reused for further experiments. This section covers 
basic configuration and usage of the project. For more details, consult the 
[wiki](https://github.com/Nicklas-Carpenter/Genetic-Algorithm-Simulator/wiki)

### Overview
To run a genetic algorithm experiment:
1. From a terminal, run [`make_experiment.py`](make_experiment.py) with Python. 
Optionally, specify any desired arguments (see 
[Options for `make_experiment.py` and `generate_tests.py`]( #options-for-make_experimentpy-and-generate_testspy) for details on the
commandline arguments to [`make_experiment.py`](make_experiment.py)
2. Enter a name for the experiment
3. Enter the number of tests to run. Note that this step will be skipped if 
either the -s or -n option were specified when invoking [`make_experiment.py`](
make_experiment.py)
4. Specify a value a base name for the configuration files for each test. The 
name of the configuration file for a given test 
will be the base name with the test number appended
5. Specify a value for each configuration parameter. See 
[Configuration File](#configuration-file) for more information about each 
parameter. This step will be skipped if the -d flag is specified
6. Move into the newly-created experiment directory
7. Make the experimental modifications to [`Bitstring.py`](Bitstring.py) or 
[`genetic_algorithm.py`](genetic_algorithm.py)
8. Run `run.py` with Python. The output should of each test will appear in a 
file with the same name name as the associated configuration file, but with a 
different extension

To add more tests to the experiment:
1. With the experiment directory, from a terminal, run [`generate_tests.py`](
generate_tests.py) with Python. Optionally, specify any desired arguments (see 
[Options for `make_experiment.py` and `generate_tests.py`]( #options-for-make_experimentpy-and-generate_testspy) and 
[Options Specific to `generate_tests.py`](
#options-specific-to-generate_testspy) for details on commandline arguments to 
[`generate_tests.py`](generate_tests.py))
2. Specify a value a base name for the configuration files for each test. The 
name of the configuration file for a given test will be the base name with the 
test number appended
3. Specify a value for each configuration parameter. See 
[Configuration File](#configuration-file) for more information about each 
parameter. This step will be stepped if the -d flag is specified

### The Difference Between `make_experiment.py` and `generate_tests.py`
[`make_experiment.py`](make_experiment.py) is used to generate the entire 
collection of files and structures for each experiment. Part of this involves 
invoking [`generate_tests.py`](generate_tests.py). [`generate_tests.py`](
generate_tests.py) is rarely used on it's own; generally only when additional 
tests needed to added that were not anticipated when the experiment was 
created.

### Options for `make_experiment.py` and `generate_tests.py`

#### Make Statistical Plot

|Option Name|Long Flag|Short Flag|Argument|
|-----------|---------|----------|--------|
|Make Statistical Plot|--make-statistical-plot|-s|n|

Generates n tests that use identical parameters, but start with different 
initial populations (the seed for the random number generator used in the 
genetic algorithm). The user is prompted to the parameters that all the test 
will use unless the [--use-defaults](#use-default-parameters) option is 
specified. Used to identify general trends or patterns in an experiment. 
Mutually exlusive with [--number-of-tests](#specify-number-of-tests). 

#### Specify Number of Tests
 
|Option Name|Long Flag|Short Flag|Argument|
|-----------|---------|----------|--------|
|Specify Number of Tests|--numbers-of-tests|-n|n|

Generates n tests. The user is prompted to the parameters for each test unless 
the [--use-defaults](#use-default-parameters) option is specified. Mutually 
exlusive with [--make-statistical-plot](#make-statistical-plot).

#### Use Default Parameters

|Option Name|Long Flag|Short Flag|Argument|
|-----------|---------|----------|--------|
|Use Default Parameters|--use-defaults|-d|None|

Use default configuration parameters for each generated test.

### Options Specific to `generate_tests.py`

#### Enable Interactive Mode

|Option Name|Long Flag|Short Flag|Argument|
|-----------|---------|----------|--------|
|Enable Interactive Mode|--interactive|-i|None|

Most commonly, [`generate_tests.py`](generate_tests.py) is run on behalf of 
[`make_experiment.py`](make_experiment.py). Enable interactive mode to run the 
script independently. 

#### Generate Temporary Files

|Option Name|Long Flag|Short Flag|Argument|
|-----------|---------|----------|--------|
|Generate Temporary Files|--generate-temporary-files|-t|None|

Creates a file that contains a list of the configuration file for each test

### Configuration File
The following options and parameters modify the behavior of the genetic 
algorithm.

#### OPTIONS

|Option|Values|Default|Description                                                              |
|------|------|-------|-------------------------------------------------------------------------|
|CROSSOVER|True\|False|True|Whether to use the crossover operator during repopulation           |
|MUTATE   |True\|False|True|Whether to use the mutate operator during repopulation              |
|PROBABALISTIC_FITNESS_FUNCTION|True\|False|True|Whether to use a probablistic fitness function|
|USE_AVERAGE_FITNESS|True\|False|False|To be implemented in the future                          |

#### PARAMETERS

|Option|Values|Default|Description                                                                 |
|------|------|-------|----------------------------------------------------------------------------|
|[*](#Note)FITNESS_FUNCTION|GENE_COMPARATIVE|GENE_COMPARATIVE|Which type of fitness function to use|
|PROBABILITY_DISTRIBUTION|UNIFORM<br>EXPONENTIAL<br>GAUSS|UNIFORM|The probability distribution to use for probabilistic fitness functions. Ignored if [probabalistic fitness function](#OPTIONS) is disabled                                                                                           |
|[*](#Note)REPOPULATION_METHOD|DEFAULT|DEFAULT|Method used to generate new individuals             |
|[*](#Note)SELECTION_METHOD|SIMPLE_ELITISM|SIMPLE_ELITISM|Method used to select parents            |
|MAX_GENERATIONS|Integers|25|The maximum number of iterations run the genetic algorithm            |
|BITSTRING_SIZE|Integers|50|The number of bits in each bitstring to                                |
|REPOPULATION_RATIO|0.0 - 1.0|0.5|The percentage of individuals to replace each generation         |
|OUTPUT_FILE|Filename|run.csv|The file where data from the genetic algorithm is output             |
|SEED|Integer|0xA5A5|The seed for the random number generator. Used for all random operations      |
|POPULATION_SIZE|Integer|100|The number of individuals at any given generation                     |

###### Note
\* \- Parameter is undergoing implementation

#### Probability Distribution Parameters 
A set of parameters that are used to modify a specific probability function.
These values are only used when PROBABALISTIC_FITNESS_FUNCTION is set to true 
and the probability function selected matches the heading of a given set of 
parameters.

##### UNIFORM

|Option|Values   |Default|Description|
|------|---------|-------|-----------|
|A     |0.0 - 1.0|0.75   |           |
|B     |0.0 - 1.0|1.0    |           |

##### EXPONENTIAL

|Option|Values   |Default|Description|
|------|---------|-------|-----------|
|LAMBDA|0.0 - 1.0|0.5    |           |

##### GAUSS

|Option|Values   |Default|Description|
|------|---------|-------|-----------|
|MU    |0.0 - 1.0|0.9    |           |
|SIGMA |0.0 - 1.0|0.05   |           |

## Contributing

This project is still very much a work in progess. The most helpful way to 
contribute currently is would be to bring up anything in the documentation that
was unclear. Similary, if you run the code and find issues, let me know. I 
would be happy to review any pull requests, but in terms of code my priority is
currently on a few specific goals. See the [project board](
https://github.com/Nicklas-Carpenter/Genetic-Algorithm-Simulator/projects/1)
for more details on these goals.

## License

This project is licensed under the GNU GPL v3.0 or greater. For more 
information please refer to [LICENSE](LICENSE)