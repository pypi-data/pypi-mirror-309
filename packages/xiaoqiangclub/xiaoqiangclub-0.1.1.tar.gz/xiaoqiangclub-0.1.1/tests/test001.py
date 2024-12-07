import os
from typing import Tuple, Optional


def get_file_name_and_extension(file_path: str) -> Tuple[str, Optional[str]]:
    """
    提取文件/文件夹的文件名和后缀。

    :param file_path: str 文件/文件夹的路径
    :return: Tuple[str, Optional[str]] 返回文件名和后缀，文件夹时后缀为 None
    """

    # 获取文件名和扩展名
    file_name, file_extension = os.path.splitext(os.path.basename(file_path))

    # 返回文件名和扩展名（去掉扩展名前的'.'符号）
    return file_name, file_extension


# 示例用法
file_path = r"\SystemDirs\Downloads\Traymond"
file_name, file_extension = get_file_name_and_extension(file_path)
print(f"文件名: {file_name}, 文件后缀: {file_extension}")
