from PySide6.QtGui import QIcon
from PySide6.QtCore import SignalInstance
import webbrowser
import os
import sys
from pathlib import Path

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_EDGE

import pyqtribbon

sys.path.append("../../lib")
import share_var

class main():
    def __init__(self):
        self.MainWindow = share_var.main_window
        ribbonbar: pyqtribbon.ribbonbar.RibbonBar = self.MainWindow.RibbonBar
        
        self.category1 = ribbonbar.addCategory("Part")
        self.solids_panel = self.category1.addPanel(_("Solids"))

        self.solids_panel.addMediumButton(_("Box"), icon=QIcon(share_var.root_path + '/icons/box.svg'), 
                                          slot=self.make_box)
        
    def make_box(self):
        shape = BRepPrimAPI_MakeBox(15,15,15).Shape()
        interactive = self.MainWindow.activity_page().display.DisplayShape(shape)[0]
        print(interactive)
        self.MainWindow.activity_page().move_to_mouse(interactive)

