from    algorithms  import  ClassBF, ClassDC, ClassKD
from    utils       import  generateTestArray
from    utils       import  safeStart, safeStop
import matplotlib.pyplot    as plt
import pandas               as pd
import argparse
import keyboard
import colorama
import timeit
import json
import os

"""
TODO :
    1-) The iterations count dictionaries are always returning the same input fix it ASAP!
"""

def execute(N:int) -> dict :

    testArray = generateTestArray(N)

    bfObject = ClassBF()
    startTimeForBF = timeit.default_timer()
    BFResult = bfObject.solve(testArray)
    endTimeForBF = timeit.default_timer()
    BFTime = (round((endTimeForBF - startTimeForBF) * 10 ** 6, 3))

    dcObject = ClassDC()
    startTimeForDC = timeit.default_timer()
    DCResult = dcObject.solve(testArray)
    endTimeForDC = timeit.default_timer()
    DCtime = (round((endTimeForDC - startTimeForDC) * 10 ** 6, 3))

    kdObject = ClassKD()
    startTimeForKD = timeit.default_timer()
    KDResult = kdObject.solve(testArray)
    endTimeForKD = timeit.default_timer()
    KDtime = (round((endTimeForKD - startTimeForKD) * 10 ** 6, 3))
    
    # if all results indexses and sum are equal then state is true
    state = (BFResult[0] == DCResult[0] == KDResult[0]) and (BFResult[1] == DCResult[1] == KDResult[1]) and (BFResult[2] == DCResult[2] == KDResult[2])

    results = {
        "Array Size" : N,
        "Test Array" : testArray,
        "Simulate Correct" : state,

        "BF Start Index" : BFResult[0],
        "BF End Index" : BFResult[1],
        "BF Sum" : BFResult[2],
        "BF Time" : BFTime,
        "BF Iterations" : BFResult[3],

        "DC Start Index" : DCResult[0],
        "DC End Index" : DCResult[1],
        "DC Sum" : DCResult[2],
        "DC Time" : DCtime,
        "DC Iterations" : DCResult[3],

        "KD Start Index" : KDResult[0],
        "KD End Index" : KDResult[1],
        "KD Sum" : KDResult[2],
        "KD Time" : KDtime,
        "KD Iterations" : KDResult[3]
    }

    return results


def simulate(N:int, continuously_generate) :

    stopperKeys = ["ESC", "C"]

    data = []

    if not continuously_generate :
        data.append(execute(N))
    else :
        for n in range(1, N + 1) :
            print("[\"{}\"+\"{}\"] to stop generation. || Generating test case by {}/{} ".format(str(stopperKeys[0]), str(stopperKeys[1]), str(n), str(N)))
            data.append(execute(n))
            if keyboard.is_pressed("ESC") and keyboard.is_pressed("C") :
                print("User stopped generating test cases. Program will now continue by results.")
                break

    return data
    
def saveToFile(data, fileName, save_to_file:bool) -> str :
    
    if not save_to_file :
        return "User didn't want to save results to file. For -> \"{}\"".format(fileName)

    path = os.path.abspath(os.path.join("data-export", fileName))

    dataFrameColumns = ["Algorithm", "Time Complexity", "SubArray Start Index", "SubArray End Index", "SubArray Sum", "Time Elapsed (microseconds)", "Iteration List", "Maximum Iteration"]

    dataFrame = pd.DataFrame(columns=dataFrameColumns)

    for result in data :
        dataFrame = pd.concat([dataFrame, pd.DataFrame([[ "Brute Force", "O(n^2)", result["BF Start Index"], result["BF End Index"], result["BF Sum"], result["BF Time"], result["BF Iterations"], max(result["BF Iterations"].values())]], columns=dataFrameColumns)])
        dataFrame = pd.concat([dataFrame, pd.DataFrame([[ "Divide and Conquer", "O(nlogn)", result["DC Start Index"], result["DC End Index"], result["DC Sum"], result["DC Time"], result["DC Iterations"], max(result["DC Iterations"].values())]], columns=dataFrameColumns)])
        dataFrame = pd.concat([dataFrame, pd.DataFrame([[ "Kadane's Algorithm", "O(n)", result["KD Start Index"], result["KD End Index"], result["KD Sum"], result["KD Time"], result["KD Iterations"], max(result["KD Iterations"].values())]], columns=dataFrameColumns)])

    dataFrame.to_excel(path, index=False)

    return "Results saved to file. For -> \"{}\"".format(path)


def plotResults(data, fileName1, fileName2, plot_results:bool) -> str :
    
    if not plot_results :
        return "User didn't want to plot results. For -> \"{}\" & \"{}\"".format(fileName1, fileName2)

    path1 = os.path.abspath(os.path.join("data-export", fileName1))
    path2 = os.path.abspath(os.path.join("data-export", fileName2))

    # matplotlib plot for timeXsize
    plt.figure(figsize=(10, 5))
    plt.plot([result["Array Size"] for result in data], [result["BF Time"] for result in data], label="Brute Force")
    plt.plot([result["Array Size"] for result in data], [result["DC Time"] for result in data], label="Divide and Conquer")
    plt.plot([result["Array Size"] for result in data], [result["KD Time"] for result in data], label="Kadane's Algorithm")
    plt.xlabel("Array Size")
    plt.ylabel("Time Elapsed (microseconds)")
    plt.title("Time Elapsed (microseconds) vs Array Size")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path1)
    
    # matplotlib plot for iterationsXsize
    plt.figure(figsize=(10, 5))
    plt.plot([result["Array Size"] for result in data], [max(result["BF Iterations"].values()) for result in data], label="Brute Force")
    plt.plot([result["Array Size"] for result in data], [max(result["DC Iterations"].values()) for result in data], label="Divide and Conquer")
    plt.plot([result["Array Size"] for result in data], [max(result["KD Iterations"].values()) for result in data], label="Kadane's Algorithm")
    plt.xlabel("Array Size")
    plt.ylabel("Maximum Iteration")
    plt.title("Maximum Iteration vs Array Size")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path2)

    return "Results plotted. For -> \"{}\" & \"{}\"".format(path1, path2)

def printResult(result) :

    if not result["Simulate Correct"] :
        print(colorama.Fore.RED + "\nSimulation failed. Results are not equal." + colorama.Fore.RESET)
    else :
        print(colorama.Fore.GREEN + "{:^240}".format("Simulation success. Results are equal.") + colorama.Fore.RESET)

    infoString1 = "The given array's size is {}. -> [{}, {}, {}, . . . {}]".format(str(result["Array Size"]), str(result["Test Array"][0]), str(result["Test Array"][1]), str(result["Test Array"][2]), str(result["Test Array"][-1]))
    infoString2 = "The maximum subarray is between the indices {} and {} with a sum of {}.".format(str(result["BF Start Index"]), str(result["BF End Index"]), str(result["BF Sum"]))

    tableString = "|{:^30}|{:^30}|{:^30}|{:^30}|{:^30}|{:^30}|{:^30}|{:^30}|".format("Algorithm", "Time Complexity", "SubArray Start Index", "SubArray End Index", "SubArray Sum", "Time Elapsed", "Iterations", "Maximum Iteration")

    resultString1 = "|{:^30}|{:^30}|{:^30}|{:^30}|{:^30}|{:^30}|{:^30}|{:^30}|".format("Brute Force", "O(n^2)", str(result["BF Start Index"]), str(result["BF End Index"]), str(result["BF Sum"]), str(result["BF Time"]), str(result["BF Iterations"]), str(max(result["BF Iterations"].values())))
    resultString2 = "|{:^30}|{:^30}|{:^30}|{:^30}|{:^30}|{:^30}|{:^30}|{:^30}|".format("Divide and Conquer", "O(nlogn)", str(result["DC Start Index"]), str(result["DC End Index"]), str(result["DC Sum"]), str(result["DC Time"]), str(result["DC Iterations"]), str(max(result["DC Iterations"].values())))
    resultString3 = "|{:^30}|{:^30}|{:^30}|{:^30}|{:^30}|{:^30}|{:^30}|{:^30}|".format("Kadane's Algorithm", "O(n)", str(result["KD Start Index"]), str(result["KD End Index"]), str(result["KD Sum"]), str(result["KD Time"]), str(result["KD Iterations"]), str(max(result["KD Iterations"].values())))

    maxLength = max(len(infoString1), len(infoString2), len(tableString), len(resultString1), len(resultString2), len(resultString3))

    tableParser = "-" * maxLength

    print(colorama.Fore.WHITE, tableParser, colorama.Fore.RESET)
    print(colorama.Fore.YELLOW, infoString1, colorama.Fore.RESET)
    print(colorama.Fore.YELLOW, infoString2, colorama.Fore.RESET)
    print(colorama.Fore.WHITE, tableParser, colorama.Fore.RESET)
    print(colorama.Fore.BLUE, tableString, colorama.Fore.RESET)
    print(colorama.Fore.WHITE, tableParser, colorama.Fore.RESET)
    print(colorama.Fore.GREEN, resultString1, colorama.Fore.RESET)
    print(colorama.Fore.GREEN, resultString2, colorama.Fore.RESET)
    print(colorama.Fore.GREEN, resultString3, colorama.Fore.RESET)
    print(colorama.Fore.WHITE, tableParser, colorama.Fore.RESET)

    print()


def main(N:int, continuously_generate:bool, save_to_file:bool, plot_results:bool) -> None :
    
    data = simulate(N, continuously_generate)

    feedback1 = saveToFile(data, "results.xlsx", save_to_file)
    feeedback2 = plotResults(data, "timeXsize_results.png", "iterationXsize_results.png", plot_results)

    print(feedback1)
    print(feeedback2)

    printResult(data[-1])

# Client Driver        
if __name__ == "__main__":

    safeStart()

    parser = argparse.ArgumentParser(description="This script is used to compare the performance of the brute force, divide and conquer and Kadane's algorithms.")
    parser.add_argument("-n", "--number-of-elements", type=int, help="The number of elements in the array.", required=False)
    parser.add_argument("-c", "--continuously-generate", type=int, help="If this flag is set, the script will generate test cases continuously from 1 to N.", required=False, default=False)
    parser.add_argument("-s", "--save-to-file", type=int, help="If this flag is set, the results will be saved to a file.", required=False, default=False)
    parser.add_argument("-p", "--plot-results", type=int, help="If this flag is set, the results will be plotted.", required=False, default=False)
    args = parser.parse_args()

    N                       = args.number_of_elements
    continuously_generate   = bool(args.continuously_generate)
    save_to_file            = bool(args.save_to_file)
    plot_results            = bool(args.plot_results)

    configPath = os.path.abspath(os.path.join("utils", "run_config.json"))
    if N == None :
        with open(configPath, "r") as configFile :
            config = json.load(configFile)
        N                       = config["N"]
        continuously_generate   = config["continuously_generate"]
        save_to_file            = config["save_to_file"]
        plot_results            = config["plot_results"]

    main(N, continuously_generate, save_to_file, plot_results)

    safeStop()