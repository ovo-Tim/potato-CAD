from pyqtribbon import *
from pyqtribbon.titlewidget import RibbonTitleWidget
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import os
import sys
import time
import logging

from OCC.Extend.DataExchange import read_step_file#STEP文件导入模块
from OCC.Extend.TopologyUtils import TopologyExplorer#STEP文件导入模块后的拓扑几何分析模块

from OCC.Display import OCCViewer
from OCC.Display.backend import load_backend,get_loaded_backend
# load_backend("qt-pyside6")
import OCC.Display.qtDisplay as qtDisplay

from pathlib import Path
__dir__ = str(Path(os.path.dirname(__file__)).parent)
os.environ['QT_API'] = 'pyside6'

import faulthandler
faulthandler.enable()

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

    def load_file(self, path):
        logging.info("加载文件:" + path)
        step = TopologyExplorer(read_step_file(path))
        for solid in step.solids():
            QApplication.processEvents()
            self.display.DisplayShape(solid)
        self.display.FitAll()

class my_RibbonBar(RibbonBar):
    def __init__(self, window, title):
        super().__init__()

        self.main_window = window

        # 添加窗口按钮
        self.minimize_button = QToolButton(
            self, icon=QIcon(__dir__ + '/icons/minimize.svg'))
        self.minimize_button.clicked.connect(self.main_window.showMinimized)
        self._titleWidget.addRightToolButton(self.minimize_button)

        self.fullscreen_button = QToolButton(self)
        self.change_fullscreen_button()
        self.fullscreen_button.clicked.connect(
            lambda: self.slot_max_or_recv(self.fullscreen_button))
        self._titleWidget.addRightToolButton(self.fullscreen_button)

        self.close_button = QToolButton(
            self, icon=QIcon(__dir__ + '/icons/close.svg'))
        self.close_button.clicked.connect(self.main_window.close)
        self._titleWidget.addRightToolButton(self.close_button)

    def change_fullscreen_button(self):
        if self.main_window.isMaximized():
            self.fullscreen_button.setIcon(QIcon(__dir__ + '/icons/fullscreen-exit.svg'))
        else:
            self.fullscreen_button.setIcon(QIcon(__dir__ + '/icons/fullscreen.svg'))

    def slot_max_or_recv(self, button):
        if self.main_window.isMaximized():
            self.main_window.showNormal()
        else:
            self.main_window.showMaximized()


class MainWindow(QMainWindow):
    BORDER_WIDTH = 3
    def __init__(self, setting: dict):
        super().__init__()
        logging.debug("window id:" + str(self.winId()))
        self.setting = setting
        self.title = "potato-CAD"
        self.initUI()

        # print("In main window:"+str(int(self.winId())))

    def initUI(self):
        self.setWindowTitle(self.title)
        if self.setting["SystemResize"]:
            self.setWindowFlags(Qt.CustomizeWindowHint)

        self.setGeometry(35, 35, 500, 500)

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.page_list = {}
        self._activity_page = None
        self.main_page_window = QTabWidget()  # 主要的文件页面
        self.main_page_window.currentChanged.connect(self.refresh_occ)
        self.main_layout.addWidget(self.main_page_window)
        
        self.new_page() # 很奇怪，如果我不在此处加载new_page然后创建RibbonBar会导致lib加载失败，详见github.com/tpaviot/pythonocc-core/issues/1214

        self.RibbonBar = my_RibbonBar(self, self.title)  # Ribbon 工具栏
        self.setMenuBar(self.RibbonBar)

        QCoreApplication.instance().installEventFilter(self)
        self._isResizeEnabled = True
        self._Resize = False
        self._ResizeEdge = 'stop'

    def eventFilter(self, obj, event):
        '''
            窗口缩放
        '''
        et = event.type()
        if et != QEvent.MouseButtonRelease and et != QEvent.MouseButtonPress and et != QEvent.MouseMove or not self._isResizeEnabled:
            return False
        edges = Qt.Edge(0)
        pos = event.globalPos() - self.pos()
        if pos.x() < self.BORDER_WIDTH:
            edges |= Qt.LeftEdge
        if pos.x() >= self.width()-self.BORDER_WIDTH:
            edges |= Qt.RightEdge
        if pos.y() < self.BORDER_WIDTH:
            edges |= Qt.TopEdge
        if pos.y() >= self.height()-self.BORDER_WIDTH:
            edges |= Qt.BottomEdge
        # change cursor
        if et == QEvent.MouseMove and self.windowState() == Qt.WindowNoState:  # noqa: F405
            if edges in (Qt.LeftEdge | Qt.TopEdge, Qt.RightEdge | Qt.BottomEdge):
                self.setCursor(Qt.SizeFDiagCursor)
            elif edges in (Qt.RightEdge | Qt.TopEdge, Qt.LeftEdge | Qt.BottomEdge):
                self.setCursor(Qt.SizeBDiagCursor)
            elif edges in (Qt.TopEdge, Qt.BottomEdge):
                self.setCursor(Qt.SizeVerCursor)
            elif edges in (Qt.LeftEdge, Qt.RightEdge):
                self.setCursor(Qt.SizeHorCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
        elif obj in (self, self.RibbonBar) and et == QEvent.MouseButtonPress and edges:
            if self.setting["SystemResize"]:
                self.windowHandle().startSystemResize(edges)
            
        if not self.setting["SystemResize"]:
            '''
                该功能目前存在严重问题，请使用正常边框
            '''
            pass
            # self.move_window(et, event, edges)
            # self.activity_page().display.View.MustBeResized()

        return super().eventFilter(obj, event)

    def move_window(self, et, event, edges):
        if et == QEvent.MouseButtonPress and edges:
            self._Resize = True
        elif et == QEvent.MouseButtonRelease or self.windowState() != Qt.WindowNoState:
            self._Resize = False
            self._ResizeEdge = 'stop'

        #print(edges)
        if not self._Resize:
            if edges == (Qt.LeftEdge | Qt.TopEdge):
                self._ResizeEdge = 'LT'
            elif edges == (Qt.LeftEdge | Qt.BottomEdge):
                self._ResizeEdge = 'LB'
            elif edges == (Qt.RightEdge | Qt.TopEdge):
                self._ResizeEdge = 'RT'
            elif edges == (Qt.RightEdge | Qt.BottomEdge):
                self._ResizeEdge = 'RB'
            elif edges & Qt.RightEdge:
                self._ResizeEdge = 'R'
            elif edges & Qt.LeftEdge:
                self._ResizeEdge = 'L'
            elif edges & Qt.BottomEdge:
                self._ResizeEdge = 'B'
            elif edges & Qt.TopEdge:
                self._ResizeEdge = 'T'

        # 手动实
        if self._Resize:
            if self._ResizeEdge == 'R':
                self.resize(event.pos().x(), self.height())
            elif self._ResizeEdge == 'B':
                # time.sleep(0.1)
                # print(event.pos().y())
                # 奇怪的BUG,获取到鼠标y坐标，3个中只有一个是正常的
                if abs(event.pos().y() - self.height()) < 100:
                    self.resize(self.width(), event.pos().y())
            elif self._ResizeEdge == 'RB':
                if abs(event.pos().y() - self.height()) < 100:
                    self.resize(event.pos().x(), event.pos().y())
                # self.resize(event.pos().x(), event.pos().y())
            elif self._ResizeEdge == 'L':
                print(event.pos().x())
                # self.setGeometry(self.x() + event.pos().x(), self.y(), self.width() - event.pos().x(), self.height())
            '''
                此处待实现
            '''

    # 改变图标
    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            self.RibbonBar.change_fullscreen_button()
        super().changeEvent(event)

    def new_page(self, file=None):
        logging.info("新建页面")

        page = occ_page()

        # self.setGeometry(x, y, w, h)

        if file != None:
            page.load_file(file)
            page.path = file
            page.name = os.path.basename(page.path)

        if page.name == None:
            i = 0
            while 'new file '+str(i) in self.page_list.keys():
                i += 1
            name = 'new file '+str(i)
            page.name = name

        self.page_list[page.name] = page
        self.main_page_window.addTab(
            self.page_list[page.name], QIcon('icon.svg'), page.name)
    
        return page

    def refresh_occ(self):
        logging.debug("刷新OCC")
        # self.activity_page().display.SetSize(self.activity_page().width(), self.activity_page().height())
        self.activity_page().InitDriver()
        

    def activity_page(self) -> occ_page:
        self._activity_page = self.page_list[self.main_page_window.tabText(self.main_page_window.currentIndex())]
        return self._activity_page