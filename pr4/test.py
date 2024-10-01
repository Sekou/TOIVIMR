import itertools
import numpy as np

def getAllPartitions(lst):
    if len(lst) == 0:
        return [[]]
    result = []
    for i in range(1, len(lst) + 1):
        for group in itertools.combinations(lst, i):
            remaining = [x for x in lst if x not in group]
            for p in getAllPartitions(remaining):
                result.append([list(group)] + p)
    return result

ii=np.arange(6)
pp=getAllPartitions(ii)
print(pp)