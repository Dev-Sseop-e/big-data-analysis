import sys

f = open(sys.argv[1], 'r')
lines = f.readlines()

# make a dataset using dictionary
data = {}
for line in lines:
  line = line.split(',')
  if int(line[0]) not in data.keys():
    data[int(line[0])] = {}
  data[int(line[0])][int(line[1])] = float(line[2])

f.close()

def cosine_distance(x, y):
  dotProduct = 0
  sum1 = sum([i**2 for i in x.values()])  # sum of x_value squares
  sum2 = sum([j**2 for j in y.values()])  # sum of y_value squares

  for k in x.keys():
    if k in y.keys():
      dotProduct += x[k]*y[k]
  
  if (sum1 == 0) or (sum2 == 0):
    return 0
  # return cosine distance of x and y
  return dotProduct/((sum1**0.5)*(sum2**0.5))

# User-based
userNorm = {}
cosDist = {}
simUser = []
movRate = {}
U = 600

# normalize the values
for user in data.keys():
  userNorm[user] = {}
  sumValue = sum([i for i in data[user].values()])
  average = sumValue/len(data[user].keys())

  for j in data[user].keys():
    userNorm[user][j] = data[user][j] - average

# use cosine distance
for user in userNorm.keys():
  if user == U:
    continue
  cosDist[user] = cosine_distance(userNorm[user], userNorm[U])

for user in sorted(cosDist, key=cosDist.get, reverse=True)[:10]:
  simUser.append(user)  # top10 users

# rate the score
for i in range(1, 1001):
  score = 0
  totalNum = 0
  for user in simUser:
    if i not in data[user].keys():
      continue
    score = score + data[user][i]
    totalNum = totalNum + 1
  if totalNum == 0:
    movRate[i] = 0
  else:
    movRate[i] = score/totalNum # average score of each movie

# for descending order of score and ascending order of movie ID
result = sorted(movRate.items(), key=lambda x: (-x[1], x[0]))[:5]
for movie in result:
  print("%d\t%.1f" %(movie[0], movie[1]))

##-------------------------------------------------------------------##
# Item-based
itemNorm = {}
cosDist2 = {}
simItem = {}
movRate2 = {}

# switch the users and items
for user in userNorm.keys():
  for item in userNorm[user].keys():
    if item not in itemNorm.keys():
      itemNorm[item] = {}
    itemNorm[item][user] = userNorm[user][item]

# compute the similarity of movie
for i in range(1, 1001):
  if not i in itemNorm.keys():  # except unrated movies
    continue
  cosDist2[i] = {}  # for the vector
  for j in itemNorm.keys():
    if j != i:
      cosDist2[i][j] = cosine_distance(itemNorm[i], itemNorm[j])

for i in range(1, 1001):
  if i not in itemNorm.keys():  # except unrated movies
    continue
  simItem[i] = [item for item in sorted(cosDist2[i], key=cosDist2[i].get, reverse=True)[:10]]

# rate the score
for i in range(1, 1001):
  if i not in itemNorm.keys():  # except unrated movies
    continue
  score = 0
  totalNum = 0
  for item in simItem[i]:  # top10 movies
    if item in data[U].keys(): # rated by U
      score = score + data[U][item]
      totalNum = totalNum + 1
  if totalNum == 0:
    movRate2[i] = 0
  else:
    movRate2[i] = score/totalNum  # average score of each movie

# for descending order of score and ascending order of movie ID
result2 = sorted(movRate2.items(), key=lambda x: (-x[1], x[0]))[:5]
for movie in result2:
  print("%d\t%.1f" %(movie[0], movie[1]))