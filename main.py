#! /bin/python3
import sys, os, pathlib, platform, subprocess  # noqa: E401
import logging
import ujson as json
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
import gettext
from locale import getlocale

import share_var

import plugin
from window import MainWindow

import cProfile

SAFE_MOD = False

# 加载配置文件
if not os.path.exists(share_var.app_path):
    os.mkdir(share_var.app_path)

if not os.path.exists(os.path.join(share_var.setting_path)):
    # 不存在就创建
    with open(share_var.setting_path, 'w') as f:
        with open(os.path.join(share_var.root_path, 'default_setting.json')) as default:
            f.write(default.read())

with open(share_var.setting_path) as f:
    share_var.setting = json.decode(f.read())

# 设置国际化
lang_domain = 'default'
# lang_localedir = os.path.abspath("locale")
if share_var.setting['window']['language'] == 'system':
    lang = getlocale()[0]
else:
    lang = share_var.setting['window']['language']

lang_localedir = os.path.join(share_var.root_path, 'locale/')
if os.path.exists(os.path.join(lang_localedir, lang)): # 检查语言是否存在
    logging.info(f"Found language:{lang}")
    translation = gettext.translation(domain=lang_domain, localedir=lang_localedir, languages=[lang])
    translation.install()
else:
    gettext.install(None)
    logging.info(f"Can't find:{lang}.Use english")


class Main():
    def __init__(self):
        # 创建 MainWindow
        self.app = QApplication(sys.argv)
        share_var.main_class = self
        self.main_window = MainWindow()
        share_var.main_window = self.main_window

        # 加载插件
        if not SAFE_MOD:
            self.plugins = plugin.plugins()
            self.plugins.load_core()
            # self.plugins.load(self) 


if __name__ == '__main__':

    Profile = cProfile.Profile()
    Profile.enable()

    win = Main()

    # debug
    # def trace(frame, event, arg):
    #     print("%s, %s:%d" % (event, frame.f_code.co_filename, frame.f_lineno))
    #     return trace

    # sys.settrace(trace)

    win.main_window.show()
    win.app.exec()

    Profile.disable()
    # Profile.dump_stats('profile.prof')
    import pstats
    pstats.Stats(Profile).dump_stats('profile.prof')

