"""
@Script, that implements an simulation environment for algorithm analysis.

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

from    Constants               import  RUN_runConfigFilePath, GUI_backgroundPhotoPath, GUI_loaderGifPath, GUI_settingsButtonPhotoPath, GUI_welcomePhotoPath, DATA_dataOutputFolderPath, connect_pathes
from    matplotlib.backends.backend_tkagg   import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from    matplotlib.figure       import Figure
from    Algorithms              import  ClassBF, ClassDC, ClassKD
from    Utilities               import  safeStart, safeStop
from    Utilities               import  generateTestArray
from    PIL                     import  Image, ImageTk
from    tkinter                 import  PhotoImage
from    math                    import  log2
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

class GUI(tk.Tk) :
    """
    Class that implements GUI for the simulation environment.
    @dialog:
        - This class includes lots of essential methods, functions, types and etc. Moreover, it is constructed by the "main.py" script. All of the execution from is same as the "main.py" script except the Graphical User Interface.
    @features :
        -   GUI for the simulation environment.
        -   Button controls.
        -   Progress tracking.
        -   Global managining.
        -   Global flow control.
        -   Global helper methods.
    @methods :
        -   __init__ : Constructor.
        -   screenShot : Takes a screenshot of the current screen.
        -   _exit : Exits the application.
        -   _start : Starts the simulation.
        -   _restart : Restarts the simulation.
        -   initialize : Initializes the simulation variables.
        -   renew : Renews the simulation canvas.
        -   updateFrames : Updates the simulation frames.
        -   switchToExperiment : Switches to experiment mode.
        -   initializeExperiment : Initializes the experiment variables.
        -   simulate : Simulates the experiment as mentoined in "main.py".
        -   updateVariables : An refresh method for the configration file.
    @non_side-methods :
        -   showGif : Shows the loader gif in a multithreaded way.
        -   settings.__init__ : Constructor and the driver of the settings scheme.
        -   timeFormat : Formats the time as it needed in output.
        -   progressBar : Prints the progress bar.
        -   execute : Executes the simulation.
        -   dataDisplayer : Displays the data in a multithreaded way in a canvas with manual drawings.
        -   plotResults : Plots the results.
        -   saveResults : Saves the results.
    """

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

        x = self.winfo_rootx()
        y = self.winfo_rooty()
        x1 = x + self.winfo_width()
        y1 = y + self.winfo_height()
        im = grab(bbox=(x, y, x1, y1))
        im.save(path)

        return path

    def _exit(self, *kwargs) :

        self.update()

        if self.frameMode == "Experiment" :
            path = self.screenShot((self.experimentID.get() or "NO INFO") + " EXIT SHOT")

            print("\nExiting...")
            print("Last screen shot of the program is saved in the \"Data Export\" folder.")
            print("SAVED | \"{}\"".format(path))

        safeStop()

    def _restart(self, *kwargs) :

        self.update()
        
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
    """
    Class that implements GUI for the simulation environment.
    @dialog:
        - This class is used for login scheme of the GUI.
    """

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
    """
    Class that implements GUI for the simulation environment.
    @dialog:
        - This class is used for settings scheme of the GUI.
    """

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
    """
    Class that implements GUI for the simulation environment.
    @dialog:
        - This class is used for experiment scheme of the GUI.
    """

    def __init__(self, root, parent, *args, **kwargs) :
        super().__init__(parent, *args, **kwargs)

        self.root = root
        self.parent = parent

        self.style = ttk.Style()
        self.style.configure("TButton", foreground="#f302e7", background="black", font=("Robotic", 18, "bold"), justify="center", anchor="center", relief="flat", borderwidth=10, highlightthickness=1, highlightbackground="black", highlightcolor="black")

        self.restartButton = ttk.Button(self.parent, text="Restart", command=self.root._restart, style="TButton")
        self.plotResultsButton = ttk.Button(self.parent, text="Plot Results", command=self.plotResults, style="TButton")
        self.saveResultsButton = ttk.Button(self.parent, text="Save Results", command=self.saveResults, style="TButton")
        self.exitButton = ttk.Button(self.parent, text="Exit", command=self.root._exit, style="TButton")

        self.restartButton.place(relx=0.17, rely=0.940, anchor="center", width=200, height=50)
        self.plotResultsButton.place(relx=0.39, rely=0.945, anchor="center", width=200, height=50)
        self.saveResultsButton.place(relx=0.61, rely=0.945, anchor="center", width=200, height=50)
        self.exitButton.place(relx=0.83, rely=0.945, anchor="center", width=200, height=50)

        self.dataDisplayer("start")

        if self.root.willPlotData.get() :
            self.plotResults()

        if self.root.willSaveData.get() :
            self.saveResults()

    def time_format(self, x):
            
        # miliseconds to dd:hh:mm:ss:ms:us

        days, time = divmod(x, 86400000)
        hours, time = divmod(time, 3600000)
        minutes, time = divmod(time, 60000)
        seconds, time = divmod(time, 1000)
        miliseconds, time = divmod(time, 1)
        microseconds, time = divmod(time, 0.001)

        minutes = str(int(minutes)).zfill(2)
        seconds = str(int(seconds)).zfill(2)
        miliseconds = str(int(miliseconds)).zfill(2)
        microseconds = str(int(microseconds)).zfill(2)

        string = minutes + ":" + seconds + ":" + miliseconds + ":" + microseconds

        return string

    def dataDisplayer(self, state) :
        
        if state == "start" :
            x = 990
            y = 550

            self.canvas = tk.Canvas(self.parent, width=x, height=y, bg="black", bd=0, highlightthickness=0, relief="ridge", border=1, borderwidth=10)
            self.canvas.place(relx=0.5, rely=0.5, anchor="center")

            result = self.root.data[-1]

            arraySize = result["Array Size"]
            testArray = result["Test Array"]
            simulateCorrect = result["Simulate Correct"]
            
            BFStartIndex = result["BF Start Index"]
            BFEndIndex = result["BF End Index"]
            BFSum = result["BF Sum"]
            BFTime = result["BF Time"]
            BFIterations = result["BF Iterations"]
            BFExpectedIterations = result["BF Expected Iterations"]

            DCStartIndex = result["DC Start Index"]
            DCEndIndex = result["DC End Index"]
            DCSum = result["DC Sum"]
            DCTime = result["DC Time"]
            DCIterations = result["DC Iterations"]
            DCExpectedIterations = result["DC Expected Iterations"]

            KDStartIndex = result["KD Start Index"]
            KDEndIndex = result["KD End Index"]
            KDSum = result["KD Sum"]
            KDTime = result["KD Time"]
            KDIterations = result["KD Iterations"]
            KDExpectedIterations = result["KD Expected Iterations"]

            if simulateCorrect :
                _use = ("Simulation is verified, results matched !", "lime green")
                _clr = "lime green"
            else :
                _use = ("Simulation is not verified, results not matched !", "red")
                _clr = "red"

            self.canvas.create_text(500, 35, text=_use[0], font=("Robotic", 14, "bold"), fill=_use[1])
            
            # add an gray line
            self.canvas.create_line(0, 62, 1000, 62, fill="gray", width=2)

            _use = (("Robotic", 13, "bold"), "yellow")
            self.canvas.create_text(500, 86, text="The given array's size is \"{}\", the array is randomly generated in [-100, 100]" .format(arraySize), font=_use[0], fill=_use[1])
            self.canvas.create_text(500, 116, text="The maximum subarray is between the indices \"{}\" and \"{}\", with a sum of {}".format(BFStartIndex, BFEndIndex, BFSum), font=_use[0], fill=_use[1])

            self.canvas.create_line(0, 140, 1000, 140, fill="gray", width=2)
            self.canvas.create_line(66, 150, 993, 150, fill="alice blue", width=2)

            _use = (("Robotic", 12, "bold"), "aqua")
            x_shifter = 20
            self.canvas.create_text(100+x_shifter, 180, text="Algorithm", font=_use[0], fill=_use[1])
            self.canvas.create_text(220+x_shifter, 180, text="Complexity", font=_use[0], fill=_use[1])
            self.canvas.create_text(365+x_shifter, 180, text="SubArray Index", font=_use[0], fill=_use[1])
            self.canvas.create_text(525+x_shifter, 180, text="SubArray Sum", font=_use[0], fill=_use[1])
            self.canvas.create_text(685+x_shifter, 169, text="Execution Time", font=_use[0], fill=_use[1])
            self.canvas.create_text(870+x_shifter, 180, text="Execution Iterations", font=_use[0], fill=_use[1])

            self.canvas.create_text(685+x_shifter, 190, text="(mm:ss:ms:us)", font=("Robotic", 10, "bold"), fill="cyan")

            self.canvas.create_line(66, 210, 993, 210, fill="alice blue", width=2)

            # vertical lines
            self.canvas.create_line(46+x_shifter, 150, 46+x_shifter, 550, fill="alice blue", width=2)
            self.canvas.create_line(157+x_shifter, 150, 157+x_shifter, 550, fill="alice blue", width=2)
            self.canvas.create_line(283+x_shifter, 150, 283+x_shifter, 550, fill="alice blue", width=2)
            self.canvas.create_line(449+x_shifter, 150, 449+x_shifter, 550, fill="alice blue", width=2)
            self.canvas.create_line(604+x_shifter, 150, 604+x_shifter, 550, fill="alice blue", width=2)
            self.canvas.create_line(767+x_shifter, 150, 767+x_shifter, 550, fill="alice blue", width=2)
            self.canvas.create_line(973+x_shifter, 150, 973+x_shifter, 550, fill="alice blue", width=2)
            self.canvas.create_line(46+x_shifter, 550, 973+x_shifter, 550, fill="alice blue", width=2)

            self.canvas.create_line(66, 210+1*113.333, 993, 210+1*113.333, fill="alice blue", width=2)
            self.canvas.create_line(66, 210+2*113.333, 993, 210+2*113.333, fill="alice blue", width=2)

            # table elements
            _use = (("Robotic", 11, "bold"), "alice blue")
            self.canvas.create_text(101+x_shifter, 210+0.5*113.333, text="Brute Force", font=_use[0], fill=_use[1])
            self.canvas.create_text(101+x_shifter, 210+1.5*113.333, text="Divide\n&\nConquer", font=_use[0], fill=_use[1], justify="center")
            self.canvas.create_text(101+x_shifter, 210+2.5*113.333, text="Kadane", font=_use[0], fill=_use[1], justify="center")

            self.canvas.create_text(220+x_shifter, 210+0.5*113.333, text="O(n^2)", font=_use[0], fill=_use[1])
            self.canvas.create_text(220+x_shifter, 210+1.5*113.333, text="O(n log n)", font=_use[0], fill=_use[1])
            self.canvas.create_text(220+x_shifter, 210+2.5*113.333, text="O(n)", font=_use[0], fill=_use[1])

            self.canvas.create_text(365+x_shifter, 210+0.5*113.333, text="\"{}\" > \"{}\"".format(BFStartIndex, BFEndIndex), font=_use[0], fill=_use[1])
            self.canvas.create_text(365+x_shifter, 210+1.5*113.333, text="\"{}\" > \"{}\"".format(DCStartIndex, DCEndIndex), font=_use[0], fill=_use[1])
            self.canvas.create_text(365+x_shifter, 210+2.5*113.333, text="\"{}\" > \"{}\"".format(KDStartIndex, KDEndIndex), font=_use[0], fill=_use[1])

            self.canvas.create_text(525+x_shifter, 210+0.5*113.333, text="\"{}\"".format(BFSum), font=_use[0], fill=_use[1])
            self.canvas.create_text(525+x_shifter, 210+1.5*113.333, text="\"{}\"".format(DCSum), font=_use[0], fill=_use[1])
            self.canvas.create_text(525+x_shifter, 210+2.5*113.333, text="\"{}\"".format(KDSum), font=_use[0], fill=_use[1])

            self.canvas.create_text(685+x_shifter, 210+0.5*113.333, text="{}".format(self.time_format(BFTime)), font=_use[0], fill=_use[1])
            self.canvas.create_text(685+x_shifter, 210+1.5*113.333, text="{}".format(self.time_format(DCTime)), font=_use[0], fill=_use[1])
            self.canvas.create_text(685+x_shifter, 210+2.5*113.333, text="{}".format(self.time_format(KDTime)), font=_use[0], fill=_use[1])

            # for now, iterationCount = 10, expectedIteration = 10
            iterationCount = 10
            expectedIteration = 10
            self.canvas.create_text(870+x_shifter, 210+0.5*113.333, text="Iteration Count\n{}\nExpected Count\n{}".format(max(result["BF Iterations"].values()), result["BF Expected Iterations"]), font=_use[0], fill=_use[1], justify="center")
            self.canvas.create_text(870+x_shifter, 210+1.5*113.333, text="Iteration Count\n{}\nExpected Count\n{}".format(max(result["DC Iterations"].values()), result["DC Expected Iterations"]), font=_use[0], fill=_use[1], justify="center")
            self.canvas.create_text(870+x_shifter, 210+2.5*113.333, text="Iteration Count\n{}\nExpected Count\n{}".format(max(result["KD Iterations"].values()), result["KD Expected Iterations"]), font=_use[0], fill=_use[1], justify="center")

            _use = (("Consolas", 13, "bold"), _clr)
            self.canvas.create_text(35, 35, text=">>>", font=_use[0], fill=_use[1])
            self.canvas.create_text(35, 86, text=">>>", font=_use[0], fill=_use[1])
            self.canvas.create_text(35, 116, text=">>>", font=_use[0], fill=_use[1])
            self.canvas.create_text(35, 176, text=">>>", font=_use[0], fill=_use[1])
            self.canvas.create_text(35, 266, text=">>>", font=_use[0], fill=_use[1])
            self.canvas.create_text(35, 386, text=">>>", font=_use[0], fill=_use[1])
            self.canvas.create_text(35, 493.3325, text=">>>", font=_use[0], fill=_use[1])

            fileN = (self.root.experimentID.get() or "NO INFO") + " CANVAS"
            self.root.screenShot(fileN)

        else :
            self.canvas.destroy()

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

        self.dataDisplayer("finish")

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

# Driver
if __name__ == "__main__" :
    
    safeStart()
    
    while True :
    
        app = GUI()
        app.mainloop()