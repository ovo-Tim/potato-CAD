import os
import sys
import logging
sys.path.append("./lib/")

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
        self.plugins = plugin.plugins("plugins/")
        self.plugins.load(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Main()
    win.main_window.show()
    app.exec_()

