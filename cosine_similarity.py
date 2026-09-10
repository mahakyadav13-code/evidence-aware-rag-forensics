import math

def dot_product(v1, v2):
    return sum(a * b for a, b in zip(v1, v2))

def magnitude(v):
    return math.sqrt(sum(a**2 for a in v))

def cosine_similarity_scratch(v1, v2):
    return dot_product(v1, v2) / (magnitude(v1) * magnitude(v2))

# Test vectors
v1 = [1, 2, 3]
v2 = [4, 5, 6]

print("From scratch:", cosine_similarity_scratch(v1, v2))

# Verify with numpy
import numpy as np
def cosine_similarity_numpy(v1, v2):
    v1, v2 = np.array(v1), np.array(v2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

print("Numpy check:", cosine_similarity_numpy(v1, v2))