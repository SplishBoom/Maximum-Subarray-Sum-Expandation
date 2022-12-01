"""
@Script, that implements Kadane's algorithm to find a contiguous subarray with the largest sum as an external method.

@Owns: "Prof. Joseph Born Kadane"
@Contiributor: "Devesh Agrawal" & "Emir Cetin Memis" & "Emircan Yaprak"

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

class ClassKadane :

    def __init__(self) -> None :

        self.iterations = {
            "A":0,
            "B":0,
            "C":0,
            "D":0,
            "E":0,
        }

    # Method that implements Kadane's algorithm.
    # @param list array: The array that will be used to find the subarray with the largest sum.
    # @return tuple: The tuple that contains the start index, end index and the sum of the subarray with the largest sum.
    def _kadane(self, array:list) -> tuple :

        currentMaxSum = 0
        maximumSum    = -inf
        startTrack    = 0
        startIndex    = 0
        endIndex      = 0

        for currentIndex in range(len(array)) :
            currentMaxSum += array[currentIndex]
            if (maximumSum < currentMaxSum) :
                maximumSum = currentMaxSum
                startIndex = startTrack
                endIndex = currentIndex
            if (currentMaxSum < 0) :
                currentMaxSum = 0
                startTrack = currentIndex + 1

        return (
            startIndex,
            endIndex,
            maximumSum,
            self.iterations
        )

    # Driver method.
    def solve(self, inputArray:list) -> tuple :
        return self._kadane(inputArray)