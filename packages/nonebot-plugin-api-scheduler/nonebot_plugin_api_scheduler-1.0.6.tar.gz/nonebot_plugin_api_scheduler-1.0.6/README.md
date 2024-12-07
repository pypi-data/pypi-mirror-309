<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-api-scheduler

_✨ 像操作API一样设置定时任务&计划任务✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/mmdexb/nonebot-plugin-api-scheduler.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-api-scheduler">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-template.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="python">

</div>





## 📖 介绍

通过NoneBot的FastAPI服务器来提供API，使得您能够对定时任务&计划任务进行增删改查。同时也提供了一个简易的WebUI

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行<br> 首先安装前置依赖nonebot_plugin_apscheduler <br>
    nb plugin install nonebot_plugin_apscheduler <br>
接下来安装本插件<br>
    nb plugin install nonebot_plugin_api-scheduler<br>

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令<br>
<summary>pip</summary>
首先安装前置依赖nonebot_plugin_apscheduler  <br>
    pip install nonebot_plugin_apscheduler<br>
接下来安装本插件  <br>
    pip install nonebot_plugin_api-scheduler<br>
</details>



## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| fastapi_docs_url = "/doc" | 否 | 无 | 设置fastapi文档地址 |


## 使用方法
[API文档](https://github.com/mmdexb/nonebot-plugin-api-scheduler/blob/master/API.md) <br>
[WebUI文档](https://github.com/mmdexb/nonebot-plugin-api-scheduler/blob/master/wiki.md)

