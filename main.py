#! /bin/python3
import sys,os
__dir__ = os.path.dirname(__file__)

import logging
sys.path.append(__dir__ + "/lib")

from PySide2.QtWidgets import *
from PySide2.QtGui import *

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Display.OCCViewer import rgb_color

from OCC.Display.backend import load_backend,get_loaded_backend
load_backend("qt-pyside2")
import OCC.Display.qtDisplay as qtDisplay

import plugin
from window import *

class Main():
    def __init__(self):
        self.main_window = MainWindow()
        self.plugins = plugin.plugins(__dir__ + "/plugins")
        self.plugins.load(self)


app = QApplication(sys.argv)
win = Main()
win.main_window.show()
app.exec_()

