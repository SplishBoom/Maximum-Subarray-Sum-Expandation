"""
@Script, that implements an own-design naive algorithm to find a contiguous subarray with the largest sum as an external method.

@Owns: "Emir Cetin Memis" & "Emircan Yaprak"
@Contiributors: "Emir Cetin Memis" & "Emircan Yaprak"

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

class ClassBruteForce :

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
        }

    # Method that implements the naive algorithm.
    # @param list array: The array that will be used to find the subarray with the largest sum.
    # @return tuple: The tuple that contains the start index, end index and the sum of the subarray with the largest sum.
    def _brute_force(self, array:list) -> tuple :

        maximumSum = -inf                                       ; self.iterations["A"] += 1
        startIndex = 0                                          ; self.iterations["B"] += 1
        endIndex   = 0                                          ; self.iterations["C"] += 1

        for currentIndex in range(len(array)) :
            pass                                                ; self.iterations["D"] += 1
            currentSum = array[currentIndex]                    ; self.iterations["E"] += 1
            if (currentSum > maximumSum) :
                pass                                            ; self.iterations["F"] += 1
                maximumSum = currentSum                         ; self.iterations["G"] += 1
                startIndex = currentIndex                       ; self.iterations["H"] += 1
                endIndex   = currentIndex                       ; self.iterations["I"] += 1

            for j in range(currentIndex+1, len(array)) :
                pass                                            ; self.iterations["J"] += 1
                currentSum += array[j]                          ; self.iterations["K"] += 1
                if (currentSum > maximumSum) :
                    pass                                        ; self.iterations["L"] += 1
                    maximumSum = currentSum                     ; self.iterations["M"] += 1
                    startIndex = currentIndex                   ; self.iterations["N"] += 1
                    endIndex   = j                              ; self.iterations["O"] += 1

        pass                                                    ; self.iterations["P"] += 1
        return ( 
            startIndex, 
            endIndex, 
            maximumSum,
            self.iterations
        )

    # Driver method.
    def solve(self, inputArray:list) -> tuple :
        return self._brute_force(inputArray)