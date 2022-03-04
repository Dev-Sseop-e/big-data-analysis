import sys
import numpy as np

np.random.seed(0)

class Fully_Connected_Layer:
  def __init__(self, learningRate):
    self.InputDim = 784
    self.HiddenDim = 128
    self.OutputDim = 10
    self.learningRate = learningRate
    
    '''Weight Initialization'''
    self.W1 = np.random.randn(self.InputDim, self.HiddenDim)
    self.W2 = np.random.randn(self.HiddenDim, self.OutputDim) 
    
    self.u = None
    self.uSig = None
    self.v = None
    
  def Forward(self, Input):
    '''Implement forward propagation'''
    self.u = Input.dot(self.W1)
    self.uSig = 1/(1+np.exp(-self.u))
    self.v = self.uSig.dot(self.W2)
    result = 1/(1+np.exp(-self.v))
    return result
    
  def Backward(self, Input, Label, Output):
    '''Implement backward propagation'''
    gradientV = (Output*(1-Output))*(Output-Label)
    gradientW2 = self.uSig.T.dot(gradientV)
    gradientUSig = gradientV.dot(self.W2.T)
    gradientU = (self.uSig*(1-self.uSig))*gradientUSig
    gradientW1 = Input.T.dot(gradientU)
    
    '''Update parameters using gradient descent'''
    self.W1 = self.W1 - self.learningRate * gradientW1
    self.W2 = self.W2 - self.learningRate * gradientW2
  
  def Train(self, Input, Label):
    Output = self.Forward(Input)
    self.Backward(Input, Label, Output)

  def Test(self, Input, Label):
    Output = self.Forward(Input)
    assert(np.shape(Output) == np.shape(Label))
    count = 0.0
    for i in range(len(Label)):
      if np.argmax(Output[i, :]) == np.argmax(Label[i, :]):
        count = count + 1
    return count / len(Label)

learningRate = 0.03
iteration = 5000
size = 100

'''Construct a fully-connected network'''
Network = Fully_Connected_Layer(learningRate)

fTrain = open(sys.argv[1], 'r')
fTest = open(sys.argv[2], 'r')
train = np.array([list(map(float, line.split(','))) for line in fTrain.readlines()])
test = np.array([list(map(float, line.split(','))) for line in fTest.readlines()])
trainData = train[:, :-1]
testData = test[:, :-1]

trainLabel = np.zeros((len(train), 10))
testLabel = np.zeros((len(test), 10))
trainLabel[np.arange(len(train)), list(map(int, train[:, -1]))] = 1
testLabel[np.arange(len(test)), list(map(int, test[:, -1]))] = 1

'''Train the network for the number of iterations'''
'''Implement function to measure the accuracy'''
for i in range(iteration):
  for j in range(0, len(trainData), size):
    Network.Train(trainData[j:(j+size), :], trainLabel[j:(j+size), :])

print(Network.Test(trainData, trainLabel))
print(Network.Test(testData, testLabel))
print(iteration)
print(learningRate)