from pyqtribbon import *
from pyqtribbon.titlewidget import RibbonTitleWidget
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import os
import sys
import time
import logging
import ujson as json
import qt_json_setting

from pathlib import Path

from occ_page import occ_page

__dir__ = str(Path(os.path.dirname(__file__)).parent)
os.environ['QT_API'] = 'pyside6'

# import faulthandler
# faulthandler.enable()

class my_RibbonBar(RibbonBar):
    def __init__(self, window, title, share_var):
        super().__init__()

        self.main_window = window
        self.share_var = share_var

        # 添加窗口按钮
        self.setting_button = QToolButton(
            self, icon=QIcon(__dir__ + '/icons/gear.svg'))
        self.setting_button.clicked.connect(self.open_setting_win)
        self._titleWidget.addRightToolButton(self.setting_button)

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

    def open_setting_win(self):
        qt_json_setting.seting_window(self.share_var.setting_path, os.path.join(self.share_var.root_path, 'setting-schema.json')).show()

class MainWindow(QMainWindow):
    BORDER_WIDTH = 5
    def __init__(self, share_var):
        super().__init__()
        logging.debug("window id:" + str(self.winId()))

        self.share_var = share_var
        
        with open(self.share_var.setting_path) as f:
            self.setting = json.decode(f.read())
        self.title = "potato-CAD"
        self.initUI()

        # print("In main window:"+str(int(self.winId())))

    def initUI(self):
        self.setWindowTitle(self.title)
        if self.setting['window']['FramelessWindow']:
            # self.setWindowFlags(Qt.CustomizeWindowHint)
            self.setWindowFlags(Qt.FramelessWindowHint)
            logging.info("Frameless window") # 无边框模式已启动

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

        self.RibbonBar = my_RibbonBar(self, self.title, self.share_var)  # Ribbon 工具栏
        self.setMenuBar(self.RibbonBar)

        if self.setting['window']['FramelessWindow']:
            QCoreApplication.instance().installEventFilter(self)
        self._isResizeEnabled = self.setting['window']['FramelessWindow']

        # self.new_page()

    def eventFilter(self, obj, event):
        '''
            窗口缩放
        '''
        et = event.type()
        if et != QEvent.MouseButtonRelease and et != QEvent.MouseButtonPress and et != QEvent.MouseMove or not self._isResizeEnabled:
            return False
        edges = Qt.Edge(0)
        pos = event.globalPos()
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
            self.windowHandle().startSystemResize(edges)

        return super().eventFilter(obj, event)

    # 改变图标
    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            self.RibbonBar.change_fullscreen_button()
        super().changeEvent(event)

    def new_page(self, file=None):
        logging.info("New page") # 新建页面

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
        logging.debug("refresh viewer")
        # self.activity_page().display.SetSize(self.activity_page().width(), self.activity_page().height())
        self.activity_page().InitDriver()
        
    def activity_page(self) -> occ_page:
        self._activity_page = self.page_list[self.main_page_window.tabText(self.main_page_window.currentIndex())]
        return self._activity_page
