#! /usr/bin/python3
# coding: utf-8

# https://www.geeksforgeeks.org/graph-plotting-in-python-set-1/

# importing the required module
import matplotlib.pyplot as plt

# x axis values
x = [1,2,3,4,5,6,7,8,9,10]
# corresponding y axis values
y = [2,5,7,9,12,15,16,17,18,19]

# plotting the points
#plt.plot(x, y)

# naming the x axis
plt.xlabel('Beam Size')
# naming the y axis
plt.ylabel('BLEU Score')

# giving a title to my graph
plt.title('Graph Title')

# plotting points as a scatter plot
plt.scatter(x, y, color= "blue",
            marker= ".", s=50)

# function to show the plot
plt.show()
