import sys

f = open(sys.argv[1], 'r')
lines = f.readlines()

D = "Department"
T = "Type"
E = "Explanation"

data = {}

for line in lines:
  line = line.split('/')
  data[str(line[2])] = {}
  data[str(line[2])][D] = str(line[0])
  data[str(line[2])][T] = str(line[1])
  data[str(line[2])][E] = str(line[3])

f.close()

realistic = 0
investigate = 0
artistic = 0
social = 0
enterprising = 0
conventional = 0


