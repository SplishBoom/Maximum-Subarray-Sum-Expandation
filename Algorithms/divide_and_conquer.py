"""
@Script, that implements the divide and conquer algorithm to find a contiguous subarray with the largest sum as an external method.

@Owns: "John von Neumann"
@Contiributors: "Anand Kumar" & "Emir Cetin Memis"

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

class ClassDivideAndConquer :

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
            "O":0,
            "P":0,
            "R":0,
            "S":0,
            "T":0,
            "U":0,
            "V":0,
            "W":0,
            "X":0,
            "Y":0,
            "Z":0,
            "Q":0,
            "AA":0,
            "AB":0,
            "AC":0,
            "AD":0,
            "AE":0,
            "AF":0,
        }

    # Method that implements the divide and conquer algorithm.
    # @param list array: The array that will be used to find the subarray with the largest sum.
    # @param int low: The lower bound of the array.
    # @param int high: The upper bound of the array.
    # @return tuple: The tuple that contains the start index, end index and the sum of the subarray with the largest sum.
    def _divide_and_conquer(self, array:list, low:int, high:int) -> tuple :

        if low == high :
            pass                                                                                ; self.iterations["A"] += 1
            return (
                low, 
                high, 
                array[low]
            )

        mid = (low+high) // 2                                                                   ; self.iterations["B"] += 1

        currentLowIndex = mid                                                                   ; self.iterations["C"] += 1
        currentSum      = 0                                                                     ; self.iterations["D"] += 1
        leftSum         = -inf                                                                  ; self.iterations["E"] += 1
        maxLeft         = mid                                                                   ; self.iterations["F"] += 1
        while (currentLowIndex >= low) :
            pass                                                                                ; self.iterations["G"] += 1
            currentSum += array[currentLowIndex]                                                ; self.iterations["H"] += 1
            if (currentSum > leftSum) :
                pass                                                                            ; self.iterations["I"] += 1
                leftSum = currentSum                                                            ; self.iterations["J"] += 1
                maxLeft = currentLowIndex                                                       ; self.iterations["K"] += 1
            currentLowIndex -= 1                                                                ; self.iterations["L"] += 1

        currentRightIndex = mid+1                                                               ; self.iterations["M"] += 1
        currentSum        = 0                                                                   ; self.iterations["N"] += 1
        rightSum          = -inf                                                                ; self.iterations["O"] += 1
        maxRight          = mid+1                                                               ; self.iterations["P"] += 1
        while (currentRightIndex <= high) :
            pass                                                                                ; self.iterations["Q"] += 1
            currentSum += array[currentRightIndex]                                              ; self.iterations["R"] += 1
            if (currentSum > rightSum) :
                pass                                                                            ; self.iterations["S"] += 1
                rightSum = currentSum                                                           ; self.iterations["T"] += 1
                maxRight = currentRightIndex                                                    ; self.iterations["U"] += 1
            currentRightIndex += 1                                                              ; self.iterations["V"] += 1

        leftLow , leftHigh , leftSumR  = self._divide_and_conquer(array, low, mid)              ; self.iterations["W"] += 1
        rightLow, rightHigh, rightSumR = self._divide_and_conquer(array, mid+1, high)           ; self.iterations["X"] += 1
        crossLow, crossHigh, crossSumR = maxLeft, maxRight, leftSum+rightSum                    ; self.iterations["Y"] += 1

        if ( (leftSumR >= rightSumR) and (leftSumR >= crossSumR) ) :
            pass                                                                                ; self.iterations["Z"] += 1
            startIndex, endIndex, maximumSum = leftLow, leftHigh, leftSumR                      ; self.iterations["AA"] += 1
        elif ( (rightSumR >= leftSumR) and (rightSumR >= crossSumR) ) :
            pass                                                                                ; self.iterations["AB"] += 1
            startIndex, endIndex, maximumSum = rightLow, rightHigh, rightSumR                   ; self.iterations["AC"] += 1
        else:
            pass                                                                                ; self.iterations["AD"] += 1
            startIndex, endIndex, maximumSum = crossLow, crossHigh, crossSumR                   ; self.iterations["AE"] += 1

        pass                                                                                    ; self.iterations["AF"] += 1
        return (
            startIndex, 
            endIndex, 
            maximumSum,
        )

    # Driver method.
    def solve(self, inputArray:list) -> tuple :
        return *self._divide_and_conquer(inputArray, 0, len(inputArray)-1), self.iterations
