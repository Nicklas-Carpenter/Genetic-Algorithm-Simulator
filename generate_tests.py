# generate_tests.py - Generates test-related files for the genetic algorithm
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

# TODO Maybe use os.tempfile() for the tempfile
# TODO Change interative mode to script mode. Scripts should be user runnable
#      by default
# TODO Improve error handling
# Improve variable names

def generate_configuration_file(test_number, name, tmp_file = None):
    try:
        config_file = open("{0}{1}.ini".format(name, test_number), mode = "w")
        config.write(config_file)
        if args.generate_temporary_files:
            try:
                tmp_file.write("{0}{1}.ini\n".format(name, test_number))
            except:
                tmp_file.close()
                print("Error writing to file list", file = sys.stderr)
                exit()
    except:
        print("Error creating file for test ", test_number, file = sys.stderr)
        config_file.close()
        exit()
    config_file.close()


#### Main ####
number_of_tests = 0

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
parser.add_argument("-i", "--interactive", action = "store_true")
parser.add_argument("-t", "--generate-temporary-files", action = "store_true")

args = parser.parse_args()

try:
    config_file = open("../../templates/default.ini")
    config = configparser.ConfigParser()
    config.read_file(config_file)
except OSError:
    print("Error reading config file", file = sys.stderr)
    exit(-1)

if args.number_of_tests > 0:
    number_of_tests = args.number_of_tests
elif args.make_statistical_plot > 0:
    number_of_tests = args.make_statistical_plot
else:
    if args.interactive:
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
    else:
        number_of_tests = 1

name = input("Base config file name: ")
if len(name) == 0:
    name = "test" # TODO Change this to error handling after testing

created_files = 0
if args.generate_temporary_files:
    created_files = open("created_files.tmp", "w", newline="")

if args.use_defaults:
    for test in range(number_of_tests):
        config.set("PARAMETERS", "OUTPUT_FILE", "test{0}".format(test))
        if args.generate_temporary_files:
            generate_configuration_file(test, name, tmp_file = created_files)
        else:
            generate_configuration_file(test, name)
elif args.make_statistical_plot:
    # print("Creating test configuration file")
    for pair in config.items():
        section = pair[0]
        for kv in config.items(section):
            new_value = input("{0} (default: {1}): ".format(kv[0], kv[1]))
            if len(new_value) > 0:
                config.set(section, kv[1], str(new_value))
    for test in range(number_of_tests):
        config.set("PARAMETERS", "SEED", str(test))
        config.set("PARAMETERS", "OUTPUT_FILE", "{0}{1}".format(name, test))
        if args.generate_temporary_files:
            generate_configuration_file(test, name, tmp_file = created_files)
        else:
            generate_configuration_file(test, name)
else:
    for test in range(number_of_tests):
        for pair in config.items():
            section = pair[0]
            print("Creating test{0} configuration file".format(test))
            for kv in config.items(section):
                new_value = input(kv[0], "(default: ", kv[1], "): ")
                config.set(section, new_value)
        config.set("PARAMETERS", "OUTPUT_FILE", "{0}{1}".format(name, test))
        if args.generate_temporary_files:
            generate_configuration_file(test, name, tmp_file = created_files)
        else:
            generate_configuration_file(test, name)

if args.generate_temporary_files:
    created_files.close()