#!/usr/bin/env python
#coding:utf-8

"""
Purpose: 
    该模块定义 Command 类，用于定义系统支持的命令
Authors: 
    Chao -- < chaosimpler@gmail.com >
    
License: 
    LGPL clause

Created: 
    06/30/18
"""

from __future__ import division
import logging
import numpy as np
import pandas as pd

# 初始化日志对象
logger = logging.getLogger(__name__)


########################################################################
class Command(object):
    """
    """

    SCREENSHOT = u'给我截图'
    
    # 系统操作命令
    SYS_OPT = u'@st'                                # 系统命令前缀
    SYS_OPT_START = SYS_OPT + 'start'
    SYS_OPT_CLOSE = SYS_OPT + 'close'
    SYS_OPT_SHUTDOWN = SYS_OPT + 'shutdown'
    SYS_OPT_CPYFILE = SYS_OPT + 'copy'
    
    SYS_OPT_START_AUTO_REPLY = SYS_OPT + 'sar'
    SYS_OPT_CLOSE_AUTO_REPLY = SYS_OPT + 'car'
    
    SRC_DIR_PATH = r'C:\Users\Administrator\Desktop\Experiments\sqlite\RandomResults'
    DST_DIR_PATH = r'aaa'