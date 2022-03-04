import re
import sys
import numpy as np

f = open(sys.argv[1], 'r')
total_list = []

while True:
  lines = f.readline()
  if not lines: break
  total_list.append(lines.split(' ')[:-1])

item_list = []  # don't have mutation
for i in range(len(total_list)):
  for j in range(len(total_list[i])):
    if not total_list[i][j] in item_list:
      item_list.append(total_list[i][j])

# frequency of items, which listed by the same index with item_list
item_frequency = [0]*len(item_list)
for list in total_list:
  for item in list:
    item_frequency[item_list.index(item)] += 1

# select the frequent items
freq_item = []
for i in range(len(item_frequency)):
  if item_frequency[i] >= 200:  # threshold: 200
    freq_item.append(item_list[i])

print(len(freq_item))

# make frequent item pairs
pairs = np.zeros((len(freq_item), len(freq_item)))
for list in total_list:
  for i in range(len(list)):
    for j in range(i+1, len(list)):
      if (list[i] in freq_item) and (list[j] in freq_item):
        if freq_item.index(list[i]) < freq_item.index(list[j]):
          pairs[freq_item.index(list[i])][freq_item.index(list[j])] += 1
        else: # this operation can consider the different order of pairs
          pairs[freq_item.index(list[j])][freq_item.index(list[i])] += 1

num_pairs = 0
freq_list = []

for i in range(len(freq_item)):
  for j in range(i+1, len(freq_item)):
    if pairs[i][j] >= 200:  # threshold: 200
      num_pairs += 1
    freq_list.append(pairs[i][j])

print(num_pairs)

# it refers the descending order of pairs' frequency
freq_list = sorted(freq_list, reverse=True)

for i in range(10):
  for j in range(len(freq_item)):
    for k in range(j+1, len(freq_item)):
      if pairs[j][k] == freq_list[i]: # finding index
        print (str(freq_item[j]) + '\t' + str(freq_item[k]) + '\t' + str(int(freq_list[i])))

f.close()