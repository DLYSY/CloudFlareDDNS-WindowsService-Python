# 简介（施工中）

CloudFlare动态域名解析，Windows 服务版本

Windows 服务部分源码由：

https://github.com/HaroldMills/Python-Windows-Service-Example

提供

由于我只是学生，既没有技术也没有时间，因此环境不同造成的兼容性问题我一律不会修复。

我开发会保持使用最新 Python 大版本（当前3.11），如果你不熟悉 Python，为了防止出现兼容性问题，建议使用二进制安装，或者与我使用相同Python版本。

# 部署（施工中）

## 使用二进制文件（推荐）

1. 从“版本发布”下载`service.exe`然后运行`.\service.exe --startup=delayed install`。

2. 重启计算机或者执行`sc start "Cloudfalre DDNS"`或者在服务管理器中启动服务"CloudFlare DDNS"。

## 自行编译

### 必要条件

#### 1. Python3.10+

获取Python： https://www.python.org/

或者你也可以使用Conda：

Anaconda：https://www.anaconda.com/

Miniconda：https://docs.conda.io/en/latest/miniconda.html

请务必使用 Python 3.10+，源码使用了`match-case`语句，该语句在 Python 3.10 被加入。虽然我不推荐，但理论上你可以自行修改源码为`if-elif`语句从而使用更低版本的 Python 。

#### 2. Requests

安装：

`pip install requsets`

#### 3. PyWin32

安装：

`pip install pywin32`

#### 4. PyInstaller

安装：

`pip install pyinstaller[encryption]`

***！！！PS： 请不要使用`conda install`安装相关包，否则将存在兼容性问题导致 Windows 服务无法正常启动！！！***

### 编译

1. 下载/克隆源码；

2. 运行`pyinstaller --hidden-import=win32timezone ./service.py -F`；

然后你就可以在`dist`目录下找到`service.exe`。

***！！！PS： 请务必添加`-F`选项，否则将导致 Windows 服务无法正常启动！！！***

### 安装为 Windows 服务

参考 *“使用二进制文件”*。

## 直接使用PythonService

### 必要条件

参考 *“自行编译”*，除 PyInstaller 外都需要安装。

###