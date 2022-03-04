import sys
import numpy as np

# make normal dataset and test dataset using dictionary
f = open(sys.argv[1], 'r')
t = open(sys.argv[2], 'r')

linesF = f.readlines()
linesT = t.readlines()
data = {}
testData = {}

for line in linesF:
  line = line.split(',')
  if int(line[0]) not in data.keys():
    data[int(line[0])] = {}
  data[int(line[0])][int(line[1])] = float(line[2])

for line in linesT:
  line = line.split(',')
  # set the key by tuple and value is zero
  testData[(int(line[0]), int(line[1]), line[3])] = 0

f.close()
t.close()

def softMax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)

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

# set variables
userNorm = {} # normalization of users
cosDist = {}  # cosine distance
simUser = {}  # similar user list
movRate = {}  # rate of movies

itemNorm = {} # normalization of items
cosDist2 = {} # cosine distance
simItem = {}  # similar item list
movRate2 = {} # rate of movies

# normalize the dataset
for user in data.keys():
  userNorm[user] = {}
  sumValue = sum([i for i in data[user].values()])
  average = sumValue/len(data[user].keys())

  for j in data[user].keys():
    userNorm[user][j] = data[user][j] - average

# compute the similarity
for user1 in data.keys():
  cosDist[user1] = {}
  for user2 in data.keys():
    if user1 == user2:
      continue
    cosDist[user1][user2] = cosine_distance(userNorm[user1], userNorm[user2])

for user in data.keys():
  simUser[user] = {}
  # list the top 300 of users
  for sim in sorted(cosDist[user], key=cosDist[user].get, reverse=True)[:300]:
    simUser[user][sim] = cosDist[user][sim]

# rate the movie
for (user, item, time) in testData.keys():
  score = []  # will be appended similar users' score
  scaler = [] # will be appended cos-distance of user
  for sim in simUser[user].keys():
    if item not in data[sim].keys():
      continue
    score.append(data[sim][item])
    scaler.append(simUser[user][sim])
  if len(scaler) == 0:
    # average of valuation
    scoreList = [i for i in data[user].values()]
    movRate[(user, item)] = sum(scoreList)/len(scoreList)
  else:
    # multiplication of matrix
    movRate[(user, item)] = np.matmul(score, np.transpose(softMax(scaler)))

# switch the users and items
for user in userNorm.keys():
  for item in userNorm[user].keys():
    if item not in itemNorm.keys():
      itemNorm[item] = {}
    itemNorm[item][user] = userNorm[user][item]

# compute the similarity
for item1 in itemNorm.keys():
  cosDist2[item1] = {}
  for item2 in itemNorm.keys():
    if item1 == item2:
      continue
    cosDist2[item1][item2] = cosine_distance(itemNorm[item1], itemNorm[item2])

for item in itemNorm.keys():
  simItem[item] = {}
  # list the top 1200 of items
  for sim in sorted(cosDist2[item], key=cosDist2[item].get, reverse=True)[:1200]:
    simItem[item][sim] = cosDist2[item][sim]

# rate the movie
for (user, item, time) in testData.keys():
  if item in simItem.keys():
    score = []  # will be appended similar users' score
    scaler = [] # will be appended cos-distance of user
    for sim in simItem[item].keys():
      if sim not in data[user].keys():
        continue
      score.append(data[user][sim])
      scaler.append(simItem[item][sim])
    if len(scaler) == 0:
      # average of valuation
      scoreList = [i for i in data[user].values()]
      movRate2[(user, item)] = sum(scoreList)/len(scoreList)
    else:
      # multiplication of matrix
      movRate2[(user, item)] = np.matmul(score, np.transpose(softMax(scaler)))
  else:
    # average of valuation
    scoreList = [i for i in data[user].values()]
    movRate2[(user, item)] = sum(scoreList)/len(scoreList)

# calculate the average value of rate
for (user, item, time) in testData.keys():
  testData[(user, item, time)] = (movRate[(user, item)]*2 + movRate2[(user, item)]*5)/7

# rewrite the output txt file
f = open("./output.txt", 'w')
for (user, item, time), rate in testData.items():
  dataset = "%d,%d,%f,%s" %(user, item, rate, time)
  f.write(dataset)

f.close()