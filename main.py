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
        self.main_window.load_plugin_select(self.plugins.plugins_information, self.switch_plugins)
    def switch_plugins(self, page_index:str):
        print(page_index)
        # 切换工具栏
        self.main_window.clean_ToolBars()
        self.main_window.plugins_ToolBars = self.plugins.plugins[page_index].ToolBars
        self.main_window.reload_toolBars()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Main()
    win.main_window.show()
    app.exec_()

