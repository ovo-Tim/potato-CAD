import os, sys
os.environ['QT_API'] = 'pyside2'

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Display.OCCViewer import rgb_color

from OCC.Display.backend import load_backend,get_loaded_backend
load_backend("qt-pyside2")
import OCC.Display.qtDisplay as qtDisplay

from pyqtribbon import RibbonBar, RibbonCategoryStyle
from pyqtribbon.screenshotwindow import RibbonScreenShotWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "potato-CAD"
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(50,50,3000,300)
        self.setWindowFlags(Qt.CustomizeWindowHint)

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.RibbonBar = RibbonBar() # Ribbon 工具栏
        self.setMenuBar(self.RibbonBar)
        # self.RibbonBar._titleWidget.addRightToolButton(QToolButton(slot=sys.exit))

        self.page_list = []
        self.main_page_window = QTabWidget() # 主要的文件页面
        self.main_layout.addWidget(self.main_page_window)

class occ_page(QWidget):
    '''
        一个包含OCC_canvas的页面。通常情况下，一个打开的3D文件(一个3D文件页面)就是一个occ_page
    '''
    def __init__(self):
        self.main_layout = QGridLayout(self)

        # 加载OCC
        self.canvas = qtDisplay.qtViewer3d(self)
        self.canvas.InitDriver()
        self.main_layout.addWidget(self.canvas)
        self.display = self.canvas._display
