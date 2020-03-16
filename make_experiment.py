import configparser
import argparse
import os
import sys
import subprocess


#### Parse arguments ####
parser = argparse.ArgumentParser()
specifies_number_of_tests = parser.add_mutually_exclusive_group()

specifies_number_of_tests.add_argument(
                                        "-s", 
                                        "--make-statistical-plot",
                                        action = "store",
                                        type = int,
                                        default = -1)
specifies_number_of_tests.add_argument(
                                        "-n", 
                                        "--number-of-tests", 
                                        action = "store", 
                                        type = int,
                                        default = -1)
parser.add_argument("-d", "--use-defaults", action = "store_true")

args = parser.parse_args()

#### Create the experiement ####

### Name the experiment ###
input_not_valid = True
while input_not_valid:
    experiment_name = input("Experiment name: ")
    try:
        os.mkdir(experiment_name)
        input_not_valid = False
    except FileExistsError:
        print(
              "Experiment ", experiment_name, " already exists", 
              file = sys.stderr)
    except FileNotFoundError:
        print("Invalid filename", file = sys.stderr)

### Determine number of tests to run###
# Obtain this number from the appropriate arguments if present.
# Otherwise, ask the user
if args.number_of_tests > 0:
    number_of_tests = args.number_of_tests
elif args.make_statistical_plot > 0:
    number_of_tests = args.make_statistical_plot
else:
    input_not_valid = True
    number_of_tests = input("Number of tests (default: 1): ")
    if number_of_tests == "":
        number_of_tests = 1
        input_not_valid = False
    else:
        try:
            number_of_tests = int(number_of_tests)
            input_not_valid = False
        except ValueError:
            print(
                  "Invalid number of tests: ", number_of_tests, 
                  file = sys.stderr)

### Generate the test configuration files ###

## Build the argument string
arguments = "-t"
if args.use_defaults:
    arguments += "-d "
if args.make_statistical_plot > 0:
    arguments += "-s {0}".format(args.make_statistical_plot)
elif args.number_of_tests > 0:
    arguments += "-n {0}".format(args.number_of_tests)


## Run the generate_tests.py script
try:
    subprocess.run("python generate_tests.py " + arguments)
except subprocess.CalledProcessError:
    print("Error attempting to generate tests", file = sys.stderr)
    exit()

### Build a runscript
try:
    runscript = open("run.py", mode = "w")
except:
    print("Error attempting to generate runscript", file = sys.stderr)

runscript.write("import subprocess\nimport sys")

try:
    tests = open("created_files.tmp", mode = "r")
except:
    print("Error opening list of files", file = sys.stderr)

test_file = tests.readline()

cmd = """\
try:
    subprocess.run('python genetic_algorithm.py {0}', check = True)
execpt: subprocess.CalledProcessError:
    print("Error running genetic_algorithm.py", file=sys.stderr)"""

while len(test_file) > 0:
    runscript.write("# Running {0}".format(test_file))
    runscript.write(cmd.format(test_file))


os.rmdir(experiment_name)