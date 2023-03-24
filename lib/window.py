from PySide2.QtWidgets import *
from PySide2.QtGui import *

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Display.OCCViewer import rgb_color

from OCC.Display.backend import load_backend,get_loaded_backend
load_backend("qt-pyside2")
import OCC.Display.qtDisplay as qtDisplay

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "potato-CAD"
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100,100,500,500)

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.page_list = []
        self.plugins_ToolBars = [] # 插件的 ToolBar

        self.main_page_window = QListWidget()
        self.main_layout.addWidget(self.main_page_window)

        self.plugin_ToolBar = QToolBar(self.tr("插件工具栏")) # 用于选择插件的工具栏
        self.addToolBar(self.plugin_ToolBar)
        self.plugin_ToolBar.setWhatsThis(self.tr("插件工具栏"))
        self.plugin_select = QComboBox(self)
        self.plugin_ToolBar.addWidget(self.plugin_select)


    def load_plugin_select(self, plugins_information: dict, func):
        ''' 初始化 plugin_ToolBar 的 plugin_select '''
        for name, attribute in plugins_information.items():
            self.plugin_select.addItem(name)
            self.plugin_select.setItemData(self.plugin_select.findText(name), attribute['synopsis'], role=Qt.ToolTipRole)
        self.plugin_select.currentTextChanged.connect(func)
    
    def clean_ToolBars(self):
        for i in self.plugins_ToolBars:
            i.hide()

    def reload_toolBars(self):
        for i in self.plugins_ToolBars:
            self.addToolBar(i)
            i.show()

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
