# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/17 13:28
# 文件名称： create_python_project_template.py
# 项目描述： 创建Python项目模板
# 开发工具： PyCharm
import os
import argparse
from typing import Dict, Union
from xiaoqiangclub.data.file import format_path
from xiaoqiangclub.utils.time_utils import get_current_date


def file_header(filename: str, description: str, date: str) -> str:
    """
    生成文件头注释。

    :param filename: 文件名
    :param description: 项目描述
    :param date: 开发时间
    :return: 文件头注释
    """
    return f"""# 开发人员： Xiaoqiang
# 微信公众号:  XiaoqiangClub
# 开发时间： {date}
# 文件名称： {filename}
# 项目描述： {description}
# 开发工具： PyCharm\n"""


def init_py_content(project_name: str) -> str:
    """
    生成 project/__init__.py 文件内容。

    :param project_name: 项目名称
    :return: constants.py 文件内容
    """
    return f"""from .utils.constants import (VERSION, AUTHOR, DESCRIPTION, EMAIL, CURRENT_SYSTEM, DATA_PATH, LOG_PATH, LOG_FILE, log)

__title__ = "{project_name}"
__version__ = VERSION
__author__ = AUTHOR
__description__ = DESCRIPTION

__all__ = [
    "__title__", "__version__", "__author__", "__description__",
    "VERSION", "AUTHOR", "DESCRIPTION", "EMAIL",
    "CURRENT_SYSTEM", "DATA_PATH", "LOG_PATH", "LOG_FILE", "log",
]
"""


def utils_init_py_content() -> str:
    """生成 project/utils/__init__.py 文件内容"""
    return """from .constants import (VERSION, AUTHOR, DESCRIPTION, EMAIL, CURRENT_SYSTEM, DATA_PATH, LOG_PATH, LOG_FILE, log)


__all__ = [
    "VERSION", "AUTHOR", "DESCRIPTION", "EMAIL",
    "CURRENT_SYSTEM", "DATA_PATH", "LOG_PATH", "LOG_FILE", "log",
]
"""


def fastapi_view_py_content() -> str:
    """生成 project/fastapi_view.py 文件内容"""
    return """import uvicorn
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, Request
from .utils import (log, CURRENT_SYSTEM)

app = FastAPI()


@app.get("/{{item_id}}")
async def index(request: Request, item_id: str,
                q: Union[str, None] = None):  # 前台的示例url：http://127.0.0.1:8000/items/foo?q=1
    log.debug(request.url)
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


class Item(BaseModel):
    name: str
    price: float


@app.post("/{{item_id}}")
async def index(request: Request, item_id: int, item: Item):
    log.debug(request.url)
    ret = {
        "item_id": item_id,
        "item": item
    }
    return ret


if __name__ == '__main__':
    if CURRENT_SYSTEM == 'Windows':  # 安装【0.17.6】版本的uvicorn：pip install -i https://pypi.tuna.tsinghua.edu.cn/simple uvicorn==0.17.6
        # uvicorn.xiaoqiangwol(app="fast_api:app", host="0.0.0.0", port=8000, reload=True, debug=True, log_level='debug')
        # 如果需要使用本地真实IP或者是映射本地端口就设置本地真实端口
        uvicorn.run(app="fast_api:app", host="192.168.1.88", port=8000, reload=True, debug=True, log_level='debug')
    else:
        uvicorn.run(app="fast_api:app", host="0.0.0.0", port=8000, reload=True, debug=False, log_level='info')
"""


def constants_py_content(project_name: str) -> str:
    """
    生成 constants.py 文件内容。

    :param project_name: 项目名称
    :return: constants.py 文件内容
    """
    return f"""import os
import platform
from xiaoqiangclub import LoggerBase

# 版本号
VERSION = '0.0.1'
# 作者
AUTHOR = 'Xiaoqiang'
# 邮箱
EMAIL = 'xiaoqiangclub@hotmail.com'
# 项目描述
DESCRIPTION = '{project_name}'

# 当前运行的系统
CURRENT_SYSTEM = platform.system()

# 项目根目录
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 创建数据存储目录 data
DATA_PATH = os.path.join(ROOT_PATH, 'data')
os.makedirs(DATA_PATH, exist_ok=True)

# 日志保存路径
LOG_PATH = os.path.join(ROOT_PATH, 'logs')
os.makedirs(LOG_PATH, exist_ok=True)
LOG_FILE = os.path.join(LOG_PATH, '{project_name}.log')

logger = LoggerBase('{project_name}', console_log_level='DEBUG', file_log_level='WARNING', log_file=LOG_FILE)
log = logger.logger
"""


def config_py_content() -> str:
    """
    生成 config.py 文件内容。

    :return: config.py 文件内容
    """
    return """from dataclasses import dataclass


@dataclass
class Config:
    pass
"""


def test_example_content() -> str:
    """
    生成 test_example.py 文件内容。

    :return: test_example.py 文件内容
    """
    return """import unittest


class TestExample(unittest.TestCase):
    def test_sample(self):
        self.assertEqual(1, 1)

if __name__ == "__main__":
    unittest.main()
"""


def setup_py_content(project_name: str) -> str:
    """
    生成 setup.py 文件内容，包含相关字段。

    :param project_name: 项目名称
    :return: setup.py 文件内容
    """
    return f"""import os
from {project_name} import (VERSION, AUTHOR, DESCRIPTION, EMAIL)
from setuptools import setup, find_packages


def get_long_description() -> str:
    \"\"\"获取详细描述\"\"\"
    try:
        if os.path.exists('README.md'):
            with open('README.md', 'r', encoding='utf-8') as f:
                return f.read()
        return DESCRIPTION
    except Exception as e:
        print(f"读取 README.md 失败: {{e}}")
        return DESCRIPTION


setup(
    name='{project_name}',
    version=VERSION,  # 示例版本号
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=get_long_description(),  # 项目详细描述
    long_description_content_type='text/markdown',
    url='https://gitee.com/xiaoqiangclub/{project_name}',
    install_requires=[],  # 依赖包

    extras_require={{  # 可选的额外依赖
        # Windows 平台特定依赖
        'windows': [],
        # Linux 平台特定依赖
        'linux': []
    }},
    packages=find_packages(),  # 自动发现所有包
    classifiers=[  # 项目分类
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='Apache 2.0',  # 指明使用的许可证
    python_requires='>=3.10',  # 指定最低 Python 版本
    zip_safe=False,  # 是否可以放心地进行 zip 安装
    entry_points={{  # 命令行入口
        'console_scripts': [
            # 'xiaoqiangclub = xiaoqiangclub.cmd.xiaoqiangclub_cli:main',
        ],
    }},
)
"""


def license_content() -> str:
    """
    生成 LICENSE 文件内容。

    :return: LICENSE 文件内容
    """
    return """MIT License

Copyright (c) YEAR YOUR NAME

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""


# 创建项目结构
def create_structure(base_path: str, structure: Dict[str, str]) -> None:
    """
    创建项目结构。

    :param base_path: 基础路径
    :param structure: 项目结构字典
    """
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)


def create_python_project(project_name: Union[str, argparse.Namespace],
                          save_path: Union[str, argparse.Namespace] = None) -> None:
    """
    创建 Python 项目结构。

    :param project_name: 项目名称
    :param save_path: 保存路径
    """
    if isinstance(project_name, argparse.Namespace):
        save_path = project_name.directory
        project_name = project_name.name

    project_name = project_name.strip()
    save_path = save_path or os.getcwd()

    current_date = get_current_date()

    # 定义项目结构
    project_structure = {
        project_name: {
            project_name: {
                '__init__.py': file_header(f'{project_name}/__init__.py', '项目初始化文件',
                                           current_date) + init_py_content(project_name),  # 导入常量
                'fastapi_view.py': file_header(f'{project_name}/fastapi_view.py', '项目初始化文件',
                                               current_date) + fastapi_view_py_content(),  # Fastapi视图文件
                'utils': {
                    '__init__.py': file_header(f'{project_name}/utils/__init__.py', 'utils 模块初始化文件',
                                               current_date) + utils_init_py_content(),
                    'constants.py': file_header(f'{project_name}/utils/constants.py', '常量定义文件',
                                                current_date) + constants_py_content(project_name),
                },
                'scripts': {
                    '__init__.py': file_header(f'{project_name}/scripts/__init__.py', 'scripts 模块初始化文件',
                                               current_date),
                },
            },
            'tests': {
                '__init__.py': file_header('tests/__init__.py', 'tests 模块初始化文件', current_date),
                'test_example.py': file_header('tests/test_example.py', '测试示例文件',
                                               current_date) + test_example_content(),
            },
            '.gitignore': file_header('.gitignore', 'Git 忽略文件', current_date) + '*.pyc\n__pycache__/\nenv/\n',
            'README.md': '# ' + project_name + '\n\nDescription of the project.',
            'setup.py': file_header('setup.py', '项目安装配置文件', current_date) + setup_py_content(project_name),
            'config.py': file_header('config.py', '配置文件', current_date) + config_py_content(),
            'LICENSE': license_content(),
        }
    }

    # 创建项目结构
    create_structure(save_path, project_structure)
    print(f"\n已生成Python项目结构：{format_path(os.path.join(save_path, project_name))}\n")


if __name__ == '__main__':
    # 示例用
    create_python_project('my_project')
