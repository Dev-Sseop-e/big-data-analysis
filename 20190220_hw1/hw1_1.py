import re
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)
sc.setLogLevel("WARN")

# split by the tab
lines = sc.textFile(sys.argv[1]) \
  .map(lambda l: l.split('\t')) \
  .filter(lambda l: l[1] != '')

# split by the ','
friends = lines.map(lambda l: (l[0], l[1].split(',')))

# pairs of actual friends
def pairs1(l):
  result1 = []
  for i in range(len(l[1])):
    # for increasing the executing speed, exclude the mutation
    if(l[0] < l[1][i]):
      result1.append(((l[0], l[1][i]), 0))
  return result1

# pairs of mutual friends
def pairs2(l):
  result2 = []
  for i in range(len(l[1])):
    for j in range(i+1, len(l[1])):
      if(l[1][i] < l[1][j]):
        result2.append(((l[1][i], l[1][j]), 1))
      else:
        # check the order and set to ascending order
        result2.append(((l[1][j], l[1][i]), 1))
  return result2  # It may has some actual friends

# counts the real mutual friend sets
def counts(n1, n2):
  if n1*n2 != 0:
    return n1+n2;
  else:
    return n1*n2  # the actual friends

actual_sets = friends.flatMap(pairs1)
mutual_sets = friends.flatMap(pairs2)

total_sets = actual_sets.union(mutual_sets)
# can reduce the actual friends in mutual_sets
final_sets = total_sets.reduceByKey(counts) \
  .filter(lambda l: l[1] != 0)

# set to descending order
result = final_sets.takeOrdered(10, key = lambda l: (-l[1], l[0][0], l[0][1]))

for i in range(0, 10):
  print(str(result[i][0][0]) + "\t" + str(result[i][0][1]) + "\t" + str(result[i][1]))

sc.stop()