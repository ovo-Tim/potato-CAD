from typing import Optional
import OCC.Display.qtDisplay as qtDisplay
from OCC.Extend.DataExchange import read_step_file, read_iges_file, read_stl_file #STEP文件导入模块
from OCC.Extend.TopologyUtils import TopologyExplorer #STEP文件导入模块后的拓扑几何分析模块
from OCC.Core.BRepTools import breptools_Read
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Vertex
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopAbs import TopAbs_VERTEX

import logging
from PySide6.QtCore import Signal
# from dayu_widgets_overlay2 import MOverlay
import share_var
import qfluentwidgets

from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout
from PySide6.QtCore import Qt
from threading import Thread

class occ_page(qtDisplay.potaoViewer):
    '''
        一个包含OCC_canvas的页面。通常情况下，一个打开的3D文件(一个3D文件页面)就是一个occ_page
    '''
    def __init__(self):
        super().__init__()

        # 基本属性
        self.name: str = None
        self.path: str = None

    def load_file(self, path: str):
        logging.info("Load file:" + path)
        suffix = path.split('.')[-1].lower()

        QApplication.processEvents()

        if suffix == 'brep':
            logging.info("Found BREP,loading")
            read_mod = TopoDS_Shape()
            builder = BRep_Builder()
            breptools_Read(read_mod, path, builder)
            self.display.DisplayShape(read_mod, update=True)
        else:
            if suffix == 'step':
                logging.info("Found STEP, loading")
                mod_file = read_step_file(path)
            elif suffix == 'iges':
                logging.info("Found IGES, loading")
                mod_file = read_iges_file(path)
            elif suffix == 'stl':
                logging.info("Found STL, loading")
                mod_file = read_stl_file(path)
            else:
                logging.error(f"Not supported {suffix}.Stop loading.")
                return

            step = TopologyExplorer(mod_file)
            for solid in step.solids():
                QApplication.processEvents()
                self.display.DisplayShape(solid, update=True)
        
        self.display.FitAll()

        self.InitDriver()

    def paintEvent(self, event):
        Thread(target=super().paintEvent, args=(event,)).start()
        # return super().paintEvent(event)

class input_dialog(QWidget):
    paintSingle = Signal()
    def __init__(self, parent:occ_page):
        super().__init__(parent)
        self._parent = parent

        self.setAutoFillBackground(True)
        # self.setAttribute(Qt.WA_TranslucentBackground)

        self.main_layout = QHBoxLayout(self)
        self.setLayout(self.main_layout)

        # self.setStyleSheet("border-radius: 10px")
        self.setStyleSheet("background-color:rgb(255, 255, 255, 0.5)")
        
        self.auto_resize()
        self.paintSingle.connect(self.auto_resize)
        # self._parent.resize_signal.connect(self.auto_resize)
        self.show()

    def auto_resize(self):
        self.adjustSize()
        self.my_pos = (int(self._parent.width()/2 - self.width()/2), self._parent.height() - self.height())
        self.move(*self.my_pos)
        # self.repaint()

    def paintEvent(self, event) -> None:
        self.paintSingle.emit()
        
        return super().paintEvent(event)


# class input_dialog(QWidget):
#     paintSingle = Signal()
#     def __init__(self, parent:occ_page):
#         super().__init__(parent)
#         self._parent = parent
#         self.main_layout = QFormLayout(self)
#         self.setLayout(self.main_layout)
#         self.main_layout.addWidget(qfluentwidgets.LineEdit(self))

#         self.setAutoFillBackground(True)

#         parent.main_layout.addWidget(self)