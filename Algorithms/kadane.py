"""
@Script, that implements Kadane's algorithm to find a contiguous subarray with the largest sum as an external method.

@Owns: "Prof. Joseph Born Kadane"
@Contiributor: "Devesh Agrawal" & "Emir Cetin Memis" & "Emircan Yaprak" & "Tuana Selen Ozhazday"

@Student_1:     "Emir Cetin Memis"    |   @Student_2:     "Emircan Yaprak"        |   @Student_3:     "Tuana Selen Ozhazday"
@StudentID_1:   041901027             |   @StudentID_2:   041901009               |   @StudentID_3:   041901024
@Contact_1:     "memise@mef.edu.tr"   |   @Contact_2:     "yaprakem@mef.edu.tr"   |   @Contact_3:     "ozhazdayt@mef.edu.tr"

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
            "F":0,
            "G":0,
            "H":0,
            "I":0,
            "J":0,
            "K":0,
            "L":0,
            "M":0,
            "N":0,
            "O":0
        }

    # Method that implements Kadane's algorithm.
    # @param list array: The array that will be used to find the subarray with the largest sum.
    # @return tuple: The tuple that contains the start index, end index and the sum of the subarray with the largest sum.
    def _kadane(self, array:list) -> tuple :

        currentMaxSum = 0                               ; self.iterations["A"] += 1
        maximumSum    = -inf                            ; self.iterations["B"] += 1
        startTrack    = 0                               ; self.iterations["C"] += 1
        startIndex    = 0                               ; self.iterations["D"] += 1
        endIndex      = 0                               ; self.iterations["E"] += 1

        for currentIndex in range(len(array)) :
            pass                                        ; self.iterations["F"] += 1
            currentMaxSum += array[currentIndex]        ; self.iterations["G"] += 1
            if (maximumSum < currentMaxSum) :
                pass                                    ; self.iterations["H"] += 1
                maximumSum = currentMaxSum              ; self.iterations["I"] += 1
                startIndex = startTrack                 ; self.iterations["J"] += 1
                endIndex = currentIndex                 ; self.iterations["K"] += 1
            if (currentMaxSum < 0) :
                pass                                    ; self.iterations["L"] += 1
                currentMaxSum = 0                       ; self.iterations["M"] += 1
                startTrack = currentIndex + 1           ; self.iterations["N"] += 1

        pass                                            ; self.iterations["O"] += 1
        return (
            startIndex,
            endIndex,
            maximumSum,
            self.iterations
        )

    # Driver method.
    def solve(self, inputArray:list) -> tuple :
        return self._kadane(inputArray)
