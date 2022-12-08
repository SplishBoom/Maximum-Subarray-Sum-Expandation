"""
@Script, that implements an simulation environment for algorithm analysis.

@Owns: "Emir Cetin Memis" & "Emircan Yaprak" & "Tuana Selen Ozhazday"
@Contiributors: "Emir Cetin Memis" & "Emircan Yaprak" & "Tuana Selen Ozhazday"

@Student_1:     "Emir Cetin Memis"    |   @Student_2:     "Emircan Yaprak"        |   @Student_3:     "Tuana Selen Ozhazday"
@StudentID_1:   041901027             |   @StudentID_2:   041901009               |   @StudentID_3:   041901024
@Contact_1:     "memise@mef.edu.tr"   |   @Contact_2:     "yaprakem@mef.edu.tr"   |   @Contact_3:     "ozhazdayt@mef.edu.tr"

@Set&Rights: "MEF University"
@Instructor: "Prof. Dr. Muhittin Gokmen"
@Course:     "Analysis of Algorithms"
@Req:        "Project 1"

@Since: 11/27/2022
"""

from    Constants           import  RUN_runConfigFilePath, DATA_dataOutputFolderPath, connect_pathes
from    Algorithms          import  ClassBF, ClassDC, ClassKD
from    Utilities           import  safeStart, safeStop
from    Utilities           import  generateTestArray
from    math                import  log2
import  matplotlib.pyplot   as plt
import  pandas              as pd
import  argparse
import  keyboard
import  colorama
import  timeit
import  json

def execute(N:int) -> dict :
    """
    Method that executes the algorithms for given array size @N.
    @params :
        N   - Required  : The size of the array (int)
    @return :
        results   -   The results of the simulation (dict)
    """

    expectedIterations = lambda N, type : (N*N if type=="BF" else (N*log2(N) if type=="DC" else N))
    
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
        "BF Expected Iterations" : expectedIterations(N, "BF"),

        "DC Start Index" : DCResult[0],
        "DC End Index" : DCResult[1],
        "DC Sum" : DCResult[2],
        "DC Time" : DCtime,
        "DC Iterations" : DCResult[3],
        "DC Expected Iterations" : expectedIterations(N, "DC"),

        "KD Start Index" : KDResult[0],
        "KD End Index" : KDResult[1],
        "KD Sum" : KDResult[2],
        "KD Time" : KDtime,
        "KD Iterations" : KDResult[3],
        "KD Expected Iterations" : expectedIterations(N, "KD"),
    }

    return results

def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iterable    - Required  : iterable object (Iterable)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()

def simulate(N:int, continuously_generate) :
    """
    Method that simulates the algorithms for given array size @N according to the @continuously_generate parameter.
    @params :
        N                       - Required  : The size of the array (int)
        continuously_generate   - Required  : If True, the program will generate arrays from 1 to size @N (bool)
    @return :
        data    -   The results of the simulation (list)
    """

    data = []

    if not continuously_generate :
        data.append(execute(N))
    else :
        print()
        iterable = [i for i in range(1, N+1)]
        for n in progressBar(iterable, prefix = 'Progress:', suffix = 'Complete', length = 50) : 
            data.append(execute(n))
            if keyboard.is_pressed("ESC") and keyboard.is_pressed("C") and keyboard.is_pressed("L") and keyboard.is_pressed("S") :
                print("User stopped generating test cases. Program will now continue by results.")
                break

    return data
    
def saveToFile(data, fileName, save_to_file:bool) -> str :
    """
    Method that saves all data into and xlsx file.
    @params :
        data            - Required  : data to be saved (List)
        fileName        - Required  : name of the file (Str)
        save_to_file    - Required  : if true then save to file (Bool)
    @return :
        filePath    - path of the file (Str)
    """

    if not save_to_file :
        return "User didn't want to save results to file. For -> \"{}\"".format(fileName)

    path = connect_pathes(DATA_dataOutputFolderPath, fileName)

    dataFrameColumns = ["Algorithm", "Array Size", "Time Complexity", "SubArray Start Index", "SubArray End Index", "SubArray Sum", "Time Elapsed (microseconds)", "Iteration List", "Maximum Iteration", "Expected Iteration"]

    dataFrame = pd.DataFrame(columns=dataFrameColumns)

    for result in data :
        dataFrame = pd.concat([dataFrame, pd.DataFrame([["Brute Force", result["Array Size"], "O(n^2)", result["BF Start Index"], result["BF End Index"], result["BF Sum"], result["BF Time"], result["BF Iterations"], max(result["BF Iterations"].values()), result["BF Expected Iterations"]]], columns=dataFrameColumns)])
        dataFrame = pd.concat([dataFrame, pd.DataFrame([["Divide and Conquer", result["Array Size"], "O(nlog(n))", result["DC Start Index"], result["DC End Index"], result["DC Sum"], result["DC Time"], result["DC Iterations"], max(result["DC Iterations"].values()), result["DC Expected Iterations"]]], columns=dataFrameColumns)])
        dataFrame = pd.concat([dataFrame, pd.DataFrame([["Kadane's Algorithm", result["Array Size"], "O(n)", result["KD Start Index"], result["KD End Index"], result["KD Sum"], result["KD Time"], result["KD Iterations"], max(result["KD Iterations"].values()), result["KD Expected Iterations"]]], columns=dataFrameColumns)])

    dataFrame.to_excel(path, index=False)

    return "Results saved to file. For -> \"{}\"".format(path)

def plotResults(data, fileName1, fileName2, plot_results:bool) -> str :
    """
    Method that uses matplotlib library to plot a given result's results.
    @params :
        data            - Required  : data to plot (List)
        fileName1       - Required  : name of the file to save the plot (Str)
        fileName2       - Required  : name of the file to save the plot (Str)
        plot_results    - Required  : if user wants to plot results (Bool)
    @returns :
        str             - message to user (Str) 
    """

    if not plot_results :
        return "User didn't want to plot results. For -> \"{}\" & \"{}\"".format(fileName1, fileName2)

    path1 = connect_pathes(DATA_dataOutputFolderPath, fileName1)
    path2 = connect_pathes(DATA_dataOutputFolderPath, fileName2)

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
    """
    Method that accepts and result dictionary, and prints it in a nice format.
    @params :
        result  - Required  : result dictionary (Dict)
    @returns :
        None
    """
    

    if not result["Simulate Correct"] :
        print(colorama.Fore.RED + "\nSimulation failed. Results are not equal." + colorama.Fore.RESET)
    else :
        print(colorama.Fore.GREEN + "{:^240}".format("Simulation success. Results are equal.") + colorama.Fore.RESET)

    infoString1 = "The given array's size is {}.]".format(str(result["Array Size"]))
    infoString2 = "The maximum subarray is between the indices {} and {} with a sum of {}.".format(str(result["BF Start Index"]), str(result["BF End Index"]), str(result["BF Sum"]))

    tableString = "|{:^20}|{:^17}|{:^22}|{:^20}|{:^14}|{:^26}|{:^42}|{:^19}|{:^20}|".format("Algorithm", "Time Complexity", "SubArray Start Index", "SubArray End Index", "SubArray Sum", "Time Elapsed", "Iterations", "Maximum Iteration", "Expected Iteration")

    resultString1 = "|{:^20}|{:^17}|{:^22}|{:^20}|{:^14}|{:^26}|{:^42}|{:^19}|{:^20}|".format("Brute Force", "O(n^2)", str(result["BF Start Index"]), str(result["BF End Index"]), str(result["BF Sum"]), str(result["BF Time"]), "HIDED", str(max(result["BF Iterations"].values())), str(result["BF Expected Iterations"]))
    resultString2 = "|{:^20}|{:^17}|{:^22}|{:^20}|{:^14}|{:^26}|{:^42}|{:^19}|{:^20}|".format("Divide and Conquer", "O(nlog(n))", str(result["DC Start Index"]), str(result["DC End Index"]), str(result["DC Sum"]), str(result["DC Time"]), "HIDED", str(max(result["DC Iterations"].values())), str(result["DC Expected Iterations"]))
    resultString3 = "|{:^20}|{:^17}|{:^22}|{:^20}|{:^14}|{:^26}|{:^42}|{:^19}|{:^20}|".format("Kadane's Algorithm", "O(n)", str(result["KD Start Index"]), str(result["KD End Index"]), str(result["KD Sum"]), str(result["KD Time"]), "HIDED", str(max(result["KD Iterations"].values())), str(result["KD Expected Iterations"]))

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
    """
    Main function of the program. It drives through the program according to gien parameters.
    @params :
        N                       - Required  : The size of the array (int)
        continuously_generate   - Required  : If True, the program will generate arrays from 1 to size @N (bool)
        save_to_file            - Required  : If True, the program will save the results to a file (bool)
        plot_results            - Required  : If True, the program will plot the results (bool)
    @return :
        None
    """


    data = simulate(N, continuously_generate)

    feedback1 = saveToFile(data, "results.xlsx", save_to_file)
    feeedback2 = plotResults(data, "timeXsize_results.png", "iterationXsize_results.png", plot_results)

    print(feedback1)
    print(feeedback2)

    printResult(data[-1])

# Client Driver        
if __name__ == "__main__":
    
    safeStart() # Read from Utilities/safeRun.py

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

    # To automatically start without passing arguments.
    if N == None :
        with open(RUN_runConfigFilePath, "r") as configFile :
            config = json.load(configFile)
        N                       = config["numberOfElements"]
        continuously_generate   = config["isContinuouslyGenerated"]
        save_to_file            = config["willSaveData"]
        plot_results            = config["willPlotData"]

    main(N, continuously_generate, save_to_file, plot_results) # Driver call

    safeStop() # Read from Utilities/safeRun.py
