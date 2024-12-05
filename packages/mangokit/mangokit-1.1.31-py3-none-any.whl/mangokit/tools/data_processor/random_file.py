# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2023-12-21 11:15
# @Author : 毛鹏
import os
from typing import BinaryIO

from mangokit.exceptions import ToolsError
from mangokit.tools import InitPath


class RandomFileData:
    """获取文件对象"""

    @classmethod
    def get_file(cls, **kwargs) -> BinaryIO:
        """传入文件名称，返回文件"""
        project_id = kwargs.get('project_id')
        file_name = kwargs.get('file_name ')
        file_path = os.path.join(InitPath.upload_files, file_name)
        if os.path.exists(file_path):
            return open(file_path, 'rb')
        else:
            raise ToolsError(300, '文件不存在')
