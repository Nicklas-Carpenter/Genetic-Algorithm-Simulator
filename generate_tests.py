import configparser
import argparse
import os
import sys

def generate_configuration_file(test_number):
    try:
        config_file = open("{0}{1}.ini".format(name, test_number), mode = "w")
        config.write(config_file)
        if args.generate_temporary_files:
            try:
                created_files.write("test{0}.ini\n".format(test_number))
            except:
                created_files.close()
                print("Error writing to file list", file = sys.stderr)
                exit()
    except:
        print("Error creating file for test ", test_number, file = sys.stderr)
        config_file.close()
        exit()
    config_file.close()


#### Main ####
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
    config_file = open("default.ini")
    config = configparser.ConfigParser()
    config.read_file(config_file)
except (FileNotFoundError, FileExistsError) as e:
    print("Error reading config file", file = sys.stderr)
finally:
    config_file.close()

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

if args.generate_temporary_files:
    try:
        created_files = open("created_files.tmp", mode="w")
    except:
        print("Error when attempting to create file list", file = sys.stderr)
        exit()

name = input("Base config file name: ")
if len(name) == 0:
    name = "test"

if args.use_defaults:
    for test in range(number_of_tests):
        config.set("PARAMETERS", "OUTPUT_FILE", "test{0}".format(test))
        generate_configuration_file(test)
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
        generate_configuration_file(test)
else:
    for test in range(number_of_tests):
        for pair in config.items():
            section = pair[0]
            print("Creating test{0} configuration file".format(test))
            for kv in config.items(section):
                new_value = input(kv[0], "(default: ", kv[1], "): ")
                config.set(section, new_value)
        config.set("PARAMETERS", "OUTPUT_FILE", "{0}{1}".format(name, test))
        generate_configuration_file(test)

if args.generate_temporary_files:
    created_files.close()