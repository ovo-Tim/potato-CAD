
from PySide6.QtGui import QIcon
from PySide6.QtCore import SignalInstance
from PySide6.QtWidgets import QLabel
import webbrowser
import os
import sys
from pathlib import Path

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Core.AIS import AIS_Shape
import qfluentwidgets
import pyqtribbon
from OCC.potato.shape import potato_box

sys.path.append("../../")
sys.path.append("../../lib")
import occ_page
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
        activity_page = self.MainWindow.activity_page()
        box = potato_box()
        # shape = box.Shape()
        activity_page.display.DisplayShape(box.AIS_Shape())
        activity_page.move_to_mouse(box)

        input_dialog = occ_page.input_dialog(activity_page)
        input_dialog.main_layout.addWidget(QLabel(_("Length:")))
        lenth_input = qfluentwidgets.LineEdit()
        input_dialog.main_layout.addWidget(lenth_input)

        input_dialog.main_layout.addWidget(QLabel(_("Width:")))
        width_input = qfluentwidgets.LineEdit()
        input_dialog.main_layout.addWidget(width_input)

        input_dialog.main_layout.addWidget(QLabel(_("Height:")))
        height_input = qfluentwidgets.LineEdit()
        input_dialog.main_layout.addWidget(height_input)

        
        


        # activity_page.main_layout.addWidget(qfluentwidgets.LineEdit())