from PySide6.QtGui import *
from PySide6.QtWidgets import *
import os
import sys
from pathlib import Path
__dir__ = str(Path(os.path.dirname(__file__)).parent.parent)

sys.path.append(__dir__)
import main as mainFile

class main():
    def __init__(self, mainClass: mainFile.Main):
        self.mainClass = mainClass
        self.MainWindow = self.mainClass.main_window
        ribbonbar = self.MainWindow.RibbonBar
        self.tr = self.MainWindow.tr