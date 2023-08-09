from PySide6.QtGui import *
from PySide6.QtWidgets import *
import webbrowser
import os
import sys
from pathlib import Path

import pyqtribbon

sys.path.append("../../lib")
import share_var

class main():
    def __init__(self):
        self.MainWindow = share_var.main_window
        ribbonbar: pyqtribbon.ribbonbar.RibbonBar = self.MainWindow.RibbonBar
        
        self.category1 = ribbonbar.addCategory("Part")
        self.solids_panel = self.category1.addPanel(_("Solids"))

        self.solids_panel.addMediumButton(_("Box"), icon=QIcon(share_var.root_path + '/icons/box.svg'))

