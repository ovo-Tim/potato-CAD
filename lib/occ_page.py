from typing import Optional
import OCCT.Display.qtDisplay as qtDisplay
from OCCT.AIS import AIS_ViewCube, AIS_Shape
from OCCT.V3d import V3d_Xpos, V3d_Ypos, V3d_Zpos, V3d_Xneg, V3d_Yneg, V3d_Zneg
from OCCT.Graphic3d import Graphic3d_TransformPers, Graphic3d_TMF_TriedronPers, Graphic3d_Vec2i
from OCCT.gp import gp_Trsf, gp_Vec
from OCCT.TopAbs import (
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
from OCCT.Aspect import Aspect_GT_Rectangular, Aspect_GDM_Lines, Aspect_TOTP_RIGHT_UPPER
from PySide6.QtCore import Qt, Signal
from shape_data import main_datas
from actions import file_io
from OCCT.TCollection import TCollection_AsciiString

from lib.multithread_manager import new_mq_thread

def occt_text(text: str):
    return TCollection_AsciiString(text)

class potato_ViewCube(AIS_ViewCube):
    def __init__(self):
        super().__init__()
        self.SetBoxSideLabel(V3d_Xpos, occt_text(_("Right")))
        self.SetBoxSideLabel(V3d_Ypos, occt_text(_("Back")))
        self.SetBoxSideLabel(V3d_Zpos, occt_text(_("Top")))
        self.SetBoxSideLabel(V3d_Xneg, occt_text(_("Left")))
        self.SetBoxSideLabel(V3d_Yneg, occt_text(_("Front")))
        self.SetBoxSideLabel(V3d_Zneg, occt_text(_("Bottom")))
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
    def SetSize(self, theValue: int, theToAdaptAnother: bool = True) -> None:
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

class multithread_viewer(potaoViewer):
    def __init__(self, *kargs):
        super().__init__(*kargs)
        self._paintThread:new_mq_thread = share_var.threads.add_thread(name="paintThread")
        self._paintEvent = self._paintThread.add_func(super().paintEvent)
        self._mouseMoveEvent = self._paintThread.add_func(super().mouseMoveEvent)
        self._mouseReleaseEvent = self._paintThread.add_func(super().mouseReleaseEvent)

    def paintEvent(self, event):
        self._paintEvent.start((event,))
        # return super().paintEvent(event)

    def mouseMoveEvent(self, event):
        self._mouseMoveEvent.start((event,))
        # return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._mouseReleaseEvent.start((event,))
        # return super().mouseReleaseEvent(event)

    

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

        self.shape_datas = main_datas(self)

    def import_file(self, path: str):
        mod_file = file_io.import_shap(path)
        if isinstance(mod_file, list):
            n=0
            for i in mod_file:
                self.shape_datas.add_shape(i, path.split('/')[-1].split('.')[0] + str(n:=n+1))
        else:
            self.shape_datas.add_shape(mod_file, path.split('/')[-1].split('.')[0])
            
        self.load_finish_singal.emit()
        

