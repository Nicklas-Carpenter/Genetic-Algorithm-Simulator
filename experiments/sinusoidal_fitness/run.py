import subprocess
import sys

# Running run0
try:
    subprocess.run(["python3", "genetic_algorithm.py", "run0.ini"], check = True)
except subprocess.CalledProcessError:
    print("Error running genetic_algorithm.py", file = sys.stderr)

#Plotting graphs
try:
    subprocess.run(["python3", "plot.py"], check=True)
except subprocess.CalledProcessError:
    print("Error running plot.py", file = sys.stderr)
