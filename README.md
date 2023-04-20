# BingLocalhost
本项目基于[gradio](https://github.com/gradio-app/gradio)和[EdgeGPT](https://github.com/acheong08/EdgeGPT)，把Bing部署在本地局域网，一台电脑开代理，其他设备也能使，轻松简单，[最终效果在文末](#成果预览图)。

不会整前端，CSS抄了几行[
ChuanhuChatGPT](https://github.com/GaiZhenbiao/ChuanhuChatGPT)，`utils.py`用于解决Markdown转义的问题，代码完全来源于[
ChuanhuChatGPT](https://github.com/GaiZhenbiao/ChuanhuChatGPT)，请原谅。

**如果您觉得本项目好用请帮忙点 Star**

## 1. 基础准备
- 安装[gradio](https://github.com/gradio-app/gradio)和[EdgeGPT](https://github.com/acheong08/EdgeGPT), [Markdown](https://github.com/Python-Markdown/markdown), [mdtex2html](https://github.com/polarwinkel/mdtex2html)这4个Python库，安装方法请看这几个库的介绍，都非常简单。

> 有时候Bing的回答内容比较长，需要较长的等待时间，但是EdgeGPT默认的最长等待时间只有10秒，就容易出现错误。因此个人建议把EdgeGPT库的`EdgeGPT.py`中的`self.session = httpx.Client`这一行把`timeout=10`改为`timeout=60, verify=False`

- 安装Python 3.10+ or 您的Python版本低于3.10（个人建议是使用单独的[venv](#5-在windows系统创建venv虚拟环境)虚拟环境运行运行本项目），请修改main.py中的change_question函数，把其中的match-case语句改为if-elif-else语句。

- 中国用户需要科学上网手段，可以参考这个项目：[free](https://github.com/freefq/free)

- 需要有可使用New Bing的账号，导出Cookie的方法请看[EdgeGPT](https://github.com/acheong08/EdgeGPT)

## 2. 下载本项目文件
下载后解压缩，然后放到您喜欢的目录

## 3. 配置Bing Cookie
打开main.py，把存放Cookie的路径地址粘贴上去

## 4. 运行main.py
支持电脑和手机

## 5. 在Windows系统创建venv虚拟环境
1. 创建venv环境

启动`CMD`或`PowerShell`，运行以下命令
```
python3 -m venv C:\FilePath\ProjectName\venv
```
这行代码会在`C:\FilePath\ProjectName\venv`目录创建名虚拟环境，`ProjectName`可以更换为您的项目名称，`FilePath`您也可以自己选择。

> 以下假设您在`C:\FilePath\ProjectName\venv`创建了虚拟环境

然后把本项目放在`C:\FilePath\ProjectName`目录下

2. 进入虚拟环境

在`C:\FilePath\ProjectName\venv\Scripts`目录中运行`CMD`或`PowerShell`
或者启动`CMD`或`PowerShell`后把工作目录切换到`C:\FilePath\ProjectName\venv\Scripts`
然后运行`activate.bat`文件启动虚拟环境

3. 在虚拟环境中安装python库

进入虚拟环境后您的命令行开头会带有`(venv)`标识，此时说明进入虚拟环境成功，然后安装Python库的方法和平常并无差别
```
pip install gradio
```

4. 删除虚拟环境

直接把`C:\FilePath\ProjectName\venv`删除即可

## 成果预览图
![preview](/preview.png)

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=gG8Fkpxq/BingLocalhost&type=Date)](https://star-history.com/#gG8Fkpxq/BingLocalhost&Date)
