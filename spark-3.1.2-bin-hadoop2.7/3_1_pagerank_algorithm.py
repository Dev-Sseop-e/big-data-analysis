import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)
sc.setLogLevel('WARN')

B = 0.9   # set Beta = 0.9
N = 1000  # set N = 1000
iterNum = 50  # set interating number = 50

lines = sc.textFile(sys.argv[1])

# remove the duplicates
pairs = lines.map(lambda l: l.split('\t'))\
              .map(lambda l: ((int(l[0]), int(l[1])), 0))\
              .reduceByKey(lambda v0, v1: v0+v1)\
              .map(lambda l: l[0])

# count the degree of destination
def countDegree(M):
  degree = len(list(M[1]))
  return [(M[0], dest, 1.0/degree) for dest in list(M[1])]
  # return (src, dest, 1/degree)

# set transition matrix
M = pairs.groupByKey()\
          .flatMap(countDegree)

# set Page-Rank vector
v = []
for i in range(N):
  v.append(1.0/N)

# calculate Page-Rank scores
for i in range(iterNum):
  # compute next estimate v'
  vPrime = M.map(lambda l: (l[1], l[2]*v[l[0]-1]))\
            .reduceByKey(lambda v0, v1: v0+v1)\
            .collect()
  # set new scores
  for score in vPrime:
    v[score[0]-1] = B*score[1] + (1.0-B)/N

result = []
for i in range(len(v)):
  result.append((i+1, v[i]))  # (srcNum, score)

# sort by descending order and print
for (dest, score) in sorted(result, key = lambda l: l[1], reverse=True)[:10]:
  print("%d\t%.5f" %(dest, score))