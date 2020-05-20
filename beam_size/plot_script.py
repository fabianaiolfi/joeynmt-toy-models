#! /usr/bin/python3
# coding: utf-8

# https://www.geeksforgeeks.org/graph-plotting-in-python-set-1/

# importing the required module
import matplotlib.pyplot as plt

# x axis values / Beam Size
x = [1,2,3,4,5,8,16,32,64,128]

# corresponding y1 axis values / BLEU Score
y1 = [1.2,0.8,0.7,0.5,0.4,0.4,0.3,0.2,0.2,0.2]

# corresponding y2 axis values / Translation Time (s)
y2 = [14,15,16,18,20,24,38,70,144,308]

# https://stackoverflow.com/a/14762601
fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.plot(x, y1, 'b-', marker='o', markersize=3, linewidth=1)
ax2.plot(x, y2, 'r-', marker='o', markersize=3, linewidth=1)

plt.title('Impact of Beam Size on Translation Quality and Time')
ax1.set_xlabel('Beam Size')
ax1.set_ylabel('BLEU Score', color='b')
ax2.set_ylabel('Translation Time (s)', color='r')

plt.show()
