"""
This script is used for test case generations.
"""

import random

def generateTestArray(N:int, BORDER:int=100) -> list :
    """
    Method, that generates a test array with N elements with BORDER borders.
    @params :
        N       - Required  : The number of elements in the array. (int)
        BORDER  - Optional  : The borders of the elements in the array. (int)
    @return : 
        The generated test array. (list)
    """

    testArray = N * [0]

    for i in range(0, N) :
        testArray[i] = random.randint(-BORDER, BORDER)

    random.shuffle(testArray)

    #return [0, -2, 3, 4, 6, 5].copy() use this when specific array input required.
    return testArray.copy()

