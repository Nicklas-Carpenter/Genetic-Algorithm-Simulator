import matplotlib.pyplot as plt
import csv
import os
from configparser import ConfigParser
import numpy as np
import numpy.fft as fft

# # Plotting run0
# plt.figure(1)

# Obtain the data from file
data = "run0.csv"

# generations = []
best = []
# average = []
# mins = []
bitstrings = []

# Obtain the data from file
csvfile = open(data, "r", newline="")
reader = csv.DictReader(csvfile)
for row in reader:
    # generations.append( row["generation"] )
    best.append(row["max"])
    # average.append(row["average"])
    # mins.append(row["min"])
    bitstrings.append(row["best"])
        
# # Plot each set of data points: best, average, and min
# plt.plot(generations, best, label = "best")
# plt.plot(generations, average, label = "average")
# plt.plot(generations, mins, label = "min")

# # Add a legend
# plt.legend()

# # Add axis lables
# plt.xlabel("generations")
# plt.ylabel("fitness")

# # Save the figure to a file
# plt.savefig("run0.png")

record = ConfigParser()
record.read("frequencies.ini")

w_list = record.get("DEFAULT", "frequencies").split(",")

for i in range(len(w_list)):
    w_list[i] = float(w_list[i])

target_w = record.getfloat("DEFAULT", "target")

bitstring = []
for c in bitstrings[len(bitstrings) - 1]:
    if c == "0" or c == "1":
        bitstring.append(int(c))

# TODO Get rid of magic number 1000 (N)
t = np.linspace(0, (4 * np.pi) / target_w, 1000)

x = np.zeros(len(t))

print("Number of genes: ", len(bitstring))
for i, gene in enumerate(bitstring):
    print("Contains gene: " + str(i))
    x += gene * np.cos(w_list[i] * t)

target = np.cos(target_w * t)

x_freqs = fft.fft(x)
F = fft.fftfreq(len(x_freqs))

plt.plot(t, target, "b:", t, x, "r")

plt.figure(2)
plt.plot(F, x_freqs)
        
# Display the plot
plt.show()

plt.savefig("run0.png")