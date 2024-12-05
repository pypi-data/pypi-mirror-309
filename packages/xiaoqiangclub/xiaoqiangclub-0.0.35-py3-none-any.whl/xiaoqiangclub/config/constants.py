# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/26 18:01
# 文件名称： constants.py
# 项目描述： 常量
# 开发工具： PyCharm
import platform
import tempfile

VERSION = '0.0.35'  # xiaoqiangclub模块版本号
# 当前运行的系统
CURRENT_SYSTEM = platform.system()
# pip镜像： 阿里云
PIP_MIRROR = 'https://mirrors.aliyun.com/pypi/simple/'

# 当前系统的临时文件目录路径
SYSTEM_TEMP_DIR = tempfile.gettempdir()
