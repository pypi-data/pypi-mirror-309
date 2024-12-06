# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/17 10:14
# 文件名称： xiaoqiangclub_cli.py
# 项目描述： xiaoqiangclub 命令行工具
# 开发工具： PyCharm
import argparse
from .commands.cli_tool_template_generator import generate_cli_tool_template
from .commands.create_python_project_template import create_python_project


def main():
    parser = argparse.ArgumentParser(prog='xiaoqiangclub', description='XiaoqiangClub命令行工具',
                                     epilog='微信公众号：XiaoqiangClub',
                                     formatter_class=argparse.RawTextHelpFormatter)  # RawTextHelpFormatter 保留描述符串中的换行符

    subparsers = parser.add_subparsers(title='子命令', dest='command')  # 添加子命令：只能有一个add_subparsers方法

    # 生成Python项目目录结构
    project_template = subparsers.add_parser('project_template', help='生成Python项目模板',
                                             description='生成Python项目模板')
    project_template.add_argument('-n', '--name', type=str, default='demo', help='项目名称，默认为demo')
    project_template.add_argument('-d', '--directory', type=str, default=None, help='项目路径，默认为当前目录')
    project_template.set_defaults(func=create_python_project)  # 设置默认函数

    # 生成命令行工具模板
    cli_template = subparsers.add_parser('cli_template', help='生成命令行工具模板文件',
                                         description='生成命令行工具模板文件')
    cli_template.add_argument('-n', '--name', type=str, default='cli_tool_template',
                              help='模板名称，默认为 "cli_tool_template.py"')
    cli_template.add_argument('-d', '--directory', type=str, default=None,
                              help='生成的模板存放目录路径，默认为当前目录')
    cli_template.set_defaults(func=generate_cli_tool_template)

    # 命令行参数解析
    args = parser.parse_args()
    if args.command:
        args.func(args)
    else:
        parser.print_help()
