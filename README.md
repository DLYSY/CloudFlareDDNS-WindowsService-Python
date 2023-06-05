# 简介

Cloudflare动态域名解析，包装为 Windows 服务

# 使用方法

参见
[wiki](https://github.com/DLYSY/CloudFlareDDNS-WindowsService-Python/wiki)

# 兼容性

目前只兼容 Windows（废话）。

不过如果你想用类 Unix 系统，也可以克隆/下载后运行`python3 main.py`，需要的包请参考 Windows 的使用方法。

由于我只是学生，既没有技术也没有时间，因此环境不同造成的兼容性问题的 issue 我一律不予修复。（这么简单的程序一般来说也不会有环境兼容性问题）

我开发会保持使用最新 Python 大版本（当前3.11），如果你不熟悉 Python，为了防止出现兼容性问题，建议使用二进制安装，或者与我使用相同Python版本。

# 未来计划

1. 支持类 Unix 系统

# 鸣谢

Windows 服务部分源码参考：

https://github.com/HaroldMills/Python-Windows-Service-Example

# Q&A

**Q：会不会支持其他 DNS 解析，比如阿里云？**

A：目前不会，这主要供我个人使用，因为个人目前使用 Cloudflare 所以暂时没有支持其他 DNS 的计划。

---

**Q：会不会支持 Linux systemd 服务？**

A：在做，什么时候做好不知道。（新建文件夹 XD）

---

**Q：那其他 Linux init 系统，比如 OpenRC 呢？**

A：你都玩 Gentoo 了，应该学会自己写脚本了。