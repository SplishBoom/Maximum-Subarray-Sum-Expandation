from    algorithms  import bf, dc, kd
from    utils       import generateTestArray
from    utils       import safeStart, safeStop
import  argparse
import  timeit
import pandas as pd
import matplotlib.pyplot as plt

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

def saveToFile(data, fileName):
    
    

# Main Method, that runs the program according to the given arguments.
# @param int N: The number of elements in the array.
# @param int BORDER: The borders of the elements in the array.
# @param bool continuouslyGenerate: If the program should generate test cases continuously.
# @param bool saveToExcel: If the program should save the results to an excel file.
# @param bool plotResults: If the program should plot the results.
# @param bool generateReport: If the program should generate a report.
# @return None
def main(N:int, BORDER:int, REPEAT:int, continuouslyGenerate:bool, savetoFile:bool, plotResults:bool, generateReport:bool) -> None :

    if not continuouslyGenerate :
        data = [simulate(N,BORDER,REPEAT)]
    else :
        data = []
        for n in range(1, N + 1) :
            data.append(simulate(n,BORDER,REPEAT))

    if savetoFile :
        saveToFile(data, "results.xlsx")
    else :
        print(data[0], " ...")


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
    parser.add_argument("-r", "--generate-report", type=int, help="If this flag is set, the results will be reported.", required=False, default=False)
    args = parser.parse_args()

    N                       = args.number_of_elements
    BORDER                  = args.border
    REPEAT                  = args.repeat 
    continuouslyGenerate    = bool(args.continuously_generate)
    savetoFile             = bool(args.save_to_file)
    plotResults             = bool(args.plot_results)
    generateReport          = bool(args.generate_report)

    main(N, BORDER, REPEAT, continuouslyGenerate, savetoFile, plotResults, generateReport)

    safeStop()