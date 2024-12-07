# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/27 6:13
# 文件名称： file.py
# 项目描述： 常用文件的读写删等工具
# 开发工具： PyCharm
import os
import re
import yaml
import json
import win32ui
import win32gui
import aiofiles
from PIL import (Image, ImageFilter)
from xiaoqiangclub.config.log_config import log
from typing import (Union, Optional, List, Tuple)


class FileFormatError(Exception):
    """自定义异常，表示文件格式不支持"""
    pass


def read_file(file_path: str, mode: str = 'r', encoding: str = 'utf-8',
              log_errors: bool = True, by_line: bool = False) -> any:
    """
    读取文件内容

    :param file_path: 文件路径
    :param mode: 读取模式，支持 'r' 或 'rb'
    :param encoding: 文件编码，默认为 'utf-8'
    :param log_errors: 是否记录错误日志，默认为 True
    :param by_line: 是否按行读取文件，默认为 False
    :return: 文件内容，格式根据文件类型返回不同类型
    """
    if not os.path.exists(file_path):
        log.error(f"文件 {file_path} 不存在！")
        return None

    try:
        if mode == 'r':
            with open(file_path, 'r', encoding=encoding) as file:
                if file_path.endswith('.json'):
                    return json.load(file)
                elif file_path.endswith(('.yaml', '.yml')):
                    return yaml.safe_load(file)
                elif file_path.endswith('.txt'):
                    if by_line:
                        return file.readlines()  # 按行读取
                    else:
                        return file.read()  # 整体读取
                else:
                    raise FileFormatError(f"不支持的文件格式: {file_path}")
        elif mode == 'rb':
            with open(file_path, 'rb') as file:
                return file.read()
        else:
            log.error(f"不支持的读取模式: {mode}")
            return None

    except Exception as e:
        log_errors and log.error(f"读取文件 {file_path} 时出错: {e}")
        return None


def write_file(file_path: str, data: Union[dict, str], mode: str = 'w', encoding: str = 'utf-8',
               ensure_ascii: bool = False, log_errors: bool = True, by_line: bool = False) -> Optional[bool]:
    """
    写入内容到文件

    :param file_path: 文件路径
    :param data: 要写入的内容，支持字符串或字典
    :param mode: 写入模式，支持 'w' 或 'wb'
    :param encoding: 文件编码，默认为 'utf-8'
    :param ensure_ascii: json文件使用 ASCII 编码，默认为 False
    :param log_errors: 是否记录错误日志，默认为 True
    :param by_line: 是否按行写入文件，默认为 False
    :return: 是否写入成功
    """
    try:
        if mode == 'w':
            with open(file_path, 'w', encoding=encoding) as file:
                if file_path.endswith('.json'):
                    json.dump(data, file, ensure_ascii=ensure_ascii, indent=4)
                elif file_path.endswith(('.yaml', '.yml')):
                    yaml.dump(data, file, allow_unicode=True)
                elif file_path.endswith('.txt'):
                    if by_line and isinstance(data, list):
                        file.writelines([line + "\n" for line in data])  # 按行写入
                    else:
                        file.write(data)  # 整体写入
                else:
                    raise FileFormatError(f"不支持的文件格式: {file_path}")
        elif mode == 'wb':
            with open(file_path, 'wb') as file:
                file.write(data)
        else:
            log.error(f"不支持的写入模式: {mode}")
            raise FileFormatError(f"不支持的写入模式: {mode}")
        return True

    except Exception as e:
        log_errors and log.error(f"写入文件 {file_path} 时出错: {e}")
        return False


async def read_file_async(file_path: str, mode: str = 'r', encoding: str = 'utf-8',
                          log_errors: bool = True, by_line: bool = False) -> any:
    """
    异步读取文件内容

    :param file_path: 文件路径
    :param mode: 读取模式，支持 'r' 或 'rb'
    :param encoding: 文件编码，默认为 'utf-8'
    :param log_errors: 是否记录错误日志，默认为 True
    :param by_line: 是否按行读取文件，默认为 False
    :return: 文件内容，格式根据文件类型返回不同类型
    """
    if not os.path.exists(file_path):
        log.error(f"文件 {file_path} 不存在！")
        return None

    try:
        if mode == 'r':
            async with aiofiles.open(file_path, mode='r', encoding=encoding) as file:
                if file_path.endswith('.json'):
                    content = await file.read()
                    return json.loads(content)
                elif file_path.endswith(('.yaml', '.yml')):
                    content = await file.read()
                    return yaml.safe_load(content)
                elif file_path.endswith('.txt'):
                    if by_line:
                        return [line async for line in file]  # 按行读取
                    else:
                        return await file.read()  # 整体读取
                else:
                    raise FileFormatError(f"不支持的文件格式: {file_path}")
        elif mode == 'rb':
            async with aiofiles.open(file_path, mode='rb') as file:
                return await file.read()
        else:
            log.error(f"不支持的读取模式: {mode}")
            raise FileFormatError(f"不支持的读取模式: {mode}")

    except Exception as e:
        log_errors and log.error(f"读取文件 {file_path} 时出错: {e}")
        return None


async def write_file_async(file_path: str, data: Union[dict, str], mode: str = 'w',
                           encoding: str = 'utf-8', ensure_ascii: bool = False,
                           log_errors: bool = True, by_line: bool = False) -> Optional[bool]:
    """
    异步写入内容到文件

    :param file_path: 文件路径
    :param data: 要写入的内容，支持字符串或字典
    :param mode: 写入模式，支持 'w' 或 'wb'
    :param encoding: 文件编码，默认为 'utf-8'
    :param ensure_ascii: json文件使用 ASCII 编码，默认为 False
    :param log_errors: 是否记录错误日志，默认为 True
    :param by_line: 是否按行写入文件，默认为 False
    :return: 是否写入成功
    """
    try:
        if mode == 'w':
            async with aiofiles.open(file_path, mode='w', encoding=encoding) as file:
                if file_path.endswith('.json'):
                    await file.write(json.dumps(data, ensure_ascii=ensure_ascii, indent=4))
                elif file_path.endswith(('.yaml', '.yml')):
                    await file.write(yaml.dump(data, allow_unicode=True))
                elif file_path.endswith('.txt'):
                    if by_line and isinstance(data, list):
                        await file.writelines([line + "\n" for line in data])  # 按行写入
                    else:
                        await file.write(data)  # 整体写入
                else:
                    raise FileFormatError(f"不支持的文件格式: {file_path}")
        elif mode == 'wb':
            async with aiofiles.open(file_path, mode='wb') as file:
                await file.write(data)
        else:
            raise FileFormatError(f"不支持的写入模式: {mode}")
        return True

    except Exception as e:
        log_errors and log.error(f"写入文件 {file_path} 时出错: {e}")
        return False


def delete_file(file_path: str) -> Optional[bool]:
    """
    删除指定文件

    :param file_path: 文件路径
    """
    if not os.path.exists(file_path):
        log.error(f"文件 {file_path} 不存在！")
        return None
    try:
        os.remove(file_path)
        log.info(f"成功删除文件: {file_path}")
        return True
    except Exception as e:
        log.error(f"删除文件 {file_path} 时出错: {e}")
        return False


def clean_filename(filename: str, extra_chars: Union[str, List[str]] = None, replacement: str = '') -> str:
    """
    清理文件名，去除特殊字符，包括反斜杠、正斜杠、冒号、星号、问号、双引号、小于号、大于号、管道符。

    :param filename: 原始文件名，类型为字符串。
    :param extra_chars: 可选参数，可以是一个字符串或者字符串列表，用于指定额外要从文件名中去除的字符。默认为 None。
    :param replacement: 可选参数，用于指定去除特殊字符后用什么字符来代替，默认为空字符串。
    :return: 优化后的文件名，类型为字符串。
    """
    invalid_chars = r'[\\/:*?"<>|]'
    if extra_chars:
        if isinstance(extra_chars, str):
            extra_chars = re.escape(extra_chars)
        elif isinstance(extra_chars, List):
            escaped_additional_chars = [re.escape(char) for char in extra_chars]
            extra_chars = '|'.join(escaped_additional_chars)
        invalid_chars += f'|{extra_chars}'
    return re.sub(invalid_chars, replacement, filename)


def format_path(path: str) -> str:
    """
    统一路径分隔符，将路径中的分隔符转换为当前操作系统默认的分隔符。

    :param path: 输入的路径字符串，可以包含多种路径分隔符。
    :return: 返回统一了分隔符后的路径。
    """
    # 获取当前操作系统的路径分隔符
    current_separator = os.sep

    # 如果是 Windows，当前分隔符是反斜杠，替换所有的正斜杠
    if current_separator == '\\':
        normalized_path = path.replace('/', '\\')
    else:
        # 如果是 Unix 系统（Linux/macOS），当前分隔符是正斜杠，替换所有的反斜杠
        normalized_path = path.replace('\\', '/')

    return normalized_path


def get_file_name_and_extension(file_path: str) -> Tuple[str, Optional[str]]:
    """
    提取文件/文件夹的文件名和后缀。

    :param file_path: str 文件/文件夹的路径
    :return: Tuple[str, Optional[str]] 返回文件名和后缀，文件夹时后缀为 None
    """

    return os.path.splitext(os.path.basename(file_path))


def get_file_icon(file_path: str, output_path: str = None, size: int = 256) -> Optional[str]:
    """
    提取文件的图标并保存为背景透明的图片，同时增强边缘的平滑度

    :param file_path: str 文件的路径
    :param output_path: str 图标图片保存的路径，如果为 None，则默认保存在文件所在目录。
    :param size: int 图片的尺寸（正方形边长），默认值为256
    :return: Optional[str] 保存的图片路径，如果失败返回 None
    """
    try:
        large, small = win32gui.ExtractIconEx(file_path, 0)
        if not large:
            log.error("未能提取到图标")
            return None
        win32gui.DestroyIcon(small[0])

        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, 32, 32)
        hdc = hdc.CreateCompatibleDC()
        hdc.SelectObject(hbmp)
        hdc.DrawIcon((0, 0), large[0])

        bmpinfo = hbmp.GetInfo()
        bmpstr = hbmp.GetBitmapBits(True)
        icon = Image.frombuffer('RGBA', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRA', 0, 1)

        # 转换为RGBA并设置透明度
        icon = icon.convert("RGBA")
        datas = icon.getdata()

        new_data = []
        for item in datas:
            if item[:3] == (0, 0, 0):
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)

        icon.putdata(new_data)

        # 将图标按指定尺寸缩放，并创建一个新的透明图像
        original_size = icon.size
        scale = min(size / original_size[0], size / original_size[1])
        new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
        icon = icon.resize(new_size, Image.Resampling.LANCZOS)

        # 使用LANCZOS算法提高边缘平滑度
        result_icon = Image.new("RGBA", (size, size), (255, 255, 255, 0))
        position = ((size - new_size[0]) // 2, (size - new_size[1]) // 2)

        result_icon.paste(icon, position, icon)

        # 增加边缘平滑处理,使用抗锯齿效果的平滑滤镜
        result_icon = result_icon.filter(ImageFilter.SMOOTH_MORE)

        # 获取原文件的名称
        file_name, _ = os.path.splitext(os.path.basename(file_path))

        if not output_path:  # 如果没有提供保存路径，默认保存到原图片目录
            output_path = os.path.join(os.path.dirname(file_path), f"{file_name}_icon.png")

        result_icon.save(output_path, "PNG")
        win32gui.DestroyIcon(large[0])
        log.info(f"图标提取到： {output_path}")
        return output_path

    except Exception as e:
        log.error(f"提取图标失败: {e}")
        return None
