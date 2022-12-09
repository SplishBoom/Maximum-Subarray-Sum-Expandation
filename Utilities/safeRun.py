"""
This script controlls the execution flow's end and start chraacteristics.
"""

import os
import json
import shutil

from Constants import DATA_dataOutputFolderPath, RUN_runConfigFilePath

def safeStart() :
    
    preEsitingCheckList = [DATA_dataOutputFolderPath, RUN_runConfigFilePath]

    for path in preEsitingCheckList :
        if not os.path.exists(path) :
            if os.path.splitext(path)[1] == "" :
                os.mkdir(path)
            else :
                with open(path, "w") as f :
                    f.write("")

    # Check if 
    try :
        with open (RUN_runConfigFilePath, "r") as infile:
            configFile = json.load(infile)
        dummy = configFile["numberOfElements"], configFile["isContinuouslyGenerated"], configFile["willSaveData"], configFile["willPlotData"]
    except :
        fixData = {
            "numberOfElements" : 10,
            "isContinuouslyGenerated" : False,
            "willSaveData" : True,
            "willPlotData" : True
        }
        with open(RUN_runConfigFilePath, "w") as f:
            json.dump(fixData, f, sort_keys=True, indent=4)

def safeStop(willCleanDataOutputFolder=False) :

    projectDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    foldersCleanCache = ["Algorithms", "Utilities", "Constants"]

    for folder in foldersCleanCache :
        folderPath = os.path.join(projectDir, folder)
        for root, dirs, files in os.walk(folderPath):
            for dir in dirs :
                if dir == "__pycache__" :
                    shutil.rmtree(os.path.join(root, dir))

    if willCleanDataOutputFolder :
        for root, dirs, files in os.walk(DATA_dataOutputFolderPath):
            for file in files :
                os.remove(os.path.join(root, file))

    exit()