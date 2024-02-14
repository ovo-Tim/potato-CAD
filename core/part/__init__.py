
from PySide6.QtGui import QIcon
from PySide6.QtCore import SignalInstance
from PySide6.QtWidgets import QLabel
import webbrowser
import os
import sys
from pathlib import Path

from OCCT.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCCT.TopExp import TopExp_Explorer
from OCCT.TopAbs import TopAbs_EDGE
from OCCT.AIS import AIS_Shape
import qfluentwidgets
import pyqtribbon

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

        self.solids_panel.addMediumButton(_("Box"), icon=QIcon(share_var.root_path + '/icons/box.svg')
                                          )
        
        
    # def make_box(self):
    #     activity_page = self.MainWindow.activity_page()
    #     box = potato_box(display=activity_page.display)
    #     shape = box.AIS_Shape()
    #     activity_page.display.DisplayShape(shape)
    #     activity_page.move_to_mouse(shape)

    #     input_dialog = occ_page.input_dialog(activity_page)
    #     input_dialog.main_layout.addWidget(QLabel(_("Length:")))
    #     lenth_input = qfluentwidgets.LineEdit()
    #     lenth_input.setText(str(box.Size()[0]))
    #     input_dialog.main_layout.addWidget(lenth_input)

    #     input_dialog.main_layout.addWidget(QLabel(_("Width:")))
    #     width_input = qfluentwidgets.LineEdit()
    #     width_input.setText(str(box.Size()[1]))
    #     input_dialog.main_layout.addWidget(width_input)

    #     input_dialog.main_layout.addWidget(QLabel(_("Height:")))
    #     height_input = qfluentwidgets.LineEdit()
    #     height_input.setText(str(box.Size()[2]))
    #     input_dialog.main_layout.addWidget(height_input)

    #     lenth_input.returnPressed.connect(lambda: box.SetSize((int(lenth_input.text()), int(width_input.text()), int(height_input.text()))))
    #     width_input.returnPressed.connect(lambda: box.SetSize((int(lenth_input.text()), int(width_input.text()), int(height_input.text()))))
    #     height_input.returnPressed.connect(lambda: box.SetSize((int(lenth_input.text()), int(width_input.text()), int(height_input.text()))))
        
        


        # activity_page.main_layout.addWidget(qfluentwidgets.LineEdit())