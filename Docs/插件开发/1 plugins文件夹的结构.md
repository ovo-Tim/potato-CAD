# 插件目录的基本结构
## plugins.json 的基本结构
`plugins.json` 位于 `plugins/plugins.json` ， 用于描述插件的基本信息
``` json
{
    "example" : {
        "path" : "example",
        "introduce" : "一个测试插件",
        "synopsis" : "一个测试插件",
        "version" : 1.0
    }
}
```
### 参数
- `path` 是插件的文件夹名称(插件必须位于 `plugins` 文件夹下)(如有多级目录需要使用`.`来替代`/`,建议直接将文件夹放入`plugins`文件夹下，并创建`__init__.py`)(建议保持`path`与`name`相同)(str)
- `introduce` 是一个插件的介绍(str)
- `synopsis` 简介(str)
- `version` 版本号(float)

## 插件文件夹
必须包含 `__init__.py` 文件作为主文件，加载时将直接加载 `path` 下的内容
