from PySide6.QtGui import *
from PySide6.QtWidgets import *
import webbrowser
import os
import sys
from pathlib import Path
__dir__ = str(Path(os.path.dirname(__file__)).parent.parent)

os.environ['QT_API'] = 'pyside2'

sys.path.append("../../")
import main as mainFile

class main():
    def __init__(self, share_var: mainFile.share_var):
        self.mainClass = share_var.main_class
        self.MainWindow = share_var.main_window
        self.tr = share_var.tr
        ribbonbar = self.MainWindow.RibbonBar

        self.category1 = ribbonbar.addCategory("Home")

        self.file_panel = self.category1.addPanel(self.tr("File"))
        self.file_panel.addLargeButton(
            self.tr("Open file"), icon=QIcon(__dir__ + '/icons/open_file.svg'), slot=self.open_file)
        
        self.file_panel.addLargeButton(
            self.tr("New page"), icon=QIcon(__dir__ + '/icons/open_file.svg'), slot=self.MainWindow.new_page)

        self.About_panel = self.category1.addPanel(
            self.tr("About"), showPanelOptionButton=False)
        self.About_panel.addSmallButton(self.tr("Home page"), icon=QIcon(
            __dir__ + "/icon.svg"), slot=lambda: webbrowser.open_new_tab("https://github.com/ovo-Tim/potato-CAD"))
        
    def open_file(self):
        self.MainWindow._isResizeEnabled = False
        file_paths = QFileDialog.getOpenFileNames(self.MainWindow, self.tr("select file"), filter = 'step files (*.step);; brep files (*.brep);; iges files (*.iges);; stl files (*.stl);; All files (*)')[0]
        self.MainWindow._isResizeEnabled = True
        for i in file_paths:
            self.MainWindow.new_page(file = i)

