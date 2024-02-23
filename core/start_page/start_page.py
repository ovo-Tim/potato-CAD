from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFileDialog
import webbrowser
import os
import sys
from pathlib import Path
import pyqtribbon
import logging
import ujson as json
__dir__ = str(Path(os.path.dirname(__file__)).parent)
from actions import file_io
sys.path.append('../../lib')
import share_var


class main():
    def __init__(self):
        self.MainWindow = share_var.main_window
        ribbonbar: pyqtribbon.ribbonbar.RibbonBar = self.MainWindow.RibbonBar

        self.category1 = ribbonbar.addCategory("Home")

        self.file_panel = self.category1.addPanel(_("File"))

        self.file_panel.addMediumButton(
            _("New page"), icon=QIcon(share_var.root_path+ '/icons/new_page.svg'), slot= lambda: self.MainWindow.new_page())
        
        self.file_panel.addMediumButton(
            _("Open file"), icon=QIcon(share_var.root_path+ '/icons/open_file.svg'), slot=self.open_file)

        self.file_panel.addMediumButton(
            _("Import file"), icon=QIcon(share_var.root_path+ '/icons/import.svg'), slot=self.import_InBackground)
        
        self.file_panel.addMediumButton(
            _("Export"), icon=QIcon(share_var.root_path+ '/icons/export.svg'), slot=self.export
        )

        self.file_panel.addMediumButton(
            _("Save"), icon=QIcon(share_var.root_path+ '/icons/save.svg'), slot=self.save
        )

        self.About_panel = self.category1.addPanel(
            _("About"), showPanelOptionButton=False)
        self.About_panel.addSmallButton(_("Home page"), icon=QIcon(
            share_var.root_path+ "/icon.svg"), slot=lambda: webbrowser.open_new_tab("https://github.com/ovo-Tim/potato-CAD"))
        
    def import_file(self):
        self.MainWindow._isResizeEnabled = False
        file_paths = QFileDialog.getOpenFileNames(self.MainWindow, _("select file"), filter = 'step files (*.step);; brep files (*.brep);; iges files (*.iges);; stl files (*.stl);; All files (*)')[0]
        self.MainWindow._isResizeEnabled = True
        for i in file_paths:
            self.MainWindow.activity_page().import_file(i)
    
    def import_InBackground(self):
        self.MainWindow._isResizeEnabled = False
        file_paths = QFileDialog.getOpenFileNames(self.MainWindow, _("select file"), filter = 'step files (*.step);; brep files (*.brep);; iges files (*.iges);; stl files (*.stl);; All files (*)')[0]
        self.MainWindow._isResizeEnabled = True
        for i in file_paths:
            share_var.threads.run_func(lambda: self.MainWindow.activity_page().import_file(i), name=_("Importing file..."))
            # self.MainWindow.activity_page().import_file(i)

    def export(self):
        self.MainWindow._isResizeEnabled = False
        path = QFileDialog.getSaveFileName(self.MainWindow, _("Export file"), filter = 'step files (*.step);; brep files (*.brep);; iges files (*.iges);; All files (*)')
        self.MainWindow._isResizeEnabled = True
        path = path[0]
        file_io.export(path, self.MainWindow.activity_page().shape_datas.export_to_list())

    def save(self):
        self.MainWindow._isResizeEnabled = False
        path = QFileDialog.getSaveFileName(self.MainWindow, _("Save file"), filter = 'potatoCAD files (*.pcad)')[0]
        self.MainWindow._isResizeEnabled = True
        file_io.save(path, self.MainWindow.activity_page().shape_datas)

    def open_file(self):
        self.MainWindow._isResizeEnabled = False
        path = QFileDialog.getOpenFileNames(self.MainWindow, _("Open file"), filter = 'potatoCAD files (*.pcad)')[0]
        self.MainWindow._isResizeEnabled = True

        for i in path:
            datas = file_io.load_file(i)
            self.MainWindow.new_page().shape_datas.load_from_json(datas)