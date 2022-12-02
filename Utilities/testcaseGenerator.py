"""
This script is used for test case generations. For more details, it is externally written here:
"""

import random

# Method, that generates a test array with N elements with BORDER borders.
# @param int N: The number of elements in the array.
# @param int BORDER: The borders of the elements in the array.
# @return list: The generated test array.
def generateTestArray(N:int, BORDER:int=100) -> list :

    testArray = N * [0]

    for i in range(0, N) :
        testArray[i] = random.randint(-BORDER, BORDER)

    random.shuffle(testArray)

    return testArray.copy()

