from PySide2.QtGui import *
from PySide2.QtWidgets import *
import webbrowser
import os
import sys
from pathlib import Path
__dir__ = str(Path(os.path.dirname(__file__)).parent.parent)

os.environ['QT_API'] = 'pyside2'

sys.path.append("../../")
import main as mainFile

class main():
    def __init__(self, mainClass: mainFile.Main):
        self.mainClass = mainClass
        self.MainWindow = self.mainClass.main_window
        ribbonbar = self.MainWindow.RibbonBar
        self.tr = self.mainClass.main_window.tr

        self.category1 = ribbonbar.addCategory("Home")

        self.file_panel = self.category1.addPanel(self.tr("文件"))
        self.file_panel.addLargeButton(
            self.tr("打开文件"), icon=QIcon(__dir__ + '/icons/open_file.svg'), slot=self.open_file)

        self.About_panel = self.category1.addPanel(
            self.tr("关于"), showPanelOptionButton=False)
        self.About_panel.addSmallButton(self.tr("访问主页"), icon=QIcon(
            __dir__ + "/icon.svg"), slot=lambda: webbrowser.open_new_tab("https://github.com/ovo-Tim/potato-CAD"))
    def open_file(self):
        file_paths = QFileDialog.getOpenFileNames(self.MainWindow, self.tr("选择文件"), filter = 'step  files (*.step);; All files (*)')[0]
        for i in file_paths:
            self.MainWindow.new_page(file = i)

