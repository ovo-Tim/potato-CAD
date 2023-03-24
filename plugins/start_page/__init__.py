import os
import sys

import webbrowser

from PySide2.QtWidgets import *
from PySide2.QtGui import *

class main():
    def __init__(self, mainClass):
        self.ToolBars = [QToolBar(mainClass.main_window.tr("开始工具栏"))]
        self.webside = QPushButton("访问github")
        self.webside.clicked.connect(lambda: webbrowser.open_new_tab('https://github.com/ovo-Tim/potato-CAD'))
        self.ToolBars[0].addWidget(self.webside)