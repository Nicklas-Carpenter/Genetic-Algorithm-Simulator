import matplotlib.pyplot as plt
import csv
import os

# Longer tutorial here
# https://docs.python.org/3/library/csv.html

data="run.csv"
generations=[]
best=[]
average=[]
mins=[]

with open(data, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        generations.append( row["generation"] )
        #adding the int() to force python to treat as numbers
        #otherwise it treats as strings and y axis will be out of order
        best.append( int(row["max"] ) )
        average.append( int(row["average"] ))
        mins.append( int(row["min"] ))
        
#plot the three different measures recorded
plt.plot(generations,best,label="best")
plt.plot(generations,average,label="average")
plt.plot(generations,mins,label="min")

#show a legend
plt.legend()

#add labels to the axes
plt.xlabel('generations')
plt.ylabel('fitness')

#saves to file
plt.savefig('demo_plot.png')

#shows on the screen
plt.show()
