import os
import sys

os.environ['QT_API'] = 'pyside2'

import webbrowser

from PySide2.QtWidgets import *
from PySide2.QtGui import *

from pyqtribbon import RibbonBar, RibbonCategoryStyle
from pyqtribbon.screenshotwindow import RibbonScreenShotWindow

class main():
    def __init__(self, mainClass):
        ribbonbar = mainClass.main_window.RibbonBar
        self.category1 = ribbonbar.addCategory("Category 1")
        self.About_panel = self.category1.addPanel("About", showPanelOptionButton=False)
        self.About_panel.addSmallButton("访问github", icon=QIcon("./icon.png"), slot = lambda: webbrowser.open_new_tab("https://github.com/ovo-Tim/potato-CAD"))
        