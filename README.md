# BingLocalhost
本项目基于[gradio](https://github.com/gradio-app/gradio)和[EdgeGPT](https://github.com/acheong08/EdgeGPT)，把Bing部署在本地局域网，一台电脑开代理，其他设备也能使，轻松简单。

不会整前端，CSS抄了几行[
ChuanhuChatGPT](https://github.com/GaiZhenbiao/ChuanhuChatGPT)，utils用于解决Markdown转义的问题，代码完全来源于[
ChuanhuChatGPT](https://github.com/GaiZhenbiao/ChuanhuChatGPT)，请原谅

# 1. 基础准备
- 安装[gradio](https://github.com/gradio-app/gradio)和[EdgeGPT](https://github.com/acheong08/EdgeGPT), [Markdown](https://github.com/Python-Markdown/markdown), [mdtex2html](https://github.com/polarwinkel/mdtex2html)这4个Python库

> 有时候Bing的回答内容比较长，需要较长的等待时间，但是EdgeGPT默认的最长等待时间只有10秒，就容易出现错误。因此个人建议把EdgeGPT库的EdgeGPT.py中的self.session = httpx.Client这一行把timeout=10改为timeout=60,verify=False

- 安装python 3.10+ or 您的python版本低于3.10，请修改main.py中的change_question函数。

- 中国用户需要科学上网手段

- 需要有可使用New Bing的账号，导出Cookie的方法请看[EdgeGPT](https://github.com/acheong08/EdgeGPT)

# 2. 下载本项目文件mdtex2html

# 3. 配置Bing Cookie
打开main.py，把存放Cookie的路径地址粘贴上去

# 4. 运行main.py
支持电脑和手机

![preview](/preview.png)
