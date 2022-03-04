import sys
import numpy as np

F = []    # features list
L = []    # labels list
acc = 0   # accuracy
C = 0.1
Eta = 0.0001
numFolds = 10
size = 600
epoch = 2500

f1 = open(sys.argv[1], 'r')
f2 = open(sys.argv[2], 'r')
lines1 = f1.readlines()
lines2 = f2.readlines()

def train(trF, trL, x):
  # train 2500 times for each train set
  for i in range(epoch):
    multiplier = trL * np.matmul(trF, x) < 1
    dL = np.matmul((multiplier*trL), trF) * -1
    dF = C*dL + x
    x = x - Eta*dF
  return x

# set features
for line in lines1:
  line = line.split(',')
  for i in range(len(line)):
    line[i] = int(line[i])
  F.append(line)
# append 1 to the end of row
for i in range(len(F)):
  F[i].append(1)
F = np.array(F)

# set labels
for line in lines2:
  L.append(int(line))
L = np.array(L)

# execute k-fold
for k in range(numFolds):
  # slice the features and labels
  cutF = F[k*size : (k+1)*size]
  cutL = L[k*size : (k+1)*size]

  # make train set
  trF = np.delete(F, np.s_[k*size : (k+1)*size], 0)
  trL = np.delete(L, np.s_[k*size : (k+1)*size])
  
  x = train(trF, trL, np.ones(F.shape[1]))  # train
  acc = acc + np.sum(np.equal(np.sign(np.matmul(cutF, x)), cutL))/size

print(acc/10)
print(C)
print(Eta)