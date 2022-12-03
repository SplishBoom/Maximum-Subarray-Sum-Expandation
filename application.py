from    Constants               import  RUN_runConfigFilePath, GUI_backgroundPhotoPath, GUI_loaderGifPath, GUI_settingsButtonPhotoPath, GUI_welcomePhotoPath, DATA_dataOutputFolderPath, connect_pathes
from    matplotlib.backends.backend_tkagg   import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from    matplotlib.figure       import Figure
from    Algorithms              import  ClassBF, ClassDC, ClassKD
from    Utilities               import  safeStart, safeStop
from    Utilities               import  generateTestArray
from    PIL                     import  Image, ImageTk
from    tkinter                 import  PhotoImage
from    math                    import  log10
from    pyscreenshot            import  grab
from    tkinter                 import  ttk
import  tkinter                 as      tk
import  pandas                  as      pd
import  matplotlib
import  threading
import  keyboard
import  timeit
import  json

matplotlib.use("TkAgg")

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

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

def execute(N:int) -> dict :

    expectedIterations = lambda N, type : (N*N if type=="BF" else (N*log10(N) if type=="DC" else N))
    
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

class GUI(tk.Tk) :

    _Width = 600
    _Height = 400

    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)

        print("█" * 100)
        print("\nGUI Running...\nWelcome to the experiment!")

        self.title("Maximum Subarray Problem")

        self.data = None

        self.experimentID = tk.StringVar(value=None)

        self.initialize()

        self.configure(background = 'black')
        self.geometry("{}x{}".format(self._Width, self._Height))
        w = self.winfo_screenwidth();h = self.winfo_screenheight();x = (self.winfo_screenwidth()/2) - (self.winfo_reqwidth()/2);y = (self.winfo_screenheight()/2) - (self.winfo_reqheight()/2);self.geometry('+%d+%d' % (x/1.30, y/1.30))
        self.resizable(False, False)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.switchFrame = tk.BooleanVar(value=False)
    
        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, sticky="nsew")
        
        self.frameMode = "Settings"
        self.currentFrame = Settings(self, self.container)
        self.currentFrame.grid(row=0, column=0, sticky="nsew")

        self.backgroundImage = ImageTk.PhotoImage(Image.open(GUI_backgroundPhotoPath).resize((self._Width, self._Height), Image.Resampling.LANCZOS))
        self.lbl = tk.Label(self.container, image=self.backgroundImage)
        self.lbl.place(relx=0.5, rely=0.5, anchor='center')

        settingImage = ImageTk.PhotoImage(Image.open(GUI_settingsButtonPhotoPath).resize((int(self._Height/10), int(self._Height/10))));self.settingsImage = settingImage
        self.settingsButton = tk.Button(self.container ,image=settingImage, command=self.updateFrames, compound=tk.TOP, bg="black", fg="white", activebackground="black", activeforeground="white")
        self.settingsButton.place(relx=0.875, rely=0.10, anchor="center")

        self.updateFrames()

        self.bind("<Return>", self.initializeExperiment)

        self.protocol("WM_DELETE_WINDOW", self._exit)

    def screenShot(self, filename) :

        path = connect_pathes(DATA_dataOutputFolderPath, filename+".png")

        self.update()

        x = self.winfo_rootx()
        y = self.winfo_rooty()
        x1 = x + self.winfo_width()
        y1 = y + self.winfo_height()
        im = grab(bbox=(x, y, x1, y1))
        im.save(path)

        return path

    def _exit(self, *kwargs) :

        if self.frameMode == "Experiment" :
            path = self.screenShot("END SCREENSHOT")

            print("\nExiting...")
            print("Last screen shot of the program is saved in the \"Data Export\" folder.")
            print("SAVED | \"{}\"".format(path))

        safeStop()

    def _restart(self, *kwargs) :
        
        print("Last screen shot of the program is saved in the \"Data Export\" folder.")
        
        path = self.screenShot("RESTARTED SCREENSHOT")
        print("SAVED | \"{}\"".format(path))
        
        self.destroy()

    def initialize(self) :
        try :
            with open (RUN_runConfigFilePath, "r") as infile:
                configFile = json.load(infile)
            settings = (configFile["numberOfElements"], configFile["isContinuouslyGenerated"], configFile["willSaveData"], configFile["willPlotData"])
        except :
            fixData = {
                "numberOfElements" : 10,
                "isContinuouslyGenerated" : False,
                "willSaveData" : True,
                "willPlotData" : True
            }
            with open(RUN_runConfigFilePath, "w") as f:
                json.dump(fixData, f, sort_keys=True, indent=4)
            with open (RUN_runConfigFilePath, "r") as infile:
                configFile = json.load(infile)
            settings = (configFile["numberOfElements"], configFile["isContinuouslyGenerated"], configFile["willSaveData"], configFile["willPlotData"])

        self.numberOfElements = tk.IntVar(value=settings[0])
        self.isContinuouslyGenerated = tk.BooleanVar(value=settings[1])
        self.willSaveData = tk.BooleanVar(value=settings[2])
        self.willPlotData = tk.BooleanVar(value=settings[3])

    def renew(self) :

        try :
            self.container.destroy()
        except :
            pass

        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, sticky="nsew")

        backgroundImage = ImageTk.PhotoImage(Image.open(GUI_backgroundPhotoPath).resize((self._Width, self._Height), Image.Resampling.LANCZOS));lbl = tk.Label(self.container, image=backgroundImage);lbl.backgroundImage = backgroundImage;lbl.place(relx=0.5, rely=0.5, anchor='center')

        settingImage = ImageTk.PhotoImage(Image.open(GUI_settingsButtonPhotoPath).resize((int(self._Height/10), int(self._Height/10))));self.settingsImage = settingImage
        self.settingsButton = tk.Button(self.container ,image=settingImage, command=self.updateFrames, compound=tk.TOP, bg="black", fg="white", activebackground="black", activeforeground="white")
        self.settingsButton.place(relx=0.875, rely=0.205, anchor="center")    

    def updateFrames(self, *args) :
        self.renew()
        if self.frameMode == "Settings" :
            self.frameMode = "MainMenu"
            self.currentFrame.destroy()
            self.currentFrame = MainMenu(self, self.container)
            self.currentFrame.grid(row=0, column=0, sticky="nsew")
        else :
            self.frameMode = "Settings"
            self.currentFrame.destroy()
            self.currentFrame = Settings(self, self.container)
            self.currentFrame.grid(row=0, column=0, sticky="nsew")

    def switchToExperiment(self, *args) :
        
        try :
            self.container.destroy()
        except :
            pass

        self.configure(background = 'black')
        self.geometry("{}x{}".format(2*self._Width, 2*self._Height))
        w = self.winfo_screenwidth();h = self.winfo_screenheight();x = (self.winfo_screenwidth()/2) - (self.winfo_reqwidth()/2);y = (self.winfo_screenheight()/2) - (self.winfo_reqheight()/2);self.geometry('+%d+%d' % (x/1.90, y/2.40))

        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, sticky="nsew")

        self.lbl.forget()
        self.backgroundImage = ImageTk.PhotoImage(Image.open(GUI_backgroundPhotoPath).resize((2*self._Width, 2*self._Height), Image.Resampling.LANCZOS))
        self.lbl = tk.Label(self.container, image=self.backgroundImage)
        self.lbl.place(relx=0.5, rely=0.5, anchor='center')

        self.frameMode = "Experiment"
        self.currentFrame.destroy()
        self.currentFrame = Experiment(self, self.container)
        self.currentFrame.grid(row=0, column=0, sticky="nsew")

    def initializeExperiment(self, *args) :

        if self.frameMode != "MainMenu" :
            return

        print("\nExperiment █ \"{}\" █ is starting with the following settings :".format(self.experimentID.get().upper()))
        print("Number of elements : {}".format(self.numberOfElements.get()))
        print("Is continuously generated : {}".format(self.isContinuouslyGenerated.get()))
        print("Auto save data : {}".format(self.willSaveData.get()))
        print("Auto plot data : {}".format(self.willPlotData.get()))

        self.settingsButton.config(state="disabled")

        self.updateVariables()
        
        self.after(0, self.currentFrame.showGif, 0)

        thread = threading.Thread(target=self.simulate, args=(self.numberOfElements.get(), self.isContinuouslyGenerated.get()))
        thread.start()
        
    def simulate(self, N:int, continuously_generate, *args) :

        self.data = []

        if not continuously_generate :
            self.data.append(execute(N))
        else :
            print()
            iterable = [i for i in range(1, N+1)]
            for n in progressBar(iterable, prefix = 'Progress:', suffix = 'Complete', length = 50) : 
                self.data.append(execute(n))
                if keyboard.is_pressed("ESC") and keyboard.is_pressed("C") and keyboard.is_pressed("L") and keyboard.is_pressed("S") :
                    print("User stopped generating test cases. Program will now continue by results.")
                    break

        self.currentFrame.isDone = True

        self.switchToExperiment()

    def updateVariables(self) :
        
        with open (RUN_runConfigFilePath, "r") as jsonFile :
            settingsData = json.load(jsonFile)
        
        settingsData["numberOfElements"] = self.numberOfElements.get()
        settingsData["isContinuouslyGenerated"] = self.isContinuouslyGenerated.get()
        settingsData["willSaveData"] = self.willSaveData.get()
        settingsData["willPlotData"] = self.willPlotData.get()
        
        json_output = json.dumps(settingsData, indent=4, sort_keys=True)
        with open (RUN_runConfigFilePath, "w") as jsonFile :
            jsonFile.write(json_output)

class MainMenu(ttk.Frame) :
    
    def __init__(self, root, parent, *args, **kwargs) :
        super().__init__(parent, *args, **kwargs)

        style = ttk.Style()

        self.isDone = False
        self.root = root

        style.configure("TEntry", foreground="black", background="black", font=("Helvetica", int(root._Height/20)))

        backgroundImage = ImageTk.PhotoImage(Image.open(GUI_welcomePhotoPath).resize((250,75), Image.Resampling.LANCZOS))
        lbl = tk.Label(parent, image=backgroundImage)
        lbl.backgroundImage = backgroundImage
        lbl.place(relx=0.5, rely=0.27, anchor='center')

        experimentIDEntry = tk.Entry(parent, width=10, font=("Helvetica", 32), justify="center", textvariable=root.experimentID)
        experimentIDEntry.place(relx=0.5, rely=0.73, anchor="center", width=350, height=75)
        experimentIDEntry.focus_set()

        self.gifFrames = [PhotoImage(file=GUI_loaderGifPath, format = 'gif -index %i' %(i)) for i in range(150)]
        self.gifLabel = tk.Label(parent, image=self.gifFrames[0])

    def showGif(self, frameIndex) :

        if self.isDone :
            return

        self.currentFrame = self.gifFrames[frameIndex]
        frameIndex += 1

        if frameIndex == 1 :
            self.gifLabel.configure(image=self.currentFrame)
            self.gifLabel.place(relx=0.5, rely=0.5, anchor="center")
        elif frameIndex == 150 :
            frameIndex = 0

        self.gifLabel.configure(image=self.currentFrame)

        self.root.after(10, self.showGif, frameIndex)

class Settings(ttk.Frame) :
    
    def __init__(self, root, parent, *args, **kwargs) :
        super().__init__(parent, *args, **kwargs)

        self.root = root

        style = ttk.Style()

        style.configure("TLabel", foreground="#f302e7", background="white")
        style.configure("TCheckbutton", background="white", foreground="white", activebackground="black", activeforeground="white", selectcolor="black")

        padx = 0.2
        padv = 0.015

        style = ttk.Style()
        style.configure("TCheckbutton", background="pink", foreground="white", activebackground="black", activeforeground="white", selectcolor="black", font=50, justify="center", anchor="center")

        numberOfElementsLabel = ttk.Label(parent, text=" Number of elements ", font=("Helvetica", 13), background="light blue", foreground="black")
        numberOfElementsSpin = tk.Spinbox(parent, from_=1, to=1000000, textvariable=root.numberOfElements, width=20, command=root.updateVariables, font=("Helvetica", 14, "bold"), justify="center", bg="pink", fg="black")

        isContinuouslyGeneratedLabel = ttk.Label(parent, text=" Continuously Generate ", font=("Helvetica", 13), background="light blue", foreground="black")
        isContinuouslyGeneratedCheckButton = ttk.Checkbutton(parent, variable=root.isContinuouslyGenerated, onvalue=True, offvalue=False, command=root.updateVariables)

        willSaveDataLabel = ttk.Label(parent, text=" Save Data ", font=("Helvetica", 13), background="light blue", foreground="black")
        willSaveDataCheckButton = ttk.Checkbutton(parent, variable=root.willSaveData, onvalue=True, offvalue=False, command=root.updateVariables)

        willPlotDataLabel = ttk.Label(parent, text=" Plot Data ", font=("Helvetica", 13), background="light blue", foreground="black")
        willPlotDataCheckButton = ttk.Checkbutton(parent, variable=root.willPlotData, onvalue=True, offvalue=False, command=root.updateVariables)

        yrelyStart = 0.100
        yrelyEnhancement = 0.16

        i = 1
        numberOfElementsLabel.place(relx=0.265+padv, rely=yrelyStart+yrelyEnhancement*i, anchor="center")
        numberOfElementsSpin.place(relx=0.475+padx, rely=yrelyStart+yrelyEnhancement*i, anchor="center", height=30, width=150)
        i += 1
        isContinuouslyGeneratedLabel.place(relx=0.265+padv, rely=yrelyStart+yrelyEnhancement*i, anchor="center")
        isContinuouslyGeneratedCheckButton.place(relx=0.475+padx, rely=yrelyStart+yrelyEnhancement*i, anchor="center", height=22, width=40)
        i += 1
        willSaveDataLabel.place(relx=0.265+padv, rely=yrelyStart+yrelyEnhancement*i, anchor="center")
        willSaveDataCheckButton.place(relx=0.475+padx, rely=yrelyStart+yrelyEnhancement*i, anchor="center", height=22, width=40)
        i += 1
        willPlotDataLabel.place(relx=0.265+padv, rely=yrelyStart+yrelyEnhancement*i, anchor="center")
        willPlotDataCheckButton.place(relx=0.475+padx, rely=yrelyStart+yrelyEnhancement*i, anchor="center", height=22, width=40)

class Experiment(ttk.Frame) :

    def __init__(self, root, parent, *args, **kwargs) :
        super().__init__(parent, *args, **kwargs)

        self.root = root

        self.style = ttk.Style()
        self.style.configure("TButton", foreground="#f302e7", background="black", font=("Robotic", 18, "bold"), justify="center", anchor="center", relief="flat", borderwidth=10, highlightthickness=1, highlightbackground="black", highlightcolor="black")


        self.restartButton = ttk.Button(parent, text="Restart", command=self.root._restart, style="TButton")
        self.plotResultsButton = ttk.Button(parent, text="Plot Results", command=self.plotResults, style="TButton")
        self.saveResultsButton = ttk.Button(parent, text="Save Results", command=self.saveResults, style="TButton")
        self.exitButton = ttk.Button(parent, text="Exit", command=self.root._exit, style="TButton")

        self.restartButton.place(relx=0.17, rely=0.940, anchor="center", width=200, height=50)
        self.plotResultsButton.place(relx=0.39, rely=0.945, anchor="center", width=200, height=50)
        self.saveResultsButton.place(relx=0.61, rely=0.945, anchor="center", width=200, height=50)
        self.exitButton.place(relx=0.83, rely=0.945, anchor="center", width=200, height=50)

        if self.root.willPlotData.get() :
            self.plotResults()

        if self.root.willSaveData.get() :
            self.saveResults()

    def _saveScreenShot(self) :
        
        pass

    def plotResults(self, *args) :

        path1 = connect_pathes(DATA_dataOutputFolderPath, (self.root.experimentID.get() or "NO INFO") + " TIME.png" )
        path2 = connect_pathes(DATA_dataOutputFolderPath, (self.root.experimentID.get() or "NO INFO") + " ITER.png")
        
        data = self.root.data

        size = (6, 4)   # you will be slapped by me if you change this. -ECM
        ddpi = 75       # you will be slapped by me if you change this. -ECM

        timeFigure = Figure(figsize=size, dpi=ddpi)
        timeFigureCanvas = FigureCanvasTkAgg(figure=timeFigure, master=self, )
        NavigationToolbar2Tk(timeFigureCanvas, self)
        axes = timeFigure.add_subplot(111)
        axes.plot([result["Array Size"] for result in data], [result["BF Time"] for result in data], label="Brute Force")
        axes.plot([result["Array Size"] for result in data], [result["DC Time"] for result in data], label="Divide and Conquer")
        axes.plot([result["Array Size"] for result in data], [result["KD Time"] for result in data], label="Kadane's Algorithm")
        axes.set_xlabel("Array Size")
        axes.set_ylabel("Time Elapsed (microseconds)")
        axes.set_title("Time Elapsed (microseconds) vs Array Size")
        axes.legend()
        timeFigureCanvas.draw()
        time_canvas = timeFigureCanvas.get_tk_widget()

        iterFigure = Figure(figsize=size, dpi=ddpi)
        iterFigureCanvas = FigureCanvasTkAgg(figure=iterFigure, master=self)
        NavigationToolbar2Tk(iterFigureCanvas, self)
        axes = iterFigure.add_subplot(111)
        axes.plot([result["Array Size"] for result in data], [max(result["BF Iterations"].values()) for result in data], label="Brute Force")
        axes.plot([result["Array Size"] for result in data], [max(result["DC Iterations"].values()) for result in data], label="Divide and Conquer")
        axes.plot([result["Array Size"] for result in data], [max(result["KD Iterations"].values()) for result in data], label="Kadane's Algorithm")
        axes.set_xlabel("Array Size")
        axes.set_ylabel("Iterations")
        axes.set_title("Iterations vs Array Size")
        axes.legend()
        iterFigureCanvas.draw()
        iter_canvas = iterFigureCanvas.get_tk_widget()
        
        self.gridButtonsForPlot()

        time_canvas.pack(side="left", fill="both", expand=True, anchor="center", padx=19,  pady=50, ipady=51)
        iter_canvas.pack(side="right", fill="both", expand=True, anchor="center", padx=19, pady=50, ipady=51)

        timeFigure.savefig(path1)
        iterFigure.savefig(path2)

        self.plotResultsButton.configure(text="Plotted", style="TButton")
        self.plotResultsButton["state"] = "disabled"

        print("\nResults are plotted. You can find them in the \"Data Export\" folder.")
        print("SAVED | TIME.png -> Time Elapsed (microseconds) vs Array Size -> \"{}\"".format(path1))
        print("SAVED | ITER.png -> Iterations vs Array Size -> \"{}\"".format(path2))

    def saveResults(self, *args) :
        
        path = connect_pathes(DATA_dataOutputFolderPath, (self.root.experimentID.get() or "NO INFO") + " RESULTS.xlsx")

        data = self.root.data

        dataFrameColumns = ["Algorithm", "Array Size", "Time Complexity", "SubArray Start Index", "SubArray End Index", "SubArray Sum", "Time Elapsed (microseconds)", "Iteration List", "Maximum Iteration", "Expected Iteration"]

        dataFrame = pd.DataFrame(columns=dataFrameColumns)

        for result in data :
            dataFrame = pd.concat([dataFrame, pd.DataFrame([["Brute Force", result["Array Size"], "O(n^2)", result["BF Start Index"], result["BF End Index"], result["BF Sum"], result["BF Time"], result["BF Iterations"], max(result["BF Iterations"].values()), result["BF Expected Iterations"]]], columns=dataFrameColumns)])
            dataFrame = pd.concat([dataFrame, pd.DataFrame([["Divide and Conquer", result["Array Size"], "O(nlog(n))", result["DC Start Index"], result["DC End Index"], result["DC Sum"], result["DC Time"], result["DC Iterations"], max(result["DC Iterations"].values()), result["DC Expected Iterations"]]], columns=dataFrameColumns)])
            dataFrame = pd.concat([dataFrame, pd.DataFrame([["Kadane's Algorithm", result["Array Size"], "O(n)", result["KD Start Index"], result["KD End Index"], result["KD Sum"], result["KD Time"], result["KD Iterations"], max(result["KD Iterations"].values()), result["KD Expected Iterations"]]], columns=dataFrameColumns)])

        dataFrame.to_excel(path, index=False)

        self.saveResultsButton.configure(text="Saved", style="TButton")
        self.saveResultsButton.configure(state="disabled")

        print("\nResults are saved. You can find them in the \"Data Export\" folder.")
        print("SAVED | \"RESULTS.xlsx\" ->", path)

    def gridButtonsForPlot(self) :

        self.restartButton.place_forget()
        self.plotResultsButton.place_forget()
        self.saveResultsButton.place_forget()
        self.exitButton.place_forget()

        self.restartButton.place(relx=0.32, rely=0.940, anchor="center", width=120, height=50)
        self.plotResultsButton.place(relx=0.47, rely=0.940, anchor="center", width=200, height=50)
        self.saveResultsButton.place(relx=0.655, rely=0.940, anchor="center", width=200, height=50)
        self.exitButton.place(relx=0.805, rely=0.940, anchor="center", width=120, height=50)

        self.style.configure("TButton", foreground="black", background="black", font=("Robotic", 18, "bold"), justify="center", anchor="center", relief="flat", borderwidth=10, highlightthickness=1, highlightbackground="black", highlightcolor="black")

if __name__ == "__main__" :
    
    safeStart()
    
    while True :
    
        app = GUI()
        app.mainloop()