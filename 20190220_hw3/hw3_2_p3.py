import sys
import math

f = open(sys.argv[1], 'r')
lines = f.readlines()

D = {}  # user list with degree
F = {}  # user list with their friends
E = {}  # edges
n = 0   # number of nodes
m = 0   # number of edges
hT = 0  # heavy-hitter triangles
oT = 0  # other triangles

# compare which node is larger
def cmp(X, Y):
  if D[X] < D[Y]:
    return True
  elif (D[X] == D[Y] and X < Y):
    return True
  return False

# check if edge is in E
def inE(X, Y):
  if (X, Y) not in E:
    if (Y, X) not in E:
      return False
  return True

# set the datasets
for line in lines:
  line = line.split('\t')
  
  if int(line[0]) == int(line[1]):
    continue
  if inE(int(line[0]), int(line[1])):
    continue
  
  # set the user list by degree
  if int(line[0]) not in D:
    D[int(line[0])] = 1
    n = n+1
  else:
    D[int(line[0])] = D[int(line[0])] + 1
  if int(line[1]) not in D:
    D[int(line[1])] = 1
    n = n+1
  else:
    D[int(line[1])] = D[int(line[1])] + 1

  # set the user list by their friends
  if int(line[0]) not in F:
    F[int(line[0])] = []
  F[int(line[0])].append(int(line[1]))
  if int(line[1]) not in F:
    F[int(line[1])] = []
  F[int(line[1])].append(int(line[0]))

  # set the edges
  E[(int(line[0]), int(line[1]))] = 1
  m = m+1

# sort the D by degree
sortD = []
for user in D.keys():
  sortD.append((user, D[user]))
sortD.sort(key = lambda l: (l[1], l[0]))
 
# check heavy-hitter triangles
for i in range(n):
  if sortD[i][1] < math.sqrt(m):
    break # degree < sqrt(m)
  
  for j in range(i+1,n):
    if sortD[j][1] < math.sqrt(m):
      break # degree < sqrt(m)
    
    for k in range(j+1,n):
      if sortD[k][1] < math.sqrt(m):
        break # degree < sqrt(m)
      
      # check edges
      if not inE(sortD[i][0], sortD[j][0]):
        continue
      if not inE(sortD[j][0], sortD[k][0]):
        continue
      if not inE(sortD[k][0], sortD[i][0]):
        continue
      hT = hT + 1

# check other triangles
for (v1, v2) in E.keys():
  if D[v1] >= math.sqrt(m) and D[v2] >= math.sqrt(m):
    continue  # both are heavy-hitters
  if cmp(v2, v1): # set v1 to the smallest
    cnt = v2
    v2 = v1
    v1 = cnt
  if D[v1] < math.sqrt(m):
    for friend in F[v1]:
      # v1 < v2 < friend
      if cmp(friend, v2):
        continue
      # check edge
      if not inE(v2, friend):
        continue
      oT = oT + 1

T = hT + oT
print(T)