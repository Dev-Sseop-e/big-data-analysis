import numpy as np

M = np.array([1/3, 1/2, 0, 1/3, 0, 1/2, 1/3, 1/2, 1/2]).reshape((3,3))
M = np.identity(3) - 0.8*M
e = 0.2*np.array([1/3, 1/3, 1/3]).reshape((3,1))

print(np.dot(np.linalg.inv(M), e))

import numpy as np

M = np.array([0, 1/2, 1, 0, 1/3, 0, 0, 1/2, 1/3, 0, 0, 1/2, 1/3, 1/2, 0, 0]).reshape((4,4))
M = np.identity(4) - 0.8*M
#e = 0.2*np.array([1, 0, 0, 0]).reshape((4,1))       # For a: A only
e = 0.2*np.array([1/2, 0, 1/2, 0]).reshape((4,1))  # For b: A and C
print(np.dot(np.linalg.inv(M), e))