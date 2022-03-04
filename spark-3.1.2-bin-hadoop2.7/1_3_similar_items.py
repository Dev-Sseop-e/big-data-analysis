import re
import sys
import random
import numpy as np

f = open(sys.argv[1], 'r')
k = 3   # k-shingles
B = 6   # bands
R = 20  # rows

# number of articles, list of text and shingles
article_id, texts, shingles = [], [], []

# return random number
def hash(x):
  return random.randint(0, x-1)

# read and split by id, text, shingles
while True:
  lines = f.readline()
  if not lines: break
  id, text = lines.split(' ', 1)
  article_id.append(id)
  text = re.sub(r'[^a-zA-Z\s]', '', text)
  texts.append(text.lower())
  for i in range(len(text) - k):
    shingles.append(text[i:i+k])
  shingles = list(set(shingles))  # remove mutations

# characteristic matrix
c_matrix = np.zeros((len(shingles), len(article_id)))

for i in range(len(texts)):
  for j in range(len(shingles)):
    if shingles[j] in texts[i]:
      c_matrix[j][i] = 1

# finding the prime number
prime_num = len(shingles)
while True:
  is_prime = True
  for i in range(2, int(prime_num ** 0.5) + 1):
    if prime_num % i == 0:
      is_prime = False
      break
  if is_prime:
    break
  prime_num += 1

# hash matrix
h_matrix = np.zeros((len(shingles), B*R)) # bands 6, rows 20

for i in range(B*R):
  a = hash(prime_num)
  b = hash(prime_num)
  for j in range(len(shingles)):
    h_matrix[j][i] = (a*j + b) % prime_num

# signature matrix
s_matrix = np.full((120, len(article_id)), np.inf)

for i in range(len(shingles)):
  for j in range(len(article_id)):
    if c_matrix[i][j] == 1:
      for k in range(B*R):
        if h_matrix[i][k] < s_matrix[k][j]:
          s_matrix[k][j] = h_matrix[i][k]

# make the list of index which satisfy 'similarity >= 0.9'
result = []

for i in range(len(article_id)):
  for j in range(i+1, len(article_id)):
    s = 0
    for k in range(B*R):
      if s_matrix[k][j] == s_matrix[k][i]:
        s += 1
    if (s / 120.0) >= 0.9:
      result.append([i, j, s / 120.0])

# print the article id of result
for i in range(len(result)):
  print(str(article_id[result[i][0]]) + '\t' + str(article_id[result[i][1]]))

f.close()