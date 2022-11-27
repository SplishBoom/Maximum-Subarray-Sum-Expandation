import os
import shutil

def safeStart() :
    pass

def safeStop() :

    projectDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    folders = ["algorithms", "utils"]

    for folder in folders :
        folderPath = os.path.join(projectDir, folder)
        for root, dirs, files in os.walk(folderPath):
            for dir in dirs :
                if dir == "__pycache__" :
                    shutil.rmtree(os.path.join(root, dir))