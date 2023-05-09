# CloudFlareDDNS-WindowsService

CloudFlare动态域名解析，Windows 服务版本

## 使用方法（施工中）

### 必要条件

#### Python3

Python： https://www.python.org/

或者你也可以使用Conda：

Anaconda：https://www.anaconda.com/

Miniconda：https://docs.conda.io/en/latest/miniconda.html

Python版本最好使用3.10+。我开发用的3.11，理论上全版本通用，但为了防止出现兼容性问题，最好与我使用相同版本。由于这是供我个人使用的，因此版本不同造成的兼容性问题我一律不会修复。

#### urllib3

可以通过：

`pip install urllib3`

安装。

**Conda用户请注意：** 请不要使用`conda`安装，否则将存在兼容性问题导致 Windows 服务无法正常启动

#### pywin32

可以通过：

`pip install pywin32`

安装。

**Conda用户请注意：** 请不要使用`conda`安装，否则将存在兼容性问题导致 Windows 服务无法正常启动