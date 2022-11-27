"""
@Script, that implements the divide and conquer algorithm to find a contiguous subarray with the largest sum as an external method.

@Owns: "John von Neumann"
@Contiributors: "Anand Kumar" & "Emir Cetin Memis"

@Student_1:     "Emir Cetin Memis"    |   @Student_2:     "Emircan Yaprak"
@StudentID_1:   041901027             |   @StudentID_2:   041901009
@Contact_1:     "memise@mef.edu.tr"   |   @Contact_2:     "yaprakem@mef.edu.tr"

@Set&Rights: "MEF University"
@Instructor: "Prof. Dr. Muhittin Gokmen"
@Course:     "Analysis of Algorithms"
@Req:        "Project 1"

@Since: 11/27/2022
"""

from math import inf

# Method that implements the divide and conquer algorithm.
# @param list array: The array that will be used to find the subarray with the largest sum.
# @param int low: The lower bound of the array.
# @param int high: The upper bound of the array.
# @return tuple: The tuple that contains the start index, end index and the sum of the subarray with the largest sum.
def _divide_and_conquer(array:list, low:int, high:int) -> tuple :

    if low == high :
        return (
            low, 
            high, 
            array[low]
        )

    mid = (low+high) // 2

    currentLowIndex = mid
    currentSum      = 0
    leftSum         = -inf
    maxLeft         = mid
    while (currentLowIndex >= low) :
        currentSum += array[currentLowIndex]
        if (currentSum > leftSum) :
            leftSum = currentSum
            maxLeft = currentLowIndex
        currentLowIndex -= 1

    currentRightIndex = mid+1
    currentSum        = 0
    rightSum          = -inf
    maxRight          = mid+1
    while (currentRightIndex <= high) :
        currentSum += array[currentRightIndex]
        if (currentSum > rightSum) :
            rightSum = currentSum
            maxRight = currentRightIndex
        currentRightIndex += 1

    leftLow , leftHigh , leftSumR  = _divide_and_conquer(array, low, mid)
    rightLow, rightHigh, rightSumR = _divide_and_conquer(array, mid+1, high)    
    crossLow, crossHigh, crossSumR = maxLeft, maxRight, leftSum+rightSum

    if ( (leftSumR >= rightSumR) and (leftSumR >= crossSumR) ) :
        startIndex, endIndex, maximumSum = leftLow, leftHigh, leftSumR
    elif ( (rightSumR >= leftSumR) and (rightSumR >= crossSumR) ) :
        startIndex, endIndex, maximumSum = rightLow, rightHigh, rightSumR
    else:
        startIndex, endIndex, maximumSum = crossLow, crossHigh, crossSumR

    return (
        startIndex, 
        endIndex, 
        maximumSum
    )

# Driver method.
def solve(inputArray:list) -> tuple :
    return _divide_and_conquer(inputArray, 0, len(inputArray)-1)