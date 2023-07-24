#! /bin/python3
import sys, os, pathlib, platform, subprocess  # noqa: E401

import logging
logging.basicConfig(level=logging.DEBUG)

__dir__ = os.path.dirname(__file__)
sys.path.append(__dir__ + "/lib")

# Support wayland (github.com/tpaviot/pythonocc-core/issues/1230)
if platform.system() == 'Linux':
    if os.popen('echo $XDG_SESSION_TYPE').read() == 'wayland\n':
        logging.info("Wayland. Set QT_QPA_PLATFORM=xcb")
        # os.system('export QT_QPA_PLATFORM=xcb')
        # subprocess.call('export QT_QPA_PLATFORM=xcb', shell=True)
        os.environ['QT_QPA_PLATFORM'] = 'xcb'

from PySide6.QtWidgets import *
from PySide6.QtGui import *

from OCC.Display.backend import load_backend,get_loaded_backend
load_backend("qt-pyside6")

import plugin
from window import MainWindow

# import faulthandler
# faulthandler.enable()

SAFE_MOD = False

class path():
    app_path = os.path.join(pathlib.Path.home(), '.potato-CAD')
    logging.info("软件目录:" + app_path)

    setting_path = os.path.join(app_path, 'setting.json')
    logging.info("配置文件路径:" + setting_path)

    root_path = __dir__
    logging.info("安装位置:" + root_path)

    plugin_path = os.path.join(app_path, "plugins")
    logging.info("插件位置" + plugin_path)

class Main():
    def __init__(self):
        if not os.path.exists(path.app_path):
            os.mkdir(path.app_path)
        self.load_the_settings()

        self.main_window = MainWindow(path)

        if not SAFE_MOD:
            self.plugins = plugin.plugins(path)
            self.plugins.load_core(self)
            # self.plugins.load(self) 
        
    def load_the_settings(self): 
        # 判断用户配置文件是否存在
        if not os.path.exists(os.path.join(path.setting_path)):
            # 不存在就创建
            with open(path.setting_path, 'w') as f:
                with open(os.path.join(path.root_path, 'default_setting.json')) as default:
                    f.write(default.read())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Main()
    win.main_window.show()
    app.exec()

