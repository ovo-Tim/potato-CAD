from typing import Optional
import OCC.Display.qtDisplay as qtDisplay
from OCC.Extend.DataExchange import read_step_file, read_iges_file, read_stl_file #STEP文件导入模块
from OCC.Extend.TopologyUtils import TopologyExplorer #STEP文件导入模块后的拓扑几何分析模块
from OCC.Core.BRepTools import breptools_Read
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Vertex
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopAbs import TopAbs_VERTEX

import logging
import share_var

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Signal
from PySide6.QtGui import QMouseEvent


        
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

    

    
    
