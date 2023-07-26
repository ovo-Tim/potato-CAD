from typing import Optional
import OCC.Display.qtDisplay as qtDisplay
from OCC.Extend.DataExchange import read_step_file, read_iges_file, read_stl_file #STEP文件导入模块
from OCC.Extend.TopologyUtils import TopologyExplorer #STEP文件导入模块后的拓扑几何分析模块
from OCC.Core.BRepTools import breptools_Read,breptools_Write
from OCC.Core.AIS import AIS_ViewCube
from OCC.Core.Graphic3d import *
from OCC.Core.V3d import *
from OCC.Core.Aspect import *
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRep import BRep_Builder
import logging
import share_var

from PySide6.QtWidgets import QApplication

class my_ViewCube(AIS_ViewCube):
    def __init__(self):
        super().__init__()

        self.SetBoxSideLabel(V3d_Xpos, _("Right"))
        self.SetBoxSideLabel(V3d_Ypos, _("Back"))
        self.SetBoxSideLabel(V3d_Zpos, _("Top"))
        self.SetBoxSideLabel(V3d_Xneg, _("Left"))
        self.SetBoxSideLabel(V3d_Yneg, _("Front"))
        self.SetBoxSideLabel(V3d_Zneg, _("Bottom"))
        self.SetFontHeight( self.Size() * 0.38)
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

        self.ViewCube = my_ViewCube()
        self.display.Context.Display(self.ViewCube, True)
        
    
    # def resizeEvent(self, event):
    #     w = event.size().width()
    #     h = event.size().height()
    #     cube_size = int( ((w ** 2) + (h ** 2)) ** 0.5)
    #     self.ViewCube.SetSize(cube_size) # TODO: 此处实时大小调整无效
    #     return super().resizeEvent(event)

    def load_file(self, path: str):
        logging.info("Load file:" + path)
        suffix = path.split('.')[-1].lower()

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