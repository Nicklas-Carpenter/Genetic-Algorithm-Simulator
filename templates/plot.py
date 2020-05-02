import matplotlib.pyplot as plt
import csv
import os

data="run.csv"
generations=[]
best=[]
average=[]
mins=[]

# Obtain data from file
csvfile = open(data, "r", newline='')
reader = csv.DictReader(csvfile)
for row in reader:
    generations.append( row["generation"] )
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
