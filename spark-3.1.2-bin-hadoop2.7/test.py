
count = 0
for n in range(1, 5):
  for i in range(1, n+1):
    if n%i == 0:
      count += 1

print(count)