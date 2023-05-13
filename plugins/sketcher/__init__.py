from PySide2.QtGui import *
from PySide2.QtWidgets import *
import webbrowser
import os
import sys
from pathlib import Path
__dir__ = str(Path(os.path.dirname(__file__)).parent.parent)

sys.path.append("../../")
import main as mainFile

class main():
    def __init__(self, mainClass: mainFile.Main):
        self.mainClass = mainClass
        self.MainWindow = self.mainClass.main_window
        ribbonbar = self.MainWindow.RibbonBar
        self.tr = self.mainClass.main_window.tr