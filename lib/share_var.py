import os
import logging
import pathlib
import window

__dir__ = os.path.join(os.path.dirname(__file__), '..')

main_window:window.MainWindow = None

app_path = os.path.join(pathlib.Path.home(), '.potato-CAD')
logging.info("software path:" + app_path)

setting_path = os.path.join(app_path, 'setting.json')
logging.info("profile path:" + setting_path)

root_path = __dir__
logging.info("install path:" + root_path)

plugin_path = os.path.join(app_path, "plugins")
logging.info("plugin path" + plugin_path)