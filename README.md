# 简介（施工中）

CloudFlare动态域名解析，Windows 服务版本

Windows 服务部分源码由：

https://github.com/HaroldMills/Python-Windows-Service-Example

提供

由于我只是学生，既没有技术也没有时间，因此环境不同造成的兼容性问题我一律不会修复。

# 使用方法（施工中）

## 必要条件

### *Python3.10+*

Python： https://www.python.org/

或者你也可以使用Conda：

Anaconda：https://www.anaconda.com/

Miniconda：https://docs.conda.io/en/latest/miniconda.html

请务必使用 Python 3.10+，源码使用了`match-case`语句，该语句在 Python 3.10 被加入。虽然我不推荐，但理论上你可以自行修改源码为`if-elif`语句从而使用更低版本的 Python 。

我开发会保持使用最新 Python 大版本（当前3.11），如果你不熟悉 Python，为了防止出现兼容性问题，最好与我使用相同版本。

### *urllib3*

通过：

`pip install urllib3`

安装。

### *pywin32*

通过：

`pip install pywin32`

安装。

***PS： 请不要使用`conda install`安装相关包，否则将存在兼容性问题导致 Windows 服务无法正常启动***