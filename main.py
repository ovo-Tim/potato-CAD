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

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTranslator

from OCC.Display.backend import load_backend,get_loaded_backend
load_backend("qt-pyside6")

import plugin
from window import MainWindow

# import faulthandler
# faulthandler.enable()

SAFE_MOD = False

class share_var():
    app_path = os.path.join(pathlib.Path.home(), '.potato-CAD')
    logging.info("software path:" + app_path)

    setting_path = os.path.join(app_path, 'setting.json')
    logging.info("profile path:" + setting_path)

    root_path = __dir__
    logging.info("install path:" + root_path)

    plugin_path = os.path.join(app_path, "plugins")
    logging.info("plugin path" + plugin_path)

class Main():
    def __init__(self):
        if not os.path.exists(share_var.app_path):
            os.mkdir(share_var.app_path)
        self.load_the_settings()

        self.app = QApplication(sys.argv)

        self.trans = QTranslator()
        self.trans.load(os.path.join(share_var.root_path, 'localization/zh_cn'))
        share_var.main_class = self
        self.app.installTranslator(self.trans)

        self.main_window = MainWindow(share_var)
        share_var.main_window = self.main_window
        # share_var.tr = self.main_window.tr
        share_var.tr = self.tr

        if not SAFE_MOD:
            self.plugins = plugin.plugins(share_var)
            self.plugins.load_core(share_var)
            # self.plugins.load(self) 

        self.main_window.show()
        
    def load_the_settings(self): 
        # 判断用户配置文件是否存在
        if not os.path.exists(os.path.join(share_var.setting_path)):
            # 不存在就创建
            with open(share_var.setting_path, 'w') as f:
                with open(os.path.join(share_var.root_path, 'default_setting.json')) as default:
                    f.write(default.read())

    def tr(self, text: str):
        return self.trans.translate(None, text)

if __name__ == '__main__':
    win = Main()
    win.app.exec()
