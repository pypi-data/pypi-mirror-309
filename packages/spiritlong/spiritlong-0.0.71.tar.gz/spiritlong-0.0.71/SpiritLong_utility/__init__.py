

#!/usr/bin/python3
# coding=utf-8
###################################################################
#           ____     _     _ __  __                 
#          / __/__  (_)___(_) /_/ /  ___  ___  ___ _
#         _\ \/ _ \/ / __/ / __/ /__/ _ \/ _ \/ _ `/
#        /___/ .__/_/_/ /_/\__/____/\___/_//_/\_, / 
#           /_/                              /___/  
# Copyright (c) 2024 Chongqing Spiritlong Technology Co., Ltd.
# All rights reserved.  
# @author	arthuryang
# @brief	其他工具集
#
###################################################################  

import sys

# 动态地将函数添加到导出的模块中
# 注意：使用此装饰器之后，_function中不可直接调用同样使用此装饰器的函数，而要用模块来引用！
# 例如，模块m中，a()和b()都用了此装饰器，b()若调用a()则必须用m.a()才行！
# 事实上，所有导出的名称中都不能直接调用其他导出名称，而要用模块来引用
def export(_function):
	setattr(sys.modules[globals()['__name__']], _function.__name__, _function)

import	SpiritLong_utility.datetime
import	SpiritLong_utility.math
import	SpiritLong_utility.string
import	SpiritLong_utility.files

# 非函数
from SpiritLong_utility.string		import	SpiritLongJsonEncoder
