from algorithms import bf, dc, kd

import random

import timeit
import argparse

def generateTestArray(N, border=100) :

    testArray = [0] * N

    for i in range(0, N) :
        testArray[i] = random.randint(-border, border)

    print("The generated test array is as follows:")
    print(testArray)

    return testArray

def main(N) :

    testArray = generateTestArray(N)

    startForBruteForce = timeit.default_timer()
    bruteForceResult = bf(testArray)
    endForBruteForce = timeit.default_timer()

    startForDivideAndConquer = timeit.default_timer()
    divideAndConquerResult = dc(testArray)
    endForDivideAndConquer = timeit.default_timer()

    startForKadane = timeit.default_timer()
    kadaneResult = kd(testArray)
    endForKadane = timeit.default_timer()

    bfTime = (round((endForBruteForce - startForBruteForce) * 10 ** 6, 3))
    dcTime = (round((endForDivideAndConquer - startForDivideAndConquer) * 10 ** 6, 3))
    kdTime = (round((endForKadane - startForKadane) * 10 ** 6, 3))

    print("\nFor the given N value of " + str(N) + " the results are as follows:")
    print("Algorithm -> {:^20} outputs as {:^15} and elapsed time is {} µs.".format("Brute Force", str(bruteForceResult), bfTime))
    print("Algorithm -> {:^20} outputs as {:^15} and elapsed time is {} µs.".format("Divide and Conquer", str(divideAndConquerResult), dcTime))
    print("Algorithm -> {:^20} outputs as {:^15} and elapsed time is {} µs.".format("Kadane", str(kadaneResult), kdTime))

        
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This script is used to compare the performance of the brute force, divide and conquer and Kadane's algorithms.")
    parser.add_argument("-n", "--number", type=int, help="The number of elements in the array.", required=True)
    args = parser.parse_args()

    N = args.number

    main(N)