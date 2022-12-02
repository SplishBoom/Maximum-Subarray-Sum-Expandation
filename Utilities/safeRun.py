import os
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

def safeStop() :

    projectDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    folders = ["Algorithms", "Utilities", "Constants"]

    for folder in folders :
        folderPath = os.path.join(projectDir, folder)
        for root, dirs, files in os.walk(folderPath):
            for dir in dirs :
                if dir == "__pycache__" :
                    shutil.rmtree(os.path.join(root, dir))

    exit()