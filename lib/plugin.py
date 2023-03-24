# 插件加载器
import ujson as json
import logging
import os,sys

logging.basicConfig(level=logging.DEBUG)

class plugins():
    def __init__(self, plugins_path):
        self.plugins = {}  #插件
        self.plugins_path = plugins_path # 插件文件夹路径

        sys.path.append(self.plugins_path)

    def load(self, *args, **kwargs):
        # for plugin_path in os.listdir(self.plugins_path):
        #     if not filename.startswith("_"):
        #         # 获取插件信息
        #         with open( os.path.join(plugin_path,"info.json") , "r") as plugin_information_f:
        #             plugin_information = json.load(plugin_information_f)
        #             plugin_name = plugin_information.name
        #             self.plugin_informations[plugin_name] = plugin_information
        #         logging.info("加载插件:{0} 在位置:{1}".format(plugin_name,plugin_path))
        #         self.plugins[plugin_name] = __import__(plugin_path)


        with open(os.path.join(self.plugins_path,"plugins.json"),'r') as plugin_information_f:
            self.plugins_information = json.load(plugin_information_f) #获取插件配置文件

        for plugin_name,plugin_information in self.plugins_information.items():
            logging.info("开始加载:{}".format(plugin_name))

            plugin_path = os.path.join(self.plugins_path, plugin_information['path'])
            logging.debug("位置:{0} 配置信息:{1}".format(plugin_path,plugin_information))

            self.plugins[plugin_name] = __import__(plugin_information['path']).main( *args, **kwargs)


if __name__ == '__main__':
    p = plugins("plugins")
    p.load()
    print(p.plugins['example'])


        


