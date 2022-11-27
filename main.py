from    algorithms  import bf, dc, kd
from    utils       import generateTestArray
from    utils       import safeStart, safeStop
import  argparse
import  timeit
import pandas as pd
import matplotlib.pyplot as plt
import time
import keyboard
import os

# Method that simulates the algorithms. For given repeat times it repeats and measures the average time of n repeats.
# @param int N: The number of elements in the array.
# @param int BORDER: The borders of the elements in the array.
# @param int REPEAT: The number of repeats.
# @return dict: The results of the simulation.
def simulate(N, BORDER, REPEAT) :

    testArray = generateTestArray(N, BORDER)

    data = []

    for i in range(REPEAT) :
        startTimeForBF = timeit.default_timer()
        BFResult = bf(testArray)
        endTimeForBF = timeit.default_timer()
        BFTime = (round((endTimeForBF - startTimeForBF) * 10 ** 6, 3))

        startTimeForDC = timeit.default_timer()
        DCResult = dc(testArray)
        endTimeForDC = timeit.default_timer()
        DCtime = (round((endTimeForDC - startTimeForDC) * 10 ** 6, 3))

        startTimeForKD = timeit.default_timer()
        KDResult = kd(testArray)
        endTimeForKD = timeit.default_timer()
        KDtime = (round((endTimeForKD - startTimeForKD) * 10 ** 6, 3))

        results = (
            BFResult,
            DCResult,
            KDResult,
            BFTime,
            DCtime,
            KDtime
        )
        
        data.append(results)

    if (REPEAT == 1) :
        return (
            N,
            data[0]
        )
    else :

        for currentTuple in data :
            for otherTuple in data :
                if (currentTuple[:3] != otherTuple[:3]) :
                    print("ERROR: Results are not the same!")
                    return (
                        N,
                        data[0]
                    )
        
        BFTime = 0
        DCtime = 0
        KDtime = 0
        for currentTuple in data :
            BFTime += currentTuple[3]
            DCtime += currentTuple[4]
            KDtime += currentTuple[5]

        BFTime = BFTime / REPEAT
        DCtime = DCtime / REPEAT
        KDtime = KDtime / REPEAT

        return (
            N,
            (
                data[0][0],
                data[0][1],
                data[0][2],
                BFTime,
                DCtime,
                KDtime
            )
        )

def saveToFile(data, fileName, save_to_file:bool):
    
    if save_to_file :
        dataFrameColumns = ["Algrotihm", "Complexity", "Time Elapsed", "Array Size", "Start Index", "End Index", "Maximum Sum"]
        dataFrame = pd.DataFrame(columns = dataFrameColumns)

        for currentTuple in data :
            dataFrame = pd.concat([dataFrame, pd.DataFrame([["Brute Force", "O(n^2)", currentTuple[1][3], currentTuple[0], currentTuple[1][0][0], currentTuple[1][0][1], currentTuple[1][0][2]]], columns = dataFrameColumns)], ignore_index = True)
            dataFrame = pd.concat([dataFrame, pd.DataFrame([["Divide & Conquer", "O(nlogn)", currentTuple[1][4], currentTuple[0], currentTuple[1][1][0], currentTuple[1][1][1], currentTuple[1][1][2]]], columns = dataFrameColumns)], ignore_index = True)
            dataFrame = pd.concat([dataFrame, pd.DataFrame([["Kadane", "O(n)", currentTuple[1][5], currentTuple[0], currentTuple[1][2][0], currentTuple[1][2][1], currentTuple[1][2][2]]], columns = dataFrameColumns)], ignore_index = True)

        path = os.path.join("data-export", fileName)
        path = os.path.abspath(path)
        
        dataFrame.to_excel(path, index = False)
        
        return path
    else :
        print("Not saving to file")
        return "No Path"

# Method that plots the results.
# @param dict data: The results of the simulation.
# @param str fileName: The name of the file to save the results to.
# @param bool plotResults: If the program should plot the results.
# @return str path: The path to the output file.
def plotResults(data, fileName, plot_results:bool) -> str :

    if plot_results :
        x   = []
        yBF = []
        yDC = []
        yKD = []

        for currentTuple in data :
            x.append(currentTuple[0])
            yBF.append(currentTuple[1][3])
            yDC.append(currentTuple[1][4])
            yKD.append(currentTuple[1][5])

        plt.plot(x, yBF, label = "Brute Force - O(n^2)")
        plt.plot(x, yDC, label = "Divide & Conquer - O(nlogn)")
        plt.plot(x, yKD, label = "Kadane - O(n)")
        plt.xlabel("Number of elements in the array")
        plt.ylabel("Time elapsed (in microseconds)")
        plt.tight_layout()
        
        plt.legend()
        path = os.path.join("data-export", fileName)
        path = os.path.abspath(path)
        plt.savefig(path)

        return path
    else :
        print("Not plotting results")
        return "No Path"

# Main Method, that runs the program according to the given arguments.
# @param int N: The number of elements in the array.
# @param int BORDER: The borders of the elements in the array.
# @param bool continuouslyGenerate: If the program should generate test cases continuously.
# @param bool saveToExcel: If the program should save the results to an excel file.
# @param bool plotResults: If the program should plot the results.
# @param bool generateReport: If the program should generate a report.
# @return None
def main(N:int, BORDER:int, REPEAT:int, continuously_generate:bool, save_to_file:bool, plot_results:bool) -> None :
    
    if not continuously_generate :
        data = [simulate(N,BORDER,REPEAT)]
    else :
        data = []
        for n in range(1, N + 1) :
            print("Generating test case for n = " + str(n))
            data.append(simulate(n,BORDER,REPEAT))

            if keyboard.is_pressed("ESC") and keyboard.is_pressed("C") :
                print("User stopped generating test cases. Program will now continue by results.")
                break


    dataPath = saveToFile(data, "results.xlsx", save_to_file)
    
    plotPath = plotResults(data, "results.png", plot_results)

    print("Results saved to: " + dataPath)
    print("Plot saved to: " + plotPath)

# Client Driver        
if __name__ == "__main__":

    safeStart()

    parser = argparse.ArgumentParser(description="This script is used to compare the performance of the brute force, divide and conquer and Kadane's algorithms.")
    parser.add_argument("-n", "--number-of-elements", type=int, help="The number of elements in the array.", required=True)
    parser.add_argument("-b", "--border", type=int, help="The borders of the elements in the array.", default=100)
    parser.add_argument("-re", "--repeat", type=int, help="The number of times to repeat a simulation.", default=1)
    parser.add_argument("-c", "--continuously-generate", type=int, help="If this flag is set, the script will generate test cases continuously from 1 to N.", required=False, default=False)
    parser.add_argument("-s", "--save-to-file", type=int, help="If this flag is set, the results will be saved to a file.", required=False, default=False)
    parser.add_argument("-p", "--plot-results", type=int, help="If this flag is set, the results will be plotted.", required=False, default=False)
    args = parser.parse_args()

    N                       = args.number_of_elements
    BORDER                  = args.border
    REPEAT                  = args.repeat 
    continuously_generate   = bool(args.continuously_generate)
    save_to_file            = bool(args.save_to_file)
    plot_results            = bool(args.plot_results)

    main(N, BORDER, REPEAT, continuously_generate, save_to_file, plot_results)

    safeStop()