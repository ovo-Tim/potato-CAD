from typing import Optional
import OCC.Display.qtDisplay as qtDisplay
from OCC.Extend.DataExchange import read_step_file #STEP文件导入模块
from OCC.Extend.TopologyUtils import TopologyExplorer #STEP文件导入模块后的拓扑几何分析模块
from OCC.Core.AIS import AIS_ViewCube
from OCC.Core.Graphic3d import *
from OCC.Core.V3d import *
from OCC.Core.Aspect import *
import logging

from PySide6.QtWidgets import QApplication

class my_ViewCube(AIS_ViewCube):
    def __init__(self, tr = lambda text:text):
        super().__init__()
        self.tr = tr

        self.SetBoxSideLabel(V3d_Xpos, self.tr("右"))
        self.SetBoxSideLabel(V3d_Ypos, self.tr("后"))
        self.SetBoxSideLabel(V3d_Zpos, self.tr("顶"))
        self.SetBoxSideLabel(V3d_Xneg, self.tr("左"))
        self.SetBoxSideLabel(V3d_Yneg, self.tr("前"))
        self.SetBoxSideLabel(V3d_Zneg, self.tr("底"))
        self.SetFontHeight( self.Size() * 0.5)
        self.SetTransparency(0.6)

        # self.SetHilightMode(0)

        self.SetTransformPersistence(
            Graphic3d_TransformPers(
                Graphic3d_TMF_TriedronPers,
                Aspect_TOTP_RIGHT_UPPER,
                Graphic3d_Vec2i(100, 100)
            )
        )
    def SetSize(self, theValue: float, theToAdaptAnother: bool = True) -> None:
        self.SetTransformPersistence(
            Graphic3d_TransformPers(
                Graphic3d_TMF_TriedronPers,
                Aspect_TOTP_RIGHT_UPPER,
                Graphic3d_Vec2i(theValue, theValue)
            )
        )
        
        super().SetSize(theValue, theToAdaptAnother)
        

class occ_page(qtDisplay.qtViewer3d):
    '''
        一个包含OCC_canvas的页面。通常情况下，一个打开的3D文件(一个3D文件页面)就是一个occ_page
    '''
    def __init__(self):
        super().__init__()

        # 基本属性
        self.name = None
        self.path = None

        # 加载OCC
        self.InitDriver()
        self.display = self._display

        self.ViewCube = my_ViewCube(tr=self.tr)
        self.display.Context.Display(self.ViewCube, True)
        
    
    # def resizeEvent(self, event):
    #     w = event.size().width()
    #     h = event.size().height()
    #     cube_size = int( ((w ** 2) + (h ** 2)) ** 0.5)
    #     self.ViewCube.SetSize(cube_size) # TODO: 此处实时大小调整无效
    #     return super().resizeEvent(event)

    def load_file(self, path):
        logging.info("加载文件:" + path)
        step = TopologyExplorer(read_step_file(path))
        for solid in step.solids():
            QApplication.processEvents()
            self.display.DisplayShape(solid)
        self.display.FitAll()