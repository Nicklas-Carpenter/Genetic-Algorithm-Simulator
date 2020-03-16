import subprocess, sys

#TODO Improve error handling

try:
    subprocess.run("python ../genetic_algorithm.py config.ini", check=True)
except subprocess.CalledProcessError:
    print("Error running genetic_algorithm.py", file=sys.stderr)

try:
    subprocess.run("python plot.py", check=True)
except subprocess.CalledProcessError:
    print("Error running plot.py", file=sys.stderr);