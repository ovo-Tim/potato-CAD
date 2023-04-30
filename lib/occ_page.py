from PySide2.QtWidgets import *
from PySide2.QtGui import *

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Display.OCCViewer import rgb_color
from OCC.Extend.DataExchange import read_step_file#STEP文件导入模块
from OCC.Extend.TopologyUtils import TopologyExplorer#STEP文件导入模块后的拓扑几何分析模块

from OCC.Display.backend import load_backend,get_loaded_backend
load_backend("qt-pyside2")
import OCC.Display.qtDisplay as qtDisplay

import logging

class occ_page(QWidget):
    '''
        一个包含OCC_canvas的页面。通常情况下，一个打开的3D文件(一个3D文件页面)就是一个occ_page
    '''

    def __init__(self):
        super().__init__()
        self.main_layout = QGridLayout(self)

        # 基本属性
        self.name = None
        self.path = None

        # 加载OCC
        self.canvas = qtDisplay.qtViewer3d(self)
        self.canvas.InitDriver()

        self.main_layout.addWidget(self.canvas)
        self.display = self.canvas._display

        self.setLayout(self.main_layout)

    def load_file(self, path):
        logging.info("加载文件:" + path)
        step = TopologyExplorer(read_step_file(path))
        for solid in step.solids():
            QApplication.processEvents()
            self.display.DisplayShape(solid)
        self.display.FitAll()
