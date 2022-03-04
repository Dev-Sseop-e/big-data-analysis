import re
import sys
from pyspark import SparkConf, SparkContext
from pyspark.sql.functions import lower, col

def remove(x):
  if 97<=ord(x[0])<=122:
    return True
  else:
    return False

conf = SparkConf()
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])
words = lines.flatMap(lambda l: re.split(r'[^\w]+', l))
words = words.filter(lambda l: len(l) != 0)
lower_words = words.map(lambda l: l.lower())

filtered_words = lower_words.filter(remove)

distinct_words = filtered_words.map(lambda w: (w, 1))
counts = distinct_words.reduceByKey(lambda n1, n2: n1 + n2)

letter = counts.map(lambda l: (l[0][0], 1))
counts2 = letter.reduceByKey(lambda n1, n2: n1 + n2)

result = counts2.collect()
result.sort()

for i in range(26):
  j = chr(i+97)
  for k in range(len(result)):
    if j == result[k][0]:
      print(j + "\t" + str(result[k][1]))
      break
    if k == len(result) - 1:
      print(j + "\t" + "0")

sc.stop()