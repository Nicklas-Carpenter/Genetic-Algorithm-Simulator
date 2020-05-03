# make_experiment.py - Sets up experiements for the genetic algorithm
# Copyright (C) 2020  Nicklas Carpenter

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import configparser
import argparse
import os
import sys
import subprocess
import shutil

# TODO Maybe use os.tempfile() for the tempfile
# TODO Refactor starting with variable names
# TODO Improve clean-up on failure
# TODO Improve error handling

run_script_imports = ["subprocess", "sys"]

run_cmd = """\

try:
    subprocess.run(["python3", "genetic_algorithm.py", "{0}"], check = True)
except subprocess.CalledProcessError:
    print("Error running genetic_algorithm.py", file = sys.stderr)
"""

plot_cmd = """\
try:
    subprocess.run(["python3", "plot.py"], check=True)
except subprocess.CalledProcessError:
    print("Error running plot.py", file = sys.stderr)
"""

plot_script_imports = [
    "matplotlib.pyplot as plt",
    "csv",
    "os"
]

plot_script_body = """

generations = []
best = []
average = []
mins = []

# Obtain the data from file
csvfile = open(data, "r", newline="")
reader = csv.DictReader(csvfile)
for row in reader:
    generations.append( row["generation"] )
    best.append( int(row["max"] ) )
    average.append( int(row["average"] ))
    mins.append( int(row["min"] ))
        
# Plot each set of data points: best, average, and min
plt.plot(generations, best, label = "best")
plt.plot(generations, average, label = "average")
plt.plot(generations, mins, label = "min")

# Add a legend
plt.legend()

# Add axis lables
plt.xlabel("generations")
plt.ylabel("fitness")

"""

# TODO Remove this after testing
experiment_name = ""

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

### Name the experiment ###
input_not_valid = True
while input_not_valid:
    experiment_name = input("Experiment name: ")
    try:
        os.mkdir("experiments/" + experiment_name)
        os.chdir("experiments/" + experiment_name)
        input_not_valid = False
    except FileExistsError:
        print(
              "Experiment ", experiment_name, " already exists", 
              file = sys.stderr)
    except FileNotFoundError:
        print("Invalid filename", file = sys.stderr)

### Determine number of tests to run ###
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
                file = sys.stderr
            )

### Generate the test configuration files ###

## Build the argument string ##
arg_vector = ["-t"]
if args.use_defaults:
    arg_vector.append("-d")
if args.make_statistical_plot > 0:
    arg_vector.append("-s {0}".format(args.make_statistical_plot))
elif number_of_tests > 1:
    arg_vector.append("-n {0}".format(number_of_tests))


## Run the generate_tests.py script ##
try:
    subprocess.run(["python3", "../../generate_tests.py"] + arg_vector)
except (subprocess.CalledProcessError, OSError): 
    print("Error attempting to generate tests", file = sys.stderr)
    os.rmdir(test_name)
    exit()

### Build a run_script ###
try:
    run_script = open("run.py", mode = "w")
except:
    print("Error attempting to generate run_script", file = sys.stderr)
    exit()

for imprt in run_script_imports:
    run_script.write("import {0}\n".format(imprt))

try:
    tests = open("created_files.tmp", mode = "r")
except:
    print("Error opening list of files", file = sys.stderr)
    exit()

test = tests.readline()
while len(test) > 0:
    data_file_name = test.split(".")[0].strip("\n")
    run_script.write("\n# Running {0}".format(data_file_name))
    run_script.write(run_cmd.format(test.strip("\n")))
    test = tests.readline()

run_script.write("\n#Plotting graphs\n" + plot_cmd)
run_script.close()

### Generate plot script ###
plot_script = open("plot.py", "w", newline="")

for imprt in plot_script_imports:
    plot_script.write("import " + imprt + "\n")

tests.seek(0)
test = tests.readline()
fig_num = 1
while len(test) > 0:
    data_file_name = test.split(".")[0].strip("\n")
    plot_script.write("\n# Plotting {0}\n".format(data_file_name))
    plot_script.write("plt.figure({0})\n\n".format(fig_num))
    fig_num += 1
    plot_script.write("# Obtain the data from file\n")
    plot_script.write("data = \"{0}.csv\"".format(data_file_name))
    plot_script.write(plot_script_body)
    plot_script.write("# Save the figure to a file\n")
    plot_script.write("plt.savefig(\"{0}.png\")\n".format(data_file_name))
    test = tests.readline()

plot_script.write("# Display the plot\nplt.show()")
plot_script.close()

tests.close()

# Give the experiment a copy of genetic_algorithm, Bitstring, and probability
shutil.copy("../../templates/genetic_algorithm.py", "./")
shutil.copy("../../templates/Bitstring.py", "./")
shutil.copy("../../templates/probability.py", "./")

# Delete the temp file
os.remove("created_files.tmp")
