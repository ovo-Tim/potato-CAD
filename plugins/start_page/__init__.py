import os
import sys
from pathlib import Path
__dir__ = str(Path(os.path.dirname(__file__)).parent.parent)

os.environ['QT_API'] = 'pyside2'

import webbrowser

from PySide2.QtWidgets import *
from PySide2.QtGui import *

from pyqtribbon import RibbonBar, RibbonCategoryStyle
from pyqtribbon.screenshotwindow import RibbonScreenShotWindow

class main():
    def __init__(self, mainClass):
        ribbonbar = mainClass.main_window.RibbonBar
        tr = mainClass.main_window.tr
        self.category1 = ribbonbar.addCategory("Home")
        self.file_panel = self.category1.addPanel(tr("文件"))
        self.file_panel.addLargeButton(tr("打开文件"), icon = QIcon(__dir__ + '/icons/open_file.svg'))
        self.About_panel = self.category1.addPanel(tr("关于"), showPanelOptionButton=False)
        self.About_panel.addSmallButton(tr("访问主页"), icon=QIcon(__dir__ + "/icon.svg"), slot = lambda: webbrowser.open_new_tab("https://github.com/ovo-Tim/potato-CAD"))
        