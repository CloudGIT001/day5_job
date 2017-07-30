#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:xieshengsen

import os
import sys

base_dir = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))  # 返回文件上一级的上一级绝对路径
print (base_dir)

sys.path.append(base_dir)  # 添加环境变量

# from conf import settings   # 导入模块
from core import main



if __name__ == "__main__":
    main.run()    # 执行main下的run函数