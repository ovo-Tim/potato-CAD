from typing import Optional
import OCC.Display.qtDisplay as qtDisplay
from OCC.Core.AIS import AIS_ViewCube, AIS_Shape
from OCC.Extend.DataExchange import read_step_file, read_iges_file, read_stl_file #STEP文件导入模块
from OCC.Extend.TopologyUtils import TopologyExplorer #STEP文件导入模块后的拓扑几何分析模块
from OCC.Core.BRepTools import breptools_Read
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Vertex
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopAbs import TopAbs_VERTEX
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopoDS import TopoDS_Edge, TopoDS_Shape
from OCC.Core.V3d import V3d_Xpos, V3d_Ypos, V3d_Zpos, V3d_Xneg, V3d_Yneg, V3d_Zneg
from OCC.Core.Graphic3d import Graphic3d_TransformPers, Graphic3d_TMF_TriedronPers, Graphic3d_Vec2i
from OCC.Core.gp import gp_Trsf, gp_Vec
from OCC.Core.TopAbs import (
    TopAbs_FACE,
    TopAbs_EDGE,
    TopAbs_VERTEX,
    TopAbs_SHELL,
    TopAbs_SOLID,
)

import logging
from PySide6.QtCore import Signal
# from dayu_widgets_overlay2 import MOverlay
import share_var
import qfluentwidgets
from OCC.Core.Aspect import Aspect_GT_Rectangular, Aspect_GDM_Lines, Aspect_TOTP_RIGHT_UPPER

from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout
from PySide6.QtCore import Qt, Signal

class potato_ViewCube(AIS_ViewCube):
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
        
class potaoViewer(qtDisplay.qtViewer3d):
    move_to_mouse_done = Signal()
    mouse_move_signal = Signal()
    resize_signal = Signal()
    def __init__(self, *kargs):
        super().__init__(*kargs)

        self.display = self._display

        # Display the view cube
        self.ViewCube = potato_ViewCube()
        self.display.Context.Display(self.ViewCube, True)

        # Display the grid
        self.display.Viewer.ActivateGrid(Aspect_GT_Rectangular, Aspect_GDM_Lines)

        self.moving_to_mouse = False

    def mouseMoveEvent(self, evt):
        super().mouseMoveEvent(evt)
        self.mouse_move_signal.emit()
    
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton and self.moving_to_mouse:
            self.mouse_move_signal.disconnect(self.moving_to_mouse)
            self.moving_to_mouse = False
            self.move_to_mouse_done.emit()

    def move_to_mouse(self, shape: AIS_Shape):
        """
        Move the given shape to the position of the mouse.

        Parameters:
            shape (AIS_Shape): The shape to be moved.

        Returns:
            None
        """
        self.moving_to_mouse = lambda: self._move_to_mouse(shape)
        self.mouse_move_signal.connect(self.moving_to_mouse)

    def _move_to_mouse(self, shape: AIS_Shape):
        if isinstance(shape, AIS_Shape):       
            trsf = gp_Trsf()
            trsf.SetTranslation(gp_Vec(
                                self.mouse_3d_pos[0],
                                self.mouse_3d_pos[1],
                                self.mouse_3d_pos[2]
                                ))
            # Toploc = TopLoc_Location(trsf)
            # self.display.Context.SetLocation(interactive, Toploc) # core_animation.py
            # shape.SetShape(shape.Shape().Move(Toploc))

            shape.SetLocalTransformation(trsf)
            
            self.display.Context.Redisplay(shape, True)

class occ_page(potaoViewer):
    '''
        一个包含OCC_canvas的页面。通常情况下，一个打开的3D文件(一个3D文件页面)就是一个occ_page
    '''
    load_finish_singal = Signal()
    def __init__(self):
        super().__init__()

        # 基本属性
        self.name: str = None
        self.path: str = None

    def load_file(self, path: str):
        logging.info("Load file:" + path)
        suffix = path.split('.')[-1].lower()

        if suffix == 'brep':
            logging.info("Found BREP,loading")
            mod_file = TopoDS_Shape()
            builder = BRep_Builder()
            breptools_Read(mod_file, path, builder)

        elif suffix == 'step':
            logging.info("Found STEP, loading")
            mod_file = read_step_file(path, as_compound=False)
        elif suffix == 'iges':
            logging.info("Found IGES, loading")
            mod_file = read_iges_file(path)
        elif suffix == 'stl':
            logging.info("Found STL, loading")
            mod_file = read_stl_file(path)
        else:
            logging.error(f"Not supported {suffix}. Stop loading.")
            return
        
        logging.info("Load finish")
        self.load_finish_singal.emit()
        self._display.DisplayShape(mod_file, update=True)

class input_dialog(QWidget):
    paintSingle = Signal()
    def __init__(self, parent:occ_page):
        super().__init__(parent)
        self._parent = parent

        self.setAutoFillBackground(True)

        self.main_layout = QHBoxLayout(self)
        self.setLayout(self.main_layout)

        self.setStyleSheet("border-radius: 10px")
        self.setStyleSheet("background-color:rgb(255, 255, 255, 0.5)")
        
        self.auto_resize()
        self.paintSingle.connect(self.auto_resize)
        self.show()

    def auto_resize(self):
        self.adjustSize()
        self.my_pos = (int(self._parent.width()/2 - self.width()/2), self._parent.height() - self.height())
        self.move(*self.my_pos)

    def paintEvent(self, event) -> None:
        self.paintSingle.emit()
        
        return super().paintEvent(event)
