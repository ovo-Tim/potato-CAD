#! /bin/python3
import sys,os,pathlib  # noqa: E401
__dir__ = os.path.dirname(__file__)

import logging
sys.path.append(__dir__ + "/lib")

from PySide6.QtWidgets import *
from PySide6.QtGui import *

from OCC.Display.backend import load_backend,get_loaded_backend
load_backend("qt-pyside6")

import plugin
import ujson as json
from window import MainWindow

import faulthandler
faulthandler.enable()

class Main():
    def __init__(self):
        self.app_path = os.path.join(pathlib.Path.home(), '.potato-CAD')
        if not os.path.exists(self.app_path):
            os.mkdir(self.app_path)
        logging.debug("软件目录:" + self.app_path)
        self.load_the_settings()

        self.main_window = MainWindow(self.setting)
        self.plugins = plugin.plugins(self.app_path + "/plugins")
        self.plugins.load_core(self)
        # self.plugins.load(self) 
        
    def load_the_settings(self): 
        # 判断用户配置文件是否存在
        setting_path = os.path.join(self.app_path, 'setting.json')
        logging.info("配置文件路径:" + setting_path)
        if os.path.exists(os.path.join(setting_path)):
            self.setting = pathlib.Path(setting_path).read_text()
        else: # 不存在就创建
            with open(setting_path, 'w') as f:
                with open(os.path.join(__dir__, 'default_setting.json')) as default:
                    self.setting = default.read()
                    f.write(self.setting)
        self.setting = json.decode(self.setting)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Main()
    win.main_window.show()
    app.exec()

