"""
This script is used to track the pathes of the vars that are used in project.
"""

import os

def connect_pathes(*pathes):
    return os.path.join(*pathes)

GUI_loaderGifPath = os.path.abspath(os.path.join("Assets", "GUI_ASSETS", "loader.gif"))
GUI_backgroundPhotoPath = os.path.abspath(os.path.join("Assets", "GUI_ASSETS", "background.jpg"))
GUI_welcomePhotoPath = os.path.abspath(os.path.join("Assets", "GUI_ASSETS", "welcome.jpg"))
GUI_settingsButtonPhotoPath = os.path.abspath(os.path.join("Assets", "GUI_ASSETS", "settings.png"))

DATA_dataOutputFolderPath = os.path.abspath(os.path.join("Data Export"))

RUN_runConfigFilePath = os.path.abspath(os.path.join("Utilities", "run_config.json"))

