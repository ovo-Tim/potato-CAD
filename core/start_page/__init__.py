from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFileDialog
import webbrowser
import os
import sys
from pathlib import Path
import pyqtribbon
from OCC.Extend.DataExchange import write_step_file, write_iges_file, write_brep_file
import logging

sys.path.append("../../")
sys.path.append("../../lib")
import share_var

class main():
    def __init__(self):
        self.mainClass = share_var.main_class
        self.MainWindow = share_var.main_window
        ribbonbar: pyqtribbon.ribbonbar.RibbonBar = self.MainWindow.RibbonBar

        self.category1 = ribbonbar.addCategory("Home")

        self.file_panel = self.category1.addPanel(_("File"))
        self.file_panel.addMediumButton(
            _("Open file"), icon=QIcon(share_var.root_path+ '/icons/open_file.svg'), slot=self.open_file)
        
        self.file_panel.addMediumButton(
            _("New page"), icon=QIcon(share_var.root_path+ '/icons/open_file.svg'), slot= lambda: self.MainWindow.new_page(None))
        
        self.file_panel.addMediumButton(
            _("save"), icon=QIcon(share_var.root_path+ '/icons/save.svg'), slot=self.save
        )

        self.About_panel = self.category1.addPanel(
            _("About"), showPanelOptionButton=False)
        self.About_panel.addSmallButton(_("Home page"), icon=QIcon(
            share_var.root_path+ "/icon.svg"), slot=lambda: webbrowser.open_new_tab("https://github.com/ovo-Tim/potato-CAD"))
        
    def open_file(self):
        self.MainWindow._isResizeEnabled = False
        file_paths = QFileDialog.getOpenFileNames(self.MainWindow, _("select file"), filter = 'step files (*.step);; brep files (*.brep);; iges files (*.iges);; stl files (*.stl);; All files (*)')[0]
        self.MainWindow._isResizeEnabled = True
        for i in file_paths:
            self.MainWindow.new_page(file = i)
    
    def save(self):
        activity_page = self.MainWindow.activity_page()
        if activity_page.path is None:
            activity_page.path = QFileDialog.getSaveFileName(self.MainWindow, _("Save file"), filter = 'step files (*.step);; brep files (*.brep);; iges files (*.iges);; All files (*)')[0]
        suffix = activity_page.path.split('.')[-1].lower()

        if suffix == 'brep':
            write_brep_file(activity_page.display.shapes, activity_page.path)
        elif suffix == 'step':
            write_step_file(activity_page.display.shapes, activity_page.path)
        elif suffix == 'iges':
            write_iges_file(activity_page.display.shapes, activity_page.path)
        else:
            logging.error(f"Not supported {suffix}.Stop saving.")
            activity_page.path = None
        
        print(activity_page.display.shapes)
        

