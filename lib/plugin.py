# 插件加载器
import ujson as json
import logging
import os,sys

logging.basicConfig(level=logging.DEBUG)

class plugins():
    def __init__(self, path):
        self.plugins = {}  #插件
        self.plugins_path = path.plugin_path # 插件文件夹路径
        self.core_path = os.path.join(path.root_path, 'core')

        sys.path.append(self.plugins_path)
        sys.path.append(self.core_path)

    def load_core(self, *args, **kwargs):
        for plugin_path in os.listdir(self.core_path):
            if not plugin_path.startswith("_"):
                # 获取插件信息
                logging.info("加载插件:{0}".format(plugin_path))
                self.plugins[plugin_path] = __import__(plugin_path).main(*args, **kwargs)

    def load(self, *args, **kwargs):
        with open(os.path.join(self.plugins_path,"plugins.json"),'r') as plugin_information_f:
            self.plugins_information = json.load(plugin_information_f) #获取插件配置文件

        for plugin_name,plugin_information in self.plugins_information.items():
            logging.info("开始加载:{}".format(plugin_name))

            plugin_path = os.path.join(self.plugins_path, plugin_information['path'])
            logging.debug("位置:{0} 配置信息:{1}".format(plugin_path,plugin_information))

            self.plugins[plugin_name] = __import__(plugin_information['path']).main(*args, **kwargs)


    def __getitem__(self, key):
        return self.plugins[key]

if __name__ == '__main__':
    p = plugins("plugins")
    p.load()
    print(p.plugins['example'])


        


