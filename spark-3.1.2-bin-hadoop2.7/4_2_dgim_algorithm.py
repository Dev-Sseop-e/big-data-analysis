import sys

# Set variables
stream = []
bucketSize = 1
bucket = {1:[]}
k_list = [] # bucket list
streamNum = sys.argv[2:]  # read the stream number

f = open(sys.argv[1], 'r')
for line in f:
  stream.append(int(line))

# Set bucket
for i in range(len(stream)):
  if stream[i] == 1:
    bucket[1].append((i, i))
  
  if len(bucket[1]) == 3:
    # test size
    j = 1
    while j < bucketSize+1:
      if len(bucket[j]) == 3:
        if j*2 not in bucket.keys():
          bucket[j*2] = []
          bucketSize = bucketSize*2
        bucket[j*2].append((bucket[j].pop(0)[0], bucket[j].pop(0)[1]))
      j = j*2

# calculate the bits
for i in bucket.keys():
  for j in reversed(range(len(bucket[i]))):
    k_list.append((i, j))

for k in streamNum:
  if k == '0':
    print(0)
  else:
    result = 0
    pos = 10000000 - int(k)
    
    for bits in k_list:
      start, end = bucket[bits[0]][bits[1]]
      if pos <= end:
        ind = k_list.index(bits)
    
    for num in k_list[:ind]:
      result = result + num[0]
    result = result + k_list[ind][0]/2
    print(result)